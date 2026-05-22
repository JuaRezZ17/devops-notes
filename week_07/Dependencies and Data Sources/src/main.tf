provider "aws" {
  region = "eu-south-2"
}

# 1. Data Source
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# 2. Dynamic Instance
resource "aws_instance" "web_server" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer-AL2023"
  }
}

# 3. EIP
resource "aws_eip" "static_ip" {
  instance = aws_instance.web_server.id
  domain   = "vpc"
}