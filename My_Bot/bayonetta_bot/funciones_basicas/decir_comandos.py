from discord.ext import commands
import discord as DC

IMAGEN_COMANDOS = "https://tse3.mm.bing.net/th/id/OIP.8Qtaz996ilSCLxTb7PbxFwHaEK?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"

@commands.command()
async def comandos(ctx):
    texto = (
        "¿Qué puedo hacer por ti, cariño?\n\n"
        "**Para charlar conmigo**\n"
        "`!hola` - un saludito, no muerdo\n"
        "`!adios` - me echarás de menos\n"
        "`!comandos` - todo lo que sé hacer\n"
        "`!repetir` - dime algo bonito~\n"
        "`!limpiar` - borro mensajes sin dejar rastro (solo admins)\n\n"

        "**Para la radio**\n"
        "`!unirse` - entro a tu canal de voz\n"
        "`!salir` - me voy, con estilo\n"
        "`!radio` - música para la noche\n"
        "`!pausa` - silencio, mírame a mí\n"
        "`!reanudar` - que siga la música~\n\n"

        "**Para mi memoria**\n"
        "`!recordar <información>` - cuéntame un secreto~\n"
        "`!consultar` - tus últimos 10 recuerdos\n"
        "`!olvidar <ID>` - como si nunca hubiera existido\n"
        "`!misdatos` - lo que sé de ti, darling\n"
        "`!memoria_auto activar` - mis oídos atrapan tus secretos\n"
        "`!memoria_auto desactivar` - cierro los oídos\n\n"

        "**Para la economía**\n"
        "`!saldo` - mira tu fortuna, cariño\n"
        "`!diario` - tu recompensa de Halos\n"
        "`!trabajar` - gana unos Halos\n"
        "`!ranking` - los más ricos de Umbra\n"
        "`!transferir @usuario cantidad` - regala Halos~\n\n"

        "**Para la tienda**\n"
        "`!tienda` - mis tentaciones para ti\n"
        "`!comprar (ID)` - date un capricho\n"
        "`!inventario` - tus tesoros, darling\n\n"

        "**Para los niveles**\n"
        "`!nivel` - cuánto has crecido\n"
        "`!nivel @usuario` - cotillea a otro, no diré nada~\n"
    )

    embed = DC.Embed(
        title="💜 COMANDOS DE BAYONETTA",
        description=texto,
        color=0xFF69B4
    )
    embed.set_image(url=IMAGEN_COMANDOS)

    await ctx.send(embed=embed)