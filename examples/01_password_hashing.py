"""
🔐 Módulo 1: Hashing Seguro de Contraseñas
===========================================

Aprende cómo proteger contraseñas de forma segura usando hashing + salt.
Este es uno de los conceptos MÁS IMPORTANTES en seguridad.

⚠️ NUNCA almacenes contraseñas en texto plano!
"""

import hashlib
import secrets
import bcrypt
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init()

def print_educational_header():
    """Muestra información educativa sobre hashing"""
    print(f"\n{Fore.CYAN}🔐 MÓDULO 1: HASHING SEGURO DE CONTRASEÑAS{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=" * 50)
    print(f"{Fore.GREEN}✅ Lo que aprenderás:")
    print("   • Por qué nunca guardar contraseñas en texto plano")
    print("   • Qué es un hash y por qué es unidireccional")
    print("   • Por qué necesitas salt (sal) en tus hashes")
    print("   • Cómo usar bcrypt (la forma profesional)")
    print(f"   • Cómo verificar contraseñas sin conocerlas{Style.RESET_ALL}\n")

def demostrar_problema_texto_plano():
    """Demuestra por qué el texto plano es peligroso"""
    print(f"{Fore.RED}🚨 PROBLEMA: Contraseñas en texto plano")
    print(f"{'=' * 40}{Style.RESET_ALL}")
    
    # Simulación de una "base de datos" insegura
    usuarios_inseguros = {
        "juan": "123456",
        "maria": "password",
        "carlos": "qwerty"
    }
    
    print("Base de datos INSEGURA:")
    for usuario, password in usuarios_inseguros.items():
        print(f"  {usuario}: {password}")
    
    print(f"\n{Fore.RED}💀 Si alguien accede a tu base de datos:")
    print("   • Ve TODAS las contraseñas inmediatamente")
    print("   • Puede acceder a TODAS las cuentas")
    print(f"   • Los usuarios están completamente expuestos{Style.RESET_ALL}\n")

def demostrar_hash_simple():
    """Demuestra hashing básico (sin salt)"""
    print(f"{Fore.YELLOW}⚠️ HASH SIMPLE (mejor, pero aún inseguro)")
    print(f"{'=' * 45}{Style.RESET_ALL}")
    
    password = "123456"
    
    # Hash SHA-256 simple
    hash_simple = hashlib.sha256(password.encode()).hexdigest()
    
    print(f"Contraseña original: {password}")
    print(f"Hash SHA-256: {hash_simple}")
    
    # Demostrar que el mismo input da el mismo hash
    print(f"\n{Fore.CYAN}🔍 Característica importante:{Style.RESET_ALL}")
    print("El mismo input SIEMPRE produce el mismo hash:")
    
    for i in range(3):
        mismo_hash = hashlib.sha256(password.encode()).hexdigest()
        print(f"  Intento {i+1}: {mismo_hash}")
    
    print(f"\n{Fore.RED}🚨 Problema del hash sin salt:")
    print("   • Ataques de diccionario")
    print("   • Tablas rainbow (hashes precalculados)")
    print(f"   • Patrones visibles si usuarios tienen la misma contraseña{Style.RESET_ALL}\n")

def demostrar_hash_con_salt():
    """Demuestra hashing con salt"""
    print(f"{Fore.GREEN}✅ HASH CON SALT (mucho mejor)")
    print(f"{'=' * 35}{Style.RESET_ALL}")
    
    password = "123456"
    
    # Generar salt aleatorio
    salt = secrets.token_hex(16)  # 32 caracteres hexadecimales
    
    # Combinar password + salt antes del hash
    salted_password = password + salt
    hash_con_salt = hashlib.sha256(salted_password.encode()).hexdigest()
    
    print(f"Contraseña original: {password}")
    print(f"Salt generado: {salt}")
    print(f"Password + Salt: {salted_password}")
    print(f"Hash final: {hash_con_salt}")
    
    print(f"\n{Fore.CYAN}🔍 ¿Qué es el salt?{Style.RESET_ALL}")
    print("• Una cadena aleatoria única para cada contraseña")
    print("• Se almacena junto al hash (no es secreto)")
    print("• Hace que cada hash sea único, incluso para la misma contraseña")
    
    # Demostrar que diferentes salts dan diferentes hashes
    print(f"\n{Fore.GREEN}Mismo password, diferente salt = diferente hash:")
    for i in range(3):
        nuevo_salt = secrets.token_hex(16)
        nuevo_hash = hashlib.sha256((password + nuevo_salt).encode()).hexdigest()
        print(f"  Salt {i+1}: {nuevo_salt[:16]}... -> Hash: {nuevo_hash[:16]}...")
    print(f"{Style.RESET_ALL}")

def demostrar_bcrypt():
    """Demuestra bcrypt - la forma profesional"""
    print(f"{Fore.MAGENTA}🏆 BCRYPT: La Forma Profesional")
    print(f"{'=' * 35}{Style.RESET_ALL}")
    
    password = "mi_contraseña_segura_123!"
    
    print(f"Contraseña a proteger: {password}")
    print(f"\n{Fore.CYAN}🔧 Generando hash con bcrypt...{Style.RESET_ALL}")
    
    # Generar hash con bcrypt (incluye salt automáticamente)
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    print(f"Hash generado: {hashed.decode('utf-8')}")
    
    # Explicar las partes del hash bcrypt
    hash_str = hashed.decode('utf-8')
    print(f"\n{Fore.CYAN}🔍 Anatomía del hash bcrypt:")
    print(f"  $2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print(f"  │  │  │                    │")
    print(f"  │  │  │                    └─ Hash (31 chars)")
    print(f"  │  │  └─ Salt (22 chars)")  
    print(f"  │  └─ Cost factor (rounds = 2^12)")
    print(f"  └─ Versión del algoritmo{Style.RESET_ALL}")
    
    return hashed

def verificar_password(password, hashed):
    """Demuestra cómo verificar una contraseña"""
    print(f"\n{Fore.GREEN}🔓 VERIFICACIÓN DE CONTRASEÑA")
    print(f"{'=' * 30}{Style.RESET_ALL}")
    
    # Probar con la contraseña correcta
    print(f"Probando contraseña: '{password}'")
    es_correcta = bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    if es_correcta:
        print(f"{Fore.GREEN}✅ ¡Contraseña CORRECTA!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Contraseña INCORRECTA{Style.RESET_ALL}")
    
    # Probar con una contraseña incorrecta
    password_incorrecta = "contraseña_equivocada"
    print(f"\nProbando contraseña incorrecta: '{password_incorrecta}'")
    es_correcta = bcrypt.checkpw(password_incorrecta.encode('utf-8'), hashed)
    
    if es_correcta:
        print(f"{Fore.GREEN}✅ ¡Contraseña CORRECTA!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Contraseña INCORRECTA (como esperábamos){Style.RESET_ALL}")

def ejemplo_sistema_autenticacion():
    """Ejemplo completo de un sistema básico de autenticación"""
    print(f"\n{Fore.BLUE}🎯 EJEMPLO PRÁCTICO: Sistema de Autenticación")
    print(f"{'=' * 50}{Style.RESET_ALL}")
    
    class SistemaAutenticacion:
        def __init__(self):
            # Simulamos una base de datos de usuarios
            self.usuarios = {}
        
        def registrar_usuario(self, username, password):
            """Registra un nuevo usuario con contraseña hasheada"""
            if username in self.usuarios:
                return False, "Usuario ya existe"
            
            # Hashear la contraseña con bcrypt
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Guardar en nuestra "base de datos"
            self.usuarios[username] = {
                'password_hash': hashed,
                'created_at': 'now'  # En una app real usarías datetime
            }
            
            return True, "Usuario registrado exitosamente"
        
        def login(self, username, password):
            """Verifica credenciales de login"""
            if username not in self.usuarios:
                return False, "Usuario no encontrado"
            
            stored_hash = self.usuarios[username]['password_hash']
            
            # Verificar contraseña
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return True, "Login exitoso"
            else:
                return False, "Contraseña incorrecta"
    
    # Demostrar el sistema
    auth = SistemaAutenticacion()
    
    print("1. Registrando usuarios...")
    usuarios_demo = [
        ("alice", "password123!"),
        ("bob", "mi_super_secreto"),
        ("charlie", "123456789")
    ]
    
    for username, password in usuarios_demo:
        success, message = auth.registrar_usuario(username, password)
        if success:
            print(f"   ✅ {username}: {message}")
        else:
            print(f"   ❌ {username}: {message}")
    
    print(f"\n2. Base de datos (hashes almacenados):")
    for username, data in auth.usuarios.items():
        hash_preview = data['password_hash'].decode('utf-8')[:30] + "..."
        print(f"   {username}: {hash_preview}")
    
    print(f"\n3. Probando logins:")
    tests = [
        ("alice", "password123!", True),
        ("alice", "password123", False),
        ("bob", "mi_super_secreto", True),
        ("charlie", "wrongpassword", False),
        ("nonexistent", "anything", False)
    ]
    
    for username, password, should_work in tests:
        success, message = auth.login(username, password)
        emoji = "✅" if success else "❌"
        print(f"   {emoji} {username} + '{password}': {message}")

def mejores_practicas():
    """Muestra las mejores prácticas de hashing"""
    print(f"\n{Fore.CYAN}📋 MEJORES PRÁCTICAS")
    print(f"{'=' * 25}{Style.RESET_ALL}")
    
    practices = [
        ("✅ USA bcrypt, scrypt o Argon2", "Son algoritmos diseñados para ser lentos"),
        ("✅ Usa un cost factor apropiado", "bcrypt: 12+ rounds, ajusta según tu hardware"),
        ("❌ NUNCA uses MD5 o SHA1 para passwords", "Son demasiado rápidos y vulnerables"),
        ("❌ NUNCA uses hash sin salt", "Vulnerable a ataques rainbow table"),
        ("✅ Genera salt aleatorio para cada password", "Usa secrets.token_hex() o bcrypt.gensalt()"),
        ("✅ Almacena salt junto con el hash", "No es información secreta"),
        ("❌ NUNCA intentes 'descifrar' un hash", "Los hashes son unidireccionales por diseño"),
        ("✅ Considera usar pepper adicional", "Un secreto adicional almacenado por separado")
    ]
    
    for practice, explanation in practices:
        color = Fore.GREEN if practice.startswith("✅") else Fore.RED
        print(f"{color}{practice}{Style.RESET_ALL}")
        print(f"   └─ {explanation}")

if __name__ == "__main__":
    print_educational_header()
    
    # Ejecutar todas las demostraciones
    demostrar_problema_texto_plano()
    demostrar_hash_simple() 
    demostrar_hash_con_salt()
    hashed_password = demostrar_bcrypt()
    verificar_password("mi_contraseña_segura_123!", hashed_password)
    ejemplo_sistema_autenticacion()
    mejores_practicas()
    
    print(f"\n{Fore.MAGENTA}🎓 ¡Felicitaciones!")
    print("Has aprendido los fundamentos del hashing seguro.")
    print("Este conocimiento es CRÍTICO para cualquier aplicación que maneje usuarios.")
    print(f"\nPróximo paso: Módulo 2 - Validación de Datos{Style.RESET_ALL}")
