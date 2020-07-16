pipeline {

    agent { dockerfile true }
    // agent { docker { image 'python' } }

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
		sh 'python --version'
		sh 'pip freeze'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing.. Compiling script'
		sh 'python -m py_compile bridge_chirpstack_iothub.py'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline successful.'
        }
        failure {
            echo 'Fail.'
        }
        unstable {
            echo 'Unstable.'
        }
        changed {
            echo 'The state of the Pipeline has changed!'
        }
    }
}
