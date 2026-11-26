
source "vagrant" "lb" {
    source_path = "output/d53-base/d53-base-v1.box"
    box_name      = "district53/base"
    provider      = "virtualbox"
    communicator  = "ssh"
    add_force     = true
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