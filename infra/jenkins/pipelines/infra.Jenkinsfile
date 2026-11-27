pipeline {
    agent any

    stages {
        stage('Destroy') {
            steps {
                dir('infra/packer') {
                    sh('vagrant destroy -f')
                }
            }
        }

        stage('Up') {
            steps {
                dir('infra/packer') {
                    sh('vagrant up')
                }
            }
        }

        stage('Status') {
            steps {
                dir('infra/packer') {
                    sh('vagrant status')
                }
            }
        }
    }
}