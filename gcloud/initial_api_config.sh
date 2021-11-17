sudo apt update
sudo apt install git ca-certificates curl gnupg lsb-release apt-transport-https -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
git clone https://github.com/kamuridesu/Spotify2Youtube.git
cd Spotify2Youtube
sudo docker build -t api .
sudo docker run -d --name api -p 5000:5000 api