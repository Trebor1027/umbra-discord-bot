from discord.ext import commands
from memoria.base_datos import conectar


@commands.command()
async def olvidar(ctx, seleccion: str):
    usuario_id = str(ctx.author.id)

    conexion = conectar()
    cursor = conexion.cursor()

    # Eliminar todos los recuerdos del usuario
    if seleccion.lower() == "todo":

        cursor.execute("""
            DELETE FROM recuerdos
            WHERE usuario_id = ?
        """, (usuario_id,))

        cantidad = cursor.rowcount

        conexion.commit()
        conexion.close()

        await ctx.reply(
            f"He eliminado tus {cantidad} recuerdos."
        )
        return

    # Comprobar que se ha introducido un número
    if not seleccion.isdigit() or int(seleccion) < 1:
        conexion.close()
        await ctx.reply(
            "Indica un número válido o escribe `!olvidar todo`."
        )
        return

    numero = int(seleccion)

    # Recuperar los identificadores en el mismo orden que !memoria
    cursor.execute("""
        SELECT id
        FROM recuerdos
        WHERE usuario_id = ?
        ORDER BY id DESC
    """, (usuario_id,))

    recuerdos = cursor.fetchall()

    if numero > len(recuerdos):
        conexion.close()
        await ctx.reply(
            "No existe un recuerdo con ese número."
        )
        return

    # Identificar el recuerdo seleccionado
    recuerdo_id = recuerdos[numero - 1][0]

    cursor.execute("""
        DELETE FROM recuerdos
        WHERE id = ? AND usuario_id = ?
    """, (recuerdo_id, usuario_id))

    conexion.commit()
    conexion.close()

    await ctx.reply(
        f"He olvidado el recuerdo número {numero}."
    )
