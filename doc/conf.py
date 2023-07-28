"""Sphinx configuration file for TSSW package"""

from documenteer.conf.pipelinespkg import *  # type: ignore # noqa

project = "ts_SalMultiLanguageTests"
html_theme_options["logotext"] = project  #  type: ignore # noqa
html_title = project
html_short_title = project
