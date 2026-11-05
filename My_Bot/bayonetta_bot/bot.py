#LIBRERIAS
import os
import discord as DC
from discord.ext import commands
from dotenv import load_dotenv


#CARGAR VARIABLES DE ENTORNO
load_dotenv()

#CONFIGURAR INTENTS DEL BOT
intents = DC.Intents.default()
intents.message_content = True

# CREAR EL BOT
bot = commands.Bot(command_prefix='!', intents=intents)

# EVENTO DE CUANDO EL BOT ESTÁ LISTO
@bot.event
async def on_ready():
    ruta = os.path.join(os.path.dirname(__file__), "videos", "bayonetta.txt")
    try:
        with open(ruta, encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("(no se encontró bayonetta.txt)")
    print(f"¡{bot.user.name} ha llegado, cariño! El espectáculo está a punto de comenzar.")


#-----------------------FUNCIONES BASICAS----------------------
# COMANDO PARA SALUDAR
from funciones_basicas.hola import hola
bot.add_command(hola)

# COMANDO PARA DESPEDIRSE
from funciones_basicas.adios import adios
bot.add_command(adios)

# COMANDO PARA REPETIR
from funciones_basicas.repetir import repetir
bot.add_command(repetir)


#-----------------------RADIO----------------------

# COMANDO PARA UNIRSE A LA RADIO
from radio.unirse_radio import unirse
from radio.salir_radio import salir
bot.add_command(unirse)
bot.add_command(salir)


# COMANDO PARA ENCENDER LA RADIO
from radio.encender_radio import radio
bot.add_command(radio)


# COMANDO PARA PAUSAR, REANUDAR Y SALIR DE LA RADIO
from radio.funciones_radio import pausa, reanudar
bot.add_command(pausa)
bot.add_command(reanudar)


#-----------------------VIDEOS----------------------

#COMANDO PARA ENVIAR VIDEOS DE SALUDO, DESPEDIDA Y MEMES
from videos.presentacion import hola_imagen
from videos.adios import adios_imagen
from videos.meme import meme_imagen

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await hola_imagen(message)
    await adios_imagen(message)
    await meme_imagen(message)
    await bot.process_commands(message)
    

#----------------------LIMPIAR CHAT----------------------

#COMANDO PARA LIMPIAR EL CHAT CON !LIMPIAR
from funciones_basicas.limpiar import limpiar
bot.add_command(limpiar)


#COMANDO PARA MOSTAR LOS COMANDOS DEL BOT
from funciones_basicas.decir_comandos import comandos
bot.add_command(comandos)


#----------------------BANEAR----------------------
from funciones_basicas.banear import detectar_insultos

@bot.listen("on_message")
async def controlar_insultos(message):
    await detectar_insultos(message)
    

#----------------------ECONOMIA----------------------
from economia.moneda import saldo, diario, trabajar, ranking
from economia.transferencia import transferir
bot.add_command(saldo)
bot.add_command(diario)
bot.add_command(trabajar)
bot.add_command(ranking)
bot.add_command(transferir)


#----------------------TIENDA----------------------
from economia.tienda import tienda, comprar, inventario
bot.add_command(tienda)
bot.add_command(comprar)
bot.add_command(inventario)


#----------------------NIVELES----------------------
from economia.niveles import nivel, procesar_experiencia
bot.add_command(nivel)
@bot.listen("on_message")
async def sistema_experiencia(message):
    await procesar_experiencia(message)
    
    
#----------------------RECORDAR----------------------
from memoria.base_datos import crear_tablas
from memoria.recordar import recordar
bot.add_command(recordar)
crear_tablas()


#----------------------CONSULTAR MEMORIA----------------------
from memoria.consultar import consultar
bot.add_command(consultar)



#----------------------OLVIDAR----------------------
from memoria.olvidar import olvidar
bot.add_command(olvidar)


#----------------------MIS DATOS----------------------
from memoria.misdatos import misdatos
bot.add_command(misdatos)


#----------------------CONFIGURACION MEMORIA----------------------
from memoria.configuracion import memoria_auto
bot.add_command(memoria_auto)


#----------------------DETECTAR RECUERDOS----------------------
from memoria.detector import (
    detectar_recuerdo,
    guardar_recuerdo_automatico
)

@bot.event
async def on_message(message):

    # Ignorar mensajes de otros bots
    if message.author.bot:
        return

    # Ignorar comandos
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    # Detectar información relevante
    resultado = detectar_recuerdo(message.content)

    if resultado:
        categoria, informacion = resultado

        guardado = guardar_recuerdo_automatico(
            str(message.author.id),
            categoria,
            informacion
        )

        if guardado:
            await message.reply(
                " He aprendido algo nuevo sobre ti."
            )

    # Mantener funcionando los comandos de Discord
    await bot.process_commands(message)



#----------------------EJECUCION----------------------

bot.run(os.environ["DISCORD_TOKEN"])

