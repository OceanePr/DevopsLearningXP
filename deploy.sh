#!/bin/bash

# Script d'automatisation pour déployer une application FastAPI avec PostgreSQL

echo "Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

echo "Installation des dépendances nécessaires..."
sudo apt install -y python3 python3-pip git postgresql-client

echo "Clonage du dépôt GitHub..."
# Cloner le dépôt GitHub
if [ ! -d "DevopsLearningXP" ]; then
    git clone https://github.com/OceanePr/DevopsLearningXP.git
else
    echo "Le dépôt existe déjà, mise à jour du dépôt..."
    cd DevopsLearningXP
    git pull
    cd ..
fi

cd DevopsLearningXP

echo "Installation des dépendances Python..."
# Installer les dépendances depuis requirements.txt
pip3 install -r requirements.txt

echo "Lancement de l'application FastAPI..."
# Lancer l'application FastAPI avec Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
