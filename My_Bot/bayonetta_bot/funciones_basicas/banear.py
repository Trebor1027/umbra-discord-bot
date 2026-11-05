import discord as DC
import re
import unicodedata
from discord.ext import commands

IMAGEN_BAYONETTA = "https://i.pinimg.com/originals/11/1a/64/111a64de87651eef6a3de8ba412021b3.jpg"

# Insultos (sin acentos). Cada uno es un patrón: "idiot[ae]s?" cubre idiota, idiotas...
INSULTOS = [
    # Clásicos
    r"idiot[ae]s?", r"estupid[oa]s?", r"imbecil(?:es)?", r"tont[oa]s?",
    r"inutil(?:es)?", r"incompetentes?", r"gilipollas", r"gilipuertas",
    r"cabron(?:a|es|as)?", r"capullo[as]?", r"cretin[oa]s?", r"subnormal(?:es)?",
    r"retrasad[oa]s?", r"mongol[oa]s?", r"tarad[oa]s?", r"burr[oa]s?",
    r"lerd[oa]s?", r"bobo[as]?", r"pendej[oa]s?", r"boluda?[s]?", r"zopenc[oa]s?",

    # Groserías
    r"mierda", r"puta", r"puton(?:a|es)?", r"zorra", r"perra", r"guarr[oa]s?",
    r"cerda", r"marran[oa]s?", r"asquerosa?s?", r"cabrona", r"maldit[oa]s?",
    r"hij[oa] de puta", r"hijueputa", r"hdp", r"ctm", r"malnacid[oa]s?",
    r"desgraciad[oa]s?", r"mamona", r"culera?", r"chupapollas",

    # Desprecio
    r"basura", r"patetic[oa]s?", r"lamentables?", r"horrible", r"horribles",
    r"fea", r"feo", r"feisima", r"inservibles?", r"mediocres?", r"estorbo",
    r"fraude", r"farsante", r"payas[oa]s?", r"ridicula?s?", r"inferior",
    r"despreciable", r"vergonzos[oa]", r"penosa", r"desastre",
    r"asco", r"das asco", r"das pena", r"eres una pena",
    r"callate", r"cierra la boca", r"vete a la mierda", r"muerete",
    r"te odio", r"no vales nada", r"no sirves", r"no sirve para nada",
    r"eres un desastre", r"eres un fracaso", r"fracasad[oa]s?",
    r"chatarra", r"vieja", r"ancian[ae]", r"loca", r"psicopata",
]

INSULTO_RE = "|".join(INSULTOS)

# Cómo pueden referirse al bot
ALIAS_BOT = [r"bayonetta", r"bayoneta", r"bayo"]

# Distancia máxima (en caracteres) entre el nombre y el insulto
VENTANA = 60

LEET = str.maketrans({
    "0": "o", "1": "i", "3": "e", "4": "a",
    "5": "s", "7": "t", "@": "a", "$": "s",
})


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )


def limpiar_mensaje(message):
    """Pone el mensaje en una forma fácil de analizar."""

    bot_id = message.guild.me.id
    contenido = message.content

    # La mención al bot cuenta como decir "bayonetta"
    contenido = re.sub(rf"<@!?{bot_id}>", " bayonetta ", contenido)

    # Otras menciones y emojis personalizados no cuentan
    contenido = re.sub(r"<@[!&]?\d+>", " usuario ", contenido)
    contenido = re.sub(r"<a?:\w+:\d+>", " ", contenido)

    contenido = normalizar(contenido)

    # Trucos típicos: "1d10t4", "idiotaaaaa"
    contenido = contenido.translate(LEET)
    contenido = re.sub(r"(.)\1{2,}", r"\1", contenido)

    return contenido


def es_insulto_al_bot(message):

    contenido = limpiar_mensaje(message)

    nombres = "|".join(ALIAS_BOT)
    nombre_propio = normalizar(message.guild.me.display_name)
    if len(nombre_propio) >= 4 and nombre_propio not in ALIAS_BOT:
        nombres += "|" + re.escape(nombre_propio)

    # Si responde directamente a un mensaje del bot, el insulto va para ella
    es_respuesta_al_bot = False
    referencia = message.reference
    if referencia and isinstance(referencia.resolved, DC.Message):
        es_respuesta_al_bot = referencia.resolved.author.id == message.guild.me.id

    # Se analiza frase por frase
    for frase in re.split(r"[.!?;\n]+", contenido):

        frase = frase.strip()

        if not frase:
            continue

        # Negaciones: "no eres tonta", "nunca dije que fueras idiota"
        if re.search(rf"\b(?:no|nunca|jamas)\b.{{0,15}}\b(?:{INSULTO_RE})\b", frase):
            continue

        if es_respuesta_al_bot:
            if re.search(rf"\b(?:{INSULTO_RE})\b", frase):
                return True

        # Nombre seguido de insulto, o insulto seguido del nombre
        patron = (
            rf"\b(?:{nombres})\b.{{0,{VENTANA}}}?\b(?:{INSULTO_RE})\b"
            rf"|\b(?:{INSULTO_RE})\b.{{0,{VENTANA}}}?\b(?:{nombres})\b"
        )

        if re.search(patron, frase):
            return True

    return False


async def detectar_insultos(message):

    if message.author.bot or message.guild is None:
        return

    # Los admins, el dueño y los moderadores con permiso de baneo no se tocan
    permisos = message.author.guild_permissions
    if (
        message.author == message.guild.owner
        or permisos.administrator
        or permisos.ban_members
    ):
        return

    if not es_insulto_al_bot(message):
        return

    try:
        if not message.guild.me.guild_permissions.ban_members:
            await message.channel.send(
                "No tengo permisos para banear, cariño."
            )
            return

        await message.author.ban(
            reason="Insultar a Bayonetta"
        )

        embed = DC.Embed(
            title="💜 ¡DESTERRADO!",
            description=(
                f"**Usuario baneado:** {message.author.mention}\n"
                "**Motivo:** Insultar a Bayonetta.\n\n"
                "Aprende a comportarte, cariño."
            ),
            color=DC.Color.dark_purple()
        )

        embed.set_image(url=IMAGEN_BAYONETTA)
        embed.set_footer(text="El espectáculo ha terminado, cariño.")

        await message.channel.send(embed=embed)

    except DC.Forbidden:
        await message.channel.send(
            "No puedo ejecutar el castigo. "
            "Revisa mis permisos y mi posición en los roles."
        )

    except DC.HTTPException as e:
        print(f"Error al banear: {e}")


#-----------------------DESBANEAR----------------------

@commands.command(name="desbanear")
@commands.has_permissions(ban_members=True)
async def desbanear(ctx, usuario_id: int):

    try:
        usuario = DC.Object(id=usuario_id)

        await ctx.guild.unban(
            usuario,
            reason=f"Desbaneado por {ctx.author}"
        )

        await ctx.send(
            f"El destierro ha terminado. "
            f"El usuario {usuario_id} ha sido perdonado."
        )

    except DC.NotFound:
        await ctx.send("Ese usuario no está baneado, cariño.")

    except DC.Forbidden:
        await ctx.send("No tengo permisos para retirar baneos.")

    except DC.HTTPException as e:
        await ctx.send(f"No se pudo retirar el baneo: {e}")