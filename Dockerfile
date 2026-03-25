# ===============================
# Dockerfile pour Django sur Render
# ===============================
FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer bash (optionnel mais utile)
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

# Copier uniquement requirements.txt depuis le sous-dossier bbpproject
COPY bbpproject/requirements.txt ./requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet dans l'image
COPY . .

# Appliquer les migrations et collecter les fichiers statiques
# Attention : si manage.py est dans bbpproject/, ajuster le chemin
RUN python bbpproject/manage.py migrate --noinput \
    && python bbpproject/manage.py collectstatic --noinput

# Définir la commande pour lancer l'application
# Remplace 'bbpproject' par le nom de ton projet Django qui contient wsgi.py
CMD ["gunicorn", "bbpproject.wsgi:application", "--bind", "0.0.0.0:10000"]

# Exposer le port attendu par Render
EXPOSE 10000