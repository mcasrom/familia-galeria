#!/bin/bash

# Script de setup rápido para Family_Project
# Coloca los templates en app/templates y asegura permisos correctos

APP_DIR="$HOME/Family_Project/app"
TEMPLATES_DIR="$APP_DIR/templates"

echo "Verificando carpeta de templates..."
mkdir -p "$TEMPLATES_DIR"

# Contenido de login.html
cat > "$TEMPLATES_DIR/login.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Login - Family Project</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        <button type="submit">Entrar</button>
    </form>
    {% if error %}
        <p style="color:red">{{ error }}</p>
    {% endif %}
</body>
</html>
EOF

# Contenido de gallery.html
cat > "$TEMPLATES_DIR/gallery.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Galería - Family Project</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
<h2>Galería de Fotos</h2>

<div class="gallery">
    {% for foto in fotos %}
    <div class="photo-card">
        <img src="{{ url_for('fotos', filename=foto) }}" onclick="openModal('{{ url_for('fotos', filename=foto) }}')">
        <form method="post" action="{{ url_for('delete', filename=foto) }}">
            <button type="submit">Eliminar</button>
        </form>
        <input type="text" value="{{ tags.get(foto, '') }}" onchange="updateTag('{{ foto }}', this.value)">
    </div>
    {% endfor %}
</div>

<!-- Modal -->
<div id="modal" onclick="closeModal()">
    <span id="close">&times;</span>
    <img id="modal-img">
</div>

<script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
EOF

echo "Templates colocados correctamente en $TEMPLATES_DIR"
echo "Ahora activa tu venv y arranca la app:"
echo "  cd ~/Family_Project"
echo "  source venv/bin/activate"
echo "  python3 app/main.py"
