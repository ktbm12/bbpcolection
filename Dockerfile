FROM python:3.13-slim

WORKDIR /app

# Copier les fichiers
COPY . .

# Installer bash (si non présent)
RUN apt-get update && apt-get install -y bash

# Rendre le script exécutable
RUN chmod +x build.sh

# Exécuter le build
RUN ./build.sh

# Commande de démarrage
CMD ["gunicorn", "bbpproject.wsgi:application", "--bind", "0.0.0.0:10000"]