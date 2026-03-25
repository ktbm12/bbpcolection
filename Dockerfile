# ===============================
# Dockerfile pour Django sur Render
# ===============================
FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . .

# Installer bash (optionnel mais utile)
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Appliquer les migrations et collecter les fichiers statiques
RUN python manage.py migrate --noinput \
    && python manage.py collectstatic --noinput

# Définir la commande pour lancer l'application
# Remplace 'myproject' par le nom de ton dossier Django qui contient wsgi.py
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:10000"]

# Exposer le port attendu par Render
EXPOSE 10000