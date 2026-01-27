# Tech Security Basics 🔐
## Guía Práctica de Seguridad y Aspectos Legales para Principiantes en Tech

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Educational-yellow.svg)]()

### 🎯 ¿Qué aprenderás?

Este repositorio te guiará paso a paso por los conceptos fundamentales de **seguridad informática** y **aspectos legales** más importantes que todo desarrollador debe conocer, usando **Python** de forma práctica y sencilla.

### 📚 Contenido del Curso

#### 🔒 **Módulo 1: Fundamentos de Criptografía**
- Hash de contraseñas con salt
- Encriptación simétrica y asimétrica
- Firmas digitales básicas
- **Ejemplo práctico:** Sistema de autenticación seguro

#### 🛡️ **Módulo 2: Validación y Sanitización**
- Validación de entrada de datos
- Prevención de inyecciones
- Escape de caracteres especiales
- **Ejemplo práctico:** Formulario web seguro

#### 🔑 **Módulo 3: Autenticación y Autorización**
- JWT (JSON Web Tokens)
- Sesiones seguras
- Control de acceso por roles
- **Ejemplo práctico:** API REST con autenticación

#### 📝 **Módulo 4: Logging y Monitoreo**
- Logs de seguridad
- Detección de patrones sospechosos
- Alertas automatizadas
- **Ejemplo práctico:** Sistema de monitoreo básico

#### ⚖️ **Módulo 5: Aspectos Legales y GDPR**
- Protección de datos personales
- Consentimiento y cookies
- Derecho al olvido
- **Ejemplo práctico:** Sistema de gestión de consentimientos

#### 🚨 **Módulo 6: Mejores Prácticas**
- Code review de seguridad
- Configuración segura
- Manejo de secretos
- **Ejemplo práctico:** Checklist de seguridad

### 🚀 Instalación Rápida

```bash
# 1. Clona el repositorio
git clone https://github.com/Pal-cloud/tech-security-basics.git
cd tech-security-basics

# 2. Crea un entorno virtual
python -m venv security_env

# 3. Activa el entorno (Windows)
security_env\Scripts\activate
# En Linux/Mac: source security_env/bin/activate

# 4. Instala las dependencias
pip install -r requirements.txt

# 5. ¡Ejecuta tu primer ejemplo!
python examples/01_password_hashing.py
```

### 🎮 Uso Interactivo

Cada módulo incluye ejemplos que puedes ejecutar inmediatamente:

```bash
# Ejecutar módulos individuales
python examples/01_password_hashing.py     # Aprende hashing seguro
python examples/02_input_validation.py     # Validación de datos
python examples/03_jwt_authentication.py   # Autenticación JWT
python examples/04_security_logging.py     # Logging de seguridad
python examples/05_gdpr_compliance.py      # Aspectos legales
python examples/06_security_best_practices.py # Mejores prácticas

# O ejecutar el demo interactivo completo
python demo.py
```

### 📁 Estructura del Proyecto

```
tech-security-basics/
├── 📂 examples/                        # Módulos educativos completos
│   ├── 01_password_hashing.py         # 🔐 Hashing seguro de contraseñas
│   ├── 02_input_validation.py         # 🛡️ Validación y sanitización
│   ├── 03_jwt_authentication.py       # 🔑 Autenticación JWT
│   ├── 04_security_logging.py         # 📝 Logging de seguridad
│   ├── 05_gdpr_compliance.py          # ⚖️ Aspectos legales GDPR
│   └── 06_security_best_practices.py  # 🚨 Mejores prácticas
├── � demo.py                         # Demo interactivo principal
├── ⚙️ config.py                       # Configuración del proyecto
├── 🔧 requirements.txt                # Dependencias Python
├── 📜 LICENSE                         # Licencia MIT
└── 📖 README.md                       # Esta guía
```

#### Dependencias Mínimas
```
cryptography==41.0.7  # Criptografía moderna
bcrypt==4.1.2         # Hashing seguro de passwords
pyjwt==2.8.0          # JSON Web Tokens
requests==2.31.0      # HTTP requests seguros
python-dotenv==1.0.0  # Gestión de variables de entorno
colorama==0.4.6       # Colores en terminal multiplataforma
```

### 🌟 Características Destacadas

- ✅ **Código comentado** línea por línea
- ✅ **Ejemplos interactivos** que funcionan desde el primer momento  
- ✅ **Tests incluidos** para verificar tu aprendizaje
- ✅ **Casos de uso reales** basados en problemas frecuentes
- ✅ **Guías de buenas prácticas** aplicables en proyectos reales
- ✅ **Aspectos legales simplificados** sin jerga jurídica compleja

### 🎯 Para Quién Es Este Curso

- **Desarrolladores junior** que quieren aprender seguridad
- **Estudiantes de programación** interesados en ciberseguridad
- **Profesionales tech** que necesitan cumplir con normativas (GDPR, etc.)
- **Cualquier persona** que quiera entender cómo proteger datos y aplicaciones

### 📖 Cómo Estudiar

1. **Empieza por el Módulo 1** y sigue el orden sugerido
2. **Ejecuta cada ejemplo** antes de pasar al siguiente
3. **Lee los comentarios** del código para entender el "por qué"
4. **Experimenta** modificando los parámetros y observa los resultados
5. **Completa los ejercicios** al final de cada módulo

### 💡 Roadmap Futuro

#### Versión 2.0
- 🌐 **Módulos adicionales**: OAuth, SAML, biometría
- 🐳 **Containerización**: Docker para entorno aislado
- 🌍 **Internacionalización**: Soporte multi-idioma
- 📱 **Versión móvil**: Conceptos aplicados a apps móviles

#### Versión 3.0
- 🤖 **AI/ML Security**: Seguridad en modelos de ML
- ☁️ **Cloud Security**: AWS, Azure, GCP best practices
- 🔗 **Blockchain**: Conceptos de seguridad en Web3
- 🎮 **Gamificación**: Challenges y certificaciones


### 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este curso:

1. Fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request


### ⚠️ Importante - Disclaimer Legal

Los ejemplos en este repositorio son **únicamente educativos**. En producción:

- 🔴 **Nunca hardcodees** credenciales o secretos
- 🔴 **Siempre usa HTTPS** en producción
- 🔴 **Implementa rate limiting** y otras protecciones
- 🔴 **Consulta con expertos** para sistemas críticos
- 🔴 **Mantén actualizadas** las dependencias de seguridad

### 📞 Autoría

¿Tienes preguntas? ¡No dudes en contactar!

- 💼 **LinkedIn**: [Pal](https://www.linkedin.com/in/palomagsal/)
- 🐙 **GitHub**: [Pal-cloud](https://github.com/Pal-cloud)

---

**⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub! ⭐**

*"La seguridad no es un producto, es un proceso"* - Bruce Schneier
