"""
🎯 Demo Principal - Tech Security Basics
========================================

Ejecuta este archivo para ver una demostración completa
de todos los conceptos de seguridad que hemos cubierto.

"""

import os
import sys
from pathlib import Path
from colorama import init, Fore, Style

# Inicializar colorama
init()

def print_welcome():
    """Mensaje de bienvenida"""
    print(f"\n{Fore.MAGENTA}{'=' * 60}")
    print(f"🔐 BIENVENIDO A TECH SECURITY BASICS")
    print(f"   Guía Práctica de Seguridad para Desarrolladores")
    print(f"{'=' * 60}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Este curso te enseñará:{Style.RESET_ALL}")
    print("   • 🔒 Hashing seguro de contraseñas")
    print("   • 🛡️ Validación y sanitización de datos")
    print("   • 🔑 Autenticación con JWT")
    print("   • 📝 Logging de seguridad")
    print("   • ⚖️ Cumplimiento GDPR básico")
    print("   • 🚨 Mejores prácticas y checklist")

def run_module(module_path: Path, module_name: str):
    """Ejecuta un módulo específico"""
    print(f"\n{Fore.YELLOW}{'─' * 50}")
    print(f"🎯 EJECUTANDO: {module_name}")
    print(f"{'─' * 50}{Style.RESET_ALL}")
    
    if not module_path.exists():
        print(f"{Fore.RED}❌ Archivo no encontrado: {module_path}{Style.RESET_ALL}")
        return False
    
    try:
        # Importar y ejecutar el módulo
        import importlib.util
        spec = importlib.util.spec_from_file_location("module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error ejecutando módulo: {e}{Style.RESET_ALL}")
        return False

def interactive_menu():
    """Menú interactivo para elegir módulos"""
    modules = [
        ("examples/01_password_hashing.py", "🔐 Módulo 1: Hashing de Contraseñas"),
        ("examples/02_input_validation.py", "🛡️ Módulo 2: Validación de Datos"),
        ("examples/03_jwt_authentication.py", "🔑 Módulo 3: Autenticación JWT"),
        ("examples/04_security_logging.py", "📝 Módulo 4: Logging de Seguridad"),
        ("examples/05_gdpr_compliance.py", "⚖️ Módulo 5: Cumplimiento GDPR"),
        ("examples/06_security_best_practices.py", "🚨 Módulo 6: Mejores Prácticas")
    ]
    
    while True:
        print(f"\n{Fore.CYAN}📚 MENÚ DE MÓDULOS")
        print(f"{'=' * 20}{Style.RESET_ALL}")
        
        for i, (_, name) in enumerate(modules, 1):
            print(f"   {i}. {name}")
        
        print(f"   0. {Fore.GREEN}🚀 Ejecutar TODOS los módulos{Style.RESET_ALL}")
        print(f"   q. {Fore.RED}❌ Salir{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.YELLOW}Elige una opción: {Style.RESET_ALL}").strip().lower()
        
        if choice == 'q':
            print(f"\n{Fore.GREEN}¡Gracias por usar Tech Security Basics!{Style.RESET_ALL}")
            print("🎓 Sigue practicando y mantente seguro!")
            break
        elif choice == '0':
            print(f"\n{Fore.MAGENTA}🚀 EJECUTANDO TODOS LOS MÓDULOS")
            print("Este proceso puede tomar varios minutos...")
            print(f"{'=' * 40}{Style.RESET_ALL}")
            
            for module_path, module_name in modules:
                success = run_module(Path(module_path), module_name)
                if success:
                    print(f"{Fore.GREEN}✅ {module_name} completado{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Error en {module_name}{Style.RESET_ALL}")
                
                input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            
            print(f"\n{Fore.MAGENTA}🎉 ¡TODOS LOS MÓDULOS COMPLETADOS!")
            print("Has terminado el curso completo de Tech Security Basics.")
            print(f"¡Felicitaciones! 🎓{Style.RESET_ALL}")
            break
            
        elif choice.isdigit() and 1 <= int(choice) <= len(modules):
            module_path, module_name = modules[int(choice) - 1]
            success = run_module(Path(module_path), module_name)
            
            if success:
                print(f"\n{Fore.GREEN}✅ Módulo completado exitosamente!{Style.RESET_ALL}")
            
            input(f"\n{Fore.CYAN}Presiona Enter para volver al menú...{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Opción inválida. Intenta de nuevo.{Style.RESET_ALL}")

def check_setup():
    """Verifica que el setup esté completo"""
    print(f"\n{Fore.BLUE}🔍 Verificando configuración...")
    
    required_files = [
        "requirements.txt",
        "config.py",
        "examples/01_password_hashing.py",
        "examples/02_input_validation.py",
        "examples/03_jwt_authentication.py",
        "examples/04_security_logging.py",
        "examples/05_gdpr_compliance.py",
        "examples/06_security_best_practices.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"{Fore.RED}❌ Archivos faltantes:{Style.RESET_ALL}")
        for file in missing_files:
            print(f"   • {file}")
        return False
    else:
        print(f"{Fore.GREEN}✅ Todos los archivos están presentes{Style.RESET_ALL}")
        return True

def show_quick_start():
    """Muestra guía de inicio rápido"""
    print(f"\n{Fore.CYAN}🚀 INICIO RÁPIDO")
    print(f"{'=' * 15}{Style.RESET_ALL}")
    
    print("Para usar este proyecto:")
    print(f"\n{Fore.GREEN}1. Instalar dependencias:{Style.RESET_ALL}")
    print("   pip install -r requirements.txt")
    
    print(f"\n{Fore.GREEN}2. Ejecutar un ejemplo específico:{Style.RESET_ALL}")
    print("   python examples/01_password_hashing.py")
    
    print(f"\n{Fore.GREEN}3. Ejecutar este demo interactivo:{Style.RESET_ALL}")
    print("   python demo.py")
    
    print(f"\n{Fore.GREEN}4. Usar VS Code task (Ctrl+Shift+P > 'Tasks: Run Task'):{Style.RESET_ALL}")
    print("   Seleccionar 'Run Security Example'")

if __name__ == "__main__":
    print_welcome()
    
    if not check_setup():
        print(f"\n{Fore.RED}⚠️ Configuración incompleta.")
        print("Asegúrate de tener todos los archivos necesarios.")
        print(f"Consulta el README.md para más información.{Style.RESET_ALL}")
        sys.exit(1)
    
    show_quick_start()
    
    # Preguntar si quiere continuar con el demo interactivo
    print(f"\n{Fore.YELLOW}¿Quieres ejecutar el demo interactivo?")
    response = input("(s/n): ").strip().lower()
    
    if response in ['s', 'y', 'si', 'yes', '']:
        interactive_menu()
    else:
        print(f"\n{Fore.GREEN}¡Perfecto!")
        print("Ejecuta los ejemplos individualmente cuando estés listo.")
        print("¡Disfruta aprendiendo sobre seguridad! 🎓{Style.RESET_ALL}")
