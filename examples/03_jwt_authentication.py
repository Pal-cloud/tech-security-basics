"""
🔑 Módulo 3: Autenticación con JSON Web Tokens (JWT)
====================================================

Aprende a implementar autenticación segura usando JWT de forma práctica.
¡Una de las formas más populares de autenticación en aplicaciones modernas!

⚠️ Los JWT deben usarse correctamente para ser seguros!
"""

import jwt
import json
import time
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple, Any
from colorama import init, Fore, Style
import bcrypt

# Inicializar colorama para Windows
init()

def print_educational_header():
    """Muestra información educativa sobre JWT"""
    print(f"\n{Fore.CYAN}🔑 MÓDULO 3: AUTENTICACIÓN CON JWT{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=" * 35)
    print(f"{Fore.GREEN}✅ Lo que aprenderás:")
    print("   • Qué son los JSON Web Tokens y cómo funcionan")
    print("   • Estructura de un JWT (Header, Payload, Signature)")
    print("   • Cómo generar y validar tokens seguros")
    print("   • Mejores prácticas de expiración y renovación")
    print(f"   • Qué información NUNCA incluir en un JWT{Style.RESET_ALL}\n")

def explicar_que_es_jwt():
    """Explica qué es un JWT y por qué se usa"""
    print(f"{Fore.BLUE}🤔 ¿QUÉ ES UN JWT?")
    print(f"{'=' * 20}{Style.RESET_ALL}")
    
    print("JWT = JSON Web Token")
    print("• Es un estándar para transmitir información de forma segura")
    print("• Se usa principalmente para autenticación en APIs")
    print("• Es 'stateless' - no necesita almacenarse en el servidor")
    print("• Permite verificar que el usuario es quien dice ser")
    
    print(f"\n{Fore.CYAN}🏗️ Estructura de un JWT:{Style.RESET_ALL}")
    print("xxxxx.yyyyy.zzzzz")
    print("  │     │     │")
    print("  │     │     └─ Signature (Firma)")
    print("  │     └─ Payload (Datos)")
    print("  └─ Header (Cabecera)")
    
    # Ejemplo de JWT
    jwt_ejemplo = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoianVhbiIsImV4cCI6MTcwNjc4NDAwMH0.abc123def456"
    print(f"\nEjemplo de JWT:")
    print(f"{jwt_ejemplo[:30]}...")
    
    print(f"\n{Fore.GREEN}✅ Ventajas del JWT:")
    print("• No requiere almacenamiento en el servidor (stateless)")
    print("• Puede incluir información del usuario")
    print("• Es estándar y funciona en cualquier plataforma")
    print("• Permite expiración automática")
    
    print(f"\n{Fore.RED}⚠️ Desventajas del JWT:")
    print("• Una vez emitido, no se puede 'revocar' fácilmente")
    print("• El tamaño crece con la información incluida")
    print("• Si se compromete la clave secreta, todos los tokens son vulnerables")
    print(f"• La información es visible (aunque firmada){Style.RESET_ALL}\n")

class JWTManager:
    """Gestor de JWT con funciones de seguridad"""
    
    def __init__(self, secret_key: Optional[str] = None):
        # Generar clave secreta segura si no se proporciona
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = "HS256"
        
        # Configuración de expiración
        self.access_token_expire = timedelta(minutes=15)  # Token corto
        self.refresh_token_expire = timedelta(days=7)     # Token largo
    
    def crear_access_token(self, user_data: Dict[str, Any]) -> str:
        """Crea un token de acceso con expiración corta"""
        now = datetime.now(timezone.utc)
        expire = now + self.access_token_expire
        
        payload = {
            "user_id": user_data.get("user_id"),
            "username": user_data.get("username"),
            "role": user_data.get("role", "user"),
            "iat": now.timestamp(),  # Issued at
            "exp": expire.timestamp(),  # Expiration
            "type": "access"
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def crear_refresh_token(self, user_id: int) -> str:
        """Crea un token de refresco con expiración larga"""
        now = datetime.now(timezone.utc)
        expire = now + self.refresh_token_expire
        
        payload = {
            "user_id": user_id,
            "iat": now.timestamp(),
            "exp": expire.timestamp(),
            "type": "refresh"
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verificar_token(self, token: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """Verifica y decodifica un JWT"""
        try:
            # Decodificar el token
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            
            return True, payload, "Token válido"
            
        except jwt.ExpiredSignatureError:
            return False, None, "Token expirado"
        
        except jwt.InvalidTokenError as e:
            return False, None, f"Token inválido: {str(e)}"
        
        except Exception as e:
            return False, None, f"Error verificando token: {str(e)}"
    
    def decodificar_sin_verificar(self, token: str) -> Dict[str, Any]:
        """Decodifica un JWT sin verificar (solo para propósitos educativos)"""
        try:
            # ADVERTENCIA: Esto es inseguro, solo para demostración
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded
        except Exception as e:
            return {"error": str(e)}

def demostrar_creacion_jwt():
    """Demuestra cómo crear JWTs"""
    print(f"{Fore.GREEN}✅ CREANDO JWTs")
    print(f"{'=' * 20}{Style.RESET_ALL}")
    
    jwt_manager = JWTManager()
    
    # Datos del usuario
    user_data = {
        "user_id": 123,
        "username": "juan_perez",
        "role": "admin"
    }
    
    print("Datos del usuario:")
    for key, value in user_data.items():
        print(f"  {key}: {value}")
    
    # Crear tokens
    access_token = jwt_manager.crear_access_token(user_data)
    refresh_token = jwt_manager.crear_refresh_token(user_data["user_id"])
    
    print(f"\n🎫 Access Token (15 minutos):")
    print(f"{access_token[:50]}...")
    
    print(f"\n🎫 Refresh Token (7 días):")
    print(f"{refresh_token[:50]}...")
    
    # Mostrar qué contiene cada token (sin verificar firma)
    print(f"\n{Fore.CYAN}🔍 Contenido del Access Token:{Style.RESET_ALL}")
    access_payload = jwt_manager.decodificar_sin_verificar(access_token)
    for key, value in access_payload.items():
        if key in ['iat', 'exp']:
            # Convertir timestamp a fecha legible
            fecha = datetime.fromtimestamp(value, tz=timezone.utc)
            print(f"  {key}: {value} ({fecha.strftime('%Y-%m-%d %H:%M:%S UTC')})")
        else:
            print(f"  {key}: {value}")
    
    return jwt_manager, access_token, refresh_token

def demostrar_verificacion_jwt():
    """Demuestra cómo verificar JWTs"""
    print(f"\n{Fore.BLUE}🔍 VERIFICANDO JWTs")
    print(f"{'=' * 20}{Style.RESET_ALL}")
    
    jwt_manager = JWTManager()
    
    # Crear un token válido
    user_data = {"user_id": 456, "username": "ana_garcia", "role": "user"}
    token_valido = jwt_manager.crear_access_token(user_data)
    
    # Casos de prueba
    casos_prueba = [
        ("Token válido", token_valido),
        ("Token malformado", "esto.no.es.un.jwt"),
        ("Token con firma incorrecta", token_valido[:-10] + "1234567890"),
        ("Token sin partes", "token_incompleto")
    ]
    
    for descripcion, token in casos_prueba:
        print(f"\nProbando: {descripcion}")
        es_valido, payload, mensaje = jwt_manager.verificar_token(token)
        
        if es_valido:
            print(f"  {Fore.GREEN}✅ {mensaje}{Style.RESET_ALL}")
            print(f"  Usuario: {payload.get('username')}")
            print(f"  Rol: {payload.get('role')}")
        else:
            print(f"  {Fore.RED}❌ {mensaje}{Style.RESET_ALL}")

def simular_token_expirado():
    """Simula un token expirado para demostración"""
    print(f"\n{Fore.YELLOW}⏰ SIMULANDO TOKEN EXPIRADO")
    print(f"{'=' * 30}{Style.RESET_ALL}")
    
    jwt_manager = JWTManager()
    
    # Crear token con expiración de 1 segundo
    now = datetime.now(timezone.utc)
    expire = now + timedelta(seconds=1)
    
    payload = {
        "user_id": 789,
        "username": "test_user",
        "iat": now.timestamp(),
        "exp": expire.timestamp(),
        "type": "access"
    }
    
    token_corto = jwt.encode(payload, jwt_manager.secret_key, algorithm="HS256")
    
    print("Token creado con expiración de 1 segundo...")
    print(f"Token: {token_corto[:30]}...")
    
    # Verificar inmediatamente (debería ser válido)
    print(f"\n⏰ Verificando inmediatamente:")
    es_valido, payload_decoded, mensaje = jwt_manager.verificar_token(token_corto)
    emoji = "✅" if es_valido else "❌"
    print(f"  {emoji} {mensaje}")
    
    # Esperar 2 segundos
    print(f"\n⏰ Esperando 2 segundos...")
    time.sleep(2)
    
    # Verificar después de expirar (debería fallar)
    print(f"⏰ Verificando después de expirar:")
    es_valido, payload_decoded, mensaje = jwt_manager.verificar_token(token_corto)
    emoji = "✅" if es_valido else "❌"
    print(f"  {emoji} {mensaje}")

class SistemaAutenticacionJWT:
    """Sistema completo de autenticación con JWT"""
    
    def __init__(self):
        self.jwt_manager = JWTManager()
        self.usuarios = {}  # Simulamos una base de datos
        self.refresh_tokens = {}  # Almacenar refresh tokens válidos
    
    def registrar_usuario(self, username: str, password: str, role: str = "user") -> Tuple[bool, str]:
        """Registra un nuevo usuario"""
        if username in self.usuarios:
            return False, "Usuario ya existe"
        
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_id = len(self.usuarios) + 1
        self.usuarios[username] = {
            "user_id": user_id,
            "password_hash": hashed_password,
            "role": role
        }
        
        return True, f"Usuario {username} registrado exitosamente"
    
    def login(self, username: str, password: str) -> Tuple[bool, Optional[Dict[str, str]], str]:
        """Procesa login y genera tokens JWT"""
        # Verificar usuario existe
        if username not in self.usuarios:
            return False, None, "Usuario no encontrado"
        
        user_data = self.usuarios[username]
        
        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash']):
            return False, None, "Contraseña incorrecta"
        
        # Crear tokens
        user_info = {
            "user_id": user_data["user_id"],
            "username": username,
            "role": user_data["role"]
        }
        
        access_token = self.jwt_manager.crear_access_token(user_info)
        refresh_token = self.jwt_manager.crear_refresh_token(user_data["user_id"])
        
        # Guardar refresh token
        self.refresh_tokens[user_data["user_id"]] = refresh_token
        
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        
        return True, tokens, "Login exitoso"
    
    def verificar_acceso(self, token: str, required_role: Optional[str] = None) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """Verifica token y permisos de acceso"""
        es_valido, payload, mensaje = self.jwt_manager.verificar_token(token)
        
        if not es_valido:
            return False, None, mensaje
        
        # Verificar que es un access token
        if payload.get("type") != "access":
            return False, None, "Token no es de tipo access"
        
        # Verificar rol si se requiere
        if required_role and payload.get("role") != required_role:
            return False, None, f"Rol insuficiente. Se requiere: {required_role}"
        
        return True, payload, "Acceso autorizado"
    
    def refresh_access_token(self, refresh_token: str) -> Tuple[bool, Optional[str], str]:
        """Genera nuevo access token usando refresh token"""
        es_valido, payload, mensaje = self.jwt_manager.verificar_token(refresh_token)
        
        if not es_valido:
            return False, None, mensaje
        
        # Verificar que es refresh token
        if payload.get("type") != "refresh":
            return False, None, "Token no es de tipo refresh"
        
        user_id = payload.get("user_id")
        
        # Verificar que el refresh token está en nuestro registro
        if user_id not in self.refresh_tokens or self.refresh_tokens[user_id] != refresh_token:
            return False, None, "Refresh token inválido"
        
        # Encontrar datos del usuario
        user_data = None
        for username, data in self.usuarios.items():
            if data["user_id"] == user_id:
                user_data = {
                    "user_id": user_id,
                    "username": username,
                    "role": data["role"]
                }
                break
        
        if not user_data:
            return False, None, "Usuario no encontrado"
        
        # Generar nuevo access token
        nuevo_access_token = self.jwt_manager.crear_access_token(user_data)
        
        return True, nuevo_access_token, "Token renovado exitosamente"

def demostrar_sistema_completo():
    """Demuestra el sistema de autenticación completo"""
    print(f"\n{Fore.MAGENTA}🎯 SISTEMA DE AUTENTICACIÓN COMPLETO")
    print(f"{'=' * 40}{Style.RESET_ALL}")
    
    sistema = SistemaAutenticacionJWT()
    
    # 1. Registrar usuarios
    print("1. Registrando usuarios...")
    usuarios = [
        ("admin", "admin123!", "admin"),
        ("usuario1", "password123", "user"),
        ("usuario2", "mypassword", "user")
    ]
    
    for username, password, role in usuarios:
        success, message = sistema.registrar_usuario(username, password, role)
        emoji = "✅" if success else "❌"
        print(f"   {emoji} {username}: {message}")
    
    # 2. Intentos de login
    print(f"\n2. Intentos de login...")
    intentos_login = [
        ("admin", "admin123!"),  # Válido
        ("usuario1", "password123"),  # Válido
        ("usuario1", "wrongpassword"),  # Contraseña incorrecta
        ("noexiste", "password")  # Usuario no existe
    ]
    
    tokens_validos = {}
    
    for username, password in intentos_login:
        success, tokens, message = sistema.login(username, password)
        emoji = "✅" if success else "❌"
        print(f"   {emoji} {username}: {message}")
        
        if success:
            tokens_validos[username] = tokens
            print(f"      Access Token: {tokens['access_token'][:30]}...")
    
    # 3. Verificar acceso con diferentes permisos
    print(f"\n3. Verificando acceso...")
    if "admin" in tokens_validos:
        admin_token = tokens_validos["admin"]["access_token"]
        
        # Acceso normal
        success, payload, message = sistema.verificar_acceso(admin_token)
        print(f"   ✅ Acceso normal admin: {message}")
        
        # Acceso que requiere rol admin
        success, payload, message = sistema.verificar_acceso(admin_token, required_role="admin")
        print(f"   ✅ Acceso admin requerido: {message}")
    
    if "usuario1" in tokens_validos:
        user_token = tokens_validos["usuario1"]["access_token"]
        
        # Acceso normal
        success, payload, message = sistema.verificar_acceso(user_token)
        print(f"   ✅ Acceso normal usuario: {message}")
        
        # Acceso que requiere rol admin (debería fallar)
        success, payload, message = sistema.verificar_acceso(user_token, required_role="admin")
        emoji = "✅" if success else "❌"
        print(f"   {emoji} Usuario intentando acceso admin: {message}")
    
    # 4. Demostrar refresh token
    if "usuario1" in tokens_validos:
        refresh_token = tokens_validos["usuario1"]["refresh_token"]
        print(f"\n4. Renovando access token...")
        
        success, new_token, message = sistema.refresh_access_token(refresh_token)
        if success:
            print(f"   ✅ {message}")
            print(f"   Nuevo token: {new_token[:30]}...")
        else:
            print(f"   ❌ {message}")

def mejores_practicas_jwt():
    """Muestra las mejores prácticas de JWT"""
    print(f"\n{Fore.CYAN}📋 MEJORES PRÁCTICAS JWT")
    print(f"{'=' * 30}{Style.RESET_ALL}")
    
    practices = [
        ("✅ Usa tokens de vida corta", "15-60 minutos para access tokens"),
        ("✅ Implementa refresh tokens", "Para renovar sin reautenticarse"),
        ("✅ Usa HTTPS siempre", "Los JWT viajan por la red"),
        ("✅ Almacena secretos seguros", "Usa variables de entorno"),
        ("❌ NO pongas info sensible en payload", "Es visible sin la clave"),
        ("✅ Valida SIEMPRE la firma", "No confíes en tokens sin verificar"),
        ("✅ Implementa logout con blacklist", "Para revocar tokens si es necesario"),
        ("❌ NO uses algoritmo 'none'", "Permite bypass de verificación"),
        ("✅ Rota las claves secretas", "Especialmente si se comprometen"),
        ("✅ Loguea intentos de tokens inválidos", "Para detectar ataques")
    ]
    
    for practice, explanation in practices:
        color = Fore.GREEN if practice.startswith("✅") else Fore.RED
        print(f"{color}{practice}{Style.RESET_ALL}")
        print(f"   └─ {explanation}")

if __name__ == "__main__":
    print_educational_header()
    
    # Ejecutar todas las demostraciones
    explicar_que_es_jwt()
    jwt_manager, access_token, refresh_token = demostrar_creacion_jwt()
    demostrar_verificacion_jwt()
    simular_token_expirado()
    demostrar_sistema_completo()
    mejores_practicas_jwt()
    
    print(f"\n{Fore.MAGENTA}🎓 ¡Felicitaciones!")
    print("Ahora entiendes cómo funciona la autenticación JWT.")
    print("Este conocimiento es fundamental para APIs modernas.")
    print(f"\nPróximo paso: Módulo 4 - Logging de Seguridad{Style.RESET_ALL}")
