packer {
  required_plugins {
    vagrant = {
      version = "~> 1"
      source  = "github.com/hashicorp/vagrant"
    }
  }
}

variable "base_box" {
  type        = string
  default     = "district53/ubuntu-26.04"
  description = "Base box built from infra/packer/base"
}

source "vagrant" "jenkins" {
  source_path  = var.base_box
  provider     = "virtualbox"
  communicator = "ssh"
  output_dir   = "output/jenkins"
  skip_add     = true
}

build {
  sources = ["source.vagrant.jenkins"]
  provisioner "shell" {
    execute_command = "sudo env {{ .Vars }} bash '{{ .Path }}'"
    scripts = [
      "scripts/install_jenkins.sh",
      "../base/scripts/cleanup.sh",
    ]
  }
}