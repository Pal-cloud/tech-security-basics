"""
⚖️ Módulo 5: Aspectos Legales - GDPR y Protección de Datos
==========================================================

Aprende los conceptos básicos de protección de datos y cumplimiento
legal que todo desarrollador debe conocer. ¡La privacidad es un derecho!

⚠️ Esta es una introducción educativa, siempre consulta con expertos legales!
"""

import json
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init()

def print_educational_header():
    """Muestra información educativa sobre GDPR"""
    print(f"\n{Fore.CYAN}⚖️ MÓDULO 5: ASPECTOS LEGALES - GDPR Y PROTECCIÓN DE DATOS{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=" * 65)
    print(f"{Fore.GREEN}✅ Lo que aprenderás:")
    print("   • Qué es el GDPR y por qué es importante")
    print("   • Principios básicos de protección de datos")
    print("   • Cómo implementar consentimiento y cookies")
    print("   • El derecho al olvido y portabilidad de datos")
    print(f"   • Cómo diseñar sistemas 'privacy by design'{Style.RESET_ALL}\n")

def explicar_gdpr():
    """Explica qué es el GDPR y sus principios básicos"""
    print(f"{Fore.BLUE}🇪🇺 ¿QUÉ ES EL GDPR?")
    print(f"{'=' * 20}{Style.RESET_ALL}")
    
    print("GDPR = General Data Protection Regulation (Reglamento General de Protección de Datos)")
    print("• Ley europea vigente desde mayo de 2018")
    print("• Se aplica a CUALQUIER empresa que procese datos de ciudadanos EU")
    print("• Multas de hasta €20M o 4% del volumen de negocio anual")
    print("• Establece derechos fundamentales sobre datos personales")
    
    print(f"\n{Fore.CYAN}🎯 Principios Básicos del GDPR:{Style.RESET_ALL}")
    principios = [
        ("Legalidad", "Procesar datos solo con base legal válida"),
        ("Limitación de finalidad", "Usar datos solo para el propósito declarado"),
        ("Minimización", "Recoger solo los datos necesarios"),
        ("Exactitud", "Mantener datos actualizados y correctos"),
        ("Limitación de conservación", "Borrar datos cuando ya no sean necesarios"),
        ("Integridad y confidencialidad", "Proteger datos con medidas apropiadas"),
        ("Responsabilidad proactiva", "Demostrar cumplimiento, no solo cumplir")
    ]
    
    for principio, descripcion in principios:
        print(f"• {Fore.GREEN}{principio}{Style.RESET_ALL}: {descripcion}")

def explicar_datos_personales():
    """Explica qué se considera datos personales"""
    print(f"\n{Fore.YELLOW}👤 ¿QUÉ SON DATOS PERSONALES?")
    print(f"{'=' * 30}{Style.RESET_ALL}")
    
    print("Cualquier información que identifique a una persona:")
    
    obvios = [
        "Nombre y apellidos",
        "Email y teléfono", 
        "Dirección física",
        "DNI/Pasaporte",
        "Número de cuenta bancaria"
    ]
    
    no_tan_obvios = [
        "Dirección IP",
        "Cookies y identificadores únicos",
        "Datos de geolocalización",
        "Fotos que muestren la cara",
        "Información médica",
        "Preferencias y comportamiento online"
    ]
    
    print(f"\n{Fore.GREEN}✅ Obviamente personales:")
    for dato in obvios:
        print(f"   • {dato}")
    
    print(f"\n{Fore.YELLOW}⚠️ Menos obvios pero también personales:")
    for dato in no_tan_obvios:
        print(f"   • {dato}")
    
    print(f"\n{Fore.RED}🎯 Regla práctica:")
    print("Si puedes vincular la información a una persona específica,")
    print("es dato personal y aplica GDPR!")

class ConsentManager:
    """Gestor de consentimientos para cumplimiento GDPR"""
    
    def __init__(self, storage_file: str = "data/consents.json"):
        self.storage_file = Path(storage_file)
        self.storage_file.parent.mkdir(exist_ok=True)
        self.consents = self._load_consents()
    
    def _load_consents(self) -> Dict[str, Any]:
        """Carga consentimientos del archivo"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error cargando consentimientos: {e}")
        return {}
    
    def _save_consents(self):
        """Guarda consentimientos al archivo"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.consents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando consentimientos: {e}")
    
    def request_consent(self, user_id: str, purposes: List[str], 
                       legal_basis: str = "consent") -> str:
        """Solicita consentimiento para propósitos específicos"""
        consent_id = str(uuid.uuid4())
        
        consent_record = {
            "consent_id": consent_id,
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "purposes": purposes,
            "legal_basis": legal_basis,
            "status": "pending",
            "ip_address": "192.168.1.100",  # En una app real vendría del request
            "user_agent": "example-browser"
        }
        
        self.consents[consent_id] = consent_record
        self._save_consents()
        
        return consent_id
    
    def record_consent(self, consent_id: str, granted: bool, 
                      specific_consents: Dict[str, bool] = None) -> bool:
        """Registra la respuesta del usuario al consentimiento"""
        if consent_id not in self.consents:
            return False
        
        self.consents[consent_id].update({
            "status": "granted" if granted else "denied",
            "response_timestamp": datetime.now(timezone.utc).isoformat(),
            "specific_consents": specific_consents or {}
        })
        
        self._save_consents()
        return True
    
    def check_consent(self, user_id: str, purpose: str) -> bool:
        """Verifica si el usuario ha dado consentimiento para un propósito"""
        for consent_record in self.consents.values():
            if (consent_record["user_id"] == user_id and 
                consent_record["status"] == "granted" and 
                purpose in consent_record["purposes"]):
                return True
        return False
    
    def withdraw_consent(self, user_id: str, purpose: str) -> bool:
        """Permite al usuario retirar consentimiento"""
        updated = False
        for consent_record in self.consents.values():
            if (consent_record["user_id"] == user_id and 
                purpose in consent_record["purposes"]):
                consent_record["status"] = "withdrawn"
                consent_record["withdrawal_timestamp"] = datetime.now(timezone.utc).isoformat()
                updated = True
        
        if updated:
            self._save_consents()
        return updated

def demostrar_consentimiento():
    """Demuestra el sistema de consentimiento"""
    print(f"\n{Fore.GREEN}✅ SISTEMA DE CONSENTIMIENTO")
    print(f"{'=' * 30}{Style.RESET_ALL}")
    
    consent_manager = ConsentManager()
    
    print("1. Solicitando consentimiento a un usuario...")
    
    # Simular solicitud de consentimiento
    user_id = "user_12345"
    purposes = [
        "marketing_emails",
        "analytics_tracking", 
        "personalized_ads",
        "newsletter"
    ]
    
    consent_id = consent_manager.request_consent(user_id, purposes)
    print(f"   Consentimiento solicitado con ID: {consent_id[:8]}...")
    
    # Simular respuesta del usuario (granular)
    print("\n2. Usuario responde al consentimiento...")
    user_choices = {
        "marketing_emails": False,    # Rechaza marketing
        "analytics_tracking": True,   # Acepta analytics
        "personalized_ads": False,    # Rechaza ads
        "newsletter": True            # Acepta newsletter
    }
    
    # Registrar consentimiento específico
    consent_manager.record_consent(consent_id, True, user_choices)
    
    print("   Respuestas del usuario:")
    for purpose, granted in user_choices.items():
        emoji = "✅" if granted else "❌"
        print(f"      {emoji} {purpose}")
    
    # Verificar consentimientos
    print("\n3. Verificando consentimientos antes de procesar datos...")
    purposes_to_check = ["analytics_tracking", "marketing_emails", "newsletter"]
    
    for purpose in purposes_to_check:
        has_consent = consent_manager.check_consent(user_id, purpose)
        emoji = "✅" if has_consent else "❌"
        action = "PROCEDER" if has_consent else "BLOQUEAR"
        print(f"   {emoji} {purpose}: {action}")

class DataController:
    """Controlador de datos que implementa derechos GDPR"""
    
    def __init__(self):
        self.users_data = {}
        self.processing_log = []
    
    def add_user_data(self, user_id: str, data: Dict[str, Any], legal_basis: str):
        """Agrega datos de usuario con base legal"""
        self.users_data[user_id] = {
            "data": data,
            "legal_basis": legal_basis,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        
        self._log_processing(user_id, "data_collected", legal_basis)
    
    def _log_processing(self, user_id: str, action: str, legal_basis: str):
        """Registra actividades de procesamiento"""
        self.processing_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "action": action,
            "legal_basis": legal_basis
        })
    
    def export_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Derecho a la portabilidad - exportar datos del usuario"""
        if user_id not in self.users_data:
            return None
        
        user_data = self.users_data[user_id].copy()
        
        # Agregar log de procesamiento para este usuario
        user_processing_log = [
            log for log in self.processing_log 
            if log["user_id"] == user_id
        ]
        
        export_package = {
            "user_data": user_data,
            "processing_history": user_processing_log,
            "export_date": datetime.now(timezone.utc).isoformat(),
            "format": "JSON"
        }
        
        self._log_processing(user_id, "data_exported", "data_subject_request")
        return export_package
    
    def delete_user_data(self, user_id: str, reason: str = "user_request") -> bool:
        """Derecho al olvido - eliminar datos del usuario"""
        if user_id not in self.users_data:
            return False
        
        # En un sistema real, esto sería más complejo:
        # - Verificar si hay obligaciones legales que impidan el borrado
        # - Notificar a terceros que también tienen los datos
        # - Asegurarse de borrar de backups
        
        deleted_data = self.users_data.pop(user_id)
        
        self._log_processing(user_id, "data_deleted", reason)
        
        print(f"   🗑️ Datos del usuario {user_id} eliminados permanentemente")
        print(f"   📝 Motivo: {reason}")
        
        return True
    
    def anonymize_user_data(self, user_id: str) -> bool:
        """Anonimizar datos (alternativa al borrado)"""
        if user_id not in self.users_data:
            return False
        
        user_data = self.users_data[user_id]
        
        # Reemplazar identificadores personales con hashes o anonimización
        anonymized_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        
        # En un sistema real, esto sería más sofisticado
        anonymized_data = {
            "data": {
                "age_range": "25-34",  # En lugar de edad exacta
                "location_region": "Europe",  # En lugar de dirección exacta
                "activity_pattern": "high"  # En lugar de datos específicos
            },
            "legal_basis": "legitimate_interest_anonymized",
            "anonymized_at": datetime.now(timezone.utc).isoformat(),
            "original_user_id_hash": anonymized_id
        }
        
        self.users_data[anonymized_id] = anonymized_data
        del self.users_data[user_id]
        
        self._log_processing(user_id, "data_anonymized", "data_retention_policy")
        
        return True

def demostrar_derechos_gdpr():
    """Demuestra la implementación de derechos GDPR"""
    print(f"\n{Fore.MAGENTA}📋 DERECHOS GDPR EN ACCIÓN")
    print(f"{'=' * 30}{Style.RESET_ALL}")
    
    controller = DataController()
    
    # Agregar datos de usuario
    print("1. Recopilando datos de usuario...")
    user_data = {
        "name": "María González",
        "email": "maria@ejemplo.com",
        "age": 28,
        "preferences": ["deportes", "tecnología"],
        "purchase_history": ["laptop", "smartphone"]
    }
    
    controller.add_user_data("user_maria", user_data, "consent")
    print("   ✅ Datos recopilados con consentimiento")
    
    # Derecho de acceso (exportar datos)
    print("\n2. Usuario solicita exportar sus datos...")
    exported = controller.export_user_data("user_maria")
    
    if exported:
        print("   ✅ Datos exportados exitosamente")
        print(f"   📦 Paquete incluye: datos personales + historial de procesamiento")
        print(f"   📅 Fecha de exportación: {exported['export_date'][:19]}")
    
    # Derecho al olvido
    print("\n3. Usuario solicita borrar sus datos...")
    deleted = controller.delete_user_data("user_maria", "user_request")
    
    if deleted:
        print("   ✅ Datos eliminados conforme al derecho al olvido")
    
    # Intentar acceder a datos borrados
    print("\n4. Verificando que los datos fueron eliminados...")
    try_export = controller.export_user_data("user_maria")
    if try_export is None:
        print("   ✅ Confirmado: No hay datos del usuario en el sistema")

def privacy_by_design_principles():
    """Explica los principios de Privacy by Design"""
    print(f"\n{Fore.CYAN}🏗️ PRIVACY BY DESIGN")
    print(f"{'=' * 25}{Style.RESET_ALL}")
    
    print("7 Principios fundamentales para diseñar sistemas que respeten la privacidad:")
    
    principles = [
        ("1. Proactivo, no reactivo", 
         "Prevenir problemas de privacidad antes de que ocurran"),
        ("2. Privacidad por defecto", 
         "Máxima protección sin que el usuario tenga que hacer nada"),
        ("3. Privacidad incorporada al diseño", 
         "Considerar privacidad desde el inicio, no como parche"),
        ("4. Funcionalidad completa", 
         "No comprometer la funcionalidad por la privacidad"),
        ("5. Seguridad de extremo a extremo", 
         "Proteger datos durante todo su ciclo de vida"),
        ("6. Visibilidad y transparencia", 
         "Que todos sepan qué datos se procesan y cómo"),
        ("7. Respeto por la privacidad del usuario", 
         "Poner los intereses del usuario primero")
    ]
    
    for principle, explanation in principles:
        print(f"\n{Fore.GREEN}{principle}{Style.RESET_ALL}")
        print(f"   └─ {explanation}")

def ejemplos_practicos_cumplimiento():
    """Muestra ejemplos prácticos de cumplimiento"""
    print(f"\n{Fore.BLUE}💡 EJEMPLOS PRÁCTICOS DE CUMPLIMIENTO")
    print(f"{'=' * 45}{Style.RESET_ALL}")
    
    examples = [
        ("🍪 Banner de Cookies", 
         "Solicitar consentimiento ANTES de cargar cookies no esenciales"),
        ("📧 Formulario de Newsletter", 
         "Checkbox opcional, no marcada por defecto"),
        ("🔒 Configuración de Privacidad", 
         "Opciones granulares, fáciles de cambiar"),
        ("📱 App Móvil", 
         "Pedir permisos específicos cuando se necesiten"),
        ("🗑️ Botón de Borrar Cuenta", 
         "Fácil de encontrar, proceso simple"),
        ("📊 Dashboard de Datos", 
         "Mostrar qué datos tienes, para qué los usas"),
        ("📤 Exportar Datos", 
         "Un click para descargar todos los datos"),
        ("⚙️ Centro de Preferencias", 
         "Control granular sobre el uso de datos")
    ]
    
    for title, description in examples:
        print(f"{Fore.GREEN}{title}{Style.RESET_ALL}")
        print(f"   └─ {description}")

def mejores_practicas_gdpr():
    """Muestra las mejores prácticas GDPR para desarrolladores"""
    print(f"\n{Fore.CYAN}📋 MEJORES PRÁCTICAS GDPR PARA DESARROLLADORES")
    print(f"{'=' * 50}{Style.RESET_ALL}")
    
    practices = [
        ("✅ Documenta todas las actividades de procesamiento", 
         "Qué datos, para qué, base legal, retención"),
        ("✅ Implementa consentimiento granular", 
         "No todo o nada, opciones específicas"),
        ("✅ Diseña flujos de retiro de consentimiento", 
         "Tan fácil como dar el consentimiento"),
        ("✅ Cifra datos personales", 
         "En tránsito y en reposo"),
        ("✅ Implementa retention policies", 
         "Borrar datos automáticamente cuando sea apropiado"),
        ("❌ NO recojas datos 'por si acaso'", 
         "Solo los que realmente necesitas"),
        ("✅ Haz auditorías regulares", 
         "Verifica qué datos tienes y por qué"),
        ("✅ Prepárate para data breaches", 
         "Plan de respuesta a incidentes"),
        ("✅ Capacita a tu equipo", 
         "Todos deben entender GDPR básico"),
        ("✅ Mantén registros de cumplimiento", 
         "Demuestra que cumples, no solo digas que cumples")
    ]
    
    for practice, explanation in practices:
        color = Fore.GREEN if practice.startswith("✅") else Fore.RED
        print(f"{color}{practice}{Style.RESET_ALL}")
        print(f"   └─ {explanation}")

if __name__ == "__main__":
    print_educational_header()
    
    # Ejecutar todas las demostraciones
    explicar_gdpr()
    explicar_datos_personales()
    demostrar_consentimiento()
    demostrar_derechos_gdpr()
    privacy_by_design_principles()
    ejemplos_practicos_cumplimiento()
    mejores_practicas_gdpr()
    
    print(f"\n{Fore.MAGENTA}🎓 ¡Fantástico!")
    print("Ahora tienes una base sólida sobre aspectos legales y GDPR.")
    print(f"{Fore.RED}⚠️ Recuerda: Esta es una introducción educativa.")
    print("Para sistemas reales, siempre consulta con expertos legales.")
    print(f"\nPróximo paso: Módulo 6 - Mejores Prácticas Finales{Style.RESET_ALL}")
