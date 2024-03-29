.. _version_history:Version_History:

===============
Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized amongst CSCs.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each CSC link to whatever method of tracking is being used for that CSC until standardization occurs.
.. No new work should be required in order to complete this section.
.. Below is an example of a version history format.

v3.2.0
------
* Updated to use ts_pre_commit_conf.

v3.1.0
------
* Removed the root user workaround from the Jenkinsfile.

v3.0.0
------
* Converted package to pyproject.toml.
* Updated paths to XML files.
* Updated Python version in .github/workflows/lint.yaml.

v2.2.0
------
* Updated to conform to SalObj7.
    * The index_generator method was moved to ts_utils.
    * The put method renamed to write.
    * Black formatting.
    
v2.1.1
------
* Fixed the build parameter reference in the agent block in Jenkinsfile.

v2.1.0
------
* Removed VERSION file.

v2.0.0
------
* Converted the C++ and Java shell script 'unit-tests' to Python unit-tests.

v1.0.0
------
* Initial release.
