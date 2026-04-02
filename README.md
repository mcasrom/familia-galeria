# Galería Familiar 📷

Galería de fotografías familiares restauradas con IA. Principios del siglo XX.

## Estructura

```
familia-galeria/
├── main.py              # Flask app
├── Procfile             # Render/gunicorn
├── requirements.txt
├── data/
│   └── tags.json        # Descripciones de fotos
├── static/
│   └── images/          # ← Fotos aquí (jpg, jpeg, png, webp)
└── templates/
    ├── login.html
    └── gallery.html
```

## Añadir fotos

Copiar las fotos a `static/images/` y hacer push:

```bash
cp ~/FotosAntiguas/*.jpg static/images/
git add static/images/
git commit -m "fotos: añadir nueva colección"
git push
```

**Nombre recomendado:** `YYYY_descripcion.jpg` → el año aparece automáticamente en la galería.  
Ejemplo: `1935_boda_abuelos.jpg`

## Variables de entorno en Render

| Variable      | Valor por defecto |
|---------------|-------------------|
| SECRET_KEY    | (generar uno)     |
| ADMIN_USER    | admin             |
| ADMIN_PASS    | admin123          |
| FAMILY_USER   | Family            |
| FAMILY_PASS   | 4321              |

## Deploy en Render

1. Conectar repo `familia-galeria` en Render → New Web Service
2. **Build command:** `pip install -r requirements.txt`
3. **Start command:** `gunicorn main:app --bind 0.0.0.0:$PORT`
4. Añadir las variables de entorno
5. Deploy

## Local

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```
