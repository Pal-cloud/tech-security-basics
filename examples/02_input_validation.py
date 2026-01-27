"""
🛡️ Módulo 2: Validación y Sanitización de Datos
===============================================

Aprende a validar y limpiar datos de entrada para prevenir ataques de inyección
y otros problemas de seguridad. ¡La primera línea de defensa!

⚠️ NUNCA confíes en datos que vienen del usuario!
"""

import re
import html
import json
import urllib.parse
from typing import Dict, List, Tuple, Union, Any
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init()

def print_educational_header():
    """Muestra información educativa sobre validación"""
    print(f"\n{Fore.CYAN}🛡️ MÓDULO 2: VALIDACIÓN Y SANITIZACIÓN DE DATOS{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=" * 55)
    print(f"{Fore.GREEN}✅ Lo que aprenderás:")
    print("   • Por qué nunca confiar en datos del usuario")
    print("   • Diferencia entre validación y sanitización")
    print("   • Prevenir inyecciones SQL, XSS y otras vulnerabilidades")
    print("   • Validar emails, URLs, números de forma segura")
    print(f"   • Escapar caracteres peligrosos correctamente{Style.RESET_ALL}\n")

def demostrar_problema_sin_validacion():
    """Demuestra los problemas de no validar datos"""
    print(f"{Fore.RED}🚨 PROBLEMA: Datos sin validar")
    print(f"{'=' * 35}{Style.RESET_ALL}")
    
    print("Imagina un formulario de registro sin validación:")
    
    # Datos maliciosos que un atacante podría enviar
    datos_maliciosos = {
        "nombre": "<script>alert('XSS Attack!')</script>",
        "email": "'; DROP TABLE users; --",
        "edad": "no_soy_un_numero",
        "website": "javascript:alert('Malicious!')",
        "comentario": "Normal text<img src=x onerror=alert('XSS')>"
    }
    
    print("\nDatos que recibimos del formulario:")
    for campo, valor in datos_maliciosos.items():
        print(f"  {campo}: {valor}")
    
    print(f"\n{Fore.RED}💀 Problemas potenciales:")
    print("   • Inyección SQL: Podría borrar tu base de datos")
    print("   • XSS: JavaScript malicioso ejecutándose en tu web")
    print("   • Datos corruptos: Crashes de aplicación")
    print(f"   • Bypass de lógica: Comportamientos inesperados{Style.RESET_ALL}\n")
    
    return datos_maliciosos

class ValidadorSeguro:
    """Clase para validar y sanitizar datos de forma segura"""
    
    def __init__(self):
        # Patrones de validación comunes
        self.patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?[\d\s\-\(\)]{10,}$',
            'url': r'^https?://[^\s/$.?#].[^\s]*$',
            'alphanumeric': r'^[a-zA-Z0-9]+$',
            'safe_string': r'^[a-zA-Z0-9\s\-_.]+$'
        }
    
    def validar_email(self, email: str) -> Tuple[bool, str]:
        """Valida formato de email"""
        if not isinstance(email, str):
            return False, "Email debe ser una cadena de texto"
        
        # Limpiar espacios
        email = email.strip().lower()
        
        # Verificar longitud
        if len(email) > 254:  # RFC 5321 límite
            return False, "Email demasiado largo"
        
        # Verificar patrón
        if not re.match(self.patterns['email'], email):
            return False, "Formato de email inválido"
        
        # Verificaciones adicionales
        if '..' in email:
            return False, "Email no puede tener puntos consecutivos"
        
        return True, email
    
    def validar_edad(self, edad: Union[str, int]) -> Tuple[bool, Union[int, str]]:
        """Valida edad como número entero en rango válido"""
        try:
            edad_int = int(edad)
            
            if edad_int < 0:
                return False, "La edad no puede ser negativa"
            
            if edad_int > 150:
                return False, "Edad no realista (mayor a 150)"
            
            return True, edad_int
            
        except (ValueError, TypeError):
            return False, "La edad debe ser un número entero"
    
    def validar_url(self, url: str) -> Tuple[bool, str]:
        """Valida y sanitiza URLs"""
        if not isinstance(url, str):
            return False, "URL debe ser una cadena de texto"
        
        url = url.strip()
        
        # Verificar longitud
        if len(url) > 2048:  # Límite práctico de URLs
            return False, "URL demasiado larga"
        
        # Verificar que no sea JavaScript
        if url.lower().startswith(('javascript:', 'data:', 'vbscript:')):
            return False, "Esquema de URL no permitido"
        
        # Verificar patrón HTTP/HTTPS
        if not re.match(self.patterns['url'], url):
            return False, "Formato de URL inválido"
        
        return True, url
    
    def sanitizar_html(self, texto: str) -> str:
        """Escapa caracteres HTML peligrosos"""
        if not isinstance(texto, str):
            return str(texto)
        
        # Escapar caracteres HTML
        texto_seguro = html.escape(texto)
        
        return texto_seguro
    
    def sanitizar_sql(self, texto: str) -> str:
        """Sanitiza texto para prevenir inyección SQL básica"""
        if not isinstance(texto, str):
            return str(texto)
        
        # Escapar comillas simples (método básico, usar parámetros en producción)
        texto_seguro = texto.replace("'", "''")
        
        # Remover caracteres peligrosos
        caracteres_peligrosos = [';', '--', '/*', '*/', 'xp_', 'sp_']
        for char in caracteres_peligrosos:
            texto_seguro = texto_seguro.replace(char, '')
        
        return texto_seguro
    
    def validar_campo_texto(self, texto: str, max_length: int = 255, 
                           allow_html: bool = False) -> Tuple[bool, str]:
        """Valida campos de texto generales"""
        if not isinstance(texto, str):
            return False, "El campo debe ser texto"
        
        # Limpiar espacios
        texto = texto.strip()
        
        # Verificar longitud
        if len(texto) == 0:
            return False, "El campo no puede estar vacío"
        
        if len(texto) > max_length:
            return False, f"El texto no puede exceder {max_length} caracteres"
        
        # Sanitizar si no se permite HTML
        if not allow_html:
            texto = self.sanitizar_html(texto)
        
        return True, texto

def demostrar_validacion():
    """Demuestra el proceso de validación"""
    print(f"{Fore.GREEN}✅ VALIDACIÓN: Verificar que los datos son correctos")
    print(f"{'=' * 50}{Style.RESET_ALL}")
    
    validador = ValidadorSeguro()
    
    # Casos de prueba para email
    emails_prueba = [
        "usuario@ejemplo.com",  # Válido
        "test.email+tag@domain.co.uk",  # Válido
        "invalid-email",  # Inválido
        "test@",  # Inválido
        "@domain.com",  # Inválido
        "test..test@domain.com",  # Inválido
        "a" * 300 + "@domain.com"  # Demasiado largo
    ]
    
    print("Validando emails:")
    for email in emails_prueba:
        es_valido, resultado = validador.validar_email(email)
        emoji = "✅" if es_valido else "❌"
        display_email = email[:30] + "..." if len(email) > 30 else email
        print(f"  {emoji} {display_email:<35} -> {resultado}")
    
    # Casos de prueba para edad
    print(f"\nValidando edades:")
    edades_prueba = [25, "30", "abc", -5, 200, "25.5"]
    
    for edad in edades_prueba:
        es_valido, resultado = validador.validar_edad(edad)
        emoji = "✅" if es_valido else "❌"
        print(f"  {emoji} {str(edad):<10} -> {resultado}")

def demostrar_sanitizacion():
    """Demuestra el proceso de sanitización"""
    print(f"\n{Fore.BLUE}🧼 SANITIZACIÓN: Limpiar datos potencialmente peligrosos")
    print(f"{'=' * 55}{Style.RESET_ALL}")
    
    validador = ValidadorSeguro()
    
    # Casos de prueba para HTML
    html_prueba = [
        "Texto normal",
        "<script>alert('XSS')</script>",
        "Hola <b>mundo</b>!",
        "<img src=x onerror=alert('hack')>",
        "5 < 10 && 3 > 1"
    ]
    
    print("Sanitizando HTML:")
    for html_text in html_prueba:
        sanitizado = validador.sanitizar_html(html_text)
        print(f"  Original:  {html_text}")
        print(f"  Sanitizado: {sanitizado}")
        print()

def demostrar_validacion_completa():
    """Ejemplo completo de validación de un formulario"""
    print(f"\n{Fore.MAGENTA}🎯 EJEMPLO PRÁCTICO: Formulario de Registro Seguro")
    print(f"{'=' * 55}{Style.RESET_ALL}")
    
    validador = ValidadorSeguro()
    
    def procesar_registro(datos: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Procesa un formulario de registro con validación completa"""
        errores = {}
        datos_limpios = {}
        
        # Validar nombre
        if 'nombre' in datos:
            valido, resultado = validador.validar_campo_texto(
                datos['nombre'], max_length=50, allow_html=False
            )
            if valido:
                datos_limpios['nombre'] = resultado
            else:
                errores['nombre'] = resultado
        else:
            errores['nombre'] = "Nombre es requerido"
        
        # Validar email
        if 'email' in datos:
            valido, resultado = validador.validar_email(datos['email'])
            if valido:
                datos_limpios['email'] = resultado
            else:
                errores['email'] = resultado
        else:
            errores['email'] = "Email es requerido"
        
        # Validar edad
        if 'edad' in datos:
            valido, resultado = validador.validar_edad(datos['edad'])
            if valido:
                datos_limpios['edad'] = resultado
            else:
                errores['edad'] = resultado
        
        # Validar website (opcional)
        if 'website' in datos and datos['website']:
            valido, resultado = validador.validar_url(datos['website'])
            if valido:
                datos_limpios['website'] = resultado
            else:
                errores['website'] = resultado
        
        # Validar comentario
        if 'comentario' in datos:
            valido, resultado = validador.validar_campo_texto(
                datos['comentario'], max_length=500, allow_html=False
            )
            if valido:
                datos_limpios['comentario'] = resultado
        
        return len(errores) == 0, datos_limpios if not errores else errores
    
    # Casos de prueba
    casos_prueba = [
        {
            "nombre": "Ana García",
            "email": "ana@ejemplo.com",
            "edad": 28,
            "website": "https://ana.blog.com",
            "comentario": "Me gusta aprender sobre seguridad"
        },
        {
            "nombre": "<script>alert('hack')</script>",
            "email": "email_invalido",
            "edad": "no_es_numero",
            "website": "javascript:alert('xss')",
            "comentario": "A" * 1000  # Demasiado largo
        },
        {
            "nombre": "",  # Vacío
            "email": "test@domain.com",
            "edad": -5,  # Negativo
            "comentario": "Comentario válido"
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n--- Caso de Prueba {i} ---")
        print("Datos originales:")
        for campo, valor in caso.items():
            display_valor = str(valor)[:50] + "..." if len(str(valor)) > 50 else str(valor)
            print(f"  {campo}: {display_valor}")
        
        es_valido, resultado = procesar_registro(caso)
        
        if es_valido:
            print(f"{Fore.GREEN}✅ Formulario VÁLIDO{Style.RESET_ALL}")
            print("Datos limpios:")
            for campo, valor in resultado.items():
                print(f"  {campo}: {valor}")
        else:
            print(f"{Fore.RED}❌ Formulario INVÁLIDO{Style.RESET_ALL}")
            print("Errores encontrados:")
            for campo, error in resultado.items():
                print(f"  {campo}: {error}")

def mejores_practicas_validacion():
    """Muestra las mejores prácticas de validación"""
    print(f"\n{Fore.CYAN}📋 MEJORES PRÁCTICAS DE VALIDACIÓN")
    print(f"{'=' * 40}{Style.RESET_ALL}")
    
    practices = [
        ("✅ Valida TODOS los datos de entrada", "Usuario, URL, cookies, headers, etc."),
        ("✅ Usa whitelist, no blacklist", "Define qué SI está permitido"),
        ("✅ Valida en el servidor SIEMPRE", "JavaScript client-side es fácil de bypassear"),
        ("✅ Sanitiza para el contexto específico", "HTML, SQL, CSV, etc. requieren sanitización diferente"),
        ("✅ Usa bibliotecas probadas", "No reinventes validadores complejos"),
        ("❌ NUNCA confíes en validación del front-end", "Es solo para UX, no para seguridad"),
        ("✅ Implementa rate limiting", "Previene ataques de fuerza bruta"),
        ("✅ Loguea intentos maliciosos", "Para detección y análisis"),
        ("❌ No uses eval() con datos del usuario", "Ejecución de código arbitrario"),
        ("✅ Parametriza consultas SQL", "La forma correcta de prevenir SQL injection")
    ]
    
    for practice, explanation in practices:
        color = Fore.GREEN if practice.startswith("✅") else Fore.RED
        print(f"{color}{practice}{Style.RESET_ALL}")
        print(f"   └─ {explanation}")

def ejemplo_prevencion_sql_injection():
    """Muestra cómo prevenir SQL injection correctamente"""
    print(f"\n{Fore.RED}🛡️ PREVENCIÓN DE SQL INJECTION")
    print(f"{'=' * 35}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}❌ FORMA INCORRECTA (Vulnerable):{Style.RESET_ALL}")
    username = "'; DROP TABLE users; --"
    query_insegura = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"Query generada: {query_insegura}")
    print("¡Esta query borraría toda la tabla users!")
    
    print(f"\n{Fore.GREEN}✅ FORMA CORRECTA (Segura):{Style.RESET_ALL}")
    print("Usando consultas parametrizadas:")
    print("query = 'SELECT * FROM users WHERE username = ?'")
    print("execute(query, (username,))")
    print("El driver de BD escapará automáticamente los caracteres peligrosos")

if __name__ == "__main__":
    print_educational_header()
    
    # Ejecutar todas las demostraciones
    datos_maliciosos = demostrar_problema_sin_validacion()
    demostrar_validacion()
    demostrar_sanitizacion()
    demostrar_validacion_completa()
    ejemplo_prevencion_sql_injection()
    mejores_practicas_validacion()
    
    print(f"\n{Fore.MAGENTA}🎓 ¡Excelente trabajo!")
    print("Ahora sabes cómo validar y sanitizar datos de forma segura.")
    print("Esta es una de las defensas MÁS IMPORTANTES contra ataques.")
    print(f"\nPróximo paso: Módulo 3 - Autenticación con JWT{Style.RESET_ALL}")
