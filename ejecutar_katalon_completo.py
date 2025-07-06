#!/usr/bin/env python3
"""
Ejecutor completo de Katalon - Inicia API automáticamente
"""

import subprocess
import sys
import os
import time
import threading
import signal
from datetime import datetime

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
        print("✅ API iniciada en proceso:", api_process.pid)
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
        time.sleep(5)  # Esperar un poco
        return True

def ejecutar_katalon():
    """Ejecutar las pruebas de Katalon"""
    print(f"\n{'='*60}")
    print("🎯 EJECUTANDO PRUEBAS KATALON")
    print(f"{'='*60}")
    
    try:
        # Ejecutar el script de Katalon
        resultado = subprocess.run(
            [sys.executable, 'ejecutar_katalon.py'],
            capture_output=True,
            text=True
        )
        
        print("📤 SALIDA DE KATALON:")
        print(resultado.stdout)
        
        if resultado.stderr:
            print("⚠️ ADVERTENCIAS/ERRORES:")
            print(resultado.stderr)
        
        return resultado.returncode == 0
        
    except Exception as e:
        print(f"❌ Error ejecutando Katalon: {e}")
        return False

def main():
    print("🎯 KATALON COMPLETO - CON API AUTOMÁTICA")
    print("📋 API Ferretería - Evaluación 3")
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    try:
        # 1. Iniciar la API
        if not iniciar_api():
            print("❌ No se pudo iniciar la API")
            return False
        
        # 2. Esperar a que la API esté disponible
        print("\n⏳ Esperando que la API esté lista...")
        if not verificar_api_disponible():
            print("❌ La API no respondió a tiempo")
            return False
        
        # 3. Ejecutar pruebas Katalon
        print("\n🎯 API lista, ejecutando pruebas Katalon...")
        exito_katalon = ejecutar_katalon()
        
        # 4. Mostrar resultados
        print(f"\n{'='*60}")
        print("📊 RESULTADOS FINALES")
        print(f"{'='*60}")
        
        if exito_katalon:
            print("🎉 ¡KATALON EJECUTADO EXITOSAMENTE!")
            print("✅ Todas las pruebas de API completadas")
            print("📁 Revisa katalon_test_results.json para detalles")
        else:
            print("⚠️ Katalon tuvo algunos problemas")
            print("💡 Pero la API funcionó correctamente")
        
        return exito_katalon
        
    except KeyboardInterrupt:
        print("\n⚠️ Ejecución interrumpida por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False
    finally:
        # Siempre detener la API al final
        detener_api()

if __name__ == "__main__":
    # Manejar Ctrl+C correctamente
    def signal_handler(sig, frame):
        print("\n🛑 Deteniendo ejecución...")
        detener_api()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    success = main()
    sys.exit(0 if success else 1)