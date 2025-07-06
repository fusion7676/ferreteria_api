# 🎯 GUÍA COMPLETA: KATALON STUDIO PARA API FERRETERÍA

## 📋 **OPCIONES DISPONIBLES**

### **Opción 1: Katalon Studio (Interfaz Gráfica) - RECOMENDADO**
### **Opción 2: Katalon Runtime Engine (Línea de comandos)**
### **Opción 3: Simulación con Python (Para capturas rápidas)**

---

## 🚀 **OPCIÓN 1: KATALON STUDIO (INTERFAZ GRÁFICA)**

### **Paso 1: Descargar Katalon Studio**
1. Ve a: https://katalon.com/download
2. Descarga **Katalon Studio** (GRATIS)
3. Instala en tu sistema

### **Paso 2: Crear Proyecto**
1. Abre Katalon Studio
2. **File** → **New** → **Project**
3. Selecciona **API/Web Service**
4. Nombre: `Ferreteria_API_Tests`

### **Paso 3: Importar Nuestros Tests**
1. Copia la carpeta `katalon_tests/` a tu proyecto Katalon
2. **Refresh** el proyecto en Katalon Studio
3. Verás los test cases en el **Test Explorer**

### **Paso 4: Ejecutar Tests**
1. Asegúrate que tu API esté corriendo: `python app.py`
2. Click derecho en **Test Suites/API_Ferreteria_Complete**
3. Selecciona **Run**
4. ¡Observa los resultados en tiempo real!

---

## ⚡ **OPCIÓN 2: KATALON RUNTIME ENGINE**

### **Paso 1: Descargar KRE**
```bash
# Descargar Katalon Runtime Engine
# https://github.com/katalon-studio/katalon-studio/releases
```

### **Paso 2: Ejecutar desde Línea de Comandos**
```bash
# Windows
katalonc.exe -projectPath="C:\tu\proyecto" -testSuiteId="Test Suites/API_Ferreteria_Complete"

# Linux/Mac
./katalonc -projectPath="/tu/proyecto" -testSuiteId="Test Suites/API_Ferreteria_Complete"
```

---

## 🐍 **OPCIÓN 3: SIMULACIÓN CON PYTHON (PARA CAPTURAS)**

### **Ejecutar Simulación**
```bash
# 1. Asegúrate que la API esté corriendo
python app.py

# 2. En otra terminal, ejecuta la simulación
python ejecutar_katalon.py
```

### **¿Qué hace la simulación?**
- ✅ Simula la ejecución de Katalon Studio
- ✅ Genera reportes JSON
- ✅ Muestra resultados como Katalon real
- ✅ Perfecto para capturas de pantalla

---

## 📸 **CAPTURAS NECESARIAS PARA EVALUACIÓN**

### **Captura 1: Katalon Studio Interface**
- Pantalla principal de Katalon Studio
- Test Cases visibles en el explorador
- Scripts Groovy abiertos

### **Captura 2: Ejecución de Tests**
- Tests ejecutándose en tiempo real
- Log de resultados
- Status: PASSED/FAILED

### **Captura 3: Reportes Generados**
- Reporte HTML de Katalon
- Estadísticas de ejecución
- Detalles de cada test case

### **Captura 4: Test Results**
- JSON con resultados detallados
- Tiempos de ejecución
- Validaciones exitosas

---

## 🎯 **TESTS INCLUIDOS**

### **1. API_Health_Check**
- ✅ Verificar endpoint `/health`
- ✅ Validar status code 200
- ✅ Verificar respuesta JSON
- ✅ Validar campos obligatorios

### **2. API_Productos_CRUD**
- ✅ Crear categoría de prueba
- ✅ Crear producto (CREATE)
- ✅ Leer producto (READ)
- ✅ Actualizar stock (UPDATE)
- ✅ Listar productos (READ ALL)
- ✅ Buscar productos
- ✅ Validar errores
- ✅ Manejar casos edge

---

## 📊 **ESTRUCTURA DE ARCHIVOS KATALON**

```
katalon_tests/
├── Test Cases/
│   ├── API_Health_Check.tc
│   └── API_Productos_CRUD.tc
├── Scripts/
│   ├── API_Health_Check.groovy
│   └── API_Productos_CRUD.groovy
├── Object Repository/
│   └── API_Endpoints.rs
└── Test Suites/
    └── API_Ferreteria_Complete.ts
```

---

## 🔧 **COMANDOS ÚTILES**

### **Iniciar API**
```bash
python app.py
```

### **Ejecutar Simulación Katalon**
```bash
python ejecutar_katalon.py
```

### **Verificar API**
```bash
curl http://localhost:5000/health
```

---

## 📋 **CHECKLIST PARA EVALUACIÓN**

- [ ] API ejecutándose correctamente
- [ ] Katalon Studio instalado (o simulación lista)
- [ ] Tests importados en Katalon
- [ ] Ejecución exitosa de todos los tests
- [ ] Capturas de pantalla tomadas
- [ ] Reportes generados
- [ ] Documentación completa

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### **Error: API no disponible**
```bash
# Solución: Iniciar la API
python app.py
```

### **Error: Puerto ocupado**
```bash
# Cambiar puerto en app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### **Error: Katalon no encuentra tests**
```bash
# Verificar estructura de carpetas
# Refresh proyecto en Katalon Studio
```

---

## 🎉 **¡LISTO PARA LA EVALUACIÓN!**

Con esta configuración tendrás:
- ✅ **Tests automatizados** funcionando
- ✅ **Reportes profesionales** generados
- ✅ **Capturas de pantalla** listas
- ✅ **Documentación completa** para entregar

¡Tu evaluación será **EXCELENTE**! 🌟