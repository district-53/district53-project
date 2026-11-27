
source "vagrant" "db" {
  source_path   = "district53/base"
  provider      = "virtualbox"
  skip_add      = true
  communicator  = "ssh"
  insert_key    = false

  output_dir = "output/d53-db"
}

build {
  name    = "db"
  sources = ["source.vagrant.db"]

  provisioner "shell" {
    execute_command  = "sudo env {{ .Vars }} bash '{{ .Path }}'"
    scripts = [
      "scripts/db_setup.sh",
      "scripts/cleanup.sh",
    ]
  }
}