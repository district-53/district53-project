
source "vagrant" "app" {
  source_path   = "district53/base"
  provider      = "virtualbox"
  skip_add      = true   
  communicator  = "ssh"
  insert_key    = false

  output_dir = "output/d53-app"
}

build {
  name    = "app"
  sources = ["source.vagrant.app"]

  provisioner "shell" {
    execute_command  = "sudo env {{ .Vars }} bash '{{ .Path }}'"
    scripts = [
      "scripts/app_setup.sh",
      "scripts/cleanup.sh"
    ]
  }
}