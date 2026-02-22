import telebot
import threading
import time
import re
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def bienvenida(message):
    texto = (
        "¡Hola! Soy tu bot de recordatorios ⏰\n\n"
        "Crea uno usando este formato: /recordar [tiempo][unidad] [Mensaje]\n"
        "Unidades: 's' (segundos), 'm' (minutos), 'h' (horas)\n\n"
        "Ejemplo: /recordar 15m Sacar la pizza del horno"
    )
    bot.reply_to(message, texto)

def enviar_recordatorio(chat_id, mensaje, espera_segundos):
    time.sleep(espera_segundos)
    bot.send_message(chat_id, f"🔔 ¡RECORDATORIO!: {mensaje}")

@bot.message_handler(commands=['recordar'])
def crear_recordatorio(message):
    try:
        # Separamos el mensaje en 3 partes: /recordar, tiempo, y el mensaje
        argumentos = message.text.split(' ', 2)
        if len(argumentos) < 3:
            raise ValueError()
        
        tiempo_str = argumentos[1].lower()
        texto_recordatorio = argumentos[2]
        
        # Buscamos un número seguido de s, m o h
        match = re.match(r"^(\d+)([smh])$", tiempo_str)
        if not match:
            bot.reply_to(message, "⚠️ Formato de tiempo inválido. Usa 's', 'm' o 'h'. Ej: 30m")
            return

        cantidad = int(match.group(1))
        unidad = match.group(2)
        
        # Diccionario para convertir todo a segundos
        multiplicadores = {'s': 1, 'm': 60, 'h': 3600}
        espera_segundos = cantidad * multiplicadores[unidad]
        
        bot.reply_to(message, f"¡Anotado! Te recordaré: '{texto_recordatorio}' en {cantidad}{unidad}.")
        
        # Hilo para el temporizador
        hilo = threading.Thread(target=enviar_recordatorio, args=(message.chat.id, texto_recordatorio, espera_segundos))
        hilo.start()
        
    except ValueError:
        bot.reply_to(message, "⚠️ Formato incorrecto. Ejemplo: /recordar 2h Revisar el servidor")

print("Bot con temporizador avanzado funcionando...")
bot.polling()