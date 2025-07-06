#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 PROBADOR DE KATALON SOLO
Para verificar que Katalon funciona independientemente
"""

import subprocess
import sys
import time
import signal
import os

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    try:
        # Intentar configurar UTF-8
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # Si falla, usar método alternativo
        os.environ['PYTHONIOENCODING'] = 'utf-8'

def safe_print(text):
    """Imprimir texto de forma segura, manejando problemas de codificación"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Si hay problemas con emojis, usar versión sin emojis
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        print(safe_text)

# Variable global para el proceso de la API
api_process = None

def iniciar_api():
    """Iniciar la API"""
    global api_process
    try:
        safe_print("🚀 Iniciando API Flask...")
        api_process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        safe_print(f"✅ API iniciada en proceso: {api_process.pid}")
        return True
    except Exception as e:
        safe_print(f"❌ Error iniciando API: {e}")
        return False

def detener_api():
    """Detener la API"""
    global api_process
    if api_process:
        try:
            safe_print("🛑 Deteniendo API...")
            api_process.terminate()
            api_process.wait(timeout=5)
            safe_print("✅ API detenida correctamente")
        except:
            try:
                api_process.kill()
                safe_print("✅ API forzada a detenerse")
            except:
                safe_print("⚠️ No se pudo detener la API completamente")

def verificar_api_disponible():
    """Verificar que la API esté disponible"""
    try:
        import requests
        for intento in range(10):
            try:
                response = requests.get('http://localhost:5000/health', timeout=2)
                if response.status_code == 200:
                    safe_print(f"✅ API disponible después de {intento + 1} intentos")
                    return True
            except:
                pass
            
            safe_print(f"⏳ Esperando API... intento {intento + 1}/10")
            time.sleep(2)
        
        return False
    except ImportError:
        safe_print("⚠️ Requests no disponible, esperando 5 segundos...")
        time.sleep(5)
        return True

def main():
    safe_print("🧪 PROBADOR DE KATALON SOLO")
    safe_print("📋 Verificar que Katalon funciona independientemente")
    safe_print("=" * 60)
    
    try:
        # Iniciar API
        if not iniciar_api():
            safe_print("❌ No se pudo iniciar la API")
            return False
        
        # Esperar API
        safe_print("\n⏳ Esperando que la API esté lista...")
        if not verificar_api_disponible():
            safe_print("❌ La API no respondió a tiempo")
            return False
        
        # Ejecutar Katalon
        safe_print("\n🎯 API lista, ejecutando pruebas Katalon...")
        resultado = subprocess.run(
            [sys.executable, "ejecutar_katalon_fixed.py"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        safe_print("📤 SALIDA DE KATALON:")
        safe_print(resultado.stdout)
        
        if resultado.stderr:
            safe_print("⚠️ ERRORES/ADVERTENCIAS:")
            safe_print(resultado.stderr)
        
        exito = resultado.returncode == 0
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        safe_print(f"\n{estado} - Katalon")
        
        return exito
        
    except KeyboardInterrupt:
        safe_print("\n⚠️ Ejecución interrumpida por el usuario")
        return False
    except Exception as e:
        safe_print(f"\n❌ Error inesperado: {e}")
        return False
    finally:
        # Siempre detener la API
        detener_api()

if __name__ == "__main__":
    # Manejar Ctrl+C correctamente
    def signal_handler(sig, frame):
        safe_print("\n🛑 Deteniendo ejecución...")
        detener_api()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        success = main()
        safe_print(f"\n🏁 RESULTADO: {'EXITOSO' if success else 'FALLÓ'}")
        sys.exit(0 if success else 1)
    except Exception as e:
        safe_print(f"❌ Error inesperado: {e}")
        sys.exit(1)