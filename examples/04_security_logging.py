"""
📝 Módulo 4: Logging de Seguridad
==================================

Aprende a implementar logging de seguridad para detectar y responder
a amenazas. ¡Los logs son fundamentales para la seguridad!

⚠️ NUNCA logees información sensible como contraseñas o tokens completos!
"""

import logging
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pathlib import Path
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init()

def print_educational_header():
    """Muestra información educativa sobre logging de seguridad"""
    print(f"\n{Fore.CYAN}📝 MÓDULO 4: LOGGING DE SEGURIDAD{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=" * 35)
    print(f"{Fore.GREEN}✅ Lo que aprenderás:")
    print("   • Por qué el logging es crítico para la seguridad")
    print("   • Qué eventos de seguridad registrar")
    print("   • Cómo estructurar logs para análisis")
    print("   • Qué información NUNCA logear")
    print(f"   • Detectar patrones de ataques en logs{Style.RESET_ALL}\n")

class SecurityLogger:
    """Logger especializado en eventos de seguridad"""
    
    def __init__(self, log_file: str = "logs/security.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Configurar logger
        self.logger = logging.getLogger("security")
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicados si ya está configurado
        if not self.logger.handlers:
            # Handler para archivo
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            
            # Handler para consola
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                f'{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - '
                f'{Fore.YELLOW}%(levelname)s{Style.RESET_ALL} - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def _create_log_entry(self, event_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una entrada de log estructurada"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
            "source": "security_system"
        }
    
    def _hash_sensitive_data(self, data: str) -> str:
        """Hashea datos sensibles para logging seguro"""
        return hashlib.sha256(data.encode()).hexdigest()[:8] + "..."
    
    def log_login_attempt(self, username: str, success: bool, ip_address: str = "127.0.0.1"):
        """Registra intento de login"""
        details = {
            "username": username,
            "success": success,
            "ip_address": ip_address,
            "user_agent": "example-browser"  # En una app real vendría del request
        }
        
        log_entry = self._create_log_entry("login_attempt", details)
        
        if success:
            self.logger.info(f"LOGIN_SUCCESS: {json.dumps(log_entry)}")
        else:
            self.logger.warning(f"LOGIN_FAILED: {json.dumps(log_entry)}")
    
    def log_permission_denied(self, username: str, resource: str, action: str):
        """Registra intento de acceso denegado"""
        details = {
            "username": username,
            "resource": resource,
            "action": action,
            "result": "DENIED"
        }
        
        log_entry = self._create_log_entry("permission_denied", details)
        self.logger.warning(f"PERMISSION_DENIED: {json.dumps(log_entry)}")
    
    def log_suspicious_activity(self, description: str, details: Dict[str, Any]):
        """Registra actividad sospechosa"""
        log_details = {
            "description": description,
            **details
        }
        
        log_entry = self._create_log_entry("suspicious_activity", log_details)
        self.logger.error(f"SUSPICIOUS_ACTIVITY: {json.dumps(log_entry)}")
    
    def log_data_access(self, username: str, data_type: str, operation: str):
        """Registra acceso a datos sensibles"""
        details = {
            "username": username,
            "data_type": data_type,
            "operation": operation
        }
        
        log_entry = self._create_log_entry("data_access", details)
        self.logger.info(f"DATA_ACCESS: {json.dumps(log_entry)}")
    
    def log_config_change(self, username: str, config_item: str, old_value: str, new_value: str):
        """Registra cambios de configuración"""
        details = {
            "username": username,
            "config_item": config_item,
            "old_value_hash": self._hash_sensitive_data(old_value),
            "new_value_hash": self._hash_sensitive_data(new_value)
        }
        
        log_entry = self._create_log_entry("config_change", details)
        self.logger.warning(f"CONFIG_CHANGE: {json.dumps(log_entry)}")

def demostrar_que_no_logear():
    """Demuestra qué información NO se debe logear"""
    print(f"{Fore.RED}🚫 QUÉ NO LOGEAR NUNCA")
    print(f"{'=' * 25}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}❌ Información que NUNCA debes logear:")
    peligrosos = [
        "Contraseñas completas",
        "Tokens JWT completos", 
        "Números de tarjetas de crédito",
        "Claves API completas",
        "Información médica personal",
        "Datos bancarios",
        "Secretos de aplicación"
    ]
    
    for item in peligrosos:
        print(f"   • {item}")
    
    print(f"\n{Fore.GREEN}✅ Alternativas seguras:")
    alternativas = [
        ("Contraseña", "Hash de la contraseña o solo indicar éxito/fallo"),
        ("Token JWT", "Solo los primeros 8 caracteres + '...'"),
        ("Email", "Solo el dominio o hash"),
        ("IP Address", "Los primeros 3 octetos: 192.168.1.xxx"),
        ("Datos sensibles", "Hash SHA-256 truncado")
    ]
    
    for dato, alternativa in alternativas:
        print(f"   • {dato}: {alternativa}")

def simular_eventos_seguridad():
    """Simula varios eventos de seguridad"""
    print(f"\n{Fore.BLUE}🎭 SIMULANDO EVENTOS DE SEGURIDAD")
    print(f"{'=' * 35}{Style.RESET_ALL}")
    
    logger = SecurityLogger()
    
    print("Generando eventos de ejemplo...")
    
    # 1. Logins exitosos y fallidos
    print(f"\n1. {Fore.GREEN}Intentos de login:{Style.RESET_ALL}")
    logins = [
        ("juan_perez", True, "192.168.1.100"),
        ("ana_garcia", True, "192.168.1.105"),
        ("atacante", False, "10.0.0.1"),
        ("atacante", False, "10.0.0.1"),
        ("atacante", False, "10.0.0.1"),  # Múltiples intentos fallidos
        ("admin", False, "192.168.1.200")
    ]
    
    for username, success, ip in logins:
        logger.log_login_attempt(username, success, ip)
    
    # 2. Accesos denegados
    print(f"\n2. {Fore.YELLOW}Accesos denegados:{Style.RESET_ALL}")
    denials = [
        ("user_normal", "/admin/config", "READ"),
        ("guest_user", "/api/users", "DELETE"),
        ("juan_perez", "/admin/logs", "WRITE")
    ]
    
    for username, resource, action in denials:
        logger.log_permission_denied(username, resource, action)
    
    # 3. Actividades sospechosas
    print(f"\n3. {Fore.RED}Actividades sospechosas:{Style.RESET_ALL}")
    suspicious = [
        ("Múltiples intentos de SQL injection", {
            "ip_address": "10.0.0.1",
            "attempts": 15,
            "payload_detected": "'; DROP TABLE users; --"
        }),
        ("Acceso fuera de horario laboral", {
            "username": "empleado_x",
            "time": "03:00 AM",
            "unusual": True
        }),
        ("Descarga masiva de archivos", {
            "username": "contractor_temp",
            "files_downloaded": 500,
            "size_mb": 2048
        })
    ]
    
    for description, details in suspicious:
        logger.log_suspicious_activity(description, details)
    
    # 4. Acceso a datos sensibles
    print(f"\n4. {Fore.MAGENTA}Acceso a datos:{Style.RESET_ALL}")
    data_access = [
        ("hr_manager", "employee_salaries", "READ"),
        ("doctor_smith", "patient_records", "UPDATE"),
        ("finance_user", "accounting_data", "EXPORT")
    ]
    
    for username, data_type, operation in data_access:
        logger.log_data_access(username, data_type, operation)
    
    print(f"\n📄 Todos los eventos se han guardado en: {logger.log_file}")

class AttackDetector:
    """Detector de patrones de ataque en logs"""
    
    def __init__(self):
        self.login_attempts = {}  # Contador de intentos por IP
        self.failed_logins = {}   # Contador de fallos por usuario
    
    def analyze_login_pattern(self, username: str, ip_address: str, success: bool):
        """Analiza patrones de login para detectar ataques"""
        
        # Contar intentos por IP
        if ip_address not in self.login_attempts:
            self.login_attempts[ip_address] = {"total": 0, "failed": 0}
        
        self.login_attempts[ip_address]["total"] += 1
        
        if not success:
            self.login_attempts[ip_address]["failed"] += 1
            
            # Contar fallos por usuario
            if username not in self.failed_logins:
                self.failed_logins[username] = 0
            self.failed_logins[username] += 1
        
        # Detectar patrones sospechosos
        alerts = []
        
        # Alerta: Muchos fallos desde una IP
        if self.login_attempts[ip_address]["failed"] >= 5:
            alerts.append(f"🚨 BRUTE FORCE: IP {ip_address} tiene {self.login_attempts[ip_address]['failed']} intentos fallidos")
        
        # Alerta: Muchos fallos para un usuario
        if username in self.failed_logins and self.failed_logins[username] >= 3:
            alerts.append(f"🚨 TARGETED ATTACK: Usuario '{username}' tiene {self.failed_logins[username]} intentos fallidos")
        
        return alerts

def demostrar_deteccion_ataques():
    """Demuestra detección automática de ataques"""
    print(f"\n{Fore.RED}🔍 DETECCIÓN DE ATAQUES")
    print(f"{'=' * 25}{Style.RESET_ALL}")
    
    detector = AttackDetector()
    logger = SecurityLogger()
    
    # Simular un ataque de fuerza bruta
    print("Simulando ataque de fuerza bruta...")
    
    ataques = [
        # Ataque de fuerza bruta desde misma IP
        ("admin", "192.168.1.200", False),
        ("admin", "192.168.1.200", False), 
        ("admin", "192.168.1.200", False),
        ("admin", "192.168.1.200", False),
        ("admin", "192.168.1.200", False),
        ("admin", "192.168.1.200", True),   # Finalmente lo logra
        
        # Ataque dirigido a múltiples usuarios desde misma IP
        ("user1", "10.0.0.5", False),
        ("user2", "10.0.0.5", False),
        ("user3", "10.0.0.5", False),
        ("admin", "10.0.0.5", False),
        ("root", "10.0.0.5", False),
        
        # Login normal
        ("juan_perez", "192.168.1.100", True)
    ]
    
    for username, ip, success in ataques:
        # Logear el evento
        logger.log_login_attempt(username, success, ip)
        
        # Analizar patrón
        alerts = detector.analyze_login_pattern(username, ip, success)
        
        # Mostrar alertas
        for alert in alerts:
            print(f"  {alert}")
            # En un sistema real, aquí activarías contramedidas
            # como bloquear IP, alertar administradores, etc.

def mejores_practicas_logging():
    """Muestra las mejores prácticas de logging de seguridad"""
    print(f"\n{Fore.CYAN}📋 MEJORES PRÁCTICAS DE LOGGING")
    print(f"{'=' * 35}{Style.RESET_ALL}")
    
    practices = [
        ("✅ Loguea todos los eventos de seguridad", "Login, logout, acceso denegado, cambios"),
        ("✅ Usa formato estructurado (JSON)", "Facilita análisis automatizado"),
        ("✅ Incluye timestamp con timezone", "Para correlación temporal"),
        ("✅ Registra dirección IP del origen", "Para identificar fuentes de ataque"),
        ("❌ NUNCA logees contraseñas o tokens", "Información sensible debe protegerse"),
        ("✅ Usa niveles de log apropiados", "INFO, WARNING, ERROR, CRITICAL"),
        ("✅ Rota logs regularmente", "Para evitar archivos enormes"),
        ("✅ Protege archivos de log", "Permisos restrictivos, backup seguro"),
        ("✅ Implementa alertas en tiempo real", "Para respuesta rápida a amenazas"),
        ("✅ Archiva logs a largo plazo", "Para análisis forense y compliance")
    ]
    
    for practice, explanation in practices:
        color = Fore.GREEN if practice.startswith("✅") else Fore.RED
        print(f"{color}{practice}{Style.RESET_ALL}")
        print(f"   └─ {explanation}")

def mostrar_ejemplo_log_file():
    """Muestra cómo se ve un archivo de log"""
    print(f"\n{Fore.MAGENTA}📄 EJEMPLO DE ARCHIVO DE LOG")
    print(f"{'=' * 30}{Style.RESET_ALL}")
    
    log_file = Path("logs/security.log")
    
    if log_file.exists():
        print(f"Contenido de {log_file}:")
        print("-" * 50)
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Mostrar las últimas 10 líneas
                for line in lines[-10:]:
                    print(line.rstrip())
        except Exception as e:
            print(f"Error leyendo log: {e}")
        print("-" * 50)
    else:
        print("No se encontró archivo de log. Ejecuta los ejemplos primero.")

if __name__ == "__main__":
    print_educational_header()
    
    # Ejecutar todas las demostraciones
    demostrar_que_no_logear()
    simular_eventos_seguridad()
    demostrar_deteccion_ataques()
    mostrar_ejemplo_log_file()
    mejores_practicas_logging()
    
    print(f"\n{Fore.MAGENTA}🎓 ¡Excelente trabajo!")
    print("Ahora sabes cómo implementar logging de seguridad efectivo.")
    print("Los logs son fundamentales para detectar y responder a amenazas.")
    print(f"\nPróximo paso: Módulo 5 - Aspectos Legales (GDPR){Style.RESET_ALL}")
