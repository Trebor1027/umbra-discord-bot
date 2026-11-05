from discord.ext import commands
from memoria.base_datos import conectar


@commands.command()
async def recordar(ctx, *, informacion: str):
    usuario_id = str(ctx.author.id)

    # Comprobamos que el recuerdo no esté vacío
    if not informacion.strip():
        await ctx.reply("No puedo guardar un recuerdo vacío.")
        return

    # Guardamos el recuerdo en SQLite
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO recuerdos
        (usuario_id, categoria, informacion, origen)
        VALUES (?, ?, ?, ?)
    """, (usuario_id, "general", informacion.strip(), "manual"))

    conexion.commit()
    conexion.close()

    await ctx.reply(
        f"He guardado este recuerdo:\n"
        f"«{informacion.strip()}»"
    )
