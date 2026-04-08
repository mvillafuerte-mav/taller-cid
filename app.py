#!/usr/bin/env python3
"""
Aplicación Flask - CI/CD Workshop
Ejecutar con: python app.py
Desplegar con Gunicorn: gunicorn app:app
"""

import os
import io
import base64
from flask import Flask, render_template_string, jsonify
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Usar backend sin GUI (importante para servidores)
matplotlib.use('Agg')

app = Flask(__name__)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def generate_sales_chart():
    """Genera gráfico de ventas mensuales"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    ventas = [65, 78, 90, 81, 88, 95]
    
    ax.plot(meses, ventas, marker='o', linewidth=3, markersize=10, color='#2E86AB')
    ax.fill_between(range(len(meses)), ventas, alpha=0.3, color='#2E86AB')
    ax.set_title('Ventas Mensuales', fontsize=14, fontweight='bold')
    ax.set_ylabel('Ingresos ($1000s)', fontsize=11)
    ax.set_xlabel('Mes', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Convertir a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

def generate_metrics_chart():
    """Genera gráfico de métricas por región"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    regiones = ['Norte', 'Centro', 'Sur', 'Oriente', 'Occidente']
    valores = [85, 92, 78, 88, 81]
    colores = ['#E63946', '#457B9D', '#A8DADC', '#F4A460', '#F1FAEE']
    
    barras = ax.bar(regiones, valores, color=colores, edgecolor='black', linewidth=1.5)
    
    # Agregar valores en las barras
    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
               f'{int(altura)}%', ha='center', va='bottom', fontweight='bold')
    
    ax.set_title('Desempeño por Región', fontsize=14, fontweight='bold')
    ax.set_ylabel('Porcentaje (%)', fontsize=11)
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Convertir a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

# ============================================================================
# RUTAS DE LA APLICACIÓN
# ============================================================================

@app.route('/')
def index():
    """Página principal"""
    sales_chart = generate_sales_chart()
    metrics_chart = generate_metrics_chart()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CI/CD Dashboard - Taller del Tecnológico</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                overflow: hidden;
            }}
            
            header {{
                background: linear-gradient(135deg, #2E86AB 0%, #457B9D 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 700;
            }}
            
            header p {{
                font-size: 1.1em;
                opacity: 0.95;
            }}
            
            .status-bar {{
                background: #d4edda;
                border-left: 5px solid #28a745;
                padding: 15px 20px;
                margin: 20px;
                border-radius: 5px;
                display: flex;
                align-items: center;
                gap: 15px;
            }}
            
            .status-dot {{
                width: 12px;
                height: 12px;
                background: #28a745;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
            
            .status-bar p {{
                color: #155724;
                font-weight: 600;
                margin: 0;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            .charts-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 30px;
                margin-bottom: 30px;
            }}
            
            .chart-container {{
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            
            .chart-container:hover {{
                transform: translateY(-5px);
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
            }}
            
            .chart-container h3 {{
                color: #333;
                margin-bottom: 15px;
                font-size: 1.2em;
            }}
            
            .chart-container img {{
                width: 100%;
                border-radius: 5px;
            }}
            
            .info-section {{
                background: #f0f7ff;
                border-left: 4px solid #2E86AB;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            
            .info-section h3 {{
                color: #2E86AB;
                margin-bottom: 10px;
            }}
            
            .info-section ul {{
                list-style-position: inside;
                color: #555;
                line-height: 1.8;
            }}
            
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #666;
                border-top: 1px solid #ddd;
            }}
            
            .badge {{
                display: inline-block;
                background: #2E86AB;
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.9em;
                margin-right: 10px;
                margin-bottom: 10px;
            }}
            
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }}
            
            .stat-card .value {{
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            
            .stat-card .label {{
                font-size: 0.95em;
                opacity: 0.9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- HEADER -->
            <header>
                <h1>🚀 CI/CD Dashboard</h1>
                <p>Taller de Integración Continua - Tecnológico de Monterrey</p>
            </header>
            
            <!-- STATUS -->
            <div class="status-bar">
                <div class="status-dot"></div>
                <p>✅ Sistema en línea y funcionando correctamente</p>
            </div>
            
            <!-- STATS -->
            <div class="content">
                <div class="stats">
                    <div class="stat-card">
                        <div class="value">100%</div>
                        <div class="label">Tests Exitosos</div>
                    </div>
                    <div class="stat-card">
                        <div class="value">0</div>
                        <div class="label">Errores Críticos</div>
                    </div>
                    <div class="stat-card">
                        <div class="value">4</div>
                        <div class="label">Despliegues (Mes)</div>
                    </div>
                    <div class="stat-card">
                        <div class="value">2.3s</div>
                        <div class="label">Build Time (avg)</div>
                    </div>
                </div>
                
                <!-- INFO SECTION -->
                <div class="info-section">
                    <h3>📋 Tecnologías Utilizadas</h3>
                    <div>
                        <span class="badge">GitHub Actions</span>
                        <span class="badge">Render (Cloud)</span>
                        <span class="badge">Python 3.10</span>
                        <span class="badge">Flask</span>
                        <span class="badge">Gunicorn</span>
                        <span class="badge">Matplotlib</span>
                    </div>
                </div>
                
                <!-- CHARTS -->
                <h2 style="margin-bottom: 20px; color: #333;">📊 Visualizaciones</h2>
                <div class="charts-grid">
                    <div class="chart-container">
                        <h3>📈 Ventas Mensuales</h3>
                        <img src="{sales_chart}" alt="Gráfico de Ventas">
                    </div>
                    <div class="chart-container">
                        <h3>🎯 Desempeño por Región</h3>
                        <img src="{metrics_chart}" alt="Gráfico de Métricas">
                    </div>
                </div>
                
                <!-- WORKFLOW INFO -->
                <div class="info-section">
                    <h3>🔄 Pipeline Automático</h3>
                    <p style="margin-bottom: 15px;">
                        Cada que haces <code>git push</code> a <strong>main</strong>:
                    </p>
                    <ul>
                        <li>✅ GitHub Actions ejecuta pruebas automáticamente</li>
                        <li>✅ Si las pruebas pasan, se dispara el deploy hook</li>
                        <li>✅ Render detecta el cambio y redespliega la app</li>
                        <li>✅ Tu código está en línea en ~2 minutos</li>
                    </ul>
                </div>
                
                <!-- NEXT STEPS -->
                <div class="info-section">
                    <h3>🎓 Próximos Pasos</h3>
                    <ul>
                        <li>Modificar <code>app.py</code> para agregar más gráficos</li>
                        <li>Escribir pruebas en <code>test_app.py</code></li>
                        <li>Ver los logs del workflow en GitHub Actions</li>
                        <li>Explorar las configuraciones en <code>.github/workflows/ci-cd.yml</code></li>
                        <li>Entender cómo Render auto-redeploy con git hooks</li>
                    </ul>
                </div>
            </div>
            
            <!-- FOOTER -->
            <footer>
                <p>
                    Hecho con ❤️ para el Tec de Monterrey | 
                    <a href="https://github.com" style="color: #2E86AB;">GitHub</a> • 
                    <a href="https://render.com" style="color: #2E86AB;">Render</a>
                </p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html)

@app.route('/api/health')
def health():
    """Health check endpoint para monitoreo"""
    return jsonify({
        'status': 'healthy',
        'message': 'App is running',
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development')
    }), 200

@app.route('/api/metrics')
def metrics():
    """Endpoint para métricas básicas"""
    return jsonify({
        'tests_passed': 15,
        'tests_total': 15,
        'deployment_count': 4,
        'error_rate': 0,
        'uptime_hours': 72
    }), 200

@app.route('/api/version')
def version():
    """Endpoint que retorna la versión"""
    return jsonify({
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'git_commit': os.getenv('GIT_COMMIT', 'unknown'),
        'deployed_at': os.getenv('DEPLOYED_AT', 'unknown')
    }), 200

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def page_not_found(e):
    """Página 404 personalizada"""
    return jsonify({'error': 'Página no encontrada', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(e):
    """Error 500 personalizado"""
    return jsonify({'error': 'Error interno del servidor', 'status': 500}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Obtener puerto de variable de entorno (Render la proporciona automáticamente)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Iniciando aplicación en puerto {port}...")
    print(f"📍 http://localhost:{port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
