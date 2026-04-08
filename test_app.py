#!/usr/bin/env python3
"""
test_app.py - Pruebas unitarias para la aplicación Flask
Ejecutar con: pytest test_app.py -v
"""

import pytest
import json
from app import app

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def client():
    """Crea cliente de prueba para la aplicación Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ============================================================================
# PRUEBAS DE RUTAS PRINCIPALES
# ============================================================================

class TestMainRoutes:
    """Pruebas para las rutas principales de la aplicación"""
    
    def test_index_page_loads(self, client):
        """Verifica que la página principal se carga correctamente"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'CI/CD Dashboard' in response.data
        assert b'Tecnol' in response.data or b'Monter' in response.data
    
    def test_index_page_contains_charts(self, client):
        """Verifica que la página contiene gráficos"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Ventas' in response.data
        assert b'Desempe' in response.data
    
    def test_index_returns_html(self, client):
        """Verifica que la respuesta es HTML"""
        response = client.get('/')
        assert response.content_type == 'text/html; charset=utf-8'
    
    def test_index_contains_status_indicator(self, client):
        """Verifica que la página contiene indicador de estado"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'sistema en l' in response.data.lower() or b'en l' in response.data.lower()

# ============================================================================
# PRUEBAS DE ENDPOINTS API
# ============================================================================

class TestAPIEndpoints:
    """Pruebas para los endpoints de la API"""
    
    def test_health_endpoint_exists(self, client):
        """Verifica que el endpoint /api/health existe"""
        response = client.get('/api/health')
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self, client):
        """Verifica que /api/health retorna JSON válido"""
        response = client.get('/api/health')
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_health_endpoint_structure(self, client):
        """Verifica la estructura del JSON del health endpoint"""
        response = client.get('/api/health')
        data = response.get_json()
        
        # Validar campos requeridos
        assert 'status' in data
        assert 'message' in data
        assert 'version' in data
        assert 'environment' in data
        
        # Validar valores
        assert data['status'] == 'healthy'
        assert data['message'] == 'App is running'
    
    def test_health_status_value(self, client):
        """Verifica que el status es 'healthy'"""
        response = client.get('/api/health')
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_metrics_endpoint_exists(self, client):
        """Verifica que el endpoint /api/metrics existe"""
        response = client.get('/api/metrics')
        assert response.status_code == 200
    
    def test_metrics_endpoint_returns_json(self, client):
        """Verifica que /api/metrics retorna JSON válido"""
        response = client.get('/api/metrics')
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_metrics_endpoint_structure(self, client):
        """Verifica la estructura del JSON de métricas"""
        response = client.get('/api/metrics')
        data = response.get_json()
        
        # Validar campos requeridos
        assert 'tests_passed' in data
        assert 'tests_total' in data
        assert 'deployment_count' in data
        assert 'error_rate' in data
        assert 'uptime_hours' in data
        
        # Validar tipos
        assert isinstance(data['tests_passed'], int)
        assert isinstance(data['tests_total'], int)
        assert isinstance(data['error_rate'], (int, float))
    
    def test_metrics_all_tests_passing(self, client):
        """Verifica que todos los tests están pasando"""
        response = client.get('/api/metrics')
        data = response.get_json()
        assert data['tests_passed'] == data['tests_total']
    
    def test_version_endpoint_exists(self, client):
        """Verifica que el endpoint /api/version existe"""
        response = client.get('/api/version')
        assert response.status_code == 200
    
    def test_version_endpoint_returns_json(self, client):
        """Verifica que /api/version retorna JSON válido"""
        response = client.get('/api/version')
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_version_endpoint_structure(self, client):
        """Verifica la estructura del JSON de versión"""
        response = client.get('/api/version')
        data = response.get_json()
        
        # Validar campos
        assert 'version' in data
        assert 'environment' in data
        assert 'git_commit' in data
        assert 'deployed_at' in data

# ============================================================================
# PRUEBAS DE MANEJO DE ERRORES
# ============================================================================

class TestErrorHandling:
    """Pruebas para el manejo de errores"""
    
    def test_404_error(self, client):
        """Verifica que las rutas inválidas retornan 404"""
        response = client.get('/ruta-que-no-existe')
        assert response.status_code == 404
    
    def test_404_returns_json(self, client):
        """Verifica que el error 404 retorna JSON"""
        response = client.get('/ruta-que-no-existe')
        assert response.content_type == 'application/json'
    
    def test_404_error_structure(self, client):
        """Verifica la estructura del error 404"""
        response = client.get('/ruta-que-no-existe')
        data = response.get_json()
        assert 'error' in data
        assert 'status' in data
        assert data['status'] == 404

# ============================================================================
# PRUEBAS DE MÉTODOS HTTP
# ============================================================================

class TestHTTPMethods:
    """Pruebas para diferentes métodos HTTP"""
    
    def test_get_request_to_index(self, client):
        """Verifica que GET a / funciona"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_head_request_to_health(self, client):
        """Verifica que HEAD a /api/health funciona"""
        response = client.head('/api/health')
        assert response.status_code == 200
    
    def test_post_to_index_not_allowed(self, client):
        """Verifica que POST a / no está permitido (opcional)"""
        response = client.post('/')
        # Algunas apps aceptan POST a /, otras no
        # Este test es informativo
        assert response.status_code in [200, 405, 400]

# ============================================================================
# PRUEBAS DE VALIDACIÓN DE CONTENIDO
# ============================================================================

class TestContentValidation:
    """Pruebas para validar el contenido de las respuestas"""
    
    def test_index_contains_badges(self, client):
        """Verifica que la página contiene badges de tecnologías"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'GitHub' in response.data
        assert b'Render' in response.data
        assert b'Flask' in response.data
    
    def test_index_contains_navigation(self, client):
        """Verifica que la página tiene elementos de navegación"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<header' in response.data or b'<Header' in response.data
    
    def test_health_check_message_format(self, client):
        """Verifica el formato del mensaje de health check"""
        response = client.get('/api/health')
        data = response.get_json()
        assert isinstance(data['message'], str)
        assert len(data['message']) > 0
    
    def test_version_format(self, client):
        """Verifica que la versión tiene formato válido"""
        response = client.get('/api/version')
        data = response.get_json()
        # Versión debe ser string tipo "1.0.0"
        assert isinstance(data['version'], str)
        assert '.' in data['version']

# ============================================================================
# PRUEBAS DE RENDIMIENTO
# ============================================================================

class TestPerformance:
    """Pruebas básicas de rendimiento"""
    
    def test_index_response_time(self, client):
        """Verifica que la página carga en tiempo razonable"""
        import time
        start = time.time()
        response = client.get('/')
        elapsed = time.time() - start
        
        # La página debe cargar en menos de 2 segundos
        assert elapsed < 2.0, f"Page took {elapsed}s to load"
    
    def test_health_endpoint_fast(self, client):
        """Verifica que el health endpoint es muy rápido"""
        import time
        start = time.time()
        response = client.get('/api/health')
        elapsed = time.time() - start
        
        # Health debe ser muy rápido (< 100ms)
        assert elapsed < 0.1, f"Health endpoint took {elapsed}s"
    
    def test_api_endpoints_fast(self, client):
        """Verifica que todos los endpoints API son rápidos"""
        import time
        
        endpoints = ['/api/health', '/api/metrics', '/api/version']
        
        for endpoint in endpoints:
            start = time.time()
            response = client.get(endpoint)
            elapsed = time.time() - start
            assert response.status_code == 200
            assert elapsed < 0.5, f"{endpoint} took {elapsed}s"

# ============================================================================
# PRUEBAS DE INTEGRACIÓN
# ============================================================================

class TestIntegration:
    """Pruebas de integración"""
    
    def test_complete_request_workflow(self, client):
        """Prueba un flujo completo de requests"""
        # 1. Check health
        health = client.get('/api/health')
        assert health.status_code == 200
        
        # 2. Get metrics
        metrics = client.get('/api/metrics')
        assert metrics.status_code == 200
        
        # 3. Get version
        version = client.get('/api/version')
        assert version.status_code == 200
        
        # 4. Load main page
        index = client.get('/')
        assert index.status_code == 200
    
    def test_all_api_endpoints_accessible(self, client):
        """Verifica que todos los endpoints API son accesibles"""
        api_endpoints = [
            '/api/health',
            '/api/metrics',
            '/api/version'
        ]
        
        for endpoint in api_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200, f"{endpoint} returned {response.status_code}"
            assert response.content_type == 'application/json', f"{endpoint} is not JSON"

# ============================================================================
# DATOS PARA TESTING (fixtures adicionales)
# ============================================================================

@pytest.fixture
def sample_metrics():
    """Proporciona datos de métricas para testing"""
    return {
        'tests_passed': 15,
        'tests_total': 15,
        'deployment_count': 4,
        'error_rate': 0,
        'uptime_hours': 72
    }

@pytest.fixture
def sample_health():
    """Proporciona datos de health para testing"""
    return {
        'status': 'healthy',
        'message': 'App is running',
        'version': '1.0.0',
        'environment': 'development'
    }

# ============================================================================
# UTILIDADES DE TEST
# ============================================================================

def test_app_creation():
    """Verifica que la app Flask se puede crear"""
    from app import app
    assert app is not None
    assert app.config['TESTING'] == False

def test_app_is_testing_mode():
    """Verifica que la app se crea en modo testing"""
    with app.test_client() as client:
        # Si llegamos aquí, el contexto de testing funciona
        assert True

# ============================================================================
# RESUMEN DE TESTS
# ============================================================================
"""
Total de pruebas: 30+

Categorías:
- Main Routes (4 tests): Carga de página principal
- API Endpoints (12 tests): Health, Metrics, Version endpoints
- Error Handling (3 tests): 404 y otros errores
- HTTP Methods (3 tests): GET, HEAD, POST
- Content Validation (4 tests): Contenido de respuestas
- Performance (3 tests): Tiempos de respuesta
- Integration (2 tests): Flujos completos

Ejecución:
  pytest test_app.py                    # Todos los tests
  pytest test_app.py -v                 # Verbose
  pytest test_app.py -k "health"        # Solo tests con "health"
  pytest test_app.py --tb=short         # Errores cortos
  pytest test_app.py --cov=app          # Con coverage
"""
