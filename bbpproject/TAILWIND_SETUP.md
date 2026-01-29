# Configuration Tailwind CSS

## 🎨 Développement local

### Installation initiale
```bash
npm install
```

### Mode watch (dev) - CSS récompilé à chaque modification
```bash
npm run dev
```

### Build production (minifié)
```bash
npm run build
```

## 📝 Notes

- Le fichier d'entrée est: `bbpproject/static/css/input.css`
- Le fichier compilé est: `bbpproject/static/css/output.css` (généré automatiquement)
- Configuration: `tailwind.config.js` (contient les templates à scanner)
- PostCSS config: `postcss.config.js`

## 🚀 Démarrage recommandé

1. Pour le développement, lancez dans un terminal:
   ```bash
   npm run dev
   ```

2. Dans un autre terminal, lancez Django normalement:
   ```bash
   python manage.py runserver
   ```

3. Le CSS sera automatiquement recompilé quand vous modifiez les templates ou les fichiers CSS

## 📦 Fichiers générés

- `output.css` - Ne pas éditer manuellement, généré automatiquement
- `package-lock.json` - Commitez ce fichier pour la reproductibilité
