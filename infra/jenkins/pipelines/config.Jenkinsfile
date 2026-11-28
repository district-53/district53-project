pipeline {
    agent any
    environment {
        ANSIBLE_HOST_KEY_CHECKING = 'False'
    }

    stages {
        stage('Syntax') {
            steps {
                dir('infra/ansible') {
                    sh('ansible-playbook --syntax-check -i inventories/hosts.ini site.yml')
                }
            }
        }

        stage('Ping') {
            steps {
                dir('infra/ansible') {
                    withCredentials([sshUserPrivateKey(credentialsId: 'ansible-ssh-key', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                        sh('ansible --private-key $SSH_KEY -u $SSH_USER all -i inventories/hosts.ini -m ping')
                    }
                }
            }
        }

        stage('Run') {
            steps {
                dir('infra/ansible') {
                    withCredentials([sshUserPrivateKey(credentialsId: 'ansible-ssh-key', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                        sh('ansible-playbook --private-key $SSH_KEY -u $SSH_USER -i inventories/hosts.ini site.yml')
                    }
                }
            }
        }
    }
    post {
        cleanup {
            cleanWs()
        }
    }
}
