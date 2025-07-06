#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas y generar reportes
"""
import subprocess
import sys
import os
from datetime import datetime

def ejecutar_comando(comando, descripcion):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n{'='*60}")
    print(f"🔧 {descripcion}")
    print(f"{'='*60}")
    print(f"Ejecutando: {comando}")
    print("-" * 40)
    
    try:
        resultado = subprocess.run(comando, shell=True, check=False)
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - EXITOSO")
            return True
        else:
            print(f"❌ {descripcion} - FALLÓ")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def main():
    print("🎯 EJECUTOR DE PRUEBAS COMPLETAS")
    print("📋 API Ferretería - Evaluación 3")
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("❌ Error: No se encuentra app.py")
        sys.exit(1)
    
    resultados = []
    
    # 1. Instalar dependencias
    exito = ejecutar_comando("pip install -r requirements.txt", "INSTALACIÓN DE DEPENDENCIAS")
    resultados.append(("Instalación dependencias", exito))
    
    # 2. Ejecutar pruebas unitarias
    exito = ejecutar_comando("python -m pytest tests/unit/ -v", "PRUEBAS UNITARIAS")
    resultados.append(("Pruebas unitarias", exito))
    
    # 3. Ejecutar pruebas de integración
    exito = ejecutar_comando("python -m pytest tests/integration/ -v", "PRUEBAS DE INTEGRACIÓN")
    resultados.append(("Pruebas integración", exito))
    
    # 4. Generar reporte de cobertura
    exito = ejecutar_comando("python -m pytest --cov=app --cov-report=html --cov-report=term", "REPORTE DE COBERTURA")
    resultados.append(("Cobertura de código", exito))
    
    # 5. Generar reporte XML
    exito = ejecutar_comando("python -m pytest --junitxml=test-results.xml", "REPORTE XML")
    resultados.append(("Reporte XML", exito))
    
    # Mostrar resumen
    print("\n" + "="*80)
    print("📊 RESUMEN FINAL")
    print("="*80)
    
    total = len(resultados)
    exitosas = sum(1 for _, exito in resultados if exito)
    
    for descripcion, exito in resultados:
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        print(f"{descripcion:<30} {estado}")
    
    print("-" * 80)
    print(f"📊 Total: {total} | Exitosas: {exitosas} | Fallidas: {total - exitosas}")
    print(f"🎯 Porcentaje de éxito: {(exitosas/total)*100:.1f}%")
    
    if exitosas == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
        print("📁 Reportes generados:")
        print("   - htmlcov/index.html (Cobertura)")
        print("   - test-results.xml (Resultados)")
    else:
        print(f"\n⚠️ {total - exitosas} prueba(s) con problemas")
    
    print("\n📸 ¡LISTO PARA CAPTURAS DE PANTALLA!")

if __name__ == "__main__":
    main()