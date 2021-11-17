resource "google_compute_firewall" "allow_http" {
  name    = "allow-http"
  network = var.network_interface
  allow {
    ports    = ["5000"]
    protocol = "tcp"
  }
  target_tags = ["allow-http"]
  priority    = 1000
}

resource "google_compute_address" "static" {
  name   = "ipv4-address"
  region = "us-central1"
}

resource "google_compute_instance" "vm_instance" {
  name         = "tf-instance"
  machine_type = var.machine_type
  metadata = {
    ssh-keys = "${var.gce_ssh_user}:${var.gce_ssh_pub_key}"
  }

  boot_disk {
    initialize_params {
      image = var.boot_image
    }
  }

  network_interface {
    network = var.network_interface
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }

  # metadata_startup_script = file("./initial_api_config.sh")

  provisioner "remote-exec" {
    inline = ["sudo apt update",
      "sudo apt install git ca-certificates curl gnupg lsb-release apt-transport-https -y",
      "curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
      "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
      "sudo apt-get update",
      "sudo apt-get install docker-ce docker-ce-cli containerd.io -y",
      "curl https://gist.githubusercontent.com/kamuridesu/a3bd18849f2067efccec3140627cd9a8/raw/26b00ad996384dddee72e0ee13beec8d642ad332/api.py > api.py",
      "curl https://gist.githubusercontent.com/kamuridesu/a3bd18849f2067efccec3140627cd9a8/raw/26b00ad996384dddee72e0ee13beec8d642ad332/products.json > products.json",
      "curl https://gist.githubusercontent.com/kamuridesu/a3bd18849f2067efccec3140627cd9a8/raw/26b00ad996384dddee72e0ee13beec8d642ad332/requirements.txt > requirements.txt",
      "curl https://gist.githubusercontent.com/kamuridesu/a3bd18849f2067efccec3140627cd9a8/raw/26b00ad996384dddee72e0ee13beec8d642ad332/Dockerfile > Dockerfile",
      "sudo docker build -t api .",
      "sudo docker run -d --name api -p 5000:5000 api"
    ]
    on_failure = fail

    connection {
      type        = "ssh"
      user        = var.gce_ssh_user
      private_key = var.ssh_private_key
      host        = self.network_interface[0].access_config[0].nat_ip
    }
  }

  tags = ["http-server", "https-server", "allow-http"]
}