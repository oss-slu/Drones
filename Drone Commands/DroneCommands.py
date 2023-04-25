# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 21:49:48 2023

@author: omars
"""
import paho.mqtt.client as mqtt
import time
import asyncio
from mavsdk import System
import json

connect_flag_drone = 0
takeoff_flag = 0 #0 is landed, 1 is taken off

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
    droneID = 1
    parseMessage(m_decode, droneID)


def parseMessage(m_decode, droneID):
    #checks id and returns command if matched id
    if droneID in m_decode["DroneID"]:
        asyncio.run(execute_command(m_decode["Commands"]))

def create_mqtt_client():
    # create a MQTT client and connect it to the broker here
    mqtt_config = get_mqtt_config()

    client=mqtt.Client("Drone1")
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
    client.subscribe("drone")

async def execute_command(command):
    global connect_flag_drone
    global takeoff_flag
    
    if connect_flag_drone == 0:
        print('connecting')
        # Connect to the drone
        drone = System()
        
        await drone.connect(system_address="serial:///dev/serial0:57600")
        print('connected')
        
        connect_flag_drone = 1

    if command == "TAKEOFF" and takeoff_flag == 0:
        try:
            print("arming")
            await drone.action.arm()

            print("take off")
            await drone.param.set_param_float("MIS_TAKEOFF_ALT", 0.5)
            await drone.action.takeoff()
            
            takeoff_flag = 1
        except:
            print("Error: takeoff denied, no GPS lock")
            
    if command == "LAND" and takeoff_flag == 1:
        try:
            print("landing")
            await drone.action.land()

            await drone.action.disarm()

            takeoff_flag = 0
        except:
            print("Error: landing denied, no flight in progress")
            
def main():

    client = create_mqtt_client() # create and connect to the MQTT broker
    subscribe_to_topics(client)
    client.loop_forever()


if __name__ == '__main__':
    main()
