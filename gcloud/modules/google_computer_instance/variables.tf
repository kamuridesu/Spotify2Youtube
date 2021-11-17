variable "machine_type" {
  description = "Type of the vm. Defaults to f1-micro"
  type        = string
}

variable "boot_image" {
  description = "Image to be used by the VM, defaults to debian-cloud/debian-9"
  type        = string
}

variable "network_interface" {
  description = "The network to be used within the VM connection"
  type        = string
}

variable "gce_ssh_user" {
  description = "ssh user to be logged on gce"
  type        = string
}

variable "gce_ssh_pub_key" {
  description = "public key to login on gce"
  type        = string
}

variable "ssh_private_key" {
  description = "private key for provisioner"
  type        = string
}