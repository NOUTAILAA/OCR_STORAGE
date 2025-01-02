# Utiliser une image légère de Python
FROM python:3.13.1-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour MySQL/MariaDB
RUN apt update && apt install -y gcc musl-dev libffi-dev libssl-dev libmariadb-dev

# Copier les fichiers du projet
COPY . .

# Copier le fichier des dépendances (si existant)
COPY requirements.txt requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Flask
EXPOSE 5002

# Commande pour démarrer l'application
CMD ["python", "app.py"]
