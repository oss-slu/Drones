#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import json

def on_connect(client,userdata,flags,rc):
    if rc==0:
        mqtt.Client.connected_flag=True
        print("connected OK")
    else:
        print("Bad Connection Returned code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code "+str(rc))
    client.loop_stop()

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=json.loads(msg.payload.decode("utf-8","ignore"))
    print(f'message received {m_decode}')
    #print(m_decode["Command"])
    droneID = 2
    parseMessage(m_decode, droneID)


def parseMessage(m_decode, droneID):
    #checks id and returns command if matched id
    if droneID == m_decode["DroneID"]:
        print(m_decode["Command"])











def create_mqtt_client():
    # create a MQTT client and connect it to the broker here
    mqtt_config = get_mqtt_config()
    
    client=mqtt.Client("missionConfigurator")
    client.connected_flag = False
    client.on_connect=on_connect
    client.on_disconnect=on_disconnect
    client.on_message=on_message

    client.connect(mqtt_config["broker"],mqtt_config["port"])

    return client
def get_mqtt_config(): 
    # fetch mqtt connecting string details here
    
    settings = json.load(open('./settings.json'))
    broker=settings['mqtt_broker_address']
    port = settings['mqtt_port']
    print("Connecting to broker {} at port {}".format(broker,port))
    return {"broker":broker, "port":port}

def subscribe_to_topics(client): 
    # subscribe to all topics here
    client.subscribe("test") 

def main():

    client = create_mqtt_client() # create and connect to the MQTT broker
    subscribe_to_topics(client)
    client.loop_forever()
  

if __name__ == '__main__':
    main()
