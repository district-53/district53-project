def selectImage() {
    def images = []
    if (params.db)      { images.add('db') }
    if (params.app)     { images.add('app') }
    if (params.lb)      { images.add('lb') }
    if (params.jenkins) { images.add('jenkins') }

    def baseMissing = sh(script: 'vagrant box list | grep -q "^district53/base "', returnStatus: true) != 0
    if (params.base || (!images.isEmpty() && baseMissing)) {
        images.add(0, 'base')
    }

    if (images.isEmpty()) { error('Select at least one image') }

    return images
}

pipeline {
    agent { label 'host' }
    parameters {
        booleanParam(name: 'base', defaultValue: false, description: 'Rebuild the base image')
        booleanParam(name: 'db', defaultValue: false, description: 'db image')
        booleanParam(name: 'app', defaultValue: false, description: 'app image: app1, app2')
        booleanParam(name: 'lb', defaultValue: false, description: 'lb image')
        booleanParam(name: 'jenkins', defaultValue: false, description: 'jenkins image')
        choice(name: 'action', choices: ['validate', 'build'], description: 'validate = check templates only, build = build and add boxes')
    }

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
                    script {
                        for (img in selectImage()) {
                            sh("packer validate ${img}.pkr.hcl")
                        }
                    }
                }
            }
        }

        stage('Build and add') {
            when { expression { params.action == 'build' } }
            steps {
                dir('infra/packer') {
                    script {
                        def boxFiles = [
                            base: 'output/d53-base/d53-base-v1.box',
                            db: 'output/d53-db/package.box',
                            app: 'output/d53-app/package.box',
                            lb: 'output/d53-lb/package.box',
                            jenkins: 'output/jenkins/package.box',
                        ]
                        for (img in selectImage()) {
                            sh("packer build -force ${img}.pkr.hcl")
                            sh("vagrant box add --force --name district53/${img} ${boxFiles[img]}")
                        }
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