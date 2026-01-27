"""
🚨 Módulo 6: Mejores Prácticas y Checklist de Seguridad
=======================================================

Consolida todo lo aprendido con una guía práctica de mejores prácticas
y un checklist de seguridad que puedes usar en tus proyectos reales.

🎯 ¡Tu hoja de ruta para desarrollo seguro!
"""

import json
import subprocess
import sys
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init()

def print_educational_header():
    """Muestra información educativa sobre mejores prácticas"""
    print(f"\n{Fore.CYAN}🚨 MÓDULO 6: MEJORES PRÁCTICAS Y CHECKLIST DE SEGURIDAD{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=" * 60)
    print(f"{Fore.GREEN}✅ Lo que consolidarás:")
    print("   • Checklist completo de seguridad para desarrollo")
    print("   • Herramientas automatizadas para auditar código")
    print("   • Configuración segura de entornos")
    print("   • Plan de respuesta a incidentes")
    print(f"   • Recursos para seguir aprendiendo{Style.RESET_ALL}\n")

class SecurityChecker:
    """Auditor automático de seguridad para proyectos"""
    
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.findings = []
    
    def add_finding(self, severity: str, category: str, message: str, fix: str):
        """Agrega un hallazgo de seguridad"""
        self.findings.append({
            "severity": severity,
            "category": category, 
            "message": message,
            "fix": fix,
            "timestamp": datetime.now().isoformat()
        })
        
        if severity in ["HIGH", "CRITICAL"]:
            self.checks_failed += 1
        else:
            self.checks_passed += 1
    
    def check_file_permissions(self, file_path: Path) -> bool:
        """Verifica permisos de archivos sensibles"""
        try:
            # En Windows esto es limitado, pero en Linux/Mac sería más útil
            if file_path.exists():
                stat_info = file_path.stat()
                # En un sistema real, verificarías permisos específicos
                self.add_finding(
                    "INFO", "File Permissions", 
                    f"Archivo {file_path.name} encontrado",
                    "Verificar permisos manualmente en producción"
                )
                return True
        except Exception as e:
            self.add_finding(
                "LOW", "File Permissions",
                f"Error verificando {file_path}: {e}",
                "Verificar acceso al archivo"
            )
        return False
    
    def check_hardcoded_secrets(self, file_path: Path) -> List[Dict[str, Any]]:
        """Busca secretos hardcodeados en archivos"""
        secrets_found = []
        
        if not file_path.exists() or file_path.suffix not in ['.py', '.js', '.json']:
            return secrets_found
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Patrones comunes de secretos (básico)
            suspicious_patterns = [
                ("password", "PASSWORD"),
                ("secret", "SECRET"),
                ("api_key", "API_KEY"),
                ("token", "TOKEN"),
                ("private_key", "PRIVATE_KEY")
            ]
            
            for pattern, description in suspicious_patterns:
                if pattern in content.lower():
                    # Verificar que no sea solo un comentario o variable vacía
                    if f'{pattern} =' in content.lower() or f'"{pattern}"' in content.lower():
                        secrets_found.append({
                            "file": str(file_path),
                            "pattern": pattern,
                            "description": description
                        })
                        
                        self.add_finding(
                            "HIGH", "Hardcoded Secrets",
                            f"Posible secreto hardcodeado en {file_path.name}: {pattern}",
                            "Mover a variables de entorno o configuración externa"
                        )
        except Exception as e:
            self.add_finding(
                "LOW", "Code Analysis",
                f"Error analizando {file_path}: {e}",
                "Verificar sintaxis del archivo"
            )
        
        return secrets_found
    
    def check_dependencies(self) -> List[str]:
        """Verifica dependencias conocidas por vulnerabilidades"""
        requirements_file = Path("requirements.txt")
        vulnerable_packages = []
        
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    deps = f.read()
                
                # Lista básica de paquetes con vulnerabilidades conocidas (ejemplo)
                known_vulnerable = [
                    ("django<3.0", "Múltiples vulnerabilidades"),
                    ("flask<1.0", "Vulnerabilidades XSS"),
                    ("requests<2.20", "Vulnerabilidad SSL"),
                ]
                
                for vuln_pattern, description in known_vulnerable:
                    if vuln_pattern.split('<')[0] in deps:
                        vulnerable_packages.append(vuln_pattern)
                        self.add_finding(
                            "MEDIUM", "Vulnerable Dependencies",
                            f"Dependencia potencialmente vulnerable: {vuln_pattern}",
                            f"Actualizar: {description}"
                        )
            except Exception as e:
                self.add_finding(
                    "LOW", "Dependencies",
                    f"Error leyendo requirements.txt: {e}",
                    "Verificar formato del archivo"
                )
        
        return vulnerable_packages
    
    def generate_report(self) -> str:
        """Genera reporte de seguridad"""
        total_checks = self.checks_passed + self.checks_failed
        
        report = f"""
🔍 REPORTE DE AUDITORÍA DE SEGURIDAD
{'=' * 40}

📊 Resumen:
   • Verificaciones realizadas: {total_checks}
   • Exitosas: {self.checks_passed}
   • Fallidas: {self.checks_failed}
   • Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📋 Hallazgos por Severidad:
"""
        
        # Contar por severidad
        severity_counts = {}
        for finding in self.findings:
            sev = finding["severity"]
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        for severity, count in severity_counts.items():
            color = {
                "CRITICAL": Fore.RED,
                "HIGH": Fore.RED, 
                "MEDIUM": Fore.YELLOW,
                "LOW": Fore.BLUE,
                "INFO": Fore.GREEN
            }.get(severity, Fore.WHITE)
            
            report += f"   • {color}{severity}{Style.RESET_ALL}: {count}\n"
        
        report += f"\n📝 Detalles de Hallazgos:\n"
        
        for i, finding in enumerate(self.findings, 1):
            color = {
                "CRITICAL": Fore.RED,
                "HIGH": Fore.RED, 
                "MEDIUM": Fore.YELLOW,
                "LOW": Fore.BLUE,
                "INFO": Fore.GREEN
            }.get(finding["severity"], Fore.WHITE)
            
            report += f"""
{i}. [{color}{finding['severity']}{Style.RESET_ALL}] {finding['category']}
   Problema: {finding['message']}
   Solución: {finding['fix']}
"""
        
        return report

def security_checklist():
    """Muestra checklist completo de seguridad"""
    print(f"{Fore.MAGENTA}📋 CHECKLIST DE SEGURIDAD COMPLETO")
    print(f"{'=' * 35}{Style.RESET_ALL}")
    
    categories = {
        "🔐 Autenticación y Autorización": [
            "✅ Usar hash + salt para contraseñas (bcrypt, Argon2)",
            "✅ Implementar autenticación multifactor (2FA/MFA)", 
            "✅ Usar tokens JWT con expiración corta",
            "✅ Implementar logout seguro",
            "✅ Validar permisos en CADA request",
            "❌ NO hardcodear credenciales",
            "❌ NO usar algoritmos débiles (MD5, SHA1 para passwords)"
        ],
        
        "🛡️ Validación de Datos": [
            "✅ Validar TODOS los datos de entrada",
            "✅ Usar consultas parametrizadas (prevenir SQL injection)",
            "✅ Escapar output HTML (prevenir XSS)",
            "✅ Validar tipos de archivo en uploads",
            "✅ Implementar rate limiting",
            "❌ NO confiar en validación client-side",
            "❌ NO usar eval() con datos del usuario"
        ],
        
        "🔒 Criptografía y Datos": [
            "✅ Cifrar datos sensibles en reposo",
            "✅ Usar HTTPS para TODO el tráfico",
            "✅ Generar claves criptográficas seguras",
            "✅ Rotar claves regularmente",
            "✅ Usar bibliotecas criptográficas establecidas",
            "❌ NO implementar tu propia criptografía",
            "❌ NO almacenar claves con los datos"
        ],
        
        "📝 Logging y Monitoreo": [
            "✅ Logear eventos de seguridad críticos",
            "✅ Monitorear intentos de login fallidos",
            "✅ Implementar alertas automatizadas",
            "✅ Proteger archivos de log",
            "✅ Mantener logs durante tiempo apropiado",
            "❌ NO logear información sensible",
            "❌ NO ignorar alertas de seguridad"
        ],
        
        "⚖️ Cumplimiento Legal": [
            "✅ Implementar consentimiento para cookies",
            "✅ Proporcionar formas de exportar/borrar datos",
            "✅ Documentar procesamiento de datos",
            "✅ Minimizar recolección de datos",
            "✅ Informar breaches dentro del tiempo legal",
            "❌ NO recoger datos sin base legal",
            "❌ NO retener datos indefinidamente"
        ],
        
        "🔧 Configuración y Despliegue": [
            "✅ Usar variables de entorno para secretos",
            "✅ Mantener software actualizado",
            "✅ Configurar firewalls apropiadamente",
            "✅ Desactivar servicios innecesarios",
            "✅ Hacer backups seguros regulares",
            "❌ NO usar configuraciones por defecto",
            "❌ NO exponer información del sistema"
        ]
    }
    
    for category, items in categories.items():
        print(f"\n{Fore.CYAN}{category}{Style.RESET_ALL}")
        for item in items:
            color = Fore.GREEN if item.startswith("✅") else Fore.RED
            print(f"  {color}{item}{Style.RESET_ALL}")

def run_security_audit():
    """Ejecuta auditoría de seguridad automática"""
    print(f"\n{Fore.BLUE}🔍 EJECUTANDO AUDITORÍA DE SEGURIDAD")
    print(f"{'=' * 35}{Style.RESET_ALL}")
    
    checker = SecurityChecker()
    
    print("Analizando proyecto...")
    
    # Verificar archivos del proyecto
    project_files = [
        Path("config.py"),
        Path("requirements.txt"),
        Path("examples/01_password_hashing.py"),
        Path("examples/02_input_validation.py"),
        Path("examples/03_jwt_authentication.py"),
    ]
    
    print("\n1. Verificando permisos de archivos...")
    for file_path in project_files:
        checker.check_file_permissions(file_path)
    
    print("2. Buscando secretos hardcodeados...")
    for file_path in project_files:
        secrets = checker.check_hardcoded_secrets(file_path)
    
    print("3. Verificando dependencias...")
    vulnerable = checker.check_dependencies()
    
    print("4. Generando reporte...")
    report = checker.generate_report()
    
    print(report)
    
    # Guardar reporte
    report_file = Path("security_audit_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        # Limpiar códigos de color para el archivo
        clean_report = report
        for color in [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Style.RESET_ALL]:
            clean_report = clean_report.replace(color, "")
        f.write(clean_report)
    
    print(f"\n📄 Reporte guardado en: {report_file}")

def incident_response_plan():
    """Muestra un plan básico de respuesta a incidentes"""
    print(f"\n{Fore.RED}🚨 PLAN DE RESPUESTA A INCIDENTES DE SEGURIDAD")
    print(f"{'=' * 50}{Style.RESET_ALL}")
    
    phases = [
        ("1. 🔍 DETECCIÓN", [
            "Identificar el incidente de seguridad",
            "Evaluar la severidad inicial", 
            "Documentar evidencia inicial",
            "Notificar al equipo de respuesta"
        ]),
        
        ("2. 🛡️ CONTENCIÓN", [
            "Aislar sistemas afectados",
            "Prevenir propagación del daño",
            "Preservar evidencia para análisis",
            "Implementar medidas temporales"
        ]),
        
        ("3. 🔧 ERRADICACIÓN", [
            "Identificar y eliminar la causa raíz",
            "Aplicar patches o fixes necesarios",
            "Mejorar controles de seguridad",
            "Verificar que la amenaza esté eliminada"
        ]),
        
        ("4. 🔄 RECUPERACIÓN", [
            "Restaurar sistemas desde backups limpios",
            "Monitorear sistemas restaurados",
            "Validar que todo funcione correctamente",
            "Gradualmente restaurar operaciones normales"
        ]),
        
        ("5. 📋 LECCIONES APRENDIDAS", [
            "Documentar el incidente completamente",
            "Identificar mejoras en procesos",
            "Actualizar planes y procedimientos",
            "Entrenar al equipo en nuevas medidas"
        ])
    ]
    
    for phase_title, steps in phases:
        print(f"\n{Fore.YELLOW}{phase_title}{Style.RESET_ALL}")
        for step in steps:
            print(f"   • {step}")

def security_tools_recommendations():
    """Recomienda herramientas de seguridad"""
    print(f"\n{Fore.CYAN}🛠️ HERRAMIENTAS DE SEGURIDAD RECOMENDADAS")
    print(f"{'=' * 45}{Style.RESET_ALL}")
    
    tools = {
        "📊 Análisis Estático de Código": [
            ("Bandit", "Escaner de seguridad específico para Python"),
            ("SonarQube", "Análisis de calidad y seguridad de código"),
            ("ESLint Security", "Plugin de seguridad para JavaScript"),
            ("Semgrep", "Análisis estático multi-lenguaje")
        ],
        
        "🔍 Análisis de Dependencias": [
            ("Safety", "Verifica vulnerabilidades en paquetes Python"),
            ("npm audit", "Auditoría de seguridad para proyectos Node.js"),
            ("Snyk", "Plataforma de seguridad para dependencias"),
            ("OWASP Dependency Check", "Identifica dependencias vulnerables")
        ],
        
        "🌐 Seguridad Web": [
            ("OWASP ZAP", "Proxy de seguridad para testing web"),
            ("Burp Suite", "Plataforma profesional de testing web"),
            ("Nmap", "Escaner de redes y puertos"),
            ("Nikto", "Escaner de vulnerabilidades web")
        ],
        
        "🔐 Gestión de Secretos": [
            ("HashiCorp Vault", "Gestión centralizada de secretos"),
            ("AWS Secrets Manager", "Gestión de secretos en AWS"),
            ("Azure Key Vault", "Gestión de claves y secretos en Azure"),
            ("Docker Secrets", "Gestión de secretos en containers")
        ]
    }
    
    for category, tool_list in tools.items():
        print(f"\n{Fore.GREEN}{category}{Style.RESET_ALL}")
        for tool_name, description in tool_list:
            print(f"   • {Fore.BLUE}{tool_name}{Style.RESET_ALL}: {description}")

def learning_resources():
    """Proporciona recursos para seguir aprendiendo"""
    print(f"\n{Fore.MAGENTA}📚 RECURSOS PARA SEGUIR APRENDIENDO")
    print(f"{'=' * 40}{Style.RESET_ALL}")
    
    resources = {
        "📖 Documentación Oficial": [
            "OWASP Top 10 - Las vulnerabilidades más críticas",
            "NIST Cybersecurity Framework - Marco de ciberseguridad",
            "CWE (Common Weakness Enumeration) - Catálogo de debilidades",
            "CVE (Common Vulnerabilities and Exposures) - Base de datos de vulnerabilidades"
        ],
        
        "🎓 Cursos y Certificaciones": [
            "CISSP - Certificación en seguridad de sistemas de información",
            "CEH - Certified Ethical Hacker",
            "Security+ - Certificación básica de seguridad",
            "OWASP WebGoat - Aplicación práctica vulnerable"
        ],
        
        "🛠️ Plataformas de Práctica": [
            "HackTheBox - Laboratorio de pentesting",
            "TryHackMe - Plataforma de aprendizaje de ciberseguridad",
            "PicoCTF - Competencias de seguridad",
            "Damn Vulnerable Web Application (DVWA)"
        ],
        
        "📰 Mantente Actualizado": [
            "Krebs on Security - Blog de noticias de seguridad",
            "SANS Internet Storm Center - Alertas de amenazas",
            "CVE Details - Seguimiento de vulnerabilidades",
            "Security Week - Noticias de la industria"
        ]
    }
    
    for category, resource_list in resources.items():
        print(f"\n{Fore.GREEN}{category}{Style.RESET_ALL}")
        for resource in resource_list:
            print(f"   • {resource}")

def final_recommendations():
    """Proporciona recomendaciones finales"""
    print(f"\n{Fore.CYAN}🎯 RECOMENDACIONES FINALES")
    print(f"{'=' * 30}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}✅ Para empezar inmediatamente:{Style.RESET_ALL}")
    immediate_actions = [
        "Implementa hashing seguro de contraseñas en tu próximo proyecto",
        "Agrega validación de entrada a todos tus formularios",
        "Configura HTTPS en todos tus sitios web",
        "Empieza a usar variables de entorno para secretos",
        "Implementa logging básico de eventos de seguridad"
    ]
    
    for action in immediate_actions:
        print(f"   1. {action}")
    
    print(f"\n{Fore.YELLOW}🔄 Para convertir en hábito:{Style.RESET_ALL}")
    habits = [
        "Haz code reviews enfocados en seguridad",
        "Mantén actualizadas todas las dependencias",
        "Lee sobre nuevas vulnerabilidades regularmente",
        "Practica con aplicaciones vulnerables",
        "Participa en comunidades de seguridad"
    ]
    
    for habit in habits:
        print(f"   • {habit}")
    
    print(f"\n{Fore.RED}⚠️ Recuerda siempre:{Style.RESET_ALL}")
    print("   • La seguridad es un proceso, no un estado final")
    print("   • Mantente paranoico (de forma constructiva)")
    print("   • Cuando dudes, consulta con expertos")
    print("   • Documenta tus decisiones de seguridad")
    print("   • La usabilidad y la seguridad pueden coexistir")

if __name__ == "__main__":
    print_educational_header()
    
    # Ejecutar todas las secciones finales
    security_checklist()
    run_security_audit()
    incident_response_plan()
    security_tools_recommendations()
    learning_resources()
    final_recommendations()
    
    print(f"\n{Fore.MAGENTA}🎓 ¡FELICITACIONES!")
    print("Has completado el curso de Tech Security Basics.")
    print("Ahora tienes las herramientas y conocimientos básicos")
    print("para desarrollar aplicaciones más seguras.")
    print(f"\n{Fore.CYAN}🚀 ¡Tu viaje en ciberseguridad apenas comienza!")
    print("Sigue practicando, aprendiendo y mantente actualizado.")
    print(f"La seguridad es responsabilidad de todos los desarrolladores.{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}💡 ¿Próximo paso? ¡Comparte este conocimiento con otros!")
    print("La seguridad mejora cuando toda la comunidad está informada.")
    print(f"⭐ Si este curso te ayudó, ¡dale una estrella en GitHub!{Style.RESET_ALL}")
