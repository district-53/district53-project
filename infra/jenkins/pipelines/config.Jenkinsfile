pipeline {
    agent { label 'built-in' }

    parameters {
        string(name: 'LIMIT', defaultValue: 'all', description: 'all, or a group: apps, db, lb, consul')
    }

    stages {
        stage('Syntax') {
            steps {
                dir('infra/ansible') {
                    sh('ansible-playbook site.yml --syntax-check')
                }
            }
        }

        stage('Ping') {
            steps {
                dir('infra/ansible') {
                    withCredentials([
                        sshUserPrivateKey(credentialsId: 'ansible-ssh-key', keyFileVariable: 'SSH_KEY'),
                        file(credentialsId: 'ansible-vault-pass', variable: 'VAULT_FILE')
                    ]) {
                        sh('ansible "$LIMIT" -m ping --private-key "$SSH_KEY" --vault-password-file "$VAULT_FILE"')
                    }
                }
            }
        }

        stage('Run') {
            steps {
                dir('infra/ansible') {
                    withCredentials([
                        sshUserPrivateKey(credentialsId: 'ansible-ssh-key', keyFileVariable: 'SSH_KEY'),
                        file(credentialsId: 'ansible-vault-pass', variable: 'VAULT_FILE')
                    ]) {
                        sh('ansible-playbook site.yml --limit "$LIMIT" --private-key "$SSH_KEY" --vault-password-file "$VAULT_FILE"')
                    }
                }
            }
        }
    }
}