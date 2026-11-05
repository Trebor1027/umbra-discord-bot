
import os
import discord as DC
from discord.ext import commands


async def enviar_con_imagen(ctx, texto, imagen_url):
    embed = DC.Embed(description=texto)
    embed.set_image(url=imagen_url)
    await ctx.send(embed=embed)


@commands.command()
async def unirse(ctx):

    # Comprobar si el usuario está en un canal de voz
    if ctx.author.voice is None:
        await ctx.send("Primero entra a un canal de voz cariño.")
        return

    canal = ctx.author.voice.channel

    # Conectarse o cambiar de canal
    if ctx.voice_client:
        voz = ctx.voice_client

        if voz.channel != canal:
            await voz.move_to(canal)
    else:
        voz = await canal.connect()

    # Detener cualquier reproducción anterior
    if voz.is_playing() or voz.is_paused():
        voz.stop()

    # Buscar el archivo de bienvenida
    ruta_audio = os.path.join(
        os.path.dirname(__file__),
        "audio",
        "bienvenida.mp3"
    )

    # Comprobar que existe el archivo
    if not os.path.isfile(ruta_audio):
        await ctx.send("No encuentro el audio de bienvenida cariño.")
        return

    # Reproducir automáticamente
    audio = DC.FFmpegPCMAudio(ruta_audio)

    voz.play(audio)

    # Mensaje de bienvenida
    await enviar_con_imagen(
        ctx,
        "Bayonetta ha llegado a ponerle ritmo a este canal.",
        "https://i.pinimg.com/originals/dc/9e/77/dc9e77f4114bcdf95e42e3a16fe3ed10.gif"
    )

  

