# 1. Create ssh key for ansible and change default path 
```ruby
variable "ansible_pubkey_file" {
  type        = string
  default     = "../../keys/ansible.pub"
  description = "Public SSH key for the ansible user"
}
```

# 2. Install plugins (virtualbox and vagrant)
./packer init .

# 3. Check the template
./packer validate ubuntu.pkr.hcl

# 4. Build the box
./packer build ubuntu.pkr.hcl

The result will be in `output/ubuntu-26.04-virtualbox.box`.

# 5. How to use the box

```bash
vagrant box add --name district53/ubuntu-26.04 output/ubuntu-26.04-virtualbox.box
vagrant box list
```

Then in the `Vagrantfile`:

```ruby
config.vm.box = "district53/ubuntu-26.04"
```

# 6. If you want to see detailed logs:

```powershell
$env:PACKER_LOG=1; $env:PACKER_LOG_PATH="packer.log"
packer build ubuntu.pkr.hcl
```
