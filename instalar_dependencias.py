#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 INSTALADOR AUTOMÁTICO DE DEPENDENCIAS
"""

import subprocess
import sys
import os

def ejecutar_comando(comando, descripcion):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔧 {descripcion}")
    print(f"📍 Ejecutando: {comando}")
    print("-" * 50)
    
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.stdout:
            print("📤 SALIDA:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("⚠️ ERRORES/ADVERTENCIAS:")
            print(resultado.stderr)
        
        exito = resultado.returncode == 0
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        print(f"{estado} - {descripcion}")
        
        return exito
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔧 INSTALADOR AUTOMÁTICO DE DEPENDENCIAS")
    print("📋 Proyecto: API Ferretería")
    print("=" * 60)
    
    # Verificar Python
    ejecutar_comando("python --version", "Verificar Python")
    
    # Actualizar pip
    ejecutar_comando("python -m pip install --upgrade pip", "Actualizar pip")
    
    # Instalar dependencias
    ejecutar_comando("pip install -r requirements.txt", "Instalar dependencias")
    
    # Verificar instalaciones
    print(f"\n{'='*60}")
    print("🔍 VERIFICANDO INSTALACIONES")
    print(f"{'='*60}")
    
    dependencias = [
        ("flask", "Flask"),
        ("pytest", "PyTest"),
        ("requests", "Requests"),
        ("coverage", "Coverage")
    ]
    
    for modulo, nombre in dependencias:
        comando = f'python -c "import {modulo}; print(\'{nombre} instalado correctamente\')"'
        ejecutar_comando(comando, f"Verificar {nombre}")
    
    print(f"\n{'='*60}")
    print("🎉 INSTALACIÓN COMPLETADA")
    print(f"{'='*60}")
    print("✅ Ahora puedes ejecutar:")
    print("   python ejecutar_todo_perfecto.py")
    print("=" * 60)

if __name__ == "__main__":
    main()