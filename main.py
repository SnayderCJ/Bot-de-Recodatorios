import telebot
import threading
import time
import os
import dotenv
dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def bienvenida(message):
    texto = (
        "¡Hola! Soy tu bot de recordatorios ⏰\n\n"
        "Para crear uno, usa el siguiente formato:\n"
        "/recordar [segundos] [Tu mensaje]\n\n"
        "Ejemplo: /recordar 10 Apagar el horno"
    )
    bot.reply_to(message, texto)


def enviar_recordatorio(chat_id, mensaje, espera):
    time.sleep(espera)
    bot.send_message(chat_id, f"🔔 ¡RECORDATORIO!: {mensaje}")

@bot.message_handler(commands=['recordar'])
def crear_recordatorio(message):
    try:
        partes = message.text.split(' ', 2)
        espera = int(partes[1])
        texto_recordatorio = partes[2]
        
        bot.reply_to(message, f"¡Anotado! Te recordaré: '{texto_recordatorio}' en {espera} segundos.")
        
        hilo = threading.Thread(target=enviar_recordatorio, args=(message.chat.id, texto_recordatorio, espera))
        hilo.start()
        
    except (IndexError, ValueError):
        bot.reply_to(message, "⚠️ Formato incorrecto. Recuerda usar: /recordar [segundos] [mensaje]")

print("El bot está funcionando...")
bot.polling()