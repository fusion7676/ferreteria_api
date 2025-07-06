#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST SIMPLE DE KATALON
Prueba rápida para verificar que Katalon funciona
"""

import subprocess
import sys
import os

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        os.environ['PYTHONIOENCODING'] = 'utf-8'

def safe_print(text):
    """Imprimir texto de forma segura"""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        print(safe_text)

def main():
    safe_print("🧪 TEST SIMPLE DE KATALON")
    safe_print("=" * 50)
    
    try:
        # Ejecutar Katalon directamente
        safe_print("🎯 Ejecutando Katalon...")
        resultado = subprocess.run(
            [sys.executable, "ejecutar_katalon_fixed.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        safe_print("📤 SALIDA:")
        safe_print(resultado.stdout)
        
        if resultado.stderr:
            safe_print("⚠️ ERRORES:")
            safe_print(resultado.stderr)
        
        exito = resultado.returncode == 0
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        safe_print(f"\n{estado} - Katalon (código: {resultado.returncode})")
        
        return exito
        
    except subprocess.TimeoutExpired:
        safe_print("⏰ TIMEOUT - Katalon tardó demasiado")
        return False
    except Exception as e:
        safe_print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    safe_print(f"\n🏁 RESULTADO FINAL: {'EXITOSO' if success else 'FALLÓ'}")
    sys.exit(0 if success else 1)