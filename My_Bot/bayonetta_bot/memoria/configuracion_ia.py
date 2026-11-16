
from discord.ext import commands
from memoria.base_datos import conectar


def memoria_ia_autorizada(usuario_id):
    conexion = conectar()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT memoria_ia
            FROM configuracion
            WHERE usuario_id = ?
        """, (str(usuario_id),))

        resultado = cursor.fetchone()
        return resultado is not None and resultado[0] == 1

    finally:
        conexion.close()


@commands.command(name="memoria_ia")
async def memoria_ia(ctx, accion: str = None):

    if accion is None:
        await ctx.reply(
            "💜 Usa `!memoria_ia activar` o "
            "`!memoria_ia desactivar`, darling."
        )
        return

    accion = accion.lower()

    if accion not in ("activar", "desactivar"):
        await ctx.reply(
            "Esa opción no existe, cariño. "
            "Elige `activar` o `desactivar`."
        )
        return

    estado = 1 if accion == "activar" else 0
    usuario_id = str(ctx.author.id)

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO configuracion (usuario_id, memoria_ia)
            VALUES (?, ?)
            ON CONFLICT(usuario_id)
            DO UPDATE SET memoria_ia = excluded.memoria_ia
        """, (usuario_id, estado))

        conexion.commit()

    finally:
        conexion.close()

    if estado:
        await ctx.reply(
            "💜 Has autorizado que utilice tus recuerdos "
            "guardados al generar respuestas con OpenAI, "
            "darling. Siempre puedes desactivarlo."
        )
    else:
        await ctx.reply(
            "💜 Ya no utilizaré tus recuerdos guardados "
            "en nuevas solicitudes a OpenAI, cariño. "
            "Tus recuerdos siguen almacenados."
        )
