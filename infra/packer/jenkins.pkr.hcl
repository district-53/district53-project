
source "vagrant" "jenkins" {
  source_path  = "output/d53-base/d53-base-v1.box"
  box_name      = "district53/base"
  provider     = "virtualbox"
  communicator = "ssh"
  output_dir   = "output/d53-jenkins"
}

build {
  sources = ["source.vagrant.jenkins"]
  provisioner "shell" {
    execute_command  = "sudo env {{ .Vars }} bash '{{ .Path }}'"
    scripts = [
      "scripts/install_jenkins.sh",
      "scripts/cleanup.sh",
    ]
  }
}