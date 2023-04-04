import paho.mqtt.client as mqtt
import time

message = ""

def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))
    print("message received ", message)
    # print("message topic=", message.topic)
    message_received = True
   
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        global connected
        connected = True
        print("Connected")
        print("..........")
    else:
        print("Unable To Connect")
       
connected = False
message_received = False
broker_address = "192.168.1.117"
MQTT_USER = ""
MQTT_PASSWORD = ""

print("creating new instance")
client = mqtt.Client("MQTT")

client.on_message = on_message
client.on_connect = on_connect

print("connecting to broker")
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(broker_address,port=1883)

client.loop_start()

print("Subscribing to topic", "test")
client.subscribe("test")

while connected != True or message_received != True:
    time.sleep(3)

client.loop_forever()
