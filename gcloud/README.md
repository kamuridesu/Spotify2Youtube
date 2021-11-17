# Google Cloud Configuration
This Terraform configuration sets up a Google Compute Engine and runs the application on it.

## Changes Needed
Open the [main.tf file on modules](https://github.com/kamuridesu/Spotify2Youtube/blob/main/gcloud/modules/google_computer_instance/main.tf) and change the local-exec provisioner as described there.

I may change this to a variable later.

### Important
Make sure to change the host on the script to "0.0.0.0" and change the callback url to the IP of your GCE. 

## Setup
Follow these steps:
```sh
# Install gcloud sdk
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
gcloud auth application-default login

# Create a SSH key called gcloud
ssh-keygen -t rsa -f ~/.ssh/gcloud

# Install Terraform
sudo pacman -Sy terraform || sudo apt-get install terraform || sudo yum install terraform || xbps-install terraform || dnf install terraform || sudo apt install terraform

```

## Running
First do `echo 'gcloud_ssh_private_key = "path_to_your_private_key"' > variables.auto.tfvars`

Then run `terraform init` to get the modules and providers and initialize the backend. And finnaly, `terraform apply` to apply your configuration.

If you did everything right, the application will be hosted on your Google Cloud Account, and can be accessed with the IP it outputs on the 5000 port.
