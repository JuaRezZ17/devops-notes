terraform {
  backend "s3" {
    bucket         = "my-terraform-state-devops-825967678288-eu-west-1-an"   # 1
    key            = "global/s3/terraform.tfstate"                           # 2
    region         = "eu-west-1"                                             # 3
    use_lockfile   = true                                                    # 4
  }
}

resource "local_file" "my_hello_file" {
  content  = "Hello, remote backend!"
  filename = "${path.module}/hello.txt"
}