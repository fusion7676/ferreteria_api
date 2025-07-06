#!/usr/bin/env python3
"""
Script para generar todas las evidencias necesarias del proyecto
Plan de Pruebas - API Ferretería
"""

import subprocess
import sys
import os
import time
import json
from datetime import datetime

def crear_directorio_evidencias():
    """Crear directorio para almacenar todas las evidencias"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_evidencias = f"evidencias_proyecto_{timestamp}"
    
    if not os.path.exists(dir_evidencias):
        os.makedirs(dir_evidencias)
        os.makedirs(f"{dir_evidencias}/capturas")
        os.makedirs(f"{dir_evidencias}/reportes")
        os.makedirs(f"{dir_evidencias}/logs")
    
    return dir_evidencias

def ejecutar_y_capturar(comando, descripcion, dir_evidencias, archivo_salida):
    """Ejecutar comando y capturar salida para evidencias"""
    print(f"\n{'='*80}")
    print(f"🔧 {descripcion}")
    print(f"{'='*80}")
    print(f"📝 Ejecutando: {comando}")
    print(f"💾 Guardando en: {archivo_salida}")
    print("-" * 80)
    
    try:
        # Ejecutar comando y capturar salida
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        # Preparar contenido para guardar
        contenido = f"""
EVALUACIÓN 3 - PLAN DE PRUEBAS API FERRETERÍA
============================================
Descripción: {descripcion}
Comando: {comando}
Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Código de salida: {resultado.returncode}

SALIDA ESTÁNDAR:
{'-' * 50}
{resultado.stdout}

ERRORES/ADVERTENCIAS:
{'-' * 50}
{resultado.stderr}

ESTADO: {'✅ EXITOSO' if resultado.returncode == 0 else '❌ FALLÓ'}
"""
        
        # Guardar en archivo
        ruta_archivo = os.path.join(dir_evidencias, "logs", archivo_salida)
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Mostrar en consola
        if resultado.stdout:
            print("SALIDA:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("ERRORES/ADVERTENCIAS:")
            print(resultado.stderr)
        
        estado = "✅ EXITOSO" if resultado.returncode == 0 else "❌ FALLÓ"
        print(f"\n{estado} - {descripcion}")
        print(f"📁 Evidencia guardada en: {ruta_archivo}")
        
        return resultado.returncode == 0, ruta_archivo
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT - {descripcion} tardó más de 5 minutos")
        return False, None
    except Exception as e:
        print(f"❌ ERROR ejecutando {descripcion}: {e}")
        return False, None

def main():
    """Función principal para generar todas las evidencias"""
    print("🎯 GENERADOR DE EVIDENCIAS - EVALUACIÓN 3")
    print("📋 Plan de Pruebas API Ferretería")
    print("=" * 80)
    
    # Crear directorio de evidencias
    dir_evidencias = crear_directorio_evidencias()
    print(f"📁 Directorio de evidencias: {dir_evidencias}")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("❌ Error: No se encuentra app.py. Ejecute desde el directorio correcto")
        sys.exit(1)
    
    resultados = []
    
    # 1. Verificar Python y pip
    exito, archivo = ejecutar_y_capturar(
        "python --version",
        "VERIFICACIÓN DE PYTHON",
        dir_evidencias,
        "01_version_python.log"
    )
    resultados.append(("Verificación Python", exito, archivo))
    
    # 2. Verificar Flask
    exito, archivo = ejecutar_y_capturar(
        "python -c \"import flask; print('Flask version:', flask.__version__)\"",
        "VERIFICACIÓN DE FLASK",
        dir_evidencias,
        "02_verificacion_flask.log"
    )
    resultados.append(("Verificación Flask", exito, archivo))
    
    # 3. Verificar estructura del proyecto
    exito, archivo = ejecutar_y_capturar(
        "dir" if os.name == 'nt' else "ls -la",
        "ESTRUCTURA DEL PROYECTO",
        dir_evidencias,
        "03_estructura_proyecto.log"
    )
    resultados.append(("Estructura del Proyecto", exito, archivo))
    
    # 4. Probar importación de app.py
    exito, archivo = ejecutar_y_capturar(
        "python -c \"import app; print('✅ app.py se importa correctamente')\"",
        "VERIFICACIÓN DE APP.PY",
        dir_evidencias,
        "04_verificacion_app.log"
    )
    resultados.append(("Verificación app.py", exito, archivo))
    
    # 5. Contar líneas de código
    exito, archivo = ejecutar_y_capturar(
        "python -c \"with open('app.py', 'r', encoding='utf-8') as f: print(f'Líneas en app.py: {len(f.readlines())}')\"",
        "CONTEO DE LÍNEAS DE CÓDIGO",
        dir_evidencias,
        "05_conteo_lineas.log"
    )
    resultados.append(("Conteo de líneas", exito, archivo))
    
    # Generar reporte resumen
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    reporte = f"""
# REPORTE INICIAL - EVALUACIÓN 3
## Plan de Pruebas API Ferretería

**Fecha de verificación:** {timestamp}
**Directorio de evidencias:** {dir_evidencias}

## 📊 Resultados de Verificación

"""
    
    total_verificaciones = len(resultados)
    exitosas = sum(1 for _, exito, _ in resultados if exito)
    
    reporte += f"- **Total de verificaciones:** {total_verificaciones}\n"
    reporte += f"- **Verificaciones exitosas:** {exitosas}\n"
    reporte += f"- **Verificaciones fallidas:** {total_verificaciones - exitosas}\n"
    reporte += f"- **Porcentaje de éxito:** {(exitosas/total_verificaciones)*100:.1f}%\n\n"
    
    reporte += "## 📋 Detalle de Verificaciones\n\n"
    
    for descripcion, exito, archivo in resultados:
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        reporte += f"### {descripcion}\n"
        reporte += f"- **Estado:** {estado}\n"
        reporte += f"- **Archivo de evidencia:** `{archivo}`\n\n"
    
    reporte += """
## 📝 PRÓXIMOS PASOS

1. **Instalar dependencias faltantes:**
   ```bash
   pip install pytest pytest-cov requests flask-sqlalchemy
   ```

2. **Crear archivos de prueba:**
   - Los archivos de prueba se crearán automáticamente
   - Se configurará la estructura completa del proyecto

3. **Ejecutar pruebas completas:**
   ```bash
   python ejecutar_pruebas_completas.py
   ```

4. **Generar capturas de pantalla**
5. **Preparar video DEMO**

---
**Generado automáticamente por generar_evidencias.py**
"""
    
    # Guardar reporte
    ruta_reporte = os.path.join(dir_evidencias, "reporte_inicial.md")
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    # Mostrar resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN DE VERIFICACIÓN INICIAL")
    print("="*80)
    
    for descripcion, exito, archivo in resultados:
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        print(f"{descripcion:<35} {estado}")
    
    print("-" * 80)
    print(f"📁 Directorio de evidencias: {dir_evidencias}")
    print(f"📋 Reporte inicial: {ruta_reporte}")
    print(f"📊 Total: {total_verificaciones} | Exitosas: {exitosas} | Fallidas: {total_verificaciones - exitosas}")
    print(f"🎯 Porcentaje de éxito: {(exitosas/total_verificaciones)*100:.1f}%")
    
    if exitosas == total_verificaciones:
        print("\n🎉 ¡VERIFICACIÓN INICIAL EXITOSA!")
        print("✅ El entorno está listo para las pruebas")
    else:
        print(f"\n⚠️ {total_verificaciones - exitosas} verificación(es) con problemas")
    
    print("\n📝 SIGUIENTE PASO:")
    print("Ejecutar: python configurar_proyecto_completo.py")

if __name__ == "__main__":
    main()