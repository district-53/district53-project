server = true
bootstrap_expect = 1
data_dir = "/opt/consul"
bind_addr = "192.168.56.12"
client_addr = "0.0.0.0"
retry_join = ["192.168.56.12"]
ui_config {
    enabled = true
}