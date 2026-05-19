terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

resource "local_file" "server_config" {
  filename = "${path.module}/config_data.txt"
  content  = "This is the initial configuration."
}