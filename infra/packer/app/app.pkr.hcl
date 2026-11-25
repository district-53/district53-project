
source "vagrant" "app" {
  source_path   = "output/d53-base/d53-base-v1.box"
  box_name      = "d53-base"
  provider      = "virtualbox"
  communicator  = "ssh"
  add_force     = true
  insert_key    = false

  output_dir = "output/d53-app"
}

build {
  name    = "app"
  sources = ["source.vagrant.app"]

  provisioner "shell" {
    execute_command = "{{ .Vars }} sudo -E bash '{{ .Path }}'"
    scripts = [
      "scripts/app_setup.sh"
    ]
  }
}