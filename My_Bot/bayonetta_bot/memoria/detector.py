import re
from .base_datos import conectar


# Para que "canción" y "cancion" cuenten igual (misma longitud, 1 a 1)
QUITAR_ACENTOS = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")

# Temas que nunca se guardan automáticamente (se comprueba sin acentos)
TEMAS_EXCLUIDOS = re.compile(
    r"politic|partido|elecciones|votar|\bvoto\b|religi|\bdios\b|iglesia|mezquita|"
    r"enfermedad|diagnostic|depresion|ansiedad|suicid|autolesi|trastorno|alergi|intoleran|"
    r"droga|sexual|\bsexo\b|\bgay\b|lesbian|bisexual|transgenero|orientacion|"
    r"contrasena|password|tarjeta|\bdni\b|\bnie\b|pasaporte|\biban\b|cuenta bancaria|"
    r"sueldo|salario|deuda|direccion|\bcalle\b|codigo postal|telefono|whatsapp|"
    r"correo|email|@|\b\d{1,2} anos\b",
    re.IGNORECASE
)

# Muletillas que se ignoran al principio y al final del mensaje
RELLENO_INICIO = re.compile(
    r"(?:hola|buenas|hey|oye|mira|pues|bueno|bueno pues|la verdad(?: es que)?|"
    r"sinceramente|honestamente|ah y|por cierto|ademas|yo|yo creo que|creo que|para mi)"
    r"[,. ]+",
    re.IGNORECASE
)
RELLENO_FINAL = re.compile(
    r"[,. ]+(?:jaja+|jeje+|jiji+|xd+|lol|porfa|gracias|:\)|:d|<3)\s*$",
    re.IGNORECASE
)

#-----------------------------PALABRAS CLAVE-----------------------------

GUSTA = (
    r"(?:me (?:gusta|encanta|fascina|flipa|mola|chifla|apasiona)n?"
    r"(?: mucho| muchisimo)?|adoro|amo|disfruto(?: de)?)"
)

DEPORTES = (
    r"futbol americano|futbol|baloncesto|basket|tenis|padel|voleibol|volley|rugby|golf|"
    r"ajedrez|badminton|beisbol|hockey|natacion|waterpolo|ciclismo|atletismo|running|"
    r"boxeo|mma|karate|judo|taekwondo|artes marciales|surf|skate|patinaje|escalada|"
    r"senderismo|yoga|pilates|gimnasia|pesas|crossfit|calistenia|esqui|snowboard|"
    r"motociclismo|formula 1|f1|paintball"
)

GENEROS_JUEGO = (
    r"rpg|fps|shooters?|terror|horror|aventuras?|accion|estrategia|puzzles?|plataformas|"
    r"mundo abierto|lucha|peleas|carreras|deportes|simulacion|supervivencia|sandbox|"
    r"roguelike|metroidvania|battle royale|moba|mmo|mmorpg|indie|cooperativos?|"
    r"multijugador|rol|musicales?|sigilo"
)

PLATAFORMAS = (
    r"pc|ordenador|movil|celular|steam|playstation|ps[1-5]|xbox|switch|nintendo|"
    r"consola|tablet"
)

COLORES = (
    r"rojo|azul|verde|amarillo|morado|violeta|rosa|negro|blanco|naranja|gris|marron|"
    r"celeste|turquesa|dorado|plateado|lila|granate|beige|fucsia"
)

GENEROS_MUSICA = (
    r"rock|pop|rap|hip hop|trap|reggaeton|regueton|heavy metal|metal|jazz|clasica|"
    r"electronica|k-pop|kpop|j-pop|jpop|indie|punk|blues|country|salsa|bachata|flamenco|"
    r"lofi|lo-fi|techno|house|edm|dubstep|synthwave|folk|soul|r&b|opera|cumbia|"
    r"alternativo|grunge|disco|reggae|ska|trance|drill|phonk|vaporwave|bandas sonoras"
)

GENEROS_PELI = (
    r"terror|comedia|accion|ciencia ficcion|fantasia|romance|romanticas?|drama|suspense|"
    r"thriller|animacion|animadas?|aventuras?|misterio|documentales?|belicas?|western|"
    r"musicales?|superheroes|policiacas?|gore|psicologicas?"
)

COMIDAS = (
    r"pizza|pasta|sushi|hamburguesas?|chocolate|paella|tortilla|tacos?|helado|ramen|"
    r"kebab|pollo|arroz|patatas|croquetas|lasana|empanadas|churros|tarta|galletas|queso|"
    r"jamon|fruta|ensalada|sopa|pan|cafe|te|cerveza|vino|zumo|batido|refresco|cola"
)

ANIMALES = (
    r"perr[oa]s?|gat[oa]s?|conejos?|hamsters?|loros?|tortugas?|caballos?|pajaros?|peces|"
    r"pez|cobayas?|erizos?|hurones?|serpientes?|lagartos?|iguanas?|ratas?|ratones?|"
    r"patos?|gallinas?|vacas?|ovejas?|cerdos?|lobos?|zorros?|pandas?|pinguinos?|"
    r"delfines|tiburones|tiburon|leones?|tigres?|panteras?|buhos?|lechuzas?|"
    r"murcielagos?|ardillas?|nutrias?|axolotl(?:es)?|ranas?|mapaches?|capibaras?|"
    r"elefantes?|jirafas?|koalas?"
)

AFICIONES = (
    r"dibujar|leer|cocinar|programar|escribir|pintar|cantar|bailar|viajar|nadar|correr|"
    r"caminar|pasear|fotografiar|fotografia|coleccionar \w+|"
    r"ver (?:series|peliculas|anime|videos|youtube|twitch)|editar videos?|grabar videos?|"
    r"salir de fiesta|dormir|tocar (?:la|el) \w+|jugar|streamear|hacer deporte|"
    r"montar en bici|acampar|pescar|jardineria|bricolaje|manualidades|tejer|coser|hornear|"
    r"reposteria|meditar|componer|producir musica|disenar|modelar en 3d|cine|teatro|"
    r"museos|conducir|bucear|esquiar|patinar|cosplay|hacer cosplay|rolear|conciertos|"
    r"escribir historias|escribir poesia|hacer musica"
)

IDIOMAS = (
    r"espanol|castellano|ingles|frances|aleman|italiano|portugues|japones|chino|"
    r"coreano|catalan|gallego|euskera|ruso|arabe|turco|holandes|sueco|griego|latin"
)

PROFESIONES = (
    r"programador[a]?|desarrollador[a]?|disenador[a]?|ingenier[oa]|medic[oa]|enfermer[oa]|"
    r"profesor[a]?|maestr[oa]|abogad[oa]|arquitect[oa]|artista|music[oa]|cociner[oa]|"
    r"camarer[oa]|mecanic[oa]|electricista|fotograf[oa]|escritor[a]?|periodista|"
    r"traductor[a]?|contable|administrativ[oa]|vendedor[a]?|tecnic[oa]|autonom[oa]|"
    r"freelance|ilustrador[a]?|animador[a]?|editor[a]?|psicolog[oa]"
)

# Un nombre: hasta 3 palabras de letras / un nick: letras, números, _ y .
NOMBRE = r"([a-zñ']{2,20}(?: [a-zñ']{2,20}){0,2})"
NICK = r"([a-zñ0-9_.']{2,20}(?: [a-zñ0-9_.']{2,20}){0,2})"

# Para que los patrones generales no atrapen frases sueltas
NO_CONJ = r"(?!que |como |cuando |si |tu |tus |porque |pero )"


def favorito(sustantivos):
    # "mi X favorito/a es ...", "mis X favoritos/as son ..."
    return (
        rf"mis? (?:{sustantivos}) (?:favorit|preferid)[oa]s? "
        rf"(?:es|son|era|seria|ha sido) (.+)"
    )


# El orden importa: gana el primer patrón que coincida.
# Primero los específicos y al final los generales.
PATRONES = [

    # DEPORTES (antes que videojuegos para que "jugar al fútbol" no sea un juego)
    (favorito(r"deportes?|equipos?|jugadores?|futbolistas?|pilotos?|clubes?|selecciones?|tenistas?|luchadores?|atletas?"), "deportes"),
    (rf"{GUSTA} (?:jugar (?:al|a la) |practicar |ver |hacer |el |la |los |las )?({DEPORTES})", "deportes"),
    (rf"(?:practico|entreno|hago|juego (?:al|a la)) ({DEPORTES})", "deportes"),
    (r"soy (?:hincha|seguidor|seguidora|aficionado|aficionada|socio|socia) (?:del?|de la) (.+)", "deportes"),
    (r"(?:voy|suelo ir) al gimnasio(?: .+)?", "deportes"),

    # VIDEOJUEGOS
    (favorito(r"juegos?|videojuegos?|sagas? de juegos|sagas? de videojuegos|armas?|mapas?|skins?|modos? de juego|jefes?"), "videojuegos"),
    (rf"{GUSTA} jugar (?:a|al) (.+)", "videojuegos"),
    (r"prefiero jugar (?:a|al) (.+)", "videojuegos"),
    (rf"{GUSTA} (?:los )?(?:juegos|videojuegos) (?:de )?({GENEROS_JUEGO})", "videojuegos"),
    (r"(?:suelo|normalmente|casi siempre) jugar (?:a|al) (.+)", "videojuegos"),
    (r"(?:estoy jugando|ando jugando|ahora estoy jugando|ahora juego) (?:a|al) (.+)", "jugando ahora"),
    (r"mi main (?:es|era) (.+)", "videojuegos"),
    (r"soy (?:un |una )?gamer", "videojuegos"),
    (r"juego (?:a|al) (.+)", "videojuegos"),

    # PLATAFORMAS
    (favorito(r"plataformas?|consolas?"), "plataformas"),
    (r"juego principalmente (?:en|con) (.+)", "plataformas"),
    (rf"juego (?:siempre |mucho |casi siempre )?(?:en|con) (?:mi |la |el )?({PLATAFORMAS})", "plataformas"),
    (rf"tengo (?:un |una )?({PLATAFORMAS})(?: .+)?", "plataformas"),

    # PREFERENCIAS DE JUEGO
    (r"prefiero jugar por (.+)", "preferencias"),
    (r"prefiero jugar en (.+)", "preferencias"),

    # PERSONAJES
    (favorito(r"personajes?|villanos?|heroes?|heroinas?|protagonistas?|antagonistas?|waifus?|husbandos?|pokemon|monstruos?"), "personajes"),

    # COLORES
    (favorito(r"colo(?:r|res)"), "colores"),
    (rf"{GUSTA} (?:el|los) colo(?:r|res) (.+)", "colores"),
    (rf"{GUSTA} (?:el |la |los |las )?({COLORES})", "colores"),

    # MUSICA
    (favorito(
        r"grupos?|cantantes?|cancion(?:es)?|generos? musicales?|artistas?|bandas?|"
        r"album(?:es)?|raperos?|compositores?|instrumentos?|bandas? sonoras?|playlists?"
    ), "musica"),
    (rf"{GUSTA} escuchar (.+)", "musica"),
    (r"escucho mucho (.+)", "musica"),
    (r"(?:estoy escuchando|ando escuchando) (.+)", "escuchando ahora"),
    (rf"{GUSTA} (?:el |la |los |las )?(?:musica )?({GENEROS_MUSICA})", "musica"),
    (r"(?:toco|se tocar) (?:el|la) (.+)", "musica"),

    # PELICULAS
    (favorito(r"peliculas?|films?|filmes?|actor(?:es)?|actrices?|directores?|sagas? de peliculas"), "peliculas"),
    (rf"{GUSTA} (?:las |los )?(?:peliculas|pelis|films) (?:de )?({GENEROS_PELI})", "peliculas"),
    (rf"{GUSTA} (?:el |la )?(?:cine )?(?:de )?({GENEROS_PELI})", "peliculas"),

    # SERIES
    (favorito(r"series?|dramas?|sitcoms?|doramas?|capitulos?|temporadas?|episodios?"), "series"),
    (rf"{GUSTA} (?:las |los )?series (?:de )?(.+)", "series"),
    (r"(?:estoy viendo|ando viendo) (.+)", "viendo ahora"),

    # ANIME
    (favorito(r"animes?|mangas?|manhwas?|donghuas?|openings?|endings?"), "anime"),
    (rf"{GUSTA} (?:el )?anime (?:de )?(.+)", "anime"),

    # LIBROS
    (favorito(r"libros?|novelas?|autores?|escritores?|sagas?|comics?|cuentos?|poemas?|poetas?|generos? literarios?"), "libros"),
    (rf"{GUSTA} leer (.+)", "libros"),
    (rf"{GUSTA} (?:los |las )?(?:libros|novelas|comics|cuentos|historias) (?:de )?(.+)", "libros"),
    (r"(?:estoy leyendo|ando leyendo) (.+)", "leyendo ahora"),

    # COMIDA
    (favorito(
        r"comidas?|platos?|bebidas?|postres?|helados?|dulces?|snacks?|pizzas?|frutas?|"
        r"verduras?|cafes?|tes?|refrescos?|restaurantes?|sabor(?:es)?|golosinas?|"
        r"cervezas?|vinos?|batidos?|zumos?|desayunos?|cenas?"
    ), "comida"),
    (rf"{GUSTA} comer (.+)", "comida"),
    (rf"{GUSTA} beber (.+)", "comida"),
    (rf"{GUSTA} (?:la )?comida (.+)", "comida"),
    (rf"{GUSTA} (?:la |el |las |los )?({COMIDAS})", "comida"),
    (r"soy (vegetarian[oa]|vegan[oa]|pescetarian[oa])", "comida"),
    (r"no como (.+)", "comida"),

    # ANIMALES
    (favorito(r"animales?|mascotas?"), "animales"),
    (rf"mis? ({ANIMALES}) se llama[n]? (.+)", "animales"),
    (r"mis? mascotas? se llama[n]? (.+)", "animales"),
    (rf"tengo (?:un|una|dos|tres|cuatro|cinco|\d+) ({ANIMALES})", "animales"),
    (rf"{GUSTA} (?:los |las |el |la )?({ANIMALES})", "animales"),

    # AFICIONES
    (favorito(r"aficion(?:es)?|hobbies|hobby|pasatiempos?|actividad(?:es)?"), "aficiones"),
    (r"mis? (?:aficion|hobby|pasatiempo|aficiones|hobbies|pasatiempos) (?:es|son) (.+)", "aficiones"),
    (r"mi pasion (?:es|son) (.+)", "aficiones"),
    (r"en mi tiempo libre (.+)", "aficiones"),
    (rf"{GUSTA} ({AFICIONES})", "aficiones"),

    # TECNOLOGIA
    (favorito(
        r"lenguajes? de programacion|lenguajes?|editor(?:es)?|frameworks?|sistemas? operativos?|"
        r"navegadores?|apps?|aplicaciones?|moviles?|marcas?|distros?|librerias?"
    ), "tecnologia"),
    (r"programo en (.+)", "tecnologia"),
    (r"se programar en (.+)", "tecnologia"),
    (r"uso (windows|linux|macos|mac|android|ios|ubuntu|arch|debian|fedora)", "tecnologia"),

    # IDIOMAS
    (favorito(r"idiomas?|lenguas?"), "idiomas"),
    (rf"hablo ((?:{IDIOMAS})(?:,? (?:y|e) (?:{IDIOMAS}))*)", "idiomas"),
    (rf"(?:estoy aprendiendo|quiero aprender|aprendo) ({IDIOMAS})", "idiomas"),
    (r"mi (?:lengua|idioma) (?:materna|materno|nativa|nativo) (?:es|son) (.+)", "idiomas"),

    # APRENDIZAJE
    (r"estoy aprendiendo (.+)", "aprendizaje"),
    (r"quiero aprender (.+)", "aprendizaje"),

    # ESTUDIOS Y TRABAJO
    (r"(?:estudio|estoy estudiando) (?:la carrera de|el grado de|el ciclo de|el master de|un master en|una carrera de) (.+)", "estudios"),
    (r"soy estudiante de (.+)", "estudios"),
    (rf"soy (?:un |una )?({PROFESIONES})", "trabajo"),
    (r"trabajo (?:de|como|en) (.+)", "trabajo"),
    (r"me dedico a (.+)", "trabajo"),

    # CREADORES Y FANDOMS
    (favorito(r"youtubers?|streamers?|creadores?|canales?|podcasts?|tiktokers?|influencers?|memes?|paginas? web|webs?|subreddits?"), "creadores"),
    (r"(?:sigo|veo mucho) a (.+)", "creadores"),
    (r"soy (?:muy |super |un gran |una gran )?fan(?:atico|atica)? de(?:l| la| los| las)? (.+)", "fandoms"),

    # LUGARES
    (favorito(r"lugar(?:es)?|ciudad(?:es)?|paises|pais|estacion(?:es)?|epoca|dia|mes|clima|region|playas?|montanas?"), "lugares"),
    (r"vivo en (.{2,40})", "lugares"),
    (r"soy de (?!los |las |esos |esas |ese |esa |aquellos |quien |mucho |poco )(.{2,40})", "lugares"),
    (r"(?:quiero|sueno con) (?:viajar|ir) a (.+)", "lugares"),

    # METAS
    (r"mi (?:mayor )?(?:sueno|meta|objetivo|proposito) (?:es|seria) (.+)", "metas"),
    (r"sueno con (.+)", "metas"),
    (r"algun dia quiero (.+)", "metas"),
    (r"quiero ser (.+)", "metas"),

    # DATOS BASICOS (solo lo inofensivo)
    (rf"me llamo {NOMBRE}", "nombre"),
    (rf"mi nombre es {NOMBRE}", "nombre"),
    (rf"mi apodo es {NICK}", "nombre"),
    (rf"mi (?:nick|usuario|gamertag) es {NICK}", "nombre"),
    (rf"(?:puedes )?llamarme {NICK}", "nombre"),
    (rf"llamame {NICK}", "nombre"),

    # RUTINAS
    (r"(?:suelo|normalmente|casi siempre) (?:conectarme|estar disponible) (.+)", "rutinas"),
    (r"juego (?:por la|por las|de) (noche|tarde|manana|madrugada)", "rutinas"),
    (r"soy (?:muy )?(madrugador[a]?|noctambul[oa]|ave nocturna|buho)", "rutinas"),
    (r"mi horario (?:es|son) (.+)", "rutinas"),

    # OPINIONES Y PREFERENCIAS GENERALES
    (r"lo que mas me gusta de (.+?) es (.+)", "gustos"),
    (r"lo que mas me gusta es (.+)", "gustos"),
    (r"lo que mas odio es (.+)", "disgustos"),
    (r"prefiero (.{3,60})", "preferencias"),

    # GENERALES (al final, atrapan lo que no encajó arriba)
    (r"mis? ([a-zñ ]{3,30}?) (?:favorit|preferid)[oa]s? (?:es|son|era|seria) (.+)", "otros"),
    (rf"(?:odio|detesto|no soporto|no aguanto|me da asco|me dan asco|me molestan?) {NO_CONJ}(.{{3,60}})", "disgustos"),
    (rf"no me gustan? (?:nada )?{NO_CONJ}(.{{3,60}})", "disgustos"),
    (rf"{GUSTA} {NO_CONJ}(.{{3,60}})", "gustos"),
]

PATRONES_COMPILADOS = [
    (re.compile(patron, re.IGNORECASE), categoria)
    for patron, categoria in PATRONES
]


def detectar_recuerdo(texto):

    texto = texto.strip()

    # Ignorar preguntas y comandos
    if texto.startswith("¿") or texto.startswith("!"):
        return None

    # Quitar signos sueltos al principio y al final
    texto = texto.strip("¡¿ ").rstrip(".,!?;: ")

    # Versión sin acentos solo para comparar (misma longitud que el original)
    busqueda = texto.translate(QUITAR_ACENTOS)

    # Quitar muletillas del principio ("pues", "la verdad", "yo"...)
    while True:
        m = RELLENO_INICIO.match(busqueda)
        if not m:
            break
        texto = texto[m.end():]
        busqueda = busqueda[m.end():]

    # Quitar muletillas del final ("jaja", "xd", "gracias"...)
    while True:
        m = RELLENO_FINAL.search(busqueda)
        if not m:
            break
        texto = texto[:m.start()]
        busqueda = busqueda[:m.start()]

    texto = texto.strip().rstrip(".,!?;: ")
    busqueda = busqueda.strip().rstrip(".,!?;: ")

    # No guardar temas delicados
    if TEMAS_EXCLUIDOS.search(busqueda):
        return None

    for patron, categoria in PATRONES_COMPILADOS:

        resultado = patron.fullmatch(busqueda)

        if resultado:

            # Recuperar el texto original (con acentos) de cada grupo
            partes = [
                texto[resultado.start(i):resultado.end(i)].strip()
                for i in range(1, patron.groups + 1)
                if resultado.group(i)
            ]

            informacion = ": ".join(partes) if partes else texto
            informacion = informacion.rstrip(".,!? ")

            if 3 <= len(informacion) <= 200:
                return categoria, informacion

    return None


def guardar_recuerdo_automatico(usuario_id, categoria, informacion):

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Comprobar si la memoria automática está activada
        cursor.execute("""
            SELECT memoria_automatica
            FROM configuracion
            WHERE usuario_id = ?
        """, (str(usuario_id),))

        configuracion = cursor.fetchone()

        if configuracion is None or configuracion[0] != 1:
            return False

        # Evitar recuerdos duplicados
        cursor.execute("""
            SELECT id
            FROM recuerdos
            WHERE usuario_id = ?
            AND categoria = ?
            AND LOWER(informacion) = LOWER(?)
        """, (str(usuario_id), categoria, informacion))

        duplicado = cursor.fetchone()

        if duplicado:
            return False

        # Guardar el nuevo recuerdo
        cursor.execute("""
            INSERT INTO recuerdos (
                usuario_id,
                categoria,
                informacion,
                origen
            )
            VALUES (?, ?, ?, ?)
        """, (
            str(usuario_id),
            categoria,
            informacion,
            "automatico"
        ))

        conexion.commit()
        return True

    finally:
        conexion.close()