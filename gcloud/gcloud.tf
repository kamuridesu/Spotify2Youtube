terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.87.0"
    }
  }
}

provider "google" {
  project = "terraform-328013"
  region  = "us-central-1"
  zone    = "us-central1-c"
}

module "google_computer_instance" {
  source            = "./modules/google_computer_instance"
  machine_type      = var.machine_type
  boot_image        = var.boot_image
  network_interface = var.network
  gce_ssh_pub_key   = var.gcloud_public_ssh_key
  gce_ssh_user      = var.ssh_user
  ssh_private_key   = var.gcloud_ssh_private_key
}