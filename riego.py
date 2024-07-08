import paho.mqtt.client as mqtt
import json
import logging
import time

# Configure logging
logging.basicConfig(filename='/home/pi/Desktop/riego/riego.log', level=logging.INFO, format='%(asctime)s %(message)s')

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

def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code " + str(rc))
    client.subscribe(topic_riego_control)

def on_message(client, userdata, msg):
    try:
        logging.info(f"Message received on topic {msg.topic}: {str(msg.payload)}")
    except Exception as e:
        logging.error(f"Error in on_message: {e}")

# Function to attempt MQTT connection with retries
def connect_mqtt(client):
    connected = False
    while not connected:
        try:
            client.connect(mqtt_broker, mqtt_port, mqtt_timeout)
            connected = True
        except Exception as e:
            logging.error(f"MQTT connection failed: {e}")
            time.sleep(5)  # Wait before retrying

# Function to start riego
def start_riego():
    try:
        result = client.publish(topic_riego, "1")
        logging.info("Riego started. Publish result: " + str(result.rc))
    except Exception as e:
        logging.error(f"Failed to start riego: {e}")

# Function to stop riego
def stop_riego():
    try:
        result = client.publish(topic_riego, "0")
        logging.info("Riego stopped. Publish result: " + str(result.rc))
    except Exception as e:
        logging.error(f"Failed to stop riego: {e}")

# Setup MQTT and start the loop
try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    connect_mqtt(client)  # Attempt to connect with retries
    logging.info("Connected to MQTT broker")

    client.loop_start()  # Starts a new thread and processes network traffic

    # Start the riego
    start_riego()

    # Wait for 5 minutes (300 seconds) while keeping the MQTT loop active
    for _ in range(60):
        time.sleep(1)  # Sleep for 1 second

    # Stop the riego
    stop_riego()

    # Add a small delay to ensure the last message is processed
    time.sleep(5)

    client.loop_stop()  # Stop the network thread
    client.disconnect()  # Ensure the client disconnects properly

except Exception as e:
    logging.error(f"Error setting up MQTT client: {e}")
