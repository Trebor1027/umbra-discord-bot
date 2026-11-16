## Inteligencia artificial

Proyecto UMBRA incorpora un sistema de inteligencia artificial basado en OpenAI, con una personalidad inspirada en Bayonetta.

El sistema permite mantener conversaciones con el bot mediante el comando `!umbra` o mencionándolo directamente en Discord.

### Características

- **Conversaciones con IA:** respuestas generadas a partir de los mensajes de los usuarios.
- **Personalidad personalizada:** estilo de conversación inspirado en Bayonetta.
- **Memoria contextual:** utilización de recuerdos almacenados para personalizar las respuestas.
- **Control de privacidad:** los recuerdos solo se utilizan como contexto de IA cuando el usuario ha autorizado su uso.
- **Memoria automática:** detección de determinados datos compartidos durante las conversaciones.
- **Control de peticiones:** evita procesar varias solicitudes de IA simultáneamente para un mismo usuario.

### Organización del sistema

La inteligencia artificial está dividida en diferentes módulos:

| Archivo | Responsabilidad |
|---|---|
| `cerebro.py` | Generación de respuestas mediante IA. |
| `contexto.py` | Construcción del contexto utilizando información disponible. |
| `personalidad.py` | Configuración de la personalidad del asistente. |
| `configuracion_ia.py` | Gestión de la autorización de memoria para IA. |

Esta separación permite mantener el código organizado y facilita la incorporación de nuevas funcionalidades.

## Sobre el proyecto

Proyecto UMBRA es un bot de Discord inspirado en el universo de Bayonetta, desarrollado en Python como parte de mi aprendizaje en programación, automatización e inteligencia artificial.

Es un **proyecto personal de aprendizaje guiado**, desarrollado progresivamente con apoyo de herramientas de inteligencia artificial para comprender conceptos, resolver problemas y mejorar la organización del código.

Lo que comenzó con unos pocos comandos básicos ha evolucionado hasta incorporar sistemas de economía, niveles, memoria persistente e inteligencia artificial.

Mi objetivo no es únicamente crear un bot funcional, sino comprender cómo funciona cada componente, adquirir experiencia práctica y seguir mejorando mis habilidades como desarrollador.