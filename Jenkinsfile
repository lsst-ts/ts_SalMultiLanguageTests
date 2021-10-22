pipeline{
    agent{
        docker {
            alwaysPull true
            image 'lsstts/develop-env:develop'
            args "-u root --entrypoint=''"
        }
    }
    environment {
        user_ci = credentials('lsst-io')
        LTD_USERNAME="${user_ci_USR}"
        LTD_PASSWORD="${user_ci_PSW}"
    }
    stages{
        stage("Run the Unit Tests") {
            steps {
                 withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh """
                    source /home/saluser/.setup_dev.sh
                    pip install -e . 
<<<<<<< HEAD
                    pytest -ra -k salobj_con -o junit_family=xunit2 --junitxml=tests/results/results.xml
=======
                    pytest -ra -o junit_family=xunit2 --junitxml=tests/results/results.xml
>>>>>>> 2711fa6... Added the Jenkinsfile to run the unit/integration tests.
                    echo "====== Unit testing complete ======"
                    """ 
                }
            }   
        }
        stage('Build and Upload Documentation') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh """
                    source /home/saluser/.setup_dev.sh
<<<<<<< HEAD
                    pip install .
                    pip install -r doc/requirements.txt
                    package-docs build
                    ltd upload --product ts-SalMultiLanguageTests --git-ref ${GIT_BRANCH} --dir doc/_build/html
=======
                    pip install -r doc/requirements.txt
                    package-docs build
                    ltd upload --product ts-integrationtests --git-ref ${GIT_BRANCH} --dir doc/_build/html
>>>>>>> 2711fa6... Added the Jenkinsfile to run the unit/integration tests.
                    """
                }
            }
        }
    }
    post{
       always {
            withEnv(["HOME=${env.WORKSPACE}"]) {
                sh 'chown -R 1003:1003 ${HOME}/'
            }
       }
       cleanup {
            deleteDir()
        }
    }
}
