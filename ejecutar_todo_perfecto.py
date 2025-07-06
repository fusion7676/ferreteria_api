#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 EJECUTOR PERFECTO - EVALUACIÓN 3 CON EMOJIS BONITOS
"""

import subprocess
import sys
import os
import time
import threading
import signal
from datetime import datetime

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Variable global para el proceso de la API
api_process = None

def iniciar_api():
    """Iniciar la API en un hilo separado"""
    global api_process
    try:
        print("🚀 Iniciando API Flask...")
        api_process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ API iniciada en proceso: {api_process.pid}")
        return True
    except Exception as e:
        print(f"❌ Error iniciando API: {e}")
        return False

def detener_api():
    """Detener la API"""
    global api_process
    if api_process:
        try:
            print("🛑 Deteniendo API...")
            api_process.terminate()
            api_process.wait(timeout=5)
            print("✅ API detenida correctamente")
        except:
            try:
                api_process.kill()
                print("✅ API forzada a detenerse")
            except:
                print("⚠️ No se pudo detener la API completamente")

def verificar_api_disponible(max_intentos=10):
    """Verificar que la API esté disponible"""
    try:
        import requests
        for intento in range(max_intentos):
            try:
                response = requests.get('http://localhost:5000/health', timeout=2)
                if response.status_code == 200:
                    print(f"✅ API disponible después de {intento + 1} intentos")
                    return True
            except:
                pass
            
            print(f"⏳ Esperando API... intento {intento + 1}/{max_intentos}")
            time.sleep(2)
        
        return False
    except ImportError:
        print("⚠️ Requests no disponible, asumiendo API funcionando")
        time.sleep(5)
        return True

def ejecutar_fase(nombre, comando, descripcion=""):
    """Ejecutar una fase del proceso"""
    print(f"\n{'='*70}")
    print(f"🔧 FASE: {nombre}")
    print(f"{'='*70}")
    if descripcion:
        print(f"📋 Descripción: {descripcion}")
    print(f"📍 Comando: {comando}")
    print("-" * 50)
    
    try:
        if isinstance(comando, list):
            resultado = subprocess.run(comando, capture_output=True, text=True, encoding='utf-8')
        else:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if resultado.stdout:
            print("📤 SALIDA:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("⚠️ ERRORES/ADVERTENCIAS:")
            print(resultado.stderr)
        
        exito = resultado.returncode == 0
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        print(f"{estado} - {nombre}")
        
        return exito
        
    except Exception as e:
        print(f"❌ Error ejecutando {nombre}: {e}")
        return False

def main():
    print("🎯 EJECUTOR PERFECTO - EVALUACIÓN 3")
    print("📋 API Ferretería - Todas las Pruebas")
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    resultados = []
    
    try:
        # 🧪 FASE 1: Pruebas unitarias
        exito = ejecutar_fase(
            "PRUEBAS UNITARIAS",
            [sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=short"],
            "Ejecutar todas las pruebas unitarias"
        )
        resultados.append(("Pruebas Unitarias", exito))
        
        # 🔗 FASE 2: Pruebas de integración
        exito = ejecutar_fase(
            "PRUEBAS DE INTEGRACIÓN",
            [sys.executable, "-m", "pytest", "tests/integration/", "-v", "--tb=short"],
            "Ejecutar pruebas de integración"
        )
        resultados.append(("Pruebas Integración", exito))
        
        # 📊 FASE 3: Cobertura
        exito = ejecutar_fase(
            "COBERTURA DE CÓDIGO",
            [sys.executable, "-m", "pytest", "--cov=app", "--cov-report=html", "--cov-report=xml"],
            "Generar reporte de cobertura"
        )
        resultados.append(("Cobertura", exito))
        
        # 🎯 FASE 4: Katalon con API
        print(f"\n{'='*70}")
        print("🎯 FASE: KATALON CON API AUTOMÁTICA")
        print(f"{'='*70}")
        
        # Iniciar API
        if not iniciar_api():
            print("❌ No se pudo iniciar la API")
            resultados.append(("Katalon", False))
        else:
            # Esperar API
            print("\n⏳ Esperando que la API esté lista...")
            if not verificar_api_disponible():
                print("❌ La API no respondió a tiempo")
                resultados.append(("Katalon", False))
            else:
                # Ejecutar Katalon corregido
                print("\n🎯 API lista, ejecutando pruebas Katalon...")
                exito = ejecutar_fase(
                    "KATALON STUDIO",
                    [sys.executable, "ejecutar_katalon_fixed.py"],
                    "Ejecutar pruebas Katalon con API"
                )
                resultados.append(("Katalon", exito))
        
        # 📸 FASE 5: Evidencias
        exito = ejecutar_fase(
            "GENERACIÓN DE EVIDENCIAS",
            [sys.executable, "generar_evidencias_fixed.py"],
            "Generar documentación de evidencias"
        )
        resultados.append(("Evidencias", exito))
        
    except KeyboardInterrupt:
        print("\n⚠️ Ejecución interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        # Siempre detener la API
        detener_api()
    
    # 📋 RESUMEN FINAL
    print(f"\n{'='*80}")
    print("📋 RESUMEN FINAL DE EJECUCIÓN")
    print(f"{'='*80}")
    
    for nombre, exito in resultados:
        estado = "✅ PASSED" if exito else "❌ FAILED"
        print(f"   {estado} - {nombre}")
    
    exitosos = sum(1 for _, exito in resultados if exito)
    total = len(resultados)
    porcentaje = (exitosos / total * 100) if total > 0 else 0
    
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   Total de fases: {total}")
    print(f"   Exitosas: {exitosos}")
    print(f"   Fallidas: {total - exitosos}")
    print(f"   Porcentaje de éxito: {porcentaje:.1f}%")
    
    print(f"\n📁 ARCHIVOS GENERADOS:")
    archivos = [
        ("htmlcov/index.html", "Reporte cobertura HTML"),
        ("coverage.xml", "Reporte cobertura XML"),
        ("katalon_test_results.json", "Resultados Katalon")
    ]
    
    for archivo, descripcion in archivos:
        if os.path.exists(archivo):
            print(f"   ✅ GENERADO - {archivo} ({descripcion})")
        else:
            print(f"   ❌ FALTANTE - {archivo} ({descripcion})")
    
    if porcentaje >= 80:
        print(f"\n🎉 ¡EXCELENTE! Tu proyecto está listo para la evaluación")
        print(f"🎯 Tienes un {porcentaje:.1f}% de éxito en las pruebas")
    else:
        print(f"\n⚠️ Revisa los errores para mejorar el porcentaje")
    
    print(f"\n🏁 EJECUCIÓN COMPLETADA")
    return porcentaje >= 80

if __name__ == "__main__":
    # Manejar Ctrl+C correctamente
    def signal_handler(sig, frame):
        print("\n🛑 Deteniendo ejecución...")
        detener_api()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)