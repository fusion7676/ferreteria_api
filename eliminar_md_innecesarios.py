#!/usr/bin/env python3
"""
Script simple para eliminar archivos .md innecesarios
Mantiene solo README.md
"""

import os

def main():
    print("🧹 ELIMINANDO ARCHIVOS .MD INNECESARIOS")
    print("✅ Manteniendo solo README.md")
    print("=" * 50)
    
    # Archivos .md a eliminar
    archivos_eliminar = [
        "git_commands.md",
        "INSTRUCCIONES_GIT.md", 
        "KATALON_SETUP_GUIDE.md",
        "RESUMEN_PROYECTO.md",
        "SOLUCION_GITHUB.md",
        "CAMBIOS_REALIZADOS.md"
    ]
    
    eliminados = 0
    
    for archivo in archivos_eliminar:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"✅ Eliminado: {archivo}")
                eliminados += 1
            except Exception as e:
                print(f"❌ Error: {archivo} - {e}")
        else:
            print(f"ℹ️  No existe: {archivo}")
    
    print(f"\n📊 RESULTADO:")
    print(f"   Archivos eliminados: {eliminados}")
    
    if os.path.exists("README.md"):
        print(f"   ✅ README.md mantenido correctamente")
    else:
        print(f"   ⚠️  README.md no encontrado!")
    
    print(f"\n🎉 Limpieza completada!")
    print(f"💡 Ahora ejecuta: git add . && git commit -m 'Optimizar documentación: mantener solo README.md' && git push")

if __name__ == "__main__":
    main()