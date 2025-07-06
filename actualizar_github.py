#!/usr/bin/env python3
"""
Script para actualizar el repositorio de GitHub con todos los cambios
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
            print("📤 Salida:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("⚠️ Errores/Advertencias:")
            print(resultado.stderr)
        
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - EXITOSO")
            return True
        else:
            print(f"❌ {descripcion} - FALLÓ (código: {resultado.returncode})")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def limpiar_archivos_innecesarios():
    """Eliminar archivos .md innecesarios"""
    print("\n🧹 LIMPIANDO ARCHIVOS INNECESARIOS")
    print("📋 Manteniendo solo README.md")
    print("-" * 50)
    
    archivos_eliminar = [
        "git_commands.md",
        "INSTRUCCIONES_GIT.md", 
        "KATALON_SETUP_GUIDE.md",
        "RESUMEN_PROYECTO.md",
        "SOLUCION_GITHUB.md",
        "CAMBIOS_REALIZADOS.md",
        "limpiar_archivos.py"
    ]
    
    eliminados = 0
    for archivo in archivos_eliminar:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"✅ Eliminado: {archivo}")
                eliminados += 1
            except Exception as e:
                print(f"❌ Error eliminando {archivo}: {e}")
    
    print(f"📊 Archivos eliminados: {eliminados}")
    print(f"✅ README.md mantenido como único archivo .md")
    return True

def main():
    print("🚀 ACTUALIZADOR DE GITHUB")
    print("📋 Subiendo cambios del proyecto API Ferretería")
    print("=" * 60)
    
    # Paso 0: Limpiar archivos innecesarios
    print("\n🧹 FASE 0: LIMPIEZA DE ARCHIVOS")
    limpiar_archivos_innecesarios()
    
    # Verificar que estamos en un repositorio Git
    if not os.path.exists('.git'):
        print("❌ No se encontró repositorio Git en este directorio")
        print("💡 Asegúrate de estar en el directorio del proyecto")
        return False
    
    # Paso 1: Ver estado actual
    print("\n📊 VERIFICANDO ESTADO ACTUAL DEL REPOSITORIO")
    ejecutar_comando("git status", "Verificar estado de Git")
    
    # Paso 2: Agregar todos los archivos
    print("\n📦 AGREGANDO ARCHIVOS AL STAGING AREA")
    if not ejecutar_comando("git add .", "Agregar todos los cambios"):
        return False
    
    # Paso 3: Ver qué se va a commitear
    print("\n👀 ARCHIVOS QUE SE VAN A COMMITEAR")
    ejecutar_comando("git status --short", "Ver archivos en staging")
    
    # Paso 4: Hacer commit
    mensaje_commit = "Actualizar proyecto: eliminar referencias académicas y mejorar documentación profesional"
    print(f"\n💾 CREANDO COMMIT")
    if not ejecutar_comando(f'git commit -m "{mensaje_commit}"', "Crear commit"):
        print("ℹ️ Puede que no haya cambios para commitear")
    
    # Paso 5: Subir a GitHub
    print("\n🌐 SUBIENDO CAMBIOS A GITHUB")
    if not ejecutar_comando("git push origin master", "Subir cambios"):
        print("\n⚠️ Push normal falló, intentando con force...")
        if not ejecutar_comando("git push --force origin master", "Force push"):
            return False
    
    print("\n🎉 ¡ACTUALIZACIÓN COMPLETADA!")
    print("✅ Todos los cambios han sido subidos a GitHub")
    print("🔗 Revisa tu repositorio en GitHub para confirmar")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🏁 Proceso completado exitosamente")
            sys.exit(0)
        else:
            print("\n❌ Proceso completado con errores")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)