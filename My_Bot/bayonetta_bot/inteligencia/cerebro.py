

#------------PROYECTO UMBRA: BAYONETTA BOT------------------
#------------CEREBRO DE INTELIGENCIA ARTIFICIAL-------------


import os
from pathlib import Path

from dotenv import load_dotenv
from openai import (
    AsyncOpenAI,
    APIConnectionError,
    APIStatusError,
    RateLimitError,
)

from inteligencia.personalidad import PERSONALIDAD_UMBRA


# ---------------- CONFIGURACIÓN ----------------

# El archivo .env está en la carpeta My_Bot exterior.
RUTA_ENV = Path(__file__).resolve().parents[3] / ".env"

load_dotenv(dotenv_path=RUTA_ENV)

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        f"UMBRA: No se encontró OPENAI_API_KEY en {RUTA_ENV}"
    )

MODELO_IA = os.getenv("OPENAI_MODEL", "gpt-5-mini")

cliente = AsyncOpenAI(
    api_key=API_KEY,
    timeout=30.0,
    max_retries=1
)


# ---------------- CEREBRO DE UMBRA ----------------

async def generar_respuesta(
    mensaje: str,
    contexto: str = ""
) -> str:
    """
    Genera respuestas utilizando OpenAI.

    mensaje:
        Mensaje enviado por el usuario.

    contexto:
        Contexto adicional opcional.
        Más adelante permitirá integrar recuerdos
        relevantes de la memoria híbrida.
    """

    if not mensaje or not mensaje.strip():
        return "¿Te has quedado sin palabras, darling? "

    # Construir la entrada de la conversación.
    entrada = mensaje.strip()

    if contexto and contexto.strip():
        entrada = (
            "Contexto adicional proporcionado por el sistema:\n"
            f"{contexto.strip()}\n\n"
            "Mensaje actual del usuario:\n"
            f"{entrada}"
        )

    try:
        respuesta = await cliente.responses.create(
            model=MODELO_IA,

            instructions=PERSONALIDAD_UMBRA,

            input=entrada,

            max_output_tokens=700
        )

        texto = respuesta.output_text.strip()

        if not texto:
            print(
                "[UMBRA] Respuesta vacía.",
                "Estado:", respuesta.status,
                "Detalles:", respuesta.incomplete_details
            )

            return (
                "Vaya, parece que hasta la magia "
                "necesita un pequeño descanso, darling. "
            )

        return texto

    except RateLimitError as error:
        print(f"[UMBRA] Error de cuota o límite: {error}")

        return (
            "Parece que mi magia está temporalmente "
            "limitada, cariño. Inténtalo más tarde."
        )

    except APIConnectionError as error:
        print(f"[UMBRA] Error de conexión: {error}")

        return (
            "Qué fastidio... Parece que he perdido "
            "la conexión con el mundo exterior."
        )

    except APIStatusError as error:
        print(
            f"[UMBRA] Error de API: {error.status_code}"
        )

        return (
            "Algo ha salido mal entre bastidores, "
            "darling. Dame otro momento."
        )