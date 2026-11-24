# Packer: Ubuntu 26.04 Vagrant Box

This folder has a Packer template that builds Vagrant box with Ubuntu Server 26.04.1 for VirtualBox.
## What it does

1. Packer downloads the Ubuntu 26.04.1 live server ISO and checks it with SHA256.
2. It creates a VirtualBox VM (2 CPU, 4 GB RAM, 20 GB disk).
3. Ubuntu installs automatically with cloud-init autoinstall (`http/user-data`). Packer starts a small HTTP server and gives this file to the installer.
4. After the install, Packer connects by SSH as `vagrant` user and runs the scripts:
   - `scripts/vagrant.sh` – adds the Vagrant insecure public keys, disables `UseDNS` in SSH.
   - `scripts/cleanup.sh` – cleans apt cache, logs, machine-id, SSH host keys and fills free space with zeros, so the box is smaller.
5. The Vagrant post-processor packs the VM into a `.box` file.

## Folder structure

```
packer/
|- ubuntu.pkr.hcl      # main Packer template
| http/
|  |- user-data        # autoinstall config (user, packages, sudo, timezone)
|  |- meta-data        # empty, but cloud-init needs this file
|- scripts/
|  |- vagrant.sh       # Vagrant-specific setup
|  |- cleanup.sh       # cleanup before packing the box
|- output/             # result (box + VM disk), not for git
|- packer_cache/       # downloaded ISO, not for git
```

## Requirements

- [Packer](https://developer.hashicorp.com/packer/install) (I use `packer.exe` on Windows)
- [VirtualBox](https://www.virtualbox.org/) 7.x
- [Vagrant](https://developer.hashicorp.com/vagrant/install)
## How to build

Run all commands from the `packer/` folder:

```bash
# 1. Install plugins (virtualbox and vagrant)
./packer init .

# 2. Check the template
./packer validate ubuntu.pkr.hcl

# 3. Build the box
./packer build ubuntu.pkr.hcl
```

The build takes about 15–30 minutes. Don't touch the VirtualBox window while it types the boot command.

If you want to see detailed logs:

```powershell
# PowerShell
$env:PACKER_LOG=1; $env:PACKER_LOG_PATH="packer.log"
packer build ubuntu.pkr.hcl
```

The result will be in `output/ubuntu-26.04.1-virtualbox.box`.

## How to use the box

```bash
vagrant box add --name district53/ubuntu-26.04 output/ubuntu-26.04.1-virtualbox.box
vagrant box list
```

Then in the `Vagrantfile`:

```ruby
config.vm.box = "district53/ubuntu-26.04"
```

## Problems I had (and how I fixed them)

- **Packer waits for SSH forever** – the autoinstall did not start. The reason was a wrong `boot_command`. Now it edits the GRUB line and adds `autoinstall ds=nocloud-net;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/`.
- **Installer asks questions** – the `meta-data` file was missing. It must exist, even if it is empty.

## How to change things

- Ubuntu version: `iso_url` and `iso_checksum` in `ubuntu.pkr.hcl`
- CPU / RAM / disk: `cpus`, `memory`, `disk_size` in `ubuntu.pkr.hcl`
- Packages, timezone, hostname: `http/user-data`
- New password: create a hash with `mkpasswd -m sha-512` and put it in `identity.password`

## Useful links

- [Packer VirtualBox builder](https://developer.hashicorp.com/packer/integrations/hashicorp/virtualbox/latest/components/builder/iso)
- [Ubuntu autoinstall reference](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html)
- [Creating a Vagrant base box](https://developer.hashicorp.com/vagrant/docs/boxes/base)
- https://tferdinand.net/en/create-vagrant-boxes-easily-using-packer/

