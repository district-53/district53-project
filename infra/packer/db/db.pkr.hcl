
source "vagrant" "db" {
  source_path   = "output/d53-base/d53-base-v1.box"
  box_name      = "d53-base"
  provider      = "virtualbox"
  communicator  = "ssh"
  add_force     = true
  insert_key    = false

  output_dir = "output/d53-db"
}

build {
  name    = "db"
  sources = ["source.vagrant.db"]

  provisioner "shell" {
    execute_command = "{{ .Vars }} sudo -E bash '{{ .Path }}'"
    scripts = [
      "scripts/db_setup.sh",
      "scripts/cleanup.sh",
    ]
  }
}