variable "machine_type" {
  description = "Type of the vm. Defaults to f1-micro"
  type        = string
  default     = "f1-micro"
}

variable "boot_image" {
  description = "Image to be used by the VM, defaults to debian-cloud/debian-9"
  type        = string
  default     = "debian-cloud/debian-9"
}

variable "network" {
  description = "The network to be used within the VM connection"
  type        = string
  default     = "default"
}

variable "ssh_user" {
  description = "ssh user to be logged on gce"
  type        = string
  default     = "kamuri"
}

variable "gcloud_public_ssh_key" {
  description = "public key to login on gce"
  type        = string
  default     = "~/.ssh/gcloud.pub"
}

variable "gcloud_ssh_private_key" {
  description = "ssh private key to provisioner"
  type        = string
}
