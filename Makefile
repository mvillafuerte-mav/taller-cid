# ============================================================================
# Makefile - Gestión del Proyecto CI/CD Workshop
# ============================================================================
# Comandos disponibles: make help (para ver todos los comandos)
# ============================================================================

.PHONY: help install install-dev test run clean lint format charts all docs

# Colores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
REQUIREMENTS := requirements.txt
REQUIREMENTS_DEV := requirements-dev.txt

# ============================================================================
# AYUDA
# ============================================================================
help:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║         CI/CD Workshop - Gestor de Proyecto                     ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Comandos Principales:$(NC)"
	@echo "  $(YELLOW)make install$(NC)          Instalar dependencias de producción"
	@echo "  $(YELLOW)make install-dev$(NC)      Instalar dependencias + herramientas de desarrollo"
	@echo "  $(YELLOW)make test$(NC)             Ejecutar pruebas unitarias"
	@echo "  $(YELLOW)make run$(NC)              Ejecutar la aplicación Flask localmente"
	@echo "  $(YELLOW)make charts$(NC)           Generar todos los gráficos de ejemplo"
	@echo "  $(YELLOW)make lint$(NC)             Análisis estático de código (pylint)"
	@echo "  $(YELLOW)make format$(NC)           Formatear código (black + isort)"
	@echo "  $(YELLOW)make clean$(NC)            Limpiar archivos temporales y caché"
	@echo "  $(YELLOW)make all$(NC)              Instalar, probar, generar gráficos y limpiar"
	@echo "  $(YELLOW)make docs$(NC)             Generar documentación del proyecto"
	@echo ""
	@echo "$(GREEN)Ambiente Virtual:$(NC)"
	@echo "  $(YELLOW)make venv$(NC)             Crear ambiente virtual de Python"
	@echo "  $(YELLOW)make venv-clean$(NC)       Eliminar ambiente virtual"
	@echo ""
	@echo "$(GREEN)Comandos de Desarrollo:$(NC)"
	@echo "  $(YELLOW)make security$(NC)         Verificar vulnerabilidades de dependencias"
	@echo "  $(YELLOW)make coverage$(NC)         Generar reporte de cobertura de pruebas"
	@echo ""

# ============================================================================
# INSTALACIÓN
# ============================================================================

## Crear ambiente virtual
venv:
	@echo "$(GREEN)→ Creando ambiente virtual...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✓ Ambiente virtual creado$(NC)"
	@echo "$(YELLOW)  Activarlo con: source $(VENV)/bin/activate$(NC) (Linux/Mac)"
	@echo "$(YELLOW)  Activarlo con: .\\$(VENV)\\Scripts\\activate$(NC) (Windows)"

## Limpiar ambiente virtual
venv-clean:
	@echo "$(GREEN)→ Eliminando ambiente virtual...$(NC)"
	rm -rf $(VENV)
	@echo "$(GREEN)✓ Ambiente virtual eliminado$(NC)"

## Instalar dependencias de producción
install: check-python
	@echo "$(GREEN)→ Instalando dependencias de producción...$(NC)"
	$(PIP) install --upgrade pip
	@if [ -f "$(REQUIREMENTS)" ]; then \
		$(PIP) install -r $(REQUIREMENTS); \
		echo "$(GREEN)✓ Dependencias instaladas desde $(REQUIREMENTS)$(NC)"; \
	else \
		echo "$(RED)✗ Archivo $(REQUIREMENTS) no encontrado$(NC)"; \
		exit 1; \
	fi

## Instalar dependencias + herramientas de desarrollo
install-dev: install
	@echo "$(GREEN)→ Instalando herramientas de desarrollo...$(NC)"
	@if [ -f "$(REQUIREMENTS_DEV)" ]; then \
		$(PIP) install -r $(REQUIREMENTS_DEV); \
	else \
		$(PIP) install pytest pytest-cov pylint black isort bandit; \
	fi
	@echo "$(GREEN)✓ Herramientas de desarrollo instaladas$(NC)"

# ============================================================================
# TESTING & CALIDAD DE CÓDIGO
# ============================================================================

## Ejecutar pruebas unitarias
test: check-python
	@echo "$(GREEN)→ Ejecutando pruebas unitarias...$(NC)"
	$(PYTHON) -m pytest test_app.py -v --tb=short --color=yes
	@echo "$(GREEN)✓ Pruebas completadas$(NC)"

## Análisis de cobertura de pruebas
coverage: check-python install-dev
	@echo "$(GREEN)→ Generando reporte de cobertura...$(NC)"
	$(PYTHON) -m pytest test_app.py --cov=. --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Reporte de cobertura generado en htmlcov/index.html$(NC)"

## Análisis estático de código (pylint)
lint: check-python install-dev
	@echo "$(GREEN)→ Ejecutando análisis estático (pylint)...$(NC)"
	$(PYTHON) -m pylint app.py --fail-under=7.0 || echo "$(YELLOW)⚠ Advertencias de linting encontradas$(NC)"
	@echo "$(GREEN)✓ Análisis completado$(NC)"

## Verificar vulnerabilidades en dependencias
security: check-python install-dev
	@echo "$(GREEN)→ Escaneando vulnerabilidades de seguridad...$(NC)"
	$(PYTHON) -m bandit -r . -ll || echo "$(YELLOW)⚠ Verificar problemas de seguridad$(NC)"
	@echo "$(GREEN)✓ Escaneo completado$(NC)"

## Formatear código (black + isort)
format: check-python install-dev
	@echo "$(GREEN)→ Formateando código con black...$(NC)"
	$(PYTHON) -m black app.py test_app.py charts_demo.py --line-length=100
	@echo "$(GREEN)→ Organizando imports con isort...$(NC)"
	$(PYTHON) -m isort app.py test_app.py charts_demo.py
	@echo "$(GREEN)✓ Código formateado$(NC)"

# ============================================================================
# EJECUCIÓN
# ============================================================================

## Ejecutar aplicación Flask
run: check-python install
	@echo "$(GREEN)→ Iniciando aplicación Flask...$(NC)"
	@echo "$(YELLOW)  Accede a: http://localhost:5000$(NC)"
	$(PYTHON) app.py

## Generar gráficos de ejemplo
charts: check-python install
	@echo "$(GREEN)→ Generando gráficos de ejemplo...$(NC)"
	$(PYTHON) charts_demo.py
	@echo "$(GREEN)✓ Gráficos guardados en ./charts/$(NC)"

# ============================================================================
# LIMPIEZA
# ============================================================================

## Limpiar archivos temporales y caché
clean:
	@echo "$(GREEN)→ Limpiando archivos temporales...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pylint* -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type f -name '.coverage' -delete 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info 2>/dev/null || true
	@echo "$(GREEN)✓ Archivos temporales eliminados$(NC)"

## Limpiar todo (ambiente virtual incluido)
clean-all: clean venv-clean
	@echo "$(GREEN)✓ Limpieza total completada$(NC)"

# ============================================================================
# UTILIDADES
# ============================================================================

## Ejecutar todos los pasos: instalar, probar, generar gráficos
all: clean install test lint charts
	@echo "$(GREEN)╔════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║  ✓ Todos los pasos completados exitosamente  ║$(NC)"
	@echo "$(GREEN)╚════════════════════════════════════════════════╝$(NC)"

## Generar documentación
docs:
	@echo "$(GREEN)→ Generando documentación...$(NC)"
	@echo "$(BLUE)Documentación disponible en:$(NC)"
	@echo "  • CI_CD_TALLER_GITHUB_ACTIONS.md - Guía completa del taller"
	@echo "  • charts_demo.py - Script con ejemplos de gráficos"
	@echo "$(GREEN)✓ Documentación lista para revisar$(NC)"

## Verificar instalación de Python
check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { \
		echo "$(RED)✗ Python 3 no está instalado$(NC)"; \
		exit 1; \
	}

## Mostrar información del proyecto
info:
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)CI/CD Workshop - Información del Proyecto$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Versión de Python:$(NC)"
	@$(PYTHON) --version
	@echo ""
	@echo "$(GREEN)Paquetes instalados:$(NC)"
	@$(PIP) list 2>/dev/null | head -10 || echo "  (ejecuta: make install)"
	@echo ""
	@echo "$(GREEN)Archivos del proyecto:$(NC)"
	@ls -la | grep -E '\.(py|txt|md|yml|yaml|makefile)' || echo "  (archivos no encontrados)"

# ============================================================================
# PHONY TARGETS (no son archivos reales)
# ============================================================================
.PHONY: help install install-dev test coverage lint security format run charts clean clean-all all docs check-python info venv venv-clean
