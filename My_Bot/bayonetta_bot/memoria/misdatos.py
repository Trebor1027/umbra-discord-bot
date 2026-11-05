import discord
from discord.ext import commands
from memoria.base_datos import conectar


@commands.command()
async def misdatos(ctx):
    usuario_id = str(ctx.author.id)

    conexion = conectar()
    cursor = conexion.cursor()

    # Contar recuerdos manuales
    cursor.execute("""
        SELECT COUNT(*)
        FROM recuerdos
        WHERE usuario_id = ? AND origen = 'manual'
    """, (usuario_id,))

    manuales = cursor.fetchone()[0]

    # Contar recuerdos automáticos
    cursor.execute("""
        SELECT COUNT(*)
        FROM recuerdos
        WHERE usuario_id = ? AND origen = 'automatico'
    """, (usuario_id,))

    automaticos = cursor.fetchone()[0]

    # Consultar configuración de memoria
    cursor.execute("""
        SELECT memoria_automatica
        FROM configuracion
        WHERE usuario_id = ?
    """, (usuario_id,))

    configuracion = cursor.fetchone()

    conexion.close()

    total = manuales + automaticos

    estado = (
        "Activada" if configuracion and configuracion[0] == 1
        else "Desactivada"
    )

    # Crear el mensaje
    embed = discord.Embed(
        title="Tus datos personales",
        description=f"Información almacenada sobre {ctx.author.display_name}",
        color=discord.Color.dark_purple()
    )

    embed.add_field(
        name="Recuerdos totales",
        value=str(total),
        inline=True
    )

    embed.add_field(
        name="Manuales",
        value=str(manuales),
        inline=True
    )

    embed.add_field(
        name="Automáticos",
        value=str(automaticos),
        inline=True
    )

    embed.add_field(
        name="Memoria automática",
        value=estado,
        inline=False
    )

    await ctx.reply(embed=embed)
