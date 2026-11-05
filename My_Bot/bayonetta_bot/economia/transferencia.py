import discord as DC
from discord.ext import commands
import random

from economia.moneda import (
    cargar_datos,
    guardar_datos,
    obtener_usuario
)


@commands.command(name="transferir")
async def transferir(ctx, destinatario: DC.Member, cantidad: int):

    # Evitar utilizar el comando fuera de un servidor
    if ctx.guild is None:
        return

    # Comprobar que la cantidad sea positiva
    if cantidad <= 0:
        await ctx.send("Una cantidad mayor que cero, darling.")
        return

    # Evitar transferencias a uno mismo
    if destinatario.id == ctx.author.id:
        await ctx.send("¿Regalarte Halos a ti misma? Qué vanidad, cariño.")
        return

    # Evitar transferencias a bots
    if destinatario.bot:
        await ctx.send("Los bots no necesitan Halos, darling.")
        return

    # Cargar los datos de la economía
    datos = cargar_datos()

    emisor = obtener_usuario(datos, ctx.author.id)
    receptor = obtener_usuario(datos, destinatario.id)

    # Comprobar que el emisor tenga suficiente dinero
    if emisor["halos"] < cantidad:
        await ctx.send("No tienes tantos Halos, cariño. Ve a trabajar")
        return

    # Realizar la transferencia
    emisor["halos"] -= cantidad
    receptor["halos"] += cantidad

    # Guardar los cambios
    guardar_datos(datos)

    frases = [
        "Qué generoso, cariño.",
        "Me gusta tu estilo, darling.",
        "Espero que lo merezca.",
        "Mmm, qué detalle.",
    ]

    # Crear confirmación
    embed = DC.Embed(
        title="💜 TRANSFERENCIA REALIZADA, CARIÑO",
        description=(
            f"{ctx.author.mention} ha enviado **{cantidad:,} Halos** "
            f"a {destinatario.mention}.\n"
            f"*{random.choice(frases)}*"
        ),
        color=DC.Color.dark_purple()
    )

    embed.add_field(
        name="Tu saldo restante",
        value=f"{emisor['halos']:,} Halos",
        inline=False
    )

    embed.add_field(
        name="Destinatario",
        value=destinatario.mention,
        inline=False
    )

    embed.set_footer(text="Proyecto Umbra | Transferencia")

    await ctx.send(embed=embed)