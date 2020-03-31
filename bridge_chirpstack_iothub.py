from azure.iot.device import IoTHubDeviceClient, Message

import paho.mqtt.client as mqtt
import json
import uuid


# Variables
# The device connection string to authenticate the device with your IoT hub.
CONNECTION_STRING = ('HostName=xxx.azure-devices.net;'
                     'DeviceId=abc123123;'
                     'SharedAccessKey=...')
iot_hub_name = 'your_iot_hub_name'

# Local Chirpstack MQTT
broker_address = 'localhost'
broker_port = 1883
broker_user = 'bridgeuser'
broker_password = 'bridgepassword'
application_id = '1'  # change for your application id in chirpstack


#####
# IOT HUB SDK
#####
def iothub_client_init():
    # Create an IoT Hub client
    return IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)


# Connection to Azure IoT Hub
azure_client = iothub_client_init()


# PAHO MQTT CALLBACKS
def on_message(client, userdata, message):
    print('Message received: ', message.payload)
    print('Parsing Payload Json:')

    # try and parse to Json
    json_data = json.loads(message.payload)

    if not isinstance(json_data, dict):
        return

    obj = json_data.get('object')

    if not obj:
        print('Info: Parsed Json did not contain "object"')

    else:
        print('DeviceID : ', json_data.get('devEUI'))
        obj['application_id'] = application_id
        obj['devEUI'] = json_data['devEUI']

        json_data_str = json.dumps(obj)

        print('Object: ', json_data_str)
        print('Azure: sending message...')

        message_to_azure = Message(json_data_str)
        message_to_azure.message_id = uuid.uuid4()
        message_to_azure.correlation_id = 'correlation-1234'

        print('Azure:Connecting azure client')
        azure_client.connect()

        print('Azure:Connected Azure client. Sending message...')
        azure_client.send_message(message_to_azure)

        print('Azure: Message Sent. ')
        azure_client.disconnect()


# Connection to Chirpstack pub/sub broker
client = mqtt.Client('bridge')  # create new instance
client.on_message = on_message  # attach function to callback

print('Connecting to pub/sub broker.')
client.username_pw_set(username=broker_user, password=broker_password)
client.connect(broker_address, broker_port)  # connect to broker

print('Mosquitto: Subscribing to device rx topic')
client.subscribe('application/' + application_id + '/device/+/rx')

client.loop_forever()
