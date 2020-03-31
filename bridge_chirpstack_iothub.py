from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv

import paho.mqtt.client as mqtt
import json
import uuid
import logging
import os


load_dotenv()

# create console handler and set level to debug
logger = logging.getLogger()
consoleHandler = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

# Variables
IOT_HUB_NAME = os.environ.get('IOT_HUB_NAME', 'default')

# Local Chirpstack MQTT
BROKER_ADDRESS = os.environ.get('BROKER_ADDRESS')
BROKER_PORT = int(os.environ.get('BROKER_PORT', 1883))
BROKER_USER = os.environ.get('BROKER_USER')
BROKER_PASSWORD = os.environ.get('BROKER_PASSWORD')

# change for your application id in chirpstack
APPLICATION_ID = os.environ.get('APPLICATION_ID')
MQTT_CLIENT_NAME = os.environ.get('MQTT_CLIENT_NAME', 'bridge')


# IOT HUB SDK
def iothub_client_init():
    # The device connection string to authenticate the device with your IoT hub
    connection_string = os.environ.get('AZURE_IOT_HUB_CONNECTION_STRING')
    return IoTHubDeviceClient.create_from_connection_string(connection_string)


# Connection to Azure IoT Hub
azure_client = iothub_client_init()


# PAHO MQTT CALLBACKS
def on_message(client, userdata, message):
    logger.info(f'Message received: {message.payload}')
    logger.info('Parsing Payload JSON...')

    # try and parse to Json
    json_data = json.loads(message.payload)

    if not isinstance(json_data, dict):
        return

    obj = json_data.get('object')

    if not obj:
        logging.warning('Parsed JSON did not contain "object".')

    else:
        logger.info('DeviceID : ', json_data.get('devEUI'))
        obj['APPLICATION_ID'] = APPLICATION_ID
        obj['devEUI'] = json_data['devEUI']

        json_data_str = json.dumps(obj)

        logger.info(f'Object: {json_data_str}')
        logger.info('Azure: sending message...')

        message_to_azure = Message(json_data_str)
        message_to_azure.message_id = uuid.uuid4()
        message_to_azure.correlation_id = 'correlation-1234'

        logger.info('Azure:Connecting azure client')
        azure_client.connect()

        logger.info('Azure:Connected Azure client. Sending message...')
        azure_client.send_message(message_to_azure)

        logger.info('Azure: Message Sent. ')
        azure_client.disconnect()


# Connection to Chirpstack pub/sub broker
client = mqtt.Client(MQTT_CLIENT_NAME)  # create new instance
client.on_message = on_message  # attach function to callback

logger.info('Connecting to pub/sub broker.')
client.username_pw_set(username=BROKER_USER, password=BROKER_PASSWORD)
client.connect(BROKER_ADDRESS, BROKER_PORT)  # connect to broker

logger.info('Broker: Subscribing to device rx topic')
client.subscribe('application/' + APPLICATION_ID + '/device/+/rx')

client.loop_forever()
