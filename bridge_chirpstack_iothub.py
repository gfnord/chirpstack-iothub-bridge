from azure.iot.device import IoTHubDeviceClient, Message

import paho.mqtt.client as mqtt
import json


# Variables
# The device connection string to authenticate the device with your IoT hub.
CONNECTION_STRING = ('HostName=xxx.azure-devices.net;'
                     'DeviceId=abc123123;'
                     'SharedAccessKey=...')
iot_hub_name = "your_iot_hub_name"

# Local Chirpstack MQTT
broker_address = 'localhost'
broker_port = 1883
broker_user = "bridgeuser"
broker_password = "bridgepassword"
application_id = '1'  # change for your application id in chirpstack


# PAHO MQTT CALLBACKS
def on_message(client, userdata, message):
    try:
        print("message received: " ,str(message.payload))
        print("Parsing Payload Json:")
        # try and parse to Json
        jsonData = json.loads(message.payload)
        if "object" in jsonData:
            print("DeviceID : ", jsonData["devEUI"])
            jsonData["object"]["application_id"] = application_id
            jsonData["object"]["devEUI"] = jsonData["devEUI"]
            jsonDataString = json.dumps(jsonData["object"])
            print("Object:  : ", jsonData["object"])
            print("Azure: sending message...")
            try:
                message = Message(jsonDataString)
                message.message_id = uuid.uuid4()
                message.correlation_id = "correlation-1234"
                print("Azure:Connecting azure client")
                azure_client.connect()
                print("Azure:Connected Azure client. Sending message...")
                azure_client.send_message(message)
                print("Azure: Message Sent. ")
                azure_client.disconnect()

            except Exception as iothub_error:
                print ( "Unexpected error %s from IoTHub" % iothub_error )
        else:
            print("Info: Parsed Json did not contain 'object'")
    except Exception as e:
        print("Some error inside MQTT message callback the message")
        print(e)

#####
# IOT HUB SDK
#####

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

# Connection to Chirpstack pub/sub broker
client = mqtt.Client("bridge") #create new instance
client.on_message=on_message #attach function to callback
print("Connecting to pub/sub broker.")
client.username_pw_set(username=broker_user, password=broker_password)
client.connect(broker_address, broker_port) #connect to broker

# Connection to Azure IoT Hub
azure_client = iothub_client_init()

print("Mosquitto: Subscribing to device rx topic")
client.subscribe("application/" + application_id + "/device/+/rx")

client.loop_forever()
