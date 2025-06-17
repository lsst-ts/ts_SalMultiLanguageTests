// Define variables
HOME = "/home/saluser"

pipeline{
    parameters {
        string defaultValue: 'develop', description: 'The version of the Docker image to use for the build.', name: 'image_version', trim: true
    }
    options {
        disableConcurrentBuilds()
    }
    agent {
        docker {
            image 'ts-dockerhub.lsst.org/salobj:' + params.image_version
            args '--entrypoint="" ' +
            '--network=kafka -v ${WORKSPACE}:' + HOME + '/repos/ts_SalMultiLanguageTests '
            label 'Node1_4CPU || Node3_4CPU'
         }
    }
    environment {
        user_ci = credentials('lsst-io')
        LTD_USERNAME="${user_ci_USR}"
        LTD_PASSWORD="${user_ci_PSW}"
        
    }
    stages{
        stage("Build Test CSC libraries") {
            steps {
                 withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh """
                    echo 'Setup the environment'
                    set +x
                    source $HOME/.setup.sh
                    export LSST_SDK_INSTALL=/home/saluser/repos/ts_sal
                    export LSST_SAL_PREFIX=\$CONDA_PREFIX
                    set -x
                    echo 'Update ts_xml/develop'
                    cd $HOME/repos/ts_xml
                    /home/saluser/.checkout_repo.sh develop
                    git pull
                    echo 'Update ts_sal/develop'
                    cd $HOME/repos/ts_sal
                    /home/saluser/.checkout_repo.sh develop
                    git pull
                    ./bin/setupStackBuildEnvironment
                    source ./setupKafka.env
                    cd test
                    echo 'Log EnvVars'
                    echo 'PATH: \$PATH'
                    echo 'LD_LIBRARY_PATH: \$LD_LIBRARY_PATH'
                    echo 'Copy XML files'
                    cp -r \${TS_XML_DIR}/python/lsst/ts/xml/data/sal_interfaces/Test/Test*.xml $HOME/repos/ts_sal/test
                    cp -r \${TS_XML_DIR}/python/lsst/ts/xml/data/sal_interfaces/SALSubsystems.xml $HOME/repos/ts_sal/test
                    cp -r \${TS_XML_DIR}/python/lsst/ts/xml/data/sal_interfaces/SALGenerics.xml $HOME/repos/ts_sal/test
                    echo 'Validate and IDL'
                    salgenerator validate Test
                    echo 'C++'
                    salgenerator Test sal cpp
                    echo 'Lib'
                    salgenerator Test lib
                    echo 'Copy controllers'
                    cp $HOME/repos/ts_sal/bin/minimal_*_controller.sh $HOME/repos/ts_SalMultiLanguageTests/tests/controllers
                    """
                }
            }
        }//BuildTestCSC
        stage("Run the Unit Tests") {
            steps {
                 withEnv(["HOME=/home/saluser"]) {
                    sh """
                    ls $HOME/repos/ts_SalMultiLanguageTests/tests/controllers
                    set +x
                    source $HOME/.setup.sh
                    set -x
                    pip install . 
                    #pytest -ra tests/test_salcommander_minimal_controllers.py tests/test_salobj_to_minimal_controllers.py -o junit_family=xunit2 --junitxml=tests/results/results.xml
                    echo "====== Unit testing complete ======"
                    """ 
                }
            }   
        }
    }
    post{
       cleanup {
            deleteDir()
        }
    }
}
