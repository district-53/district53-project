# Jenkins VM

Vagrant creates the VM from the base box. Ansible installs Java and Jenkins and configures them (no setup wizard, plugins, admin account with JCasC).

## Before you start
Create the admin password file:
```bash
echo "your-password" > infra/secrets/jenkins_admin_password
```

## Run
```bash
cd infra/jenkins
vagrant up
```
On Apple Silicon:
```bash
JENKINS_BOX=bento/ubuntu-24.04 vagrant up
```

Open http://192.168.56.30:8080 and log in as `admin` with the password from `infra/secrets/jenkins_admin_password`.

## Change config
Edit `ansible/jenkins.yml`, `ansible/plugins.txt` or `ansible/templates/jenkins.yaml.j2`, then:
```bash
vagrant provision
```

## Pipelines

Jenkins creates 3 jobs on startup. Jenkinsfiles are in `infra/jenkins/pipelines/` and are read from `main`.

| Job      | Runs on      | What it does                                                    |
|----------|--------------|-----------------------------------------------------------------|
| `packer` | `host` agent | validate or build images: `base`, `db`, `app`, `lb`, `jenkins`  |
| `infra`  | `host` agent | `up`, `reload`, `halt` or `destroy` selected VMs                |
| `config` | Jenkins      | Ansible: syntax check, ping, run `site.yml`                     |

### Ansible key
Generate it as described in `infra/packer/README.md`(`infra/packer/keys/ansible`). `vagrant provision` adds it to Jenkins as the `ansible-ssh-key` credential.

### Agent: `host`
Packer and Vagrant run on the host machine, not inside the Jenkins VM.

Requirements: Java 17+, Packer, Vagrant, VirtualBox.

1. `mkdir -p ~/jenkins-agent`
2. In Jenkins: Manage Jenkins → Nodes → `host`, copy the commands and run them in `~/jenkins-agent`. Don't share the secret.
3. Wait for `INFO: Connected`. Keep the terminal open.

### Run a job
The first run of a job only loads the parameters. After that use **Build with Parameters**.