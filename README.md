# Sistema de Riego Automatizado con MQTT y Telegram

Este proyecto implementa un sistema de control de riego automatizado utilizando MQTT para la comunicación entre dispositivos y Telegram para enviar notificaciones en tiempo real sobre el estado del riego.

## Características

- **Control Remoto**: Activa o desactiva el sistema de riego desde cualquier lugar utilizando mensajes MQTT.
- **Notificaciones en Tiempo Real**: Recibe actualizaciones sobre el estado del riego directamente en tu teléfono a través de un bot de Telegram.

## Requisitos Previos

Para utilizar este proyecto, necesitarás:
- Python 3.x
- Un broker MQTT (como Mosquitto)
- Una cuenta de Telegram y un bot creado a través de BotFather

## Librerías Necesarias

- `paho-mqtt`: Cliente MQTT para Python.
- `python-telegram-bot`: API wrapper para interactuar con bots de Telegram.

Instala las dependencias con el siguiente comando:

```bash
pip install paho-mqtt python-telegram-bot
