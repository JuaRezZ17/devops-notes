output "instance_public_ip" {
  description = "The public IP address of the newly created EC2 instance"
  value       = aws_instance.web.public_ip
}