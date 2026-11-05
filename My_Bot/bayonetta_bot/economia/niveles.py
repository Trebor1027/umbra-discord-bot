import discord as DC
from discord.ext import commands
import random
import time

from economia.moneda import (
    cargar_datos,
    guardar_datos,
    obtener_usuario
)


# Configuración del sistema
XP_MINIMA = 10
XP_MAXIMA = 20
TIEMPO_ESPERA = 60


async def procesar_experiencia(message):

    # Ignorar mensajes privados y mensajes de bots
    if message.guild is None or message.author.bot:
        return

    datos = cargar_datos()
    usuario = obtener_usuario(datos, message.author.id)

    # Crear los datos de nivel si no existen
    usuario.setdefault("xp", 0)
    usuario.setdefault("nivel", 0)
    usuario.setdefault("ultimo_mensaje", 0)

    ahora = time.time()

    # Evitar ganar XP enviando mensajes continuamente
    if ahora - usuario["ultimo_mensaje"] < TIEMPO_ESPERA:
        return

    usuario["ultimo_mensaje"] = ahora

    # Otorgar experiencia aleatoria
    experiencia = random.randint(XP_MINIMA, XP_MAXIMA)
    usuario["xp"] += experiencia

    # Comprobar si ha subido de nivel
    subida = False

    while usuario["xp"] >= (usuario["nivel"] + 1) * 100:
        experiencia_necesaria = (usuario["nivel"] + 1) * 100

        usuario["xp"] -= experiencia_necesaria
        usuario["nivel"] += 1
        subida = True

    guardar_datos(datos)

    # Avisar cuando suba de nivel
    if subida:

        frases = [
            "Mmm, empiezas a gustarme~",
            "Cada vez más fuerte, darling.",
            "Así me gusta, cariño. Sigue así",
            "Los ángeles ya deberían temerte.",
        ]

        embed = DC.Embed(
            title="💜 ¡NUEVO NIVEL, CARIÑO!",
            description=(
                f"{message.author.mention}, has llegado al nivel **{usuario['nivel']}**.\n"
                f"*{random.choice(frases)}*"
            ),
            color=DC.Color.dark_purple()
        )

        await message.channel.send(embed=embed)


@commands.command(name="nivel")
async def nivel(ctx, miembro: DC.Member = None):

    miembro = miembro or ctx.author

    datos = cargar_datos()
    usuario = obtener_usuario(datos, miembro.id)

    usuario.setdefault("xp", 0)
    usuario.setdefault("nivel", 0)

    nivel_actual = usuario["nivel"]
    xp_actual = usuario["xp"]
    xp_necesaria = (nivel_actual + 1) * 100

    if nivel_actual < 5:
        comentario = "Aún eres un aprendiz, darling"
    elif nivel_actual < 15:
        comentario = "Mmm, vas mejorando, cariño."
    elif nivel_actual < 30:
        comentario = "Ya empiezas a impresionarme, darling"
    else:
        comentario = "Toda una bruja de Umbra, cariño."

    embed = DC.Embed(
        title=f"💜 Nivel de {miembro.display_name}",
        description=f"*{comentario}*",
        color=DC.Color.dark_purple()
    )

    embed.add_field(
        name="Nivel",
        value=f"**{nivel_actual}**",
        inline=True
    )

    embed.add_field(
        name="Experiencia",
        value=f"**{xp_actual}/{xp_necesaria} XP**",
        inline=True
    )

    embed.set_thumbnail(url=miembro.display_avatar.url)

    await ctx.send(embed=embed)