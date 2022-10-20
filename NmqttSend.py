import paho.mqtt.client as mqtt
import time
from random import randint
import json



connected = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        connected = True
        print("Connected")
    else:
        print("Not Able To Connect")

broker_address = "192.168.1.117"
user = ""
password = ""
name = "VR2"

client = mqtt.Client(name)
client.on_connect = on_connect
client.username_pw_set(user,password)
client.connect(broker_address)
time.sleep(0.4)
client.loop_start()
testnum = 0

def createCommand(ID, command, name):
    cdict= {
        "DroneID": ID,
        "Command": command,
        "VR_name": name,
        }
    return json.dumps(cdict)



while True:
    ID = randint(1,4)
    randCommand = randint(0,5)
    commandList = ["takeoff", "land", "left", "right", "up", "down"]
    command = commandList[randCommand]
    message = createCommand(ID, command, name)
    client.publish("test", message)
    print("Publishing... " + f"test{message}")
    testnum += 1
    time.sleep(4)
   
client.loop_stop()