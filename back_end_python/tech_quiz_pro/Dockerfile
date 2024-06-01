# Utilisez une image Python officielle comme base
FROM python:3.12

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers du projet Django dans le conteneur
COPY . /app

# Installez les dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# Exposez le port sur lequel Django s'exécute par défaut
EXPOSE 8000

# Démarrez le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]