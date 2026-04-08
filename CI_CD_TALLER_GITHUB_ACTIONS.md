# Taller: Integración Continua con GitHub Actions + Render

## Objetivo
Aprender a automatizar el despliegue de una aplicación Python usando GitHub Actions y Render (servicio en la nube gratuito).

---

## Índice
1. [Prerrequisitos](#prerrequisitos)
2. [Conceptos Clave de CI/CD](#conceptos-clave)
3. [Setup del Proyecto](#setup-del-proyecto)
4. [Configurar Render](#configurar-render)
5. [Crear el Workflow de GitHub Actions](#crear-workflow)
6. [Pruebas y Validación](#pruebas)
7. [Troubleshooting](#troubleshooting)

---

## Prerrequisitos

### Herramientas Necesarias
- Git instalado en tu máquina
- Cuenta en GitHub (gratuita)
- Cuenta en Render (gratuita): https://render.com
- Python 3.9+ instalado
- Acceso a terminal/cmd

### Cuentas Requeridas
1. **GitHub**: para alojar código y configurar workflows
2. **Render**: para desplegar aplicación en la nube sin costo

---

## Conceptos Clave de CI/CD

### ¿Qué es CI/CD?
- **CI (Integración Continua)**: Cada que subes código, se ejecutan pruebas automáticamente
- **CD (Despliegue Continuo)**: Si las pruebas pasan, el código se despliega automáticamente a producción

### GitHub Actions
- Servicio de automatización incluido en GitHub
- Ejecuta scripts cuando ocurren eventos (push, pull request, etc.)
- Gratuito para repositorios públicos
- Se define en archivos YAML en `.github/workflows/`

### Render
- Plataforma de despliegue moderna
- Tier gratuito: 750 horas/mes de servidor
- Se conecta directamente a GitHub
- Auto-redeploy cuando detecta cambios

---

## Setup del Proyecto

### Paso 1: Clonar o Crear el Repositorio

```bash
# Opción A: Si ya tienes un repo
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# Opción B: Crear repositorio nuevo
mkdir mi-app-python
cd mi-app-python
git init
git remote add origin https://github.com/tu-usuario/mi-app-python.git
```

### Paso 2: Estructura del Proyecto

Asegúrate de que tu proyecto tenga esta estructura:

```
mi-app-python/
├── Makefile
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── app.py
├── test_app.py
└── README.md
```

### Paso 3: Crear Archivo `requirements.txt`

```
flask==2.3.0
matplotlib==3.7.0
pandas==2.0.0
pytest==7.3.0
gunicorn==20.1.0
```

### Paso 4: Crear `Makefile`

```makefile
.PHONY: install test run help

help:
	@echo "Comandos disponibles:"
	@echo "  make install    - Instalar dependencias"
	@echo "  make test       - Ejecutar pruebas"
	@echo "  make run        - Ejecutar aplicación localmente"
	@echo "  make clean      - Limpiar archivos temporales"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest test_app.py -v

run:
	python app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache
```

### Paso 5: Crear Aplicación Flask Simple

**Archivo: `app.py`**

```python
from flask import Flask, render_template_string
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
import pandas as pd

matplotlib.use('Agg')  # Backend sin GUI

app = Flask(__name__)

def generate_chart():
    """Genera gráfico y lo convierte a base64 para HTML"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Datos de ejemplo
    x = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    y = [65, 78, 90, 81, 88, 95]
    
    ax.plot(x, y, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    ax.fill_between(range(len(x)), y, alpha=0.3, color='#2E86AB')
    ax.set_title('Ventas Mensuales', fontsize=16, fontweight='bold')
    ax.set_ylabel('Ingresos ($1000s)', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Convertir a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

@app.route('/')
def index():
    chart = generate_chart()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CI/CD Dashboard</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            .status {{
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
                font-weight: bold;
            }}
            img {{
                width: 100%;
                border-radius: 5px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Aplicación con CI/CD</h1>
            <div class="status">✅ Sistema en funcionamiento</div>
            <img src="{chart}" alt="Gráfico de ventas">
            <p style="text-align: center; color: #666;">
                Este gráfico se genera automáticamente en cada despliegue
            </p>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html)

@app.route('/health')
def health():
    """Endpoint para health checks"""
    return {'status': 'healthy', 'message': 'App is running'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### Paso 6: Crear Pruebas Unitarias

**Archivo: `test_app.py`**

```python
import pytest
from app import app

@pytest.fixture
def client():
    """Crea cliente de prueba"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Prueba que la página principal carga correctamente"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'CI/CD' in response.data

def test_health_endpoint(client):
    """Prueba el endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_health_returns_json(client):
    """Valida que health retorna JSON válido"""
    response = client.get('/health')
    assert response.content_type == 'application/json'
```

---

## Configurar Render

### Paso 1: Crear Cuenta en Render

1. Ve a https://render.com
2. Haz clic en "Sign Up"
3. Conecta tu cuenta de GitHub
4. Autoriza a Render para acceder a tus repositorios

### Paso 2: Crear un Servicio Web

1. En el dashboard de Render, haz clic en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio GitHub (selecciona el repo con tu código)
4. Completa la configuración:
   - **Name**: `mi-app-python`
   - **Region**: Selecciona la más cercana (ej: Ohio para Norteamérica)
   - **Branch**: `main` o `master`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free` (es suficiente para demostración)

5. Haz clic en "Create Web Service"

### Paso 3: Obtener URL de Render

- Una vez desplegado, Render te dará una URL pública (ej: `https://mi-app-python.onrender.com`)
- Guarda esta URL, la necesitarás en GitHub Actions

### Paso 4: Crear Deploy Hook en Render

1. En Render, ve a tu servicio web
2. Copia el **Deploy Hook** (en Settings → Deploy Hooks)
3. Ese hook es un endpoint que puedes llamar para triggerar un redeploy

---

## Crear el Workflow de GitHub Actions

### Paso 1: Crear Archivo del Workflow

Crea el archivo `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout código
      uses: actions/checkout@v3
    
    - name: 🐍 Configurar Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: 📦 Instalar dependencias
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: 🧪 Ejecutar pruebas
      run: |
        pytest test_app.py -v --tb=short
    
    - name: 🔍 Análisis básico de código
      run: |
        pip install pylint
        pylint app.py --fail-under=7.0 || echo "Linting warnings (no critical)"

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
    - name: 📥 Checkout código
      uses: actions/checkout@v3
    
    - name: 🚀 Triggerar deploy en Render
      run: |
        curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
      env:
        DEPLOY_HOOK: ${{ secrets.RENDER_DEPLOY_HOOK }}
```

### Paso 2: Agregar el Deploy Hook como Secret en GitHub

1. En tu repositorio GitHub, ve a **Settings → Secrets and variables → Actions**
2. Haz clic en "New repository secret"
3. Nombre: `RENDER_DEPLOY_HOOK`
4. Valor: Pega el URL que copiaste de Render
5. Haz clic en "Add secret"

### Paso 3: Hacer Push del Código

```bash
git add .
git commit -m "Agregar CI/CD con GitHub Actions y Render"
git push origin main
```

---

## Pruebas y Validación

### Paso 1: Ver Workflow en GitHub

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña **Actions**
3. Deberías ver tu workflow ejecutándose
4. Haz clic en la ejecución para ver los detalles

### Paso 2: Validar Despliegue

- Una vez que el workflow termine (si todo va bien), tu app estará desplegada en Render
- Abre tu URL de Render en el navegador
- Deberías ver la página con el gráfico

### Paso 3: Hacer un Cambio para Probar CI/CD

1. Modifica `app.py` (ej: cambia el color del gráfico)
2. Haz commit y push:
   ```bash
   git add app.py
   git commit -m "Cambiar color del gráfico"
   git push origin main
   ```
3. Ve a Actions y observa cómo se ejecuta automáticamente
4. El despliegue se hará automáticamente si las pruebas pasan

---

## Troubleshooting

### El workflow falla en pruebas
- Verifica que `pytest` está en `requirements.txt`
- Revisa los logs del workflow en GitHub Actions
- Ejecuta `make test` localmente para replicar el error

### Deploy hook no funciona
- Verifica que el secret `RENDER_DEPLOY_HOOK` está correctamente configurado
- Copia y pega nuevamente el hook desde Render
- En GitHub, ve a Settings → Secrets y valida

### La app no se ve en Render
- Espera 2-3 minutos después del despliegue
- Verifica los logs en Render (Logs tab)
- Asegúrate que `gunicorn app:app` es el Start Command correcto

### Puerto incorrecto
- Render automáticamente asigna el puerto a través de una variable de entorno
- En `app.py`, cambia la línea final a:
  ```python
  if __name__ == '__main__':
      import os
      port = int(os.environ.get('PORT', 5000))
      app.run(host='0.0.0.0', port=port, debug=False)
  ```

---

## Conceptos Extras para Discutir en el Taller

### Matrix Strategy (Pruebas en múltiples versiones de Python)
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11']

steps:
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
```

### Notifications (Notificaciones en Slack/Email)
```yaml
- name: Notificar éxito
  if: success()
  run: echo "✅ Deploy exitoso"

- name: Notificar fallo
  if: failure()
  run: echo "❌ Deploy falló"
```

### Scheduled Workflows (Ejecutar en horarios específicos)
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Ejecutar diariamente a las 2 AM UTC
```

---

## Recursos Adicionales

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Render Docs**: https://render.com/docs
- **Python Testing**: https://docs.pytest.org/
- **Flask**: https://flask.palletsprojects.com/

---

## Resumen del Workflow Completo

```
Desarrollador hace push a GitHub
         ↓
GitHub Actions se dispara automáticamente
         ↓
✅ Instala dependencias
✅ Ejecuta pruebas
✅ Análisis de código
         ↓
Si TODO es OK:
         ↓
Triggerea deploy hook en Render
         ↓
Render actualiza la app en la nube
         ↓
✅ Nueva versión disponible en https://tu-app.onrender.com
```

---

**¡Tu taller está listo! Buena suerte con la presentación en el Tec.** 🚀
