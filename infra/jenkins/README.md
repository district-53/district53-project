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