#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de evidencias para Evaluación 3 - CON EMOJIS BONITOS
"""

import subprocess
import sys
import os
import json
from datetime import datetime

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def crear_directorio_evidencias():
    """Crear directorio para evidencias con timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    directorio = f"evidencias_evaluacion3_{timestamp}"
    
    # Crear estructura de directorios
    os.makedirs(directorio, exist_ok=True)
    os.makedirs(f"{directorio}/logs", exist_ok=True)
    os.makedirs(f"{directorio}/reportes", exist_ok=True)
    os.makedirs(f"{directorio}/capturas", exist_ok=True)
    
    return directorio

def ejecutar_comando_evidencia(comando, nombre_archivo, descripcion):
    """Ejecutar comando y guardar evidencia"""
    print(f"\n{'='*80}")
    print(f"🔧 {descripcion.upper()}")
    print(f"{'='*80}")
    print(f"📝 Ejecutando: {comando}")
    print(f"💾 Guardando en: {nombre_archivo}")
    print("-" * 80)
    
    try:
        if isinstance(comando, list):
            resultado = subprocess.run(comando, capture_output=True, text=True, encoding='utf-8')
        else:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        # Mostrar salida en consola
        if resultado.stdout:
            print("SALIDA:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("ERRORES/ADVERTENCIAS:")
            print(resultado.stderr)
        
        # Guardar en archivo
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(f"=== {descripcion} ===\n")
            f.write(f"Comando: {comando}\n")
            f.write(f"Fecha: {datetime.now().isoformat()}\n")
            f.write(f"Código de salida: {resultado.returncode}\n\n")
            
            if resultado.stdout:
                f.write("=== SALIDA ===\n")
                f.write(resultado.stdout)
                f.write("\n\n")
            
            if resultado.stderr:
                f.write("=== ERRORES/ADVERTENCIAS ===\n")
                f.write(resultado.stderr)
                f.write("\n\n")
        
        exito = resultado.returncode == 0
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        print(f"\n{estado} - {descripcion}")
        print(f"📁 Evidencia guardada en: {nombre_archivo}")
        
        return exito
        
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def generar_reporte_markdown(directorio, resultados):
    """Generar reporte en formato Markdown"""
    archivo_reporte = f"{directorio}/reporte_inicial.md"
    
    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        f.write("# 📋 Reporte de Evidencias - Evaluación 3\n\n")
        f.write("## 🎯 API Ferretería - Plan de Pruebas\n\n")
        f.write(f"**📅 Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**📁 Directorio:** `{directorio}`\n\n")
        
        f.write("## 📊 Resumen de Verificaciones\n\n")
        f.write("| Verificación | Estado | Archivo |\n")
        f.write("|--------------|--------|----------|\n")
        
        for nombre, exito, archivo in resultados:
            estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
            f.write(f"| {nombre} | {estado} | `{archivo}` |\n")
        
        exitosos = sum(1 for _, exito, _ in resultados if exito)
        total = len(resultados)
        porcentaje = (exitosos / total * 100) if total > 0 else 0
        
        f.write(f"\n## 📈 Estadísticas\n\n")
        f.write(f"- **Total:** {total}\n")
        f.write(f"- **Exitosas:** {exitosos}\n")
        f.write(f"- **Fallidas:** {total - exitosos}\n")
        f.write(f"- **Porcentaje de éxito:** {porcentaje:.1f}%\n\n")
        
        if porcentaje >= 80:
            f.write("## 🎉 ¡EXCELENTE!\n\n")
            f.write("Tu proyecto está listo para la evaluación.\n\n")
        else:
            f.write("## ⚠️ Revisar\n\n")
            f.write("Algunas verificaciones necesitan atención.\n\n")
        
        f.write("## 📝 Próximos Pasos\n\n")
        f.write("1. 🧪 Ejecutar todas las pruebas\n")
        f.write("2. 📊 Revisar reportes de cobertura\n")
        f.write("3. 📸 Tomar capturas de pantalla\n")
        f.write("4. 📋 Documentar resultados\n\n")
    
    return archivo_reporte

def main():
    print("🎯 GENERADOR DE EVIDENCIAS - EVALUACIÓN 3")
    print("📋 Plan de Pruebas API Ferretería")
    print("=" * 80)
    
    # Crear directorio de evidencias
    directorio = crear_directorio_evidencias()
    print(f"📁 Directorio de evidencias: {directorio}")
    
    # Lista de verificaciones a realizar
    verificaciones = [
        {
            'comando': 'python --version',
            'archivo': f'{directorio}/logs/01_version_python.log',
            'descripcion': 'Verificación de Python',
            'nombre': 'Verificación Python'
        },
        {
            'comando': 'python -c "import flask; print(f\'Flask version: {flask.__version__}\')"',
            'archivo': f'{directorio}/logs/02_verificacion_flask.log',
            'descripcion': 'Verificación de Flask',
            'nombre': 'Verificación Flask'
        },
        {
            'comando': 'dir' if sys.platform.startswith('win') else 'ls -la',
            'archivo': f'{directorio}/logs/03_estructura_proyecto.log',
            'descripcion': 'Estructura del Proyecto',
            'nombre': 'Estructura del Proyecto'
        },
        {
            'comando': 'python -c "import app; print(\'app.py se importa correctamente\')"',
            'archivo': f'{directorio}/logs/04_verificacion_app.log',
            'descripcion': 'Verificación de app.py',
            'nombre': 'Verificación app.py'
        },
        {
            'comando': 'python -c "with open(\'app.py\', \'r\', encoding=\'utf-8\') as f: print(f\'Líneas en app.py: {len(f.readlines())}\')"',
            'archivo': f'{directorio}/logs/05_conteo_lineas.log',
            'descripcion': 'Conteo de líneas de código',
            'nombre': 'Conteo de líneas'
        }
    ]
    
    resultados = []
    
    # Ejecutar cada verificación
    for verificacion in verificaciones:
        exito = ejecutar_comando_evidencia(
            verificacion['comando'],
            verificacion['archivo'],
            verificacion['descripcion']
        )
        resultados.append((verificacion['nombre'], exito, verificacion['archivo']))
    
    # Generar reporte
    print(f"\n{'='*80}")
    print("📊 RESUMEN DE VERIFICACIÓN INICIAL")
    print(f"{'='*80}")
    
    for nombre, exito, archivo in resultados:
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        print(f"{nombre:<35} {estado}")
    
    print("-" * 80)
    print(f"📁 Directorio de evidencias: {directorio}")
    
    # Generar reporte markdown
    archivo_reporte = generar_reporte_markdown(directorio, resultados)
    print(f"📋 Reporte inicial: {archivo_reporte}")
    
    # Estadísticas finales
    exitosos = sum(1 for _, exito, _ in resultados if exito)
    total = len(resultados)
    porcentaje = (exitosos / total * 100) if total > 0 else 0
    
    print(f"📊 Total: {total} | Exitosas: {exitosos} | Fallidas: {total - exitosos}")
    print(f"🎯 Porcentaje de éxito: {porcentaje:.1f}%")
    
    if total - exitosos > 0:
        print(f"\n⚠️ {total - exitosos} verificación(es) con problemas")
    
    print(f"\n📝 SIGUIENTE PASO:")
    print("Ejecutar: python configurar_proyecto_completo.py")
    
    return porcentaje >= 80

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)