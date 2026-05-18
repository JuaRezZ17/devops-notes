resource "local_file" "greeting" {
      content  = "Hello, this is my first resource managed by Terraform"
      filename = "${path.module}/greeting.txt"
    }