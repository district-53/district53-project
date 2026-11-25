packer {
  required_plugins {
    virtualbox = {
      version = "~> 1"
      source  = "github.com/hashicorp/virtualbox"
    }
    vagrant = {
      version = "~> 1"
      source  = "github.com/hashicorp/vagrant"
    }
  }
}

variable "ansible_pubkey_file" {
  type        = string
  default     = "../../keys/ansible.pub"
  description = "Public SSH key for the ansible user"
}


source "virtualbox-iso" "ubuntu" {
  vm_name       = "ubuntu-26.04"
  guest_os_type = "Ubuntu_64"
  iso_url       = "https://releases.ubuntu.com/resolute/ubuntu-26.04-live-server-amd64.iso"
  iso_checksum  = "file:https://releases.ubuntu.com/resolute/SHA256SUMS"

  cpus      = 2
  memory    = 4096
  disk_size = 20480

  output_directory     = "output/vm-ubuntu"
  guest_additions_mode = "disable"
  http_directory       = "http"

  vboxmanage = [
    ["modifyvm", "{{ .Name }}", "--nat-localhostreachable1", "on"],
  ]

  boot_wait = "5s"
  boot_command = [
    "c<wait>",
    "linux /casper/vmlinuz --- autoinstall ds=\"nocloud-net;seedfrom=http://{{ .HTTPIP }}:{{ .HTTPPort }}/\"",
    "<enter><wait>",
    "initrd /casper/initrd",
    "<enter><wait>",
    "boot",
    "<enter>"
  ]

  shutdown_command = "sudo -S shutdown -P now"

  ssh_username = "vagrant"
  ssh_password = "vagrant"
  ssh_timeout  = "30m"
}

build {
  sources = ["source.virtualbox-iso.ubuntu"]

  provisioner "shell" {
    execute_command  = "sudo env {{ .Vars }} bash '{{ .Path }}'"
    environment_vars = [
      "ANSIBLE_PUBKEY=${trimspace(file(var.ansible_pubkey_file))}",
    ]
    scripts = [
      "scripts/base.sh",
      "scripts/vagrant.sh",
      "scripts/add_user_ansible.sh",
      "scripts/consul_base.sh",
      "scripts/cleanup.sh",
    ]
  }

  post-processor "vagrant" {
    output = "output/ubuntu-26.04.1-{{ .Provider }}.box"
  }
}