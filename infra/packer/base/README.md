# 1. Install plugins (virtualbox and vagrant)
./packer init .

# 2. Check the template
./packer validate ubuntu.pkr.hcl

# 3. Build the box
./packer build ubuntu.pkr.hcl

The result will be in `output/ubuntu-26.04-virtualbox.box`.

## How to use the box

```bash
vagrant box add --name district53/ubuntu-26.04 output/ubuntu-26.04-virtualbox.box
vagrant box list
```

Then in the `Vagrantfile`:

```ruby
config.vm.box = "district53/ubuntu-26.04"


If you want to see detailed logs:

```powershell
$env:PACKER_LOG=1; $env:PACKER_LOG_PATH="packer.log"
packer build ubuntu.pkr.hcl
```