
source "vagrant" "lb" {
    source_path   = "district53/base"
    provider      = "virtualbox"
    skip_add      = true   
    communicator  = "ssh"
    insert_key    = false

    output_dir = "output/d53-lb"
}


build {
    name    = "lb"
    sources = ["source.vagrant.lb"]

    provisioner "shell" {
        execute_command  = "sudo env {{ .Vars }} bash '{{ .Path }}'"
        scripts = [
        "scripts/lb_setup.sh",
        "scripts/cleanup.sh"
        ]
    }
}