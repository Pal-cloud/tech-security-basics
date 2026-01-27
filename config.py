"""
Configuración central para el proyecto Tech Security Basics
"""
import os
from pathlib import Path

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent
MODULES_DIR = PROJECT_ROOT / "modules"
EXAMPLES_DIR = PROJECT_ROOT / "examples"
TESTS_DIR = PROJECT_ROOT / "tests"
LOGS_DIR = PROJECT_ROOT / "logs"

# Crear directorios si no existen
LOGS_DIR.mkdir(exist_ok=True)

# Configuración de seguridad
SECURITY_CONFIG = {
    "hash_algorithm": "SHA-256",
    "salt_length": 32,
    "jwt_algorithm": "HS256",
    "session_timeout": 3600,  # 1 hora en segundos
    "max_login_attempts": 3,
    "password_min_length": 8
}

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": LOGS_DIR / "security.log",
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5
}

# Mensajes educativos
EDUCATIONAL_MESSAGES = {
    "password_hash": "🔐 Siempre usa hash + salt para contraseñas. Nunca las almacenes en texto plano.",
    "jwt_security": "🎫 Los JWT deben tener expiración corta y secretos seguros.",
    "input_validation": "🛡️ Valida TODOS los datos de entrada para prevenir inyecciones.",
    "https_only": "🔒 En producción, usa SIEMPRE HTTPS para datos sensibles.",
    "gdpr_compliance": "⚖️ Respeta la privacidad: pide consentimiento, permite borrado.",
    "logging_security": "📝 Nunca logees información sensible (contraseñas, tokens, etc.)"
}

# Variables de entorno (para desarrollo)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-production-please!")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///security_demo.db")

# Validación de configuración
def validate_config():
    """Valida que la configuración sea segura para desarrollo"""
    warnings = []
    
    if SECRET_KEY == "dev-key-change-in-production-please!":
        warnings.append("⚠️ Usando SECRET_KEY por defecto. Cámbiala en producción!")
    
    if len(SECRET_KEY) < 32:
        warnings.append("⚠️ SECRET_KEY muy corta. Usa al menos 32 caracteres.")
    
    return warnings

if __name__ == "__main__":
    print("🔧 Configuración de Tech Security Basics")
    print(f"📁 Directorio del proyecto: {PROJECT_ROOT}")
    
    warnings = validate_config()
    if warnings:
        print("\n⚠️ Advertencias de configuración:")
        for warning in warnings:
            print(f"  {warning}")
    else:
        print("✅ Configuración básica correcta")
