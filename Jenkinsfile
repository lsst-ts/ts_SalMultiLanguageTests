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
            args '-u root --entrypoint="" ' +
            '-e LSST_DDS_PARTITION_PREFIX=citest -v ${WORKSPACE}:' + HOME + '/repos/ts_SalMultiLanguageTests '
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
                 withEnv(["HOME=/home/saluser"]) {
                    sh """
                    echo 'Setup the environment'
                    set +x
                    source $HOME/.setup.sh
                    set -x
                    echo 'Update ts_idl/develop'
                    cd $HOME/repos/ts_idl
                    /home/saluser/.checkout_repo.sh develop
                    git pull
                    echo 'Update ts_xml/develop'
                    cd $HOME/repos/ts_xml
                    /home/saluser/.checkout_repo.sh develop
                    git pull
                    echo 'Update ts_sal/develop'
                    cd $HOME/repos/ts_sal
                    /home/saluser/.checkout_repo.sh develop
                    git pull
                    cd test
                    echo 'Copy XML files'
                    cp -r $HOME/repos/ts_xml/sal_interfaces/Test/Test*.xml $HOME/repos/ts_sal/test
                    cp -r $HOME/repos/ts_xml/sal_interfaces/SALSubsystems.xml $HOME/repos/ts_sal/test
                    cp -r $HOME/repos/ts_xml/sal_interfaces/SALGenerics.xml $HOME/repos/ts_sal/test
                    echo 'Validate and IDL'
                    make_idl_files.py --keep Test
                    echo 'C++'
                    salgenerator Test sal cpp
                    echo 'Java'
                    salgenerator Test sal java version=pre${BUILD_NUMBER}-SNAPSHOT
                    echo 'Maven'
                    salgenerator Test maven version=pre${BUILD_NUMBER}-SNAPSHOT
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
                    pip install -e . 
                    pytest -ra -o junit_family=xunit2 --junitxml=tests/results/results.xml
                    echo "====== Unit testing complete ======"
                    """ 
                }
            }   
        }
    }
    post{
       always {
            withEnv(["HOME=${env.WORKSPACE}"]) {
                sh 'chown -R 1003:1003 $HOME/'
            }
       }
       cleanup {
            deleteDir()
        }
    }
}
