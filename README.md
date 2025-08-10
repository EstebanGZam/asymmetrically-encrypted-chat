# Sistema de Chat Seguro con Cifrado Asimétrico

Este proyecto implementa un sistema de comunicación seguro end-to-end entre dos usuarios utilizando criptografía asimétrica RSA. El sistema garantiza confidencialidad, integridad, autenticación y no repudio de los mensajes intercambiados.

## Características Técnicas

### Seguridad Criptográfica

- **Cifrado asimétrico RSA 2048-bit**: Cada usuario genera su propio par de llaves criptográficas
- **Arquitectura descentralizada**: El servidor actúa únicamente como relay, sin acceso a llaves privadas
- **Firmas digitales**: Autenticación y verificación de integridad usando PSS padding
- **Verificación de identidad**: Fingerprints SHA-256 para prevenir ataques man-in-the-middle
- **Cifrado OAEP**: Padding óptimo para máxima seguridad en el cifrado RSA

### Arquitectura del Sistema

- **Servidor relay**: Facilita el intercambio de llaves públicas y retransmite mensajes cifrados
- **Clientes independientes**: Generación y gestión local de llaves criptográficas
- **Comunicación TCP/IP**: Protocolo confiable para el transporte de datos

### Interfaz de Usuario

- **Interfaz gráfica moderna**: GUI elegante con tema oscuro profesional
- **Interfaz de línea de comandos**: Terminal tradicional para usuarios avanzados
- **Monitoreo del servidor**: Ventana dedicada para supervisar conexiones y actividad
- **Indicadores de seguridad**: Estado visual del cifrado y verificación de identidad

## Estructura del Proyecto

```
asymmetrically-encrypted-chat/
├── crypto_utils.py     # Módulo de utilidades criptográficas
├── main_gui.py         # Punto de entrada principal (GUI)
├── gui_client.py       # Adaptador para GUI de cliente de chat seguro
├── gui_server.py       # Adaptador para GUI de servidor relay para comunicaciones
├── gui/                # Módulo de interfaz gráfica
│   ├── __init__.py     # Inicialización del módulo
│   ├── main_window.py  # Ventana principal de la aplicación
│   ├── chat_window.py  # Interfaz de chat con indicadores de seguridad
│   ├── server_window.py# Monitor del servidor con logs en tiempo real
│   └── styles.py       # Tema moderno y componentes estilizados
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación del proyecto
```

## Instalación y Configuración

### Requisitos del Sistema

- Python 3.8 o superior
- Biblioteca `cryptography` versión 41.0.0 o superior
- `tkinter` (incluido por defecto en la mayoría de instalaciones de Python)

### Instalación de Dependencias

Si tkinter NO está instalado:

- Windows: tkinter viene incluido con Python. Durante la instalación de Python, marcar la opción "Tcl/Tk and IDLE"
- macOS: tkinter viene incluido por defecto. Si es necesario instalarlo manualmente:

```bash
brew install python-tk
```

- Linux (Ubuntu/Debian):

```bash
sudo apt install python3-tk
```

Luego, se procede a instalar las demás depedencias:

```bash
pip install -r requirements.txt
```

## Uso del Sistema

### Interfaz Gráfica

#### Ejecución de la aplicación GUI

```bash
python main_gui.py
```

#### Flujo de uso con interfaz gráfica:

1. **Iniciar el servidor**: Clic en el botón "🚀 Iniciar Servidor" en la ventana principal
2. **Conectar primer cliente**: Ingresar nombre de usuario y clic en "🔗 Conectar como Cliente"
3. **Conectar segundo cliente**: Repetir el proceso en otra instancia de la aplicación
4. **Verificar identidad**: Cuando aparezca el fingerprint del contacto, verificarlo por un canal seguro independiente
5. **Confirmar verificación**: Clic en "✅ Verificar Identidad" para establecer el canal seguro
6. **Comunicación segura**: Enviar mensajes cifrados end-to-end


## Protocolo de Comunicación Segura

### Proceso de Establecimiento de Canal Seguro

1. **Generación de Llaves**: Cada cliente genera independientemente un par de llaves RSA 2048-bit
2. **Registro en Servidor**: Los clientes envían sus llaves públicas al servidor relay
3. **Intercambio de Llaves**: El servidor facilita el intercambio de llaves públicas entre los participantes
4. **Verificación de Identidad**: Los usuarios verifican los fingerprints SHA-256 a través de un canal seguro alternativo
5. **Comunicación Cifrada**: Los mensajes se cifran con la llave pública del destinatario y se firman con la llave privada del remitente

### Comandos Disponibles (Terminal)

- `verify`: Confirma la verificación del fingerprint del contacto
- `quit`: Termina la sesión de chat de forma segura
- Cualquier otro texto: Envía un mensaje cifrado y firmado

### Características de la GUI

- **Indicadores visuales de seguridad**: Estado del cifrado y verificación de identidad
- **Monitor del servidor**: Logs en tiempo real, contador de clientes y mensajes
- **Verificación simplificada**: Botón dedicado para confirmar la identidad del contacto
- **Tema moderno**: Interfaz oscura profesional con elementos visuales intuitivos

## Garantías de Seguridad

### Propiedades Criptográficas

- **Confidencialidad**: Solo el destinatario legítimo puede descifrar los mensajes
- **Autenticidad**: Las firmas digitales garantizan la identidad del remitente
- **Integridad**: Cualquier alteración del mensaje es detectada mediante verificación de firma
- **No repudio**: El remitente no puede negar la autoría de un mensaje firmado

### Amenazas Mitigadas

- **Interceptación de comunicaciones**: Los mensajes están cifrados end-to-end
- **Ataques man-in-the-middle**: Verificación obligatoria de fingerprints
- **Suplantación de identidad**: Autenticación mediante firmas digitales
- **Modificación de mensajes**: Detección de alteraciones mediante verificación criptográfica

## Consideraciones de Seguridad

### Procedimientos Recomendados

1. **Verificación de Fingerprints**: Siempre verificar los fingerprints a través de un canal de comunicación alternativo y seguro (teléfono, encuentro presencial)
2. **Gestión de Llaves**: Las llaves privadas nunca salen del dispositivo del usuario
3. **Validación de Firmas**: Verificar la validez de las firmas digitales en cada mensaje recibido

### Limitaciones del Sistema

- **Sin Forward Secrecy**: El compromiso de llaves privadas puede afectar mensajes históricos
- **Dependencia del Servidor**: Aunque el servidor no puede leer mensajes, su disponibilidad es necesaria para la comunicación
- **Escalabilidad**: El sistema está optimizado para comunicación entre dos participantes

## Detalles de Implementación

### Algoritmos Criptográficos Utilizados

- **Generación de Llaves**: RSA con exponente público 65537 y módulo de 2048 bits
- **Cifrado**: RSA-OAEP con SHA-256 y MGF1
- **Firma Digital**: RSA-PSS con SHA-256 y longitud de sal máxima
- **Hash de Verificación**: SHA-256 para generación de fingerprints

### Formato de Mensajes

Los mensajes intercambiados incluyen:

- Contenido cifrado en formato Base64
- Firma digital en formato Base64
- Timestamp de envío
- Identificación del remitente

### Arquitectura de la GUI

La interfaz gráfica utiliza:

- **tkinter**: Framework GUI nativo de Python para máxima compatibilidad
- **Threading**: Operaciones de red no bloqueantes para mantener la responsividad
- **Patrón Observer**: Callbacks para comunicación entre lógica y interfaz
- **Separación de responsabilidades**: Adaptadores GUI que no modifican el código original

## Personalización y Extensiones

### Configuración de Red

- Modificar host/puerto en las clases `SecureChatServer` y `SecureChatClient`
- Ajustar timeout de conexiones según requisitos de red

### Mejoras de Seguridad

- Incrementar tamaño de llaves RSA a 4096 bits para mayor seguridad a largo plazo
- Implementar rotación periódica de llaves
- Agregar forward secrecy mediante intercambio de llaves efímeras

### Escalabilidad

- Extender soporte para múltiples usuarios simultáneos
- Implementar salas de chat grupales
- Agregar persistencia de mensajes cifrados

### Personalización de la GUI

- Modificar tema de colores en `gui/styles.py`
- Ajustar tipografías y espaciados
- Agregar funcionalidades adicionales en las ventanas existentes

## Resolución de Problemas

### Problemas Comunes

- **Error de conexión**: Verificar que el servidor esté ejecutándose y el puerto esté disponible
- **Fallo en intercambio de llaves**: Asegurar que ambos clientes estén conectados simultáneamente
- **Firma inválida**: Verificar integridad de la conexión y validez de las llaves públicas
- **GUI no se inicia**: Verificar que tkinter esté instalado correctamente

### Logs y Depuración

El sistema proporciona logs detallados de:

- Estado de conexiones
- Intercambio de llaves públicas
- Retransmisión de mensajes cifrados
- Errores de comunicación

La interfaz gráfica incluye un monitor en tiempo real que muestra toda la actividad del servidor.

## Cumplimiento y Estándares

Este sistema implementa mejores prácticas de seguridad criptográfica basadas en:

- NIST SP 800-57: Recomendaciones para gestión de llaves criptográficas
- RFC 8017: PKCS #1 v2.2 - RSA Cryptography Specifications
- FIPS 186-4: Digital Signature Standard (DSS)