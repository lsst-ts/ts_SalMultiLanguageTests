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

import asyncio
import logging
import pathlib
import unittest
import warnings

from lsst.ts import salobj, utils

# Long enough to perform any reasonable operation
# including starting a CSC or loading a script (seconds)
STD_TIMEOUT = 60

INITIAL_LOG_LEVEL = 20

index_gen = utils.index_generator()


class SalObjToMinimalControllerTestCase(unittest.IsolatedAsyncioTestCase):
    """Test a salobj-based Remote talking to various minimal controllers."""

    def setUp(self) -> None:
        salobj.set_random_lsst_dds_partition_prefix()
        self.index = next(index_gen)

    async def test_cpp_controller(self) -> None:
        await self.check_minimal_controller("minimal_cpp_controller.sh")

    async def test_java_controller(self) -> None:
        await self.check_minimal_controller("minimal_java_controller.sh")

    async def test_salobj_controller(self) -> None:
        await self.check_minimal_controller("minimal_salobj_controller.py")

    async def check_minimal_controller(self, exec_name: str) -> None:
        # Create the remote before the subprocess
        # to be sure the remote sees telemetry from the subprocess
        # (telemetry is volatile, so has no historical data).
        print(f"salobj Remote: create salobj remote with index={self.index}")
        async with salobj.Domain() as domain:
            # ts_sal requires a CSC identity
            # (or explicitly issuing the setAuthList command)
            domain.default_identity = f"Test:{self.index}"
            async with salobj.Remote(
                domain=domain,
                name="Test",
                index=self.index,
                evt_max_history=1,
            ) as remote:
                remote.salinfo.log.addHandler(logging.StreamHandler())

                exec_path = (
                    pathlib.Path(__file__).parent.absolute() / "controllers" / exec_name
                )
                assert exec_path.is_file()
                print(f"salobj Remote: start {exec_path} in a subprocess")
                process = await asyncio.create_subprocess_exec(
                    str(exec_path), str(self.index), str(INITIAL_LOG_LEVEL)
                )

                try:
                    print("salobj Remote: wait for initial logLevel event")
                    data = await remote.evt_logLevel.next(
                        flush=False, timeout=STD_TIMEOUT
                    )
                    print(f"salobj Remote: read initial logLevel.level={data.level}")
                    assert data.level == INITIAL_LOG_LEVEL

                    for level in (10, 52, 0):
                        print(f"salobj Remote: send setLogLevel(level={level}) command")
                        ackcmd = await remote.cmd_setLogLevel.set_start(
                            level=level, timeout=STD_TIMEOUT
                        )
                        assert ackcmd.identity == remote.salinfo.identity
                        print("salobj Remote: wait for logLevel event")
                        data = await remote.evt_logLevel.next(
                            flush=False, timeout=STD_TIMEOUT
                        )
                        print(f"salobj Remote: read logLevel={data.level}")
                        assert data.level == level
                        print("salobj Remote: wait for scalars telemetry")
                        data = await remote.tel_scalars.next(
                            flush=False, timeout=STD_TIMEOUT
                        )
                        print(f"salobj Remote: read scalars.int0={data.int0}")
                        assert data.int0 == level
                        await asyncio.sleep(0.1)

                    await asyncio.wait_for(process.wait(), timeout=STD_TIMEOUT)
                finally:
                    print("salobj Remote: done")
                    if process.returncode is None:
                        process.terminate()
                        warnings.warn(
                            "Killed a process that was not properly terminated"
                        )
