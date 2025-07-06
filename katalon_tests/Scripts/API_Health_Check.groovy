import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import static com.kms.katalon.core.testobject.ObjectRepository.findWindowsObject
import com.kms.katalon.core.checkpoint.Checkpoint as Checkpoint
import com.kms.katalon.core.cucumber.keyword.CucumberBuiltinKeywords as CucumberKW
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import com.kms.katalon.core.model.FailureHandling as FailureHandling
import com.kms.katalon.core.testcase.TestCase as TestCase
import com.kms.katalon.core.testdata.TestData as TestData
import com.kms.katalon.core.testng.keyword.TestNGBuiltinKeywords as TestNGKW
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.kms.katalon.core.windows.keyword.WindowsBuiltinKeywords as Windows
import internal.GlobalVariable as GlobalVariable
import org.openqa.selenium.Keys as Keys

/**
 * Test Case: API Health Check
 * Descripción: Verificar que el endpoint de health check responda correctamente
 * Autor: Sistema de Pruebas Ferretería
 * Fecha: 2025-07-01
 */

// Configuración de la prueba
String baseUrl = base_url
String endpoint = '/health'
String fullUrl = baseUrl + endpoint

println("🎯 INICIANDO PRUEBA: API Health Check")
println("📍 URL: " + fullUrl)

// Crear objeto de solicitud
TestObject healthCheckRequest = new TestObject()
healthCheckRequest.setRestUrl(fullUrl)
healthCheckRequest.setRestRequestMethod('GET')

// Agregar headers
healthCheckRequest.setHttpHeaderProperties([
    new TestObjectProperty('Content-Type', ConditionType.EQUALS, 'application/json'),
    new TestObjectProperty('Accept', ConditionType.EQUALS, 'application/json')
])

try {
    // Ejecutar la solicitud
    println("📤 Enviando solicitud GET a " + endpoint)
    def response = WS.sendRequest(healthCheckRequest)
    
    // Verificar código de estado
    println("📥 Código de respuesta: " + response.getStatusCode())
    WS.verifyResponseStatusCode(response, 200)
    
    // Obtener y verificar el cuerpo de la respuesta
    String responseBody = response.getResponseBodyContent()
    println("📄 Cuerpo de respuesta: " + responseBody)
    
    // Verificar que la respuesta contiene los campos esperados
    WS.verifyElementPropertyValue(response, 'status', 'healthy')
    WS.verifyElementPropertyValue(response, 'version', '1.0.0')
    
    // Verificar que el timestamp existe
    def jsonResponse = new groovy.json.JsonSlurper().parseText(responseBody)
    assert jsonResponse.timestamp != null : "El timestamp debe estar presente"
    assert jsonResponse.timestamp != "" : "El timestamp no debe estar vacío"
    
    println("✅ PRUEBA EXITOSA: Health Check respondió correctamente")
    println("   - Status: " + jsonResponse.status)
    println("   - Version: " + jsonResponse.version)
    println("   - Timestamp: " + jsonResponse.timestamp)
    
} catch (Exception e) {
    println("❌ ERROR EN LA PRUEBA: " + e.getMessage())
    throw e
}

println("🏁 FINALIZANDO PRUEBA: API Health Check")