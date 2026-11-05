import discord as DC
from discord.ext import commands
import json
import random
import time
from pathlib import Path

# Ruta del archivo donde guardaremos el dinero
RUTA_DATOS = Path(__file__).parent / "datos.json"

# IMAGENES DE LA ECONOMIA

IMAGEN_SALDO = "https://i.pinimg.com/originals/6e/77/df/6e77dfc69107af3d89a3ec7b1a39c5d6.jpg"
IMAGEN_DIARIO = "https://i.pinimg.com/736x/0a/aa/e5/0aaae5769db82aa062ee977f2add931b.jpg"
IMAGEN_TRABAJO = "https://th.bing.com/th/id/R.a7467502802570bf41fabf4587330c11?rik=acokjhVokaY2GQ&pid=ImgRaw&r=0"
IMAGEN_RANKING = "https://static1.personalitydatabase.net/2/pdb-images-prod/49b6760e/profile_images/cdcd0fb310a14985b29468cd810c706b.png"

#-------------SISTEMA DE ALMACENAMIENTO-------------

def cargar_datos():
    if not RUTA_DATOS.exists():
        RUTA_DATOS.write_text("{}", encoding="utf-8")

    with open(RUTA_DATOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_datos(datos):
    with open(RUTA_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)


def obtener_usuario(datos, usuario_id):
    usuario_id = str(usuario_id)

    if usuario_id not in datos:
        datos[usuario_id] = {
            "halos": 0,
            "ultimo_diario": None,
            "ultimo_trabajo": 0,
            "inventario": []
        }

    # Añadir inventario a cuentas antiguas
    if "inventario" not in datos[usuario_id]:
        datos[usuario_id]["inventario"] = []

    return datos[usuario_id]


#-----------------------------COMANDOS ECONOMICOS-----------------------------

@commands.command(name="saldo")
async def saldo(ctx, usuario: DC.Member = None):

    usuario = usuario or ctx.author

    datos = cargar_datos()
    cuenta = obtener_usuario(datos, usuario.id)
    guardar_datos(datos)

    halos = cuenta["halos"]
    es_otro = usuario != ctx.author

    if halos == 0:
        comentario = random.choice([
            "Ni un Halo... qué triste, darling.",
            "Bolsillos vacíos, cariño. Ve a trabajar.",
        ])
    elif halos < 500:
        comentario = random.choice([
            "Un comienzo humilde, cariño",
            "Poquito, pero con potencial, darling.",
        ])
    elif halos < 5000:
        comentario = random.choice([
            "Mmm, nada mal, cariño",
            "Vas bien, darling. Sigue así.",
        ])
    else:
        comentario = random.choice([
            "Vaya, vaya... ¿y mi invitación, darling?",
            "Una fortuna digna de Umbra, cariño",
        ])

    posesivo = f"la fortuna de {usuario.mention}" if es_otro else "tu fortuna"

    embed = DC.Embed(
        title="💜 BANCO DE UMBRA",
        description=f"Veamos {posesivo}, cariño...\n\n*{comentario}*",
        color=DC.Color.dark_purple()
    )

    embed.add_field(
        name="Halos disponibles",
        value=f"**{halos:,} Halos**",
        inline=False
    )

    embed.set_image(url=IMAGEN_SALDO)
    embed.set_footer(text="Proyecto Umbra | Banco de Bayonetta")

    await ctx.send(embed=embed)


#-----------------------------COMANDO: !DIARIO-----------------------------

@commands.command(name="diario")
async def diario(ctx):

    datos = cargar_datos()
    cuenta = obtener_usuario(datos, ctx.author.id)

    hoy = time.strftime("%Y-%m-%d", time.gmtime())

    if cuenta["ultimo_diario"] == hoy:

        embed = DC.Embed(
            title="💜 NO SEAS AVARICIOSO, CARIÑO",
            description=(
                f"{ctx.author.mention}, ya cobraste hoy.\n"
                "Vuelve mañana, cariño~"
            ),
            color=DC.Color.dark_purple()
        )

        embed.set_image(url=IMAGEN_DIARIO)
        embed.set_footer(text="Proyecto Umbra | Recompensa diaria")
        await ctx.send(embed=embed)
        return

    recompensa = random.randint(100, 250)

    cuenta["halos"] += recompensa
    cuenta["ultimo_diario"] = hoy

    guardar_datos(datos)

    frases = [
        "Hoy estoy generosa, no te acostumbres, darling.",
        "Te lo has ganado, darling.",
        "Gástalo con estilo, cariño.",
        "Un regalito de tu bruja favorita.",
    ]

    embed = DC.Embed(
        title="💜 RECOMPENSA RECIBIDA, CARIÑO",
        description=(
            f"{ctx.author.mention}\n"
            f"*{random.choice(frases)}*"
        ),
        color=DC.Color.dark_purple()
    )

    embed.add_field(
        name="Halos ganados",
        value=f"**+{recompensa} Halos**",
        inline=True
    )

    embed.add_field(
        name="Nuevo saldo",
        value=f"**{cuenta['halos']:,} Halos**",
        inline=True
    )

    embed.set_image(url=IMAGEN_DIARIO)
    embed.set_footer(text="Proyecto Umbra | Recompensa diaria")

    await ctx.send(embed=embed)


#-----------------------------COMANDO: !TRABAJAR-----------------------------

@commands.command(name="trabajar")
async def trabajar(ctx):

    datos = cargar_datos()
    cuenta = obtener_usuario(datos, ctx.author.id)

    ahora = time.time()
    espera = 3600

    tiempo_restante = espera - (ahora - cuenta["ultimo_trabajo"])

    if tiempo_restante > 0:

        minutos = int(tiempo_restante // 60) + 1

        embed = DC.Embed(
            title="💜 DESCANSO, DARLING",
            description=(
                f"{ctx.author.mention}, hasta las brujas descansan.\n"
                f"Vuelve en **{minutos} minutos**, cariño"
            ),
            color=DC.Color.dark_purple()
        )

        embed.set_image(url=IMAGEN_TRABAJO)
        embed.set_footer(text="Proyecto Umbra | Trabajo")
        await ctx.send(embed=embed)
        return

    recompensa = random.randint(20, 100)

    trabajos = [
        "Has cazado unos cuantos ángeles. Elegante, darling.",
        "Has ayudado a Bayonetta. Casi no estorbaste~",
        "Has limpiado las calles. Ni un rasguño, cariño.",
        "Un encargo para Rodin. No preguntes qué llevaba.",
        "Has encontrado un tesoro. Buen ojo, darling.",
        "Has bailado con la muerte y ganaste~",
    ]

    cuenta["halos"] += recompensa
    cuenta["ultimo_trabajo"] = ahora

    guardar_datos(datos)

    embed = DC.Embed(
        title="💜 TRABAJO COMPLETADO, CARIÑO",
        description=(
            f"{ctx.author.mention}\n"
            f"*{random.choice(trabajos)}*"
        ),
        color=DC.Color.dark_purple()
    )

    embed.add_field(
        name="Recompensa",
        value=f"**+{recompensa} Halos**",
        inline=True
    )

    embed.add_field(
        name="Nuevo saldo",
        value=f"**{cuenta['halos']:,} Halos**",
        inline=True
    )

    embed.set_image(url=IMAGEN_TRABAJO)
    embed.set_footer(text="Proyecto Umbra | Trabajo")

    await ctx.send(embed=embed)


#-----------------------------COMANDO: !RANKING-----------------------------

@commands.command(name="ranking")
async def ranking(ctx):

    if ctx.guild is None:
        return

    datos = cargar_datos()

    if not datos:
        await ctx.send("Nadie tiene Halos todavía, darling. Qué aburrimiento")
        return

    mejores = sorted(
        datos.items(),
        key=lambda x: x[1]["halos"],
        reverse=True
    )[:10]

    posiciones = []

    for posicion, (usuario_id, cuenta) in enumerate(mejores, start=1):

        miembro = ctx.guild.get_member(int(usuario_id))

        # Si no está en caché, buscarlo directamente en Discord
        if miembro is None:
            try:
                miembro = await ctx.guild.fetch_member(int(usuario_id))
            except (DC.NotFound, DC.Forbidden, DC.HTTPException, ValueError):
                miembro = None

        nombre = miembro.display_name if miembro else "Un fantasma de Umbra"

        posiciones.append(
            f"**{posicion}.** {nombre}\n"
            f"{cuenta['halos']:,} Halos"
        )

    descripcion = (
        "Los más ricos de Umbra, cariño\n\n"
        + "\n\n".join(posiciones)
        + "\n\n*¿No estás aquí? Ya sabes qué hacer, darling.*"
    )

    embed = DC.Embed(
        title="💜 LOS MÁS RICOS DE UMBRA",
        description=descripcion,
        color=DC.Color.dark_purple()
    )

    embed.set_image(url=IMAGEN_RANKING)
    embed.set_footer(text="Proyecto Umbra | Ranking de riqueza")

    await ctx.send(embed=embed)