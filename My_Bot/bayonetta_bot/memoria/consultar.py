import discord
from discord.ext import commands
from memoria.base_datos import conectar


@commands.command(name="memoria")
async def consultar(ctx):
    usuario_id = str(ctx.author.id)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT categoria, informacion, origen, fecha
        FROM recuerdos
        WHERE usuario_id = ?
        ORDER BY id DESC
        LIMIT 10
    """, (usuario_id,))

    recuerdos = cursor.fetchall()
    conexion.close()

    if not recuerdos:
        await ctx.reply(
            "💜 Aún no sé nada de ti, darling. Cuéntame algo~"
        )
        return

    embed = discord.Embed(
        title="💜 MEMORIA DE BAYONETTA",
        description=f"Esto es lo que sé de ti, {ctx.author.display_name}, cariño~",
        color=discord.Color.dark_purple()
    )

    for numero, recuerdo in enumerate(recuerdos, start=1):
        categoria, informacion, origen, fecha = recuerdo

        embed.add_field(
            name=f"{numero}. {categoria.capitalize()}",
            value=(
                f"{informacion}\n"
                f"**Origen:** {origen}"
            ),
            inline=False
        )

    embed.set_footer(
        text=f"Proyecto Umbra | {len(recuerdos)} recuerdos guardados"
    )

    await ctx.reply(embed=embed)