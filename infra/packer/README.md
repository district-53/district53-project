
```bash
plugins.pkr.hcl  - plugins for Packer
ubuntu.pkr.hcl   - base box ubuntu 26.04

lb.pkr.hcl       - box for lb VM
jenkins.pkr.hcl  - box for jenkins + ansible VM
db.pkr.hcl       - box for db VM
app.pkr.hcl      - box for app VM
```



# 1. Create ssh key for ansible and change default path 
```ruby
variable "ansible_pubkey_file" {
  type        = string
  default     = "keys/ansible.pub"
  description = "Public SSH key for the ansible user"
}
```

# * Create SSH keys

Run all commands from the folder packer
### Linux

```bash
mkdir -p keys
ssh-keygen -t ed25519 -f keys/ansible -C "ansible@vagrant" -N ""
chmod 700 keys
chmod 600 keys/ansible
chmod 644 keys/ansible.pub
```

### macOS

The same as Linux (open the **Terminal** app):

```bash
mkdir -p keys
ssh-keygen -t ed25519 -f keys/ansible -C "ansible@vagrant" -N ""
chmod 700 keys
chmod 600 keys/ansible
chmod 644 keys/ansible.pub
```

### Windows (PowerShell)

Windows 10/11 already has OpenSSH. Open **PowerShell** in the project folder:

```bash
New-Item -ItemType Directory -Force -Path keys
ssh-keygen -t ed25519 -f keys\ansible -C "ansible@vagrant"
```

When it asks for a passphrase, press Enter two times (empty passphrase).

Then give access to the private key only to your user.


# * For arm64. Change: iso_url and iso_checksum
```ruby
iso_url       = "https://cdimage.ubuntu.com/ubuntu/releases/26.04/release/ubuntu-26.04-live-server-arm64.iso"

iso_checksum  = "file:https://cdimage.ubuntu.com/ubuntu/releases/26.04/release/SHA256SUMS"
```

# 2. Install plugins
./packer init .

# 3. Check the template
./packer validate base.pkr.hcl

# 4. Build the box
./packer build base.pkr.hcl

The result will be in `output/d53-base/d53-base-v1.box`.

# 5. How to use the box

```bash
vagrant box add --name district53/base output/d53-base/d53-base-v1.box
vagrant box list
```

# 6. If you want to see detailed logs:

```bash
# ADD:
$env:PACKER_LOG=1; $env:PACKER_LOG_PATH="packer.log"
# before:
./packer build base.pkr.hcl
```


# 7. Create boxes 

```bash
packer build lb.pkr.hcl
packer build db.pkr.hcl 
packer build jenkins.pkr.hcl
packer build app.pkr.hcl 
```
# 8. ADD to vagrant
```bash
vagrant box add --name district53/lb  output\d53-lb\package.box
vagrant box add --name district53/db  output\d53-db\package.box
vagrant box add --name district53/jenkins output\jenkins\package.box
vagrant box add --name district53/app output\d53-app\package.box
```

# 9. Start all VM
```bash
vagrant up
vagrant status
```