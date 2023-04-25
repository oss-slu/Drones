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
    for drone in m_decode["DroneID"]:
        if droneID == drone:
            execute_command(m_decode["Commands"])

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

async def connect_drone():
    return


async def execute_command(command):

    # Connect to the drone
    drone = System()
    print('connecting')
    await drone.connect(system_address="serial:///dev/serial0:57600")
    print('connected')

    if command == "TAKEOFF":
        print("arming")
        await drone.action.arm()

        print("take off")
        await drone.param.set_param_float("MIS_TAKEOFF_ALT", 0.5)
        await drone.action.takeoff()

    if command == "LAND":
        print("landing")
        await drone.action.land()

        await drone.action.disarm()


def main():

    client = create_mqtt_client() # create and connect to the MQTT broker
    subscribe_to_topics(client)
    # asyncio.run(connect_drone())
    client.loop_forever()


if __name__ == '__main__':
    main()
