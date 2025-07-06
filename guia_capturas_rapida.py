#!/usr/bin/env python3
"""
Guía rápida para generar capturas del proyecto
"""

import os
import subprocess
import webbrowser
import time

def print_instruccion(numero, titulo, descripcion, comando=None):
    """Imprimir instrucción de captura"""
    print(f"\n{'='*80}")
    print(f"📸 CAPTURA {numero}: {titulo}")
    print(f"{'='*80}")
    print(f"📝 {descripcion}")
    
    if comando:
        print(f"\n💻 COMANDO A EJECUTAR:")
        print(f"   {comando}")
    
    print(f"\n📷 QUÉ CAPTURAR:")

def main():
    print("🎯 GUÍA RÁPIDA DE CAPTURAS DEL PROYECTO")
    print("📋 Plan de Pruebas API Ferretería")
    print("=" * 80)
    
    # Verificar archivos necesarios
    archivos_necesarios = ['app.py', 'tests', 'requirements.txt']
    faltantes = [archivo for archivo in archivos_necesarios if not os.path.exists(archivo)]
    
    if faltantes:
        print("❌ FALTAN ARCHIVOS NECESARIOS:")
        for archivo in faltantes:
            print(f"   - {archivo}")
        print("\n💡 Ejecuta primero: python configurar_proyecto_completo.py")
        return
    
    print("✅ Archivos necesarios encontrados")
    
    # Captura 1: Pruebas Unitarias
    print_instruccion(
        1, 
        "PRUEBAS UNITARIAS EJECUTÁNDOSE",
        "Mostrar todas las pruebas unitarias pasando",
        "python -m pytest tests/unit/ -v"
    )
    print("   - Terminal con pruebas en verde (PASSED)")
    print("   - Número total de pruebas ejecutadas")
    print("   - Tiempo de ejecución")
    
    input("\n⏸️  Presiona ENTER cuando hayas tomado la CAPTURA 1...")
    
    # Captura 2: Pruebas de Integración
    print_instruccion(
        2,
        "PRUEBAS DE INTEGRACIÓN EJECUTÁNDOSE", 
        "Mostrar pruebas de integración completas",
        "python -m pytest tests/integration/ -v"
    )
    print("   - Pruebas de integración en verde")
    print("   - Flujos completos funcionando")
    
    input("\n⏸️  Presiona ENTER cuando hayas tomado la CAPTURA 2...")
    
    # Captura 3: Cobertura de Código
    print_instruccion(
        3,
        "REPORTE DE COBERTURA DE CÓDIGO",
        "Generar y mostrar reporte de cobertura",
        "python -m pytest --cov=app --cov-report=html"
    )
    print("   - Porcentaje de cobertura >80%")
    print("   - Tabla de archivos con cobertura")
    print("   - Líneas cubiertas vs no cubiertas")
    
    # Ejecutar comando de cobertura
    print("\n🔧 Ejecutando comando de cobertura...")
    try:
        subprocess.run("python -m pytest --cov=app --cov-report=html", shell=True, check=True)
        print("✅ Reporte de cobertura generado")
        
        # Abrir reporte en navegador
        if os.path.exists("htmlcov/index.html"):
            print("🌐 Abriendo reporte en navegador...")
            webbrowser.open("htmlcov/index.html")
            time.sleep(2)
        
    except subprocess.CalledProcessError:
        print("⚠️ Error generando reporte. Ejecuta manualmente el comando.")
    
    input("\n⏸️  Presiona ENTER cuando hayas tomado la CAPTURA 3...")
    
    # Captura 4: API Funcionando
    print_instruccion(
        4,
        "API FUNCIONANDO",
        "Mostrar API respondiendo correctamente",
        "python app.py (en terminal separada)"
    )
    print("   - API ejecutándose sin errores")
    print("   - Mensaje 'Running on http://127.0.0.1:5000'")
    print("   - Health check respondiendo")
    
    print("\n💡 INSTRUCCIONES ESPECIALES:")
    print("   1. Abre una nueva terminal")
    print("   2. Ejecuta: python app.py")
    print("   3. En otra terminal ejecuta: curl http://localhost:5000/health")
    print("   4. Captura ambas terminales")
    
    input("\n⏸️  Presiona ENTER cuando hayas tomado la CAPTURA 4...")
    
    # Captura 5: Reporte XML
    print_instruccion(
        5,
        "REPORTE XML DE RESULTADOS",
        "Generar y mostrar archivo XML de resultados",
        "python -m pytest --junitxml=test-results.xml"
    )
    print("   - Archivo test-results.xml generado")
    print("   - Contenido XML con estructura de pruebas")
    print("   - Número de test cases y tiempo")
    
    # Ejecutar comando XML
    print("\n🔧 Ejecutando comando XML...")
    try:
        subprocess.run("python -m pytest --junitxml=test-results.xml", shell=True, check=True)
        print("✅ Reporte XML generado: test-results.xml")
        
        if os.path.exists("test-results.xml"):
            print("📄 Archivo XML creado exitosamente")
        
    except subprocess.CalledProcessError:
        print("⚠️ Error generando XML. Ejecuta manualmente el comando.")
    
    input("\n⏸️  Presiona ENTER cuando hayas tomado la CAPTURA 5...")
    
    # Captura 6: Estructura del Proyecto
    print_instruccion(
        6,
        "ESTRUCTURA DEL PROYECTO",
        "Mostrar organización completa del proyecto",
        "dir /s (Windows) o tree (si está disponible)"
    )
    print("   - Estructura de directorios")
    print("   - Archivos de pruebas organizados")
    print("   - Archivos de configuración")
    
    input("\n⏸️  Presiona ENTER cuando hayas tomado la CAPTURA 6...")
    
    # Resumen final
    print("\n" + "="*80)
    print("🎉 ¡CAPTURAS COMPLETADAS!")
    print("="*80)
    
    print("📁 ARCHIVOS GENERADOS PARA EVIDENCIAS:")
    archivos_evidencia = [
        "htmlcov/index.html",
        "test-results.xml", 
        "tests/",
        ".coverage"
    ]
    
    for archivo in archivos_evidencia:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} (no encontrado)")
    
    print("\n📋 CHECKLIST DE CAPTURAS:")
    capturas = [
        "Pruebas unitarias ejecutándose",
        "Pruebas de integración ejecutándose", 
        "Reporte de cobertura HTML (>80%)",
        "API funcionando (health check)",
        "Reporte XML de resultados",
        "Estructura del proyecto"
    ]
    
    for i, captura in enumerate(capturas, 1):
        print(f"   📸 Captura {i}: {captura}")
    
    print("\n🎬 PRÓXIMO PASO:")
    print("   - Organizar las capturas en una carpeta")
    print("   - Preparar video DEMO (10-15 minutos)")
    print("   - Completar presentación PPT")
    
    print("\n✅ ¡EVALUACIÓN 3 LISTA PARA ENTREGAR!")

if __name__ == "__main__":
    main()