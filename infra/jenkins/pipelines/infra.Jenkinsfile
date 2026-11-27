pipeline {
    agent any
    parameters {
        booleanParam(name: 'db', defaultValue: false, description: 'db VM')
        booleanParam(name: 'consul', defaultValue: false, description: 'consul VM')
        booleanParam(name: 'app1', defaultValue: false, description: 'app1 VM')
        booleanParam(name: 'app2', defaultValue: false, description: 'app2 VM')
        booleanParam(name: 'lb', defaultValue: false, description: 'lb VM')
        choice(name: 'action', choices: ['up', 'reload', 'destroy'], description: 'what to do with the selected VMs')
    }

    stages {
        stage('Select VMs') {
            steps {
                script {
                    def vms = []
                    if(params.db) { vms.add('db') }
                    if(params.consul) { vms.add('consul') }
                    if(params.app1)   { vms.add('app1') }
                    if(params.app2)   { vms.add('app2') }
                    if(params.lb)     { vms.add('lb') }
                    if(vms.isEmpty()) {error('Select at least one VM')}

                    env.VMS = vms.join(' ')
                    echo "Selected VMs: ${env.VMS}"

                }
            }
        }

        stage('Destroy') {
            when { expression { params.action == 'destroy' } }
            steps {
                dir('infra/packer') {
                    sh('vagrant destroy -f $VMS')
                }
            }
        }

        stage('Up') {
            when { expression { params.action == 'up' } }
            steps {
                dir('infra/packer') {
                    sh('vagrant up $VMS')
                }
            }
        }

        stage('Reload') {
            when { expression { params.action == 'reload' } }
            steps {
                dir('infra/packer') {
                    sh('vagrant reload $VMS')
                }
            }
        }
    }
}