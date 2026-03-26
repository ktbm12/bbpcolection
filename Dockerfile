# ===============================
# Dockerfile pour Django sur Render
# ===============================
FROM python:3.13-slim

WORKDIR /app

# Installer bash et dépendances nécessaires pour PostgreSQL
RUN apt-get update && \
    apt-get install -y bash gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copier requirements.txt
COPY bbpproject/requirements.txt ./requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Définir la commande pour lancer l'application
# Migrations + collectstatic + gunicorn
CMD ["sh", "-c", "\
echo 'Lancement des migrations...' && \
python bbpproject/manage.py migrate --noinput && \
echo 'Collectstatic...' && \
python bbpproject/manage.py collectstatic --noinput && \
echo 'Démarrage de Gunicorn...' && \
gunicorn bbpproject.config.wsgi:application --bind 0.0.0.0:$PORT \
"]

EXPOSE 10000