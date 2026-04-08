#!/usr/bin/env python3
"""
Script de demostración: Múltiples tipos de gráficos con Matplotlib
Uso: python charts_demo.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Configurar backend para no necesitar GUI
import matplotlib
matplotlib.use('Agg')

class ChartsDemo:
    """Clase para generar y guardar múltiples tipos de gráficos"""
    
    def __init__(self, output_dir='./charts'):
        self.output_dir = output_dir
        self.import_datetime = datetime.now()
        
    def create_all_charts(self):
        """Genera todos los tipos de gráficos"""
        print("📊 Generando gráficos...")
        
        self.line_chart()
        self.bar_chart()
        self.pie_chart()
        self.scatter_plot()
        self.histogram()
        self.box_plot()
        self.heatmap()
        self.area_chart()
        self.combined_chart()
        
        print(f"✅ Todos los gráficos han sido guardados en '{self.output_dir}/'")
    
    def line_chart(self):
        """Gráfico de líneas: Evolución de temperaturas"""
        print("  • Generando gráfico de líneas...")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Datos
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        temp_monterrey = [18, 20, 24, 27, 30, 32, 33, 32, 31, 27, 22, 19]
        temp_ciudad_mexico = [15, 16, 19, 21, 23, 23, 22, 22, 21, 19, 17, 15]
        
        ax.plot(meses, temp_monterrey, marker='o', linewidth=2.5, 
                markersize=8, label='Monterrey', color='#E63946', alpha=0.8)
        ax.plot(meses, temp_ciudad_mexico, marker='s', linewidth=2.5, 
                markersize=8, label='CDMX', color='#457B9D', alpha=0.8)
        
        ax.set_title('Temperatura Promedio Mensual (°C)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Temperatura (°C)', fontsize=11)
        ax.set_xlabel('Mes', fontsize=11)
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(10, 35)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/1_linea.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def bar_chart(self):
        """Gráfico de barras: Ventas por región"""
        print("  • Generando gráfico de barras...")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Datos
        regiones = ['Norte', 'Centro', 'Occidente', 'Sur', 'Bajío']
        ventas_2022 = [150, 200, 120, 180, 160]
        ventas_2023 = [180, 250, 145, 210, 195]
        
        x = np.arange(len(regiones))
        ancho = 0.35
        
        barras1 = ax.bar(x - ancho/2, ventas_2022, ancho, label='2022', color='#A8DADC', edgecolor='black', linewidth=1.2)
        barras2 = ax.bar(x + ancho/2, ventas_2023, ancho, label='2023', color='#457B9D', edgecolor='black', linewidth=1.2)
        
        # Agregar valores en las barras
        for barras in [barras1, barras2]:
            for barra in barras:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2., altura,
                       f'{int(altura)}k', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_ylabel('Ventas (miles de pesos)', fontsize=11, fontweight='bold')
        ax.set_title('Ventas por Región (Comparativo 2022-2023)', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(regiones)
        ax.legend()
        ax.set_ylim(0, 280)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/2_barras.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def pie_chart(self):
        """Gráfico de pastel: Distribución de mercado"""
        print("  • Generando gráfico de pastel...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Datos
        empresas = ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Otros']
        cuotas = [35, 25, 20, 12, 8]
        colores = ['#E63946', '#457B9D', '#A8DADC', '#F1FAEE', '#F4A460']
        
        # Pastel simple
        ax1.pie(cuotas, labels=empresas, autopct='%1.1f%%', startangle=90,
               colors=colores, textprops={'fontsize': 10, 'weight': 'bold'})
        ax1.set_title('Cuota de Mercado', fontsize=12, fontweight='bold')
        
        # Pastel con estilo donut
        wedges, texts, autotexts = ax2.pie(cuotas, labels=empresas, autopct='%1.1f%%',
                                            startangle=90, colors=colores,
                                            textprops={'fontsize': 10, 'weight': 'bold'})
        # Crear agujero en el centro (donut)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax2.add_artist(centre_circle)
        ax2.set_title('Cuota de Mercado (Donut)', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/3_pastel.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def scatter_plot(self):
        """Scatter plot: Relación entre variables"""
        print("  • Generando scatter plot...")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Datos: Inversión en Marketing vs. Ventas
        np.random.seed(42)
        inversion = np.random.uniform(10, 100, 50)
        ventas = inversion * 5 + np.random.normal(0, 30, 50)
        empresas_tamaño = np.random.uniform(20, 200, 50)
        
        scatter = ax.scatter(inversion, ventas, s=empresas_tamaño, alpha=0.6,
                           c=inversion, cmap='viridis', edgecolors='black', linewidth=0.5)
        
        # Agregar línea de tendencia
        z = np.polyfit(inversion, ventas, 1)
        p = np.poly1d(z)
        ax.plot(inversion, p(inversion), "r--", linewidth=2, alpha=0.8, label='Tendencia')
        
        ax.set_xlabel('Inversión en Marketing (miles $)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Ventas Generadas (miles $)', fontsize=11, fontweight='bold')
        ax.set_title('Correlación: Inversión en Marketing vs. Ventas', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Inversión (miles $)', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/4_scatter.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def histogram(self):
        """Histograma: Distribución de edades"""
        print("  • Generando histograma...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Datos: Distribución de edades de clientes
        np.random.seed(42)
        edades = np.concatenate([
            np.random.normal(35, 8, 200),
            np.random.normal(55, 10, 150)
        ])
        edades = edades[(edades >= 18) & (edades <= 80)]
        
        # Histograma simple
        ax1.hist(edades, bins=20, color='#457B9D', edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Edad (años)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
        ax1.set_title('Distribución de Edades (Clientes)', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Histograma con múltiples variables
        edades_hombres = np.random.normal(40, 10, 150)
        edades_mujeres = np.random.normal(38, 9, 180)
        
        ax2.hist([edades_hombres, edades_mujeres], bins=15, label=['Hombres', 'Mujeres'],
                color=['#457B9D', '#E63946'], alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Edad (años)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
        ax2.set_title('Distribución de Edades (Por Género)', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/5_histograma.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def box_plot(self):
        """Box plot: Distribución de datos por categoría"""
        print("  • Generando box plot...")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Datos: Salarios por departamento
        np.random.seed(42)
        salarios_ventas = np.random.normal(45000, 8000, 50)
        salarios_ingenieria = np.random.normal(65000, 10000, 50)
        salarios_rrhh = np.random.normal(40000, 6000, 50)
        salarios_admin = np.random.normal(35000, 5000, 50)
        
        datos = [salarios_ventas, salarios_ingenieria, salarios_rrhh, salarios_admin]
        etiquetas = ['Ventas', 'Ingeniería', 'RRHH', 'Administración']
        
        bp = ax.boxplot(datos, labels=etiquetas, patch_artist=True,
                       notch=False, showmeans=True)
        
        # Colorear las cajas
        colores = ['#E63946', '#457B9D', '#A8DADC', '#F4A460']
        for patch, color in zip(bp['boxes'], colores):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel('Salario Anual (pesos)', fontsize=11, fontweight='bold')
        ax.set_title('Distribución Salarial por Departamento', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/6_boxplot.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def heatmap(self):
        """Heatmap: Matriz de correlación"""
        print("  • Generando heatmap...")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Crear matriz de correlación simulada
        variables = ['Edad', 'Ingresos', 'Gasto', 'Antiguedad', 'Educación']
        matriz_corr = np.array([
            [1.00, 0.65, 0.72, 0.58, 0.45],
            [0.65, 1.00, 0.88, 0.62, 0.70],
            [0.72, 0.88, 1.00, 0.55, 0.65],
            [0.58, 0.62, 0.55, 1.00, 0.48],
            [0.45, 0.70, 0.65, 0.48, 1.00]
        ])
        
        # Crear heatmap
        im = ax.imshow(matriz_corr, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)
        
        # Etiquetas
        ax.set_xticks(np.arange(len(variables)))
        ax.set_yticks(np.arange(len(variables)))
        ax.set_xticklabels(variables, rotation=45, ha='right')
        ax.set_yticklabels(variables)
        
        # Agregar valores en las celdas
        for i in range(len(variables)):
            for j in range(len(variables)):
                text = ax.text(j, i, f'{matriz_corr[i, j]:.2f}',
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_title('Matriz de Correlación de Variables', fontsize=14, fontweight='bold')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Correlación', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/7_heatmap.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def area_chart(self):
        """Gráfico de área: Evolución acumulada"""
        print("  • Generando gráfico de área...")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Datos: Crecimiento de usuarios por región
        meses = np.arange(1, 13)
        usuarios_norte = 100 + meses * 15
        usuarios_centro = 80 + meses * 12
        usuarios_sur = 60 + meses * 10
        
        ax.fill_between(meses, 0, usuarios_norte, alpha=0.5, label='Norte', color='#E63946')
        ax.fill_between(meses, usuarios_norte, usuarios_norte + usuarios_centro, 
                       alpha=0.5, label='Centro', color='#457B9D')
        ax.fill_between(meses, usuarios_norte + usuarios_centro, 
                       usuarios_norte + usuarios_centro + usuarios_sur,
                       alpha=0.5, label='Sur', color='#A8DADC')
        
        ax.plot(meses, usuarios_norte, color='#E63946', linewidth=2, marker='o')
        ax.plot(meses, usuarios_norte + usuarios_centro, color='#457B9D', linewidth=2, marker='s')
        ax.plot(meses, usuarios_norte + usuarios_centro + usuarios_sur, 
               color='#A8DADC', linewidth=2, marker='^')
        
        ax.set_xlabel('Mes', fontsize=11, fontweight='bold')
        ax.set_ylabel('Número de Usuarios', fontsize=11, fontweight='bold')
        ax.set_title('Crecimiento Acumulado de Usuarios por Región', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(meses)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/8_area.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def combined_chart(self):
        """Gráfico combinado: Barras + Línea"""
        print("  • Generando gráfico combinado...")
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Datos
        trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
        ingresos = [100, 150, 140, 180]
        gastos = [60, 80, 75, 95]
        margen_ganancia = [40, 70, 65, 85]
        
        # Eje izquierdo: Barras (Ingresos y Gastos)
        x = np.arange(len(trimestres))
        ancho = 0.35
        
        barras1 = ax1.bar(x - ancho/2, ingresos, ancho, label='Ingresos', color='#457B9D', alpha=0.8)
        barras2 = ax1.bar(x + ancho/2, gastos, ancho, label='Gastos', color='#E63946', alpha=0.8)
        
        ax1.set_xlabel('Trimestre', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Cantidad (miles $)', fontsize=11, fontweight='bold', color='black')
        ax1.set_title('Análisis Financiero Trimestral', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(trimestres)
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.legend(loc='upper left')
        
        # Eje derecho: Línea (Margen de Ganancia)
        ax2 = ax1.twinx()
        linea = ax2.plot(x, margen_ganancia, 'o-', linewidth=2.5, markersize=8,
                        color='#F4A460', label='Margen Ganancia')
        ax2.set_ylabel('Margen de Ganancia (%)', fontsize=11, fontweight='bold', color='#F4A460')
        ax2.tick_params(axis='y', labelcolor='#F4A460')
        
        # Leyenda combinada
        linhas1, etiquetas1 = ax1.get_legend_handles_labels()
        linhas2, etiquetas2 = ax2.get_legend_handles_labels()
        ax1.legend(linhas1 + linhas2, etiquetas1 + etiquetas2, loc='upper left')
        
        ax1.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/9_combinado.png', dpi=150, bbox_inches='tight')
        plt.close()

def main():
    """Función principal"""
    import os
    
    # Crear directorio de salida
    output_dir = './charts'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generar todos los gráficos
    demo = ChartsDemo(output_dir=output_dir)
    demo.create_all_charts()
    
    print("\n" + "="*60)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("="*60)
    print(f"\nArchivos generados en: {output_dir}/")
    print("\nGráficos creados:")
    print("  1. Gráfico de líneas (comparación de series)")
    print("  2. Gráfico de barras (comparativo año a año)")
    print("  3. Gráfico de pastel (simple y donut)")
    print("  4. Scatter plot (relación entre variables)")
    print("  5. Histograma (distribución de datos)")
    print("  6. Box plot (distribución por categoría)")
    print("  7. Heatmap (matriz de correlación)")
    print("  8. Gráfico de área (evolución acumulada)")
    print("  9. Gráfico combinado (barras + línea)")
    print("\n" + "="*60)

if __name__ == '__main__':
    main()
