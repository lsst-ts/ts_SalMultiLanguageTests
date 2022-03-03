# This file is part of ts_SalMultiLanguageTests.
#
# Developed for the Rubin Observatory Telescope and Site System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
import enum
import subprocess
import pathlib
import warnings

from lsst.ts import salobj
from lsst.ts import utils

# Long enough to perform any reasonable operation
# including starting a CSC or loading a script (seconds)
STD_TIMEOUT = 60

INITIAL_LOG_LEVEL = 20

index_gen = utils.index_generator()


class Language(enum.Enum):
    CPP = enum.auto()
    JAVA = enum.auto()


class SalCommanderToMinimalControllerTestCase(unittest.TestCase):
    """Test a C++ or Java Commander communicating to
    various minimal controllers."""

    def setUp(self) -> None:
        salobj.set_random_lsst_dds_partition_prefix()
        self.index = next(index_gen)

    def get_langauge_variables(self, language: Language) -> None:
        """Get the language specific test values;
        either cpp (C++) or java (Java).

        Parameters
        ----------
        language : `Language`
            Options are "JAVA" or "CPP".

        """
        return {
            Language.CPP: ("minimal_cpp_commander.sh", "initial_log_level="),
            Language.JAVA: ("minimal_java_commander.sh", "initial logLevel.level "),
        }[language]

    def test_cpp_controller(self) -> None:
        for language in Language:
            with self.subTest(language=language):
                self.check_minimal_controller(language, "minimal_cpp_controller.sh")

    def test_java_controller(self) -> None:
        for language in Language:
            with self.subTest(language=language):
                self.check_minimal_controller(language, "minimal_java_controller.sh")

    def test_salobj_controller(self) -> None:
        for language in Language:
            with self.subTest(language=language):
                self.check_minimal_controller(language, "minimal_salobj_controller.py")

    def check_minimal_controller(self, language: Language, exec_name: str) -> None:
        # Start the Commander before the Controller subprocess
        # to be sure the Commander sees telemetry from the Controller
        # (telemetry is volatile, so has no historical data).
        commander, initial_log = self.get_langauge_variables(language)
        commander_path = pathlib.Path(__file__).home() / "repos/ts_sal/bin" / commander
        assert commander_path.is_file()
        controller_path = (
            pathlib.Path(__file__).parent.absolute() / "controllers" / exec_name
        )
        assert controller_path.is_file()
        print(
            f"{language.name} Commander: start {commander_path} with index={self.index} in a subprocess"
        )
        print(
            f"{language.name} Controller: start {controller_path} with index={self.index} in a subprocess"
        )
        with subprocess.Popen(
            [
                commander_path,
                str(self.index),
                str(INITIAL_LOG_LEVEL),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        ) as commander_process, subprocess.Popen(
            [str(controller_path), str(self.index), str(INITIAL_LOG_LEVEL)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        ) as controller_process:
            print(f"{language.name} Commander: wait for completion")
            commander_process.wait()
            commander_output = commander_process.communicate()[0]
            commander_output = commander_output.decode("utf-8")
            assert commander_process.returncode == 0
            print(f"{language.name} Controller: wait for completion")
            controller_process.wait()
            controller_output = controller_process.communicate()[0]
            controller_output = controller_output.decode("utf-8")
            print(f"{language.name} Commander: read initial logLevel")
            self.assertIn(str(initial_log) + str(INITIAL_LOG_LEVEL), commander_output)

            for level in (10, 52, 0):
                print(
                    f"{language.name} Commander: send setLogLevel(level={level}) command"
                )
                self.assertIn(
                    f"Commmander:  send setLogLevel(level={level}) command",
                    commander_output,
                )
                print(f"{language.name} Controller: write logLevel={level} event")
                self.assertIn(
                    f"Controller: writing logLevel={level} event", controller_output
                )

        print("Ensure Commander and Controller processes are terminated")
        if commander_process.returncode is None:
            commander_process.terminate()
            warnings.warn(
                "Killed the Commander process that was not properly terminated"
            )
        else:
            print(f"{language.name} Commander: done")
        if controller_process.returncode is None:
            controller_process.terminate()
            warnings.warn(
                "Killed the Controller process that was not properly terminated"
            )
        else:
            print(f"{language.name} Controller: done")
