pipeline {
    agent any

    stages {
        stage('Init') {
            steps {
                dir('infra/packer') {
                    sh('packer init .')
                }
            }
        }

        stage('Validate') {
            steps {
                dir('infra/packer') {
                    sh('packer validate base.pkr.hcl')
                }
            }
        }

        stage('Build base') {
            steps {
                dir('infra/packer') {
                    sh('packer build -force base.pkr.hcl')
                }
            }
        }

        stage('Add base box') {
            steps {
                dir('infra/packer') {
                    sh('vagrant box add --force --name district53/base output/d53-base/d53-base-v1.box')
                }
            }
        }

        stage('Build boxes') {
            steps {
                dir('infra/packer') {
                    sh('packer build -force lb.pkr.hcl')
                    sh('packer build -force db.pkr.hcl')
                    sh('packer build -force jenkins.pkr.hcl')
                    sh('packer build -force app.pkr.hcl')
                }
            }
        }

        stage('Add boxes') {
            steps {
                dir('infra/packer') {
                    sh('vagrant box add --force --name district53/lb  output/d53-lb/package.box')
                    sh('vagrant box add --force --name district53/db  output/d53-db/package.box')
                    sh('vagrant box add --force --name district53/jenkins output/jenkins/package.box')
                    sh('vagrant box add --force --name district53/app output/d53-app/package.box')
                }
            }
        }
    }
}