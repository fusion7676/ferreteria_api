import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.testobject.TestObjectProperty
import com.kms.katalon.core.testobject.ConditionType
import groovy.json.JsonBuilder
import groovy.json.JsonSlurper

/**
 * Test Case: API Productos CRUD
 * Descripción: Pruebas completas de CRUD para productos
 * Autor: Sistema de Pruebas Ferretería
 * Fecha: 2025-07-01
 */

// Configuración de la prueba
String baseUrl = base_url
def jsonSlurper = new JsonSlurper()
def productosCreados = []

println("🎯 INICIANDO PRUEBA: API Productos CRUD")
println("📍 URL Base: " + baseUrl)

try {
    // ========================================
    // 1. CREAR CATEGORÍA PARA LAS PRUEBAS
    // ========================================
    println("\n📝 PASO 1: Crear categoría de prueba")
    
    TestObject createCategoryRequest = new TestObject()
    createCategoryRequest.setRestUrl(baseUrl + '/categorias')
    createCategoryRequest.setRestRequestMethod('POST')
    createCategoryRequest.setHttpHeaderProperties([
        new TestObjectProperty('Content-Type', ConditionType.EQUALS, 'application/json')
    ])
    
    def categoryData = [
        nombre: "Herramientas de Prueba Katalon",
        descripcion: "Categoría creada para pruebas automatizadas"
    ]
    
    createCategoryRequest.setBodyContent(new JsonBuilder(categoryData).toString())
    
    def categoryResponse = WS.sendRequest(createCategoryRequest)
    WS.verifyResponseStatusCode(categoryResponse, 201)
    
    def categoryJson = jsonSlurper.parseText(categoryResponse.getResponseBodyContent())
    def categoriaId = categoryJson.id
    
    println("✅ Categoría creada con ID: " + categoriaId)
    
    // ========================================
    // 2. CREAR PRODUCTO (CREATE)
    // ========================================
    println("\n📝 PASO 2: Crear producto")
    
    TestObject createProductRequest = new TestObject()
    createProductRequest.setRestUrl(baseUrl + '/productos')
    createProductRequest.setRestRequestMethod('POST')
    createProductRequest.setHttpHeaderProperties([
        new TestObjectProperty('Content-Type', ConditionType.EQUALS, 'application/json')
    ])
    
    def productData = [
        nombre: "Martillo de Prueba Katalon",
        descripcion: "Martillo creado para pruebas automatizadas",
        precio: 29.99,
        stock: 10,
        categoria_id: categoriaId
    ]
    
    createProductRequest.setBodyContent(new JsonBuilder(productData).toString())
    
    def createResponse = WS.sendRequest(createProductRequest)
    WS.verifyResponseStatusCode(createResponse, 201)
    
    def createdProduct = jsonSlurper.parseText(createResponse.getResponseBodyContent())
    def productoId = createdProduct.id
    productosCreados.add(productoId)
    
    println("✅ Producto creado con ID: " + productoId)
    
    // Verificar datos del producto creado
    assert createdProduct.nombre == productData.nombre
    assert createdProduct.precio == productData.precio
    assert createdProduct.stock == productData.stock
    
    // ========================================
    // 3. LEER PRODUCTO (READ)
    // ========================================
    println("\n📝 PASO 3: Leer producto creado")
    
    TestObject getProductRequest = new TestObject()
    getProductRequest.setRestUrl(baseUrl + '/productos/' + productoId)
    getProductRequest.setRestRequestMethod('GET')
    
    def getResponse = WS.sendRequest(getProductRequest)
    WS.verifyResponseStatusCode(getResponse, 200)
    
    def retrievedProduct = jsonSlurper.parseText(getResponse.getResponseBodyContent())
    
    println("✅ Producto recuperado: " + retrievedProduct.nombre)
    
    // Verificar que los datos coinciden
    assert retrievedProduct.id == productoId
    assert retrievedProduct.nombre == productData.nombre
    assert retrievedProduct.precio == productData.precio
    
    // ========================================
    // 4. ACTUALIZAR STOCK (UPDATE)
    // ========================================
    println("\n📝 PASO 4: Actualizar stock del producto")
    
    TestObject updateStockRequest = new TestObject()
    updateStockRequest.setRestUrl(baseUrl + '/productos/' + productoId + '/stock')
    updateStockRequest.setRestRequestMethod('PUT')
    updateStockRequest.setHttpHeaderProperties([
        new TestObjectProperty('Content-Type', ConditionType.EQUALS, 'application/json')
    ])
    
    def stockData = [cantidad: 25]
    updateStockRequest.setBodyContent(new JsonBuilder(stockData).toString())
    
    def updateResponse = WS.sendRequest(updateStockRequest)
    WS.verifyResponseStatusCode(updateResponse, 200)
    
    def updatedProduct = jsonSlurper.parseText(updateResponse.getResponseBodyContent())
    
    println("✅ Stock actualizado a: " + updatedProduct.stock)
    assert updatedProduct.stock == 25
    
    // ========================================
    // 5. LISTAR PRODUCTOS (READ ALL)
    // ========================================
    println("\n📝 PASO 5: Listar todos los productos")
    
    TestObject listProductsRequest = new TestObject()
    listProductsRequest.setRestUrl(baseUrl + '/productos')
    listProductsRequest.setRestRequestMethod('GET')
    
    def listResponse = WS.sendRequest(listProductsRequest)
    WS.verifyResponseStatusCode(listResponse, 200)
    
    def productsList = jsonSlurper.parseText(listResponse.getResponseBodyContent())
    
    println("✅ Total de productos: " + productsList.size())
    
    // Verificar que nuestro producto está en la lista
    def nuestroProducto = productsList.find { it.id == productoId }
    assert nuestroProducto != null : "El producto creado debe estar en la lista"
    
    // ========================================
    // 6. BUSCAR PRODUCTOS
    // ========================================
    println("\n📝 PASO 6: Buscar productos")
    
    TestObject searchProductsRequest = new TestObject()
    searchProductsRequest.setRestUrl(baseUrl + '/productos?buscar=Katalon')
    searchProductsRequest.setRestRequestMethod('GET')
    
    def searchResponse = WS.sendRequest(searchProductsRequest)
    WS.verifyResponseStatusCode(searchResponse, 200)
    
    def searchResults = jsonSlurper.parseText(searchResponse.getResponseBodyContent())
    
    println("✅ Productos encontrados en búsqueda: " + searchResults.size())
    assert searchResults.size() > 0 : "Debe encontrar al menos un producto"
    
    // ========================================
    // 7. PRUEBAS DE VALIDACIÓN
    // ========================================
    println("\n📝 PASO 7: Pruebas de validación")
    
    // Intentar crear producto sin nombre
    TestObject invalidProductRequest = new TestObject()
    invalidProductRequest.setRestUrl(baseUrl + '/productos')
    invalidProductRequest.setRestRequestMethod('POST')
    invalidProductRequest.setHttpHeaderProperties([
        new TestObjectProperty('Content-Type', ConditionType.EQUALS, 'application/json')
    ])
    
    def invalidData = [
        descripcion: "Producto sin nombre",
        precio: 10.0,
        stock: 5
    ]
    
    invalidProductRequest.setBodyContent(new JsonBuilder(invalidData).toString())
    
    def invalidResponse = WS.sendRequest(invalidProductRequest)
    WS.verifyResponseStatusCode(invalidResponse, 400)
    
    println("✅ Validación correcta: Producto sin nombre rechazado")
    
    // ========================================
    // 8. PRUEBA DE PRODUCTO NO ENCONTRADO
    // ========================================
    println("\n📝 PASO 8: Prueba de producto no encontrado")
    
    TestObject notFoundRequest = new TestObject()
    notFoundRequest.setRestUrl(baseUrl + '/productos/99999')
    notFoundRequest.setRestRequestMethod('GET')
    
    def notFoundResponse = WS.sendRequest(notFoundRequest)
    WS.verifyResponseStatusCode(notFoundResponse, 404)
    
    println("✅ Manejo correcto de producto no encontrado")
    
    println("\n🎉 TODAS LAS PRUEBAS CRUD COMPLETADAS EXITOSAMENTE")
    println("📊 Resumen:")
    println("   - Categoría creada: ID " + categoriaId)
    println("   - Producto creado: ID " + productoId)
    println("   - Stock actualizado: 10 → 25")
    println("   - Búsqueda funcional")
    println("   - Validaciones correctas")
    
} catch (Exception e) {
    println("❌ ERROR EN LA PRUEBA CRUD: " + e.getMessage())
    e.printStackTrace()
    throw e
}

println("🏁 FINALIZANDO PRUEBA: API Productos CRUD")