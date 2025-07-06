#!/usr/bin/env python3
"""
EJECUTOR COMPLETO PARA EVALUACIÓN 3
API Ferretería - Todas las pruebas en secuencia
"""

import subprocess
import sys
import os
import time
from datetime import datetime

def ejecutar_comando(comando, descripcion, directorio=None):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n{'='*70}")
    print(f"🔧 {descripcion}")
    print(f"{'='*70}")
    print(f"📍 Comando: {comando}")
    if directorio:
        print(f"📁 Directorio: {directorio}")
    print("-" * 50)
    
    try:
        kwargs = {'shell': True, 'check': False}
        if directorio:
            kwargs['cwd'] = directorio
            
        resultado = subprocess.run(comando, **kwargs)
        
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - EXITOSO")
            return True
        else:
            print(f"❌ {descripcion} - FALLÓ (código: {resultado.returncode})")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def verificar_archivos():
    """Verificar que los archivos necesarios existen"""
    archivos_necesarios = [
        'app.py',
        'requirements.txt',
        'ejecutar_katalon.py'
    ]
    
    print("🔍 VERIFICANDO ARCHIVOS NECESARIOS...")
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✅ {archivo} - Encontrado")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            return False
    return True

def main():
    print("🎯 EJECUTOR COMPLETO - EVALUACIÓN 3")
    print("📋 API Ferretería - Todas las Pruebas")
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Verificar archivos
    if not verificar_archivos():
        print("❌ Faltan archivos necesarios. Abortando.")
        return False
    
    resultados = []
    
    # 1. INSTALAR DEPENDENCIAS
    print("\n🔧 FASE 1: PREPARACIÓN DEL ENTORNO")
    exito = ejecutar_comando(
        "pip install -r requirements.txt", 
        "INSTALACIÓN DE DEPENDENCIAS"
    )
    resultados.append(("Instalación dependencias", exito))
    
    if not exito:
        print("⚠️ Continuando sin instalar dependencias...")
    
    # 2. EJECUTAR PRUEBAS UNITARIAS
    print("\n🧪 FASE 2: PRUEBAS UNITARIAS")
    exito = ejecutar_comando(
        "python -m pytest tests/unit/ -v --tb=short", 
        "PRUEBAS UNITARIAS"
    )
    resultados.append(("Pruebas unitarias", exito))
    
    # 3. EJECUTAR PRUEBAS DE INTEGRACIÓN
    print("\n🔗 FASE 3: PRUEBAS DE INTEGRACIÓN")
    exito = ejecutar_comando(
        "python -m pytest tests/integration/ -v --tb=short", 
        "PRUEBAS DE INTEGRACIÓN"
    )
    resultados.append(("Pruebas integración", exito))
    
    # 4. GENERAR REPORTE DE COBERTURA
    print("\n📊 FASE 4: COBERTURA DE CÓDIGO")
    exito = ejecutar_comando(
        "python -m pytest --cov=app --cov-report=html --cov-report=xml", 
        "REPORTE DE COBERTURA"
    )
    resultados.append(("Cobertura código", exito))
    
    # 5. EJECUTAR SIMULACIÓN KATALON
    print("\n🎯 FASE 5: PRUEBAS KATALON")
    exito = ejecutar_comando(
        "python ejecutar_katalon.py", 
        "SIMULACIÓN KATALON STUDIO"
    )
    resultados.append(("Katalon Studio", exito))
    
    # 6. GENERAR EVIDENCIAS
    print("\n📸 FASE 6: GENERACIÓN DE EVIDENCIAS")
    if os.path.exists('generar_evidencias.py'):
        exito = ejecutar_comando(
            "python generar_evidencias.py", 
            "GENERACIÓN DE EVIDENCIAS"
        )
        resultados.append(("Evidencias", exito))
    else:
        print("⚠️ Script de evidencias no encontrado, saltando...")
        resultados.append(("Evidencias", False))
    
    # MOSTRAR RESUMEN FINAL
    print(f"\n{'='*80}")
    print("📋 RESUMEN FINAL DE EJECUCIÓN")
    print(f"{'='*80}")
    
    exitosos = 0
    for nombre, exito in resultados:
        estado = "✅ PASSED" if exito else "❌ FAILED"
        print(f"   {estado} - {nombre}")
        if exito:
            exitosos += 1
    
    total = len(resultados)
    porcentaje = (exitosos / total * 100) if total > 0 else 0
    
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   Total de fases: {total}")
    print(f"   Exitosas: {exitosos}")
    print(f"   Fallidas: {total - exitosos}")
    print(f"   Porcentaje de éxito: {porcentaje:.1f}%")
    
    # ARCHIVOS GENERADOS
    print(f"\n📁 ARCHIVOS GENERADOS:")
    archivos_salida = [
        'htmlcov/index.html',
        'coverage.xml',
        'katalon_test_results.json',
        'pytest_report.xml'
    ]
    
    for archivo in archivos_salida:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} (no generado)")
    
    # PRÓXIMOS PASOS
    print(f"\n🎯 PRÓXIMOS PASOS PARA LA EVALUACIÓN:")
    print("   1. Revisar reportes HTML generados")
    print("   2. Tomar capturas de pantalla")
    print("   3. Documentar resultados")
    print("   4. Preparar presentación")
    
    if porcentaje >= 80:
        print(f"\n🎉 ¡EXCELENTE! Tu proyecto está listo para la evaluación")
        print("   Tienes un {:.1f}% de éxito en las pruebas".format(porcentaje))
    elif porcentaje >= 60:
        print(f"\n👍 ¡BIEN! Tu proyecto está en buen estado")
        print("   Considera revisar las pruebas que fallaron")
    else:
        print(f"\n⚠️ Necesitas revisar algunos problemas")
        print("   Revisa los errores mostrados arriba")
    
    return porcentaje >= 60

if __name__ == "__main__":
    success = main()
    print(f"\n🏁 EJECUCIÓN COMPLETADA")
    sys.exit(0 if success else 1)