from discord.ext import commands
from memoria.base_datos import conectar


@commands.command(name="memoria_auto")
async def memoria_auto(ctx, accion: str = None):

    usuario_id = str(ctx.author.id)

    # Comprobar que se ha indicado una acción
    if accion is None:
        await ctx.reply(
            "Dime qué quieres, darling: "
            "`!memoria_auto activar` o `!memoria_auto desactivar`."
        )
        return

    accion = accion.lower()

    if accion not in ["activar", "desactivar"]:
        await ctx.reply(
            "Esa opción no existe, cariño. Usa `activar` o `desactivar`."
        )
        return

    # Determinar el estado
    estado = 1 if accion == "activar" else 0

    conexion = conectar()
    cursor = conexion.cursor()

    # Crear o actualizar la configuración del usuario
    cursor.execute("""
        INSERT INTO configuracion (usuario_id, memoria_automatica)
        VALUES (?, ?)
        ON CONFLICT(usuario_id)
        DO UPDATE SET memoria_automatica = excluded.memoria_automatica
    """, (usuario_id, estado))

    conexion.commit()
    conexion.close()

    if estado == 1:
        await ctx.reply(
            "💜 Memoria automática activada, cariño. "
            "Mis oídos atraparán tus secretos~"
        )
    else:
        await ctx.reply(
            "💜 Memoria automática desactivada, darling. "
            "Ya no guardaré nada por mi cuenta."
        )