#!/bin/bash

# Actualizar lista de paquetes y dependencias
sudo apt-get update

# Instalar dependencias necesarias
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Descargar la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Añadir el repositorio oficial de Docker a las fuentes de apt
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Actualizar lista de paquetes y dependencias con el nuevo repositorio
sudo apt-get update

# Instalar la última versión estable de Docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Agregar el usuario actual al grupo docker para poder ejecutar Docker sin sudo
sudo usermod -aG docker $USER

# Reiniciar el servicio de Docker para que los cambios de permisos tengan efecto
sudo systemctl restart docker
