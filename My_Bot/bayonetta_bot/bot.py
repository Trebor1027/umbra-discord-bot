
# ============================================================
# PROYECTO UMBRA: BAYONETTA BOT
# ARCHIVO PRINCIPAL - BOT.PY
# ============================================================


# ---------------------- LIBRERÍAS ----------------------

import os
from pathlib import Path

import discord as DC
from discord.ext import commands
from dotenv import load_dotenv


# ---------------------- CONFIGURACIÓN ----------------------

RUTA_ENV = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=RUTA_ENV)

intents = DC.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ---------------------- EVENTO READY ----------------------

@bot.event
async def on_ready():

    ruta = Path(__file__).parent / "videos" / "bayonetta.txt"

    try:
        with open(ruta, encoding="utf-8") as archivo:
            print(archivo.read())

    except FileNotFoundError:
        print("(no se encontró bayonetta.txt)")

    print(
        f"¡{bot.user.name} ha llegado, cariño! "
        "El espectáculo está a punto de comenzar."
    )


# ============================================================
# FUNCIONES BÁSICAS
# ============================================================

from funciones_basicas.hola import hola
from funciones_basicas.adios import adios
from funciones_basicas.repetir import repetir

bot.add_command(hola)
bot.add_command(adios)
bot.add_command(repetir)


# ============================================================
# RADIO
# ============================================================

from radio.unirse_radio import unirse
from radio.salir_radio import salir
from radio.encender_radio import radio
from radio.funciones_radio import pausa, reanudar

bot.add_command(unirse)
bot.add_command(salir)
bot.add_command(radio)
bot.add_command(pausa)
bot.add_command(reanudar)


# ============================================================
# VÍDEOS
# ============================================================

from videos.presentacion import hola_imagen
from videos.adios import adios_imagen
from videos.meme import meme_imagen


# ============================================================
# LIMPIAR CHAT Y LISTA DE COMANDOS
# ============================================================

from funciones_basicas.limpiar import limpiar
from funciones_basicas.decir_comandos import comandos

bot.add_command(limpiar)
bot.add_command(comandos)


# ============================================================
# MODERACIÓN
# ============================================================

from funciones_basicas.banear import detectar_insultos


@bot.listen("on_message")
async def controlar_insultos(message):

    if message.author.bot:
        return

    await detectar_insultos(message)


# ============================================================
# ECONOMÍA
# ============================================================

from economia.moneda import saldo, diario, trabajar, ranking
from economia.transferencia import transferir

bot.add_command(saldo)
bot.add_command(diario)
bot.add_command(trabajar)
bot.add_command(ranking)
bot.add_command(transferir)


# ============================================================
# TIENDA
# ============================================================

from economia.tienda import tienda, comprar, inventario

bot.add_command(tienda)
bot.add_command(comprar)
bot.add_command(inventario)


# ============================================================
# NIVELES
# ============================================================

from economia.niveles import nivel, procesar_experiencia

bot.add_command(nivel)


@bot.listen("on_message")
async def sistema_experiencia(message):

    if message.author.bot:
        return

    await procesar_experiencia(message)


# ============================================================
# SISTEMA DE MEMORIA
# ============================================================

from memoria.base_datos import crear_tablas

from memoria.recordar import recordar
from memoria.consultar import consultar
from memoria.olvidar import olvidar
from memoria.misdatos import misdatos

from memoria.configuracion import memoria_auto

# Crear las tablas y actualizar su estructura
crear_tablas()

bot.add_command(recordar)
bot.add_command(consultar)
bot.add_command(olvidar)
bot.add_command(misdatos)
bot.add_command(memoria_auto)


# ============================================================
# MEMORIA AUTOMÁTICA
# ============================================================

from memoria.detector import (
    detectar_recuerdo,
    guardar_recuerdo_automatico
)


# ============================================================
# MEMORIA CON INTELIGENCIA ARTIFICIAL
# ============================================================

from memoria.configuracion_ia import (
    memoria_ia,
    memoria_ia_autorizada
)

bot.add_command(memoria_ia)


# ============================================================
# CEREBRO DE BAYONETTA
# ============================================================

from inteligencia.cerebro import generar_respuesta
from inteligencia.contexto import construir_contexto


# Evitar peticiones simultáneas del mismo usuario
usuarios_ia_activos = set()


async def responder_umbra(message, pregunta: str):
    """
    Genera una respuesta utilizando OpenAI.

    Solo utiliza recuerdos guardados cuando el usuario
    ha autorizado expresamente la memoria con IA.
    """

    usuario_id = str(message.author.id)

    # Evitar peticiones simultáneas
    if usuario_id in usuarios_ia_activos:

        await message.reply(
            "Un momento, darling. Ya estoy pensando "
            "en tu anterior pregunta. 💋",
            mention_author=False
        )

        return

    usuarios_ia_activos.add(usuario_id)

    try:

        # --------------------------------------------
        # 1. COMPROBAR PERMISO DE MEMORIA IA
        # --------------------------------------------

        contexto = ""

        if memoria_ia_autorizada(usuario_id):

            contexto = construir_contexto(
                usuario_id,
                pregunta
            )

        # --------------------------------------------
        # 2. GENERAR RESPUESTA
        # --------------------------------------------

        async with message.channel.typing():

            respuesta = await generar_respuesta(
                mensaje=pregunta,
                contexto=contexto
            )

        # --------------------------------------------
        # 3. ENVIAR RESPUESTA A DISCORD
        # --------------------------------------------

        if not respuesta or not respuesta.strip():

            await message.channel.send(
                "Parece que me he quedado sin palabras, "
                "darling. Qué situación tan poco habitual. 💋"
            )

            return

        # Discord permite un máximo de 2000 caracteres.
        # Dividimos los mensajes largos en fragmentos.

        for inicio in range(0, len(respuesta), 1900):

            fragmento = respuesta[
                inicio:inicio + 1900
            ]

            await message.channel.send(fragmento)

    except Exception as error:

        print(
            f"[UMBRA IA] Error: "
            f"{type(error).__name__}: {error}"
        )

        await message.channel.send(
            "Mi magia ha sufrido una pequeña "
            "interrupción, cariño. "
            "Inténtalo más tarde. 💜"
        )

    finally:

        usuarios_ia_activos.discard(usuario_id)


# ============================================================
# COMANDO !UMBRA
# ============================================================

@bot.command(name="umbra")
async def hablar_con_umbra(ctx, *, pregunta: str = None):

    if not pregunta:

        await ctx.reply(
            "¿Querías hablar conmigo, darling? "
            "Escribe `!umbra` seguido de tu pregunta. 💋"
        )

        return

    await responder_umbra(
        ctx.message,
        pregunta
    )


# ============================================================
# EVENTO PRINCIPAL DE MENSAJES
# ============================================================

@bot.event
async def on_message(message):

    # --------------------------------------------
    # 1. IGNORAR OTROS BOTS
    # --------------------------------------------

    if message.author.bot:
        return

    contenido = message.content.strip()

    # --------------------------------------------
    # 2. PROCESAR COMANDOS
    # --------------------------------------------

    if contenido.startswith("!"):

        await bot.process_commands(message)
        return

    # --------------------------------------------
    # 3. SISTEMA DE VÍDEOS
    # --------------------------------------------

    await hola_imagen(message)
    await adios_imagen(message)
    await meme_imagen(message)

    # --------------------------------------------
    # 4. MEMORIA AUTOMÁTICA
    # --------------------------------------------

    resultado = detectar_recuerdo(contenido)

    if resultado:

        categoria, informacion = resultado

        guardado = guardar_recuerdo_automatico(
            str(message.author.id),
            categoria,
            informacion
        )

        if guardado:

            await message.reply(
                "He aprendido algo nuevo sobre ti, "
                "darling. 💜",
                mention_author=False
            )

    # --------------------------------------------
    # 5. RESPONDER A MENCIONES
    # --------------------------------------------

    if bot.user and bot.user.mentioned_in(message):

        pregunta = contenido.replace(
            f"<@{bot.user.id}>",
            ""
        ).replace(
            f"<@!{bot.user.id}>",
            ""
        ).strip()

        if not pregunta:

            pregunta = (
                "Hola Bayonetta, "
                "preséntate brevemente."
            )

        await responder_umbra(
            message,
            pregunta
        )

    # --------------------------------------------
    # 6. MANTENER LOS COMANDOS DE DISCORD
    # --------------------------------------------

    await bot.process_commands(message)


# ============================================================
# EJECUCIÓN DEL BOT
# ============================================================

if __name__ == "__main__":

    token = os.getenv("DISCORD_TOKEN")

    if not token:

        raise RuntimeError(
            "UMBRA: No se encontró "
            "DISCORD_TOKEN en .env"
        )

    bot.run(token)
