#!/bin/bash

# Update list of packages and dependencies
sudo apt-get update

# Install necessary dependencies
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Download the official Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add the official docker repository to the apt sources
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update list of packages and dependencies with the new repository
sudo apt-get update

# Install the latest stable version of Docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Add the current user to the docker group so that docker can be run without sudo
sudo usermod -aG docker $USER

# Restart the Docker service for the permission changes to take effect
sudo systemctl restart docker
