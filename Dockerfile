# ===============================
# Dockerfile optimisé pour Django sur Render
# ===============================
FROM python:3.13-slim

# -------------------------------
# Variables d'environnement
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=false

# -------------------------------
# Définir le répertoire de travail
# -------------------------------
WORKDIR /app

# -------------------------------
# Installer les dépendances système essentielles
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    bash \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Copier uniquement requirements pour le cache Docker
# -------------------------------
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Copier le reste du projet
# -------------------------------
COPY . .

# -------------------------------
# Appliquer les migrations et collecter les fichiers statiques
# -------------------------------
RUN python manage.py migrate --noinput \
    && python manage.py collectstatic --noinput

# -------------------------------
# Exposer le port attendu par Render
# -------------------------------
EXPOSE 10000

# -------------------------------
# Lancer l'application via Gunicorn
# Remplace 'myproject' par le nom de ton projet Django
# -------------------------------
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:10000"]