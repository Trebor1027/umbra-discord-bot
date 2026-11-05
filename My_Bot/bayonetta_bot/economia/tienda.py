import discord as DC
from discord.ext import commands
import random

# Importar funciones del sistema económico
from economia.moneda import (
    cargar_datos,
    guardar_datos,
    obtener_usuario
)


#-----------------------------OBJETOS DE LA TIENDA-----------------------------

OBJETOS = {
    "1": {
        "nombre": "Cazador de ángeles",
        "precio": 500,
        "tipo": "Título",
        "descripcion": "Un cazador digno de Umbra, darling."
    },

    "2": {
        "nombre": "Bruja de Umbra",
        "precio": 1000,
        "tipo": "Título",
        "descripcion": "Solo para los elegidos, cariño"
    },

    "3": {
        "nombre": "Leyenda de Umbra",
        "precio": 3000,
        "tipo": "Título",
        "descripcion": "Casi tan legendario como yo."
    },

    "4": {
        "nombre": "Gafas de Bayonetta",
        "precio": 750,
        "tipo": "Accesorio",
        "descripcion": "Elegancia y peligro, darling"
    },

    "5": {
        "nombre": "Medalla dorada",
        "precio": 1500,
        "tipo": "Accesorio",
        "descripcion": "Para que todos vean tu prestigio."
    }
}


# URL de la imagen de la tienda
IMAGEN_TIENDA = "https://i.pinimg.com/736x/07/df/ef/07dfef6281c428f36e507bae295adfcd.jpg"


#-----------------------------COMANDO: !TIENDA-----------------------------

@commands.command(name="tienda")
async def tienda(ctx):

    embed = DC.Embed(
        title="💜 TIENDA DE UMBRA",
        description=(
            "Bienvenido, cariño.\n"
            "Mira qué tentaciones tengo para ti, darling.\n\n"
        ),
        color=DC.Color.dark_purple()
    )

    for identificador, objeto in OBJETOS.items():

        embed.add_field(
            name=f"ID {identificador} - {objeto['nombre']}",
            value=(
                f"**Tipo:** {objeto['tipo']}\n"
                f"**Precio:** {objeto['precio']:,} Halos\n"
                f"*{objeto['descripcion']}*"
            ),
            inline=False
        )

    embed.add_field(
        name="¿Cómo comprar?",
        value="Escribe `!comprar ID`, darling.",
        inline=False
    )

    embed.set_image(url=IMAGEN_TIENDA)
    embed.set_footer(text="Proyecto Umbra | Tienda oficial")

    await ctx.send(embed=embed)


#-----------------------------COMANDO: !COMPRAR-----------------------------

@commands.command(name="comprar")
async def comprar(ctx, identificador: str):

    if identificador not in OBJETOS:
        await ctx.send("Ese objeto no existe, darling.")
        return

    datos = cargar_datos()
    cuenta = obtener_usuario(datos, ctx.author.id)

    objeto = OBJETOS[identificador]

    # Comprobar si ya tiene el objeto
    if identificador in cuenta["inventario"]:
        await ctx.send("Ya lo tienes, cariño. No seas codicioso")
        return

    # Comprobar el dinero disponible
    if cuenta["halos"] < objeto["precio"]:
        await ctx.send(
            f"Te faltan Halos, darling.\n"
            f"Necesitas {objeto['precio']:,}."
        )
        return

    # Realizar la compra
    cuenta["halos"] -= objeto["precio"]
    cuenta["inventario"].append(identificador)

    guardar_datos(datos)

    frases = [
        "Buena elección, cariño~",
        "Te queda de maravilla, darling.",
        "Un capricho bien merecido.",
        "Mmm, tienes buen gusto~",
    ]

    embed = DC.Embed(
        title="💜 COMPRA REALIZADA, CARIÑO",
        description=(
            f"{ctx.author.mention}, ahora tienes "
            f"**{objeto['nombre']}**.\n"
            f"*{random.choice(frases)}*"
        ),
        color=DC.Color.dark_purple()
    )

    embed.add_field(
        name="Precio",
        value=f"{objeto['precio']:,} Halos",
        inline=True
    )

    embed.add_field(
        name="Saldo restante",
        value=f"{cuenta['halos']:,} Halos",
        inline=True
    )

    embed.add_field(
        name="Objeto adquirido",
        value=f"*{objeto['descripcion']}*",
        inline=False
    )

    embed.set_footer(
        text="Proyecto Umbra | Un placer hacer negocios"
    )

    await ctx.send(embed=embed)


#-----------------------------COMANDO: !INVENTARIO-----------------------------

@commands.command(name="inventario")
async def inventario(ctx, usuario: DC.Member = None):

    usuario = usuario or ctx.author

    datos = cargar_datos()
    cuenta = obtener_usuario(datos, usuario.id)

    guardar_datos(datos)

    embed = DC.Embed(
        title="💜 INVENTARIO DE UMBRA",
        description=f"Veamos qué guarda {usuario.mention}, cariño...",
        color=DC.Color.dark_purple()
    )

    if not cuenta["inventario"]:

        embed.description += "\n\n*Vacío, darling. Qué triste*"

    else:

        for identificador in cuenta["inventario"]:

            objeto = OBJETOS.get(identificador)

            if objeto:
                embed.add_field(
                    name=f"{objeto['nombre']}",
                    value=f"{objeto['tipo']} | ID: {identificador}",
                    inline=False
                )

    embed.set_footer(
        text="Proyecto Umbra | Tus objetos son permanentes"
    )

    await ctx.send(embed=embed)