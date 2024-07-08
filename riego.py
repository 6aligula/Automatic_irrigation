import asyncio
import json
import logging
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from telegram import Bot

# Cargar variables de entorno desde .env
load_dotenv()

# Configure logging
logging.basicConfig(filename='/home/pi/Desktop/riego/riego.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Leer las variables de entorno
token_bot = os.getenv('BOT_API')
chat_id = os.getenv('CHAT_ID')

# Telegram bot token and chat ID
TELEGRAM_TOKEN = token_bot
TELEGRAM_CHAT_ID = chat_id

# Inicializar el bot de Telegram de manera asíncrona
bot = Bot(token=TELEGRAM_TOKEN)

# Read the configuration file
def load_config():
    with open('config.json') as config_file:
        config = json.load(config_file)
    return config

# Load the initial configuration
config = load_config()

mqtt_broker = config['mqtt_broker']
mqtt_port = config['mqtt_port']
mqtt_timeout = config['mqtt_timeout']
topic_riego = config['topic_riego']
topic_riego_control = config['topic_riego_control']

# Cliente MQTT
client = mqtt.Client()

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")

def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code " + str(rc))
    client.subscribe(topic_riego_control)

def on_message(client, userdata, msg):
    try:
        message = f"Message received on topic {msg.topic}: {str(msg.payload.decode())}"
        #asyncio.run(send_telegram_message(message))
        logging.info(message)
    except Exception as e:
        logging.error(f"Error in on_message: {e}")

async def connect_mqtt():
    connected = False
    while not connected:
        try:
            client.connect(mqtt_broker, mqtt_port, mqtt_timeout)
            connected = True
        except Exception as e:
            logging.error(f"MQTT connection failed: {e}")
            await asyncio.sleep(5)  # Wait before retrying

async def start_riego():
    try:
        result = client.publish(topic_riego, "1")
        logging.info("Riego started. Publish result: " + str(result.rc))
        await send_telegram_message("Riego started." + str(result.rc))
    except Exception as e:
        logging.error(f"Failed to start riego: {e}")
        await send_telegram_message(f"Riego started error.  {e}")

async def stop_riego():
    try:
        result = client.publish(topic_riego, "0")
        logging.info("Riego stopped. Publish result: " + str(result.rc))
        await send_telegram_message("Riego stopped." + str(result.rc))
    except Exception as e:
        logging.error(f"Failed to stop riego: {e}")
        await send_telegram_message(f"Riego stopped error. {e}")

async def main():
    client.on_connect = on_connect
    client.on_message = on_message

    await connect_mqtt()

    client.loop_start()

    await start_riego()

    # Wait for 5 minutes (300 seconds) while keeping the MQTT loop active
    await asyncio.sleep(60)

    await stop_riego()

    client.loop_stop()
    client.disconnect()

    await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
