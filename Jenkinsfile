pipeline {

    agent { dockerfile true }
    // agent { docker { image 'python' } }

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
		sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
