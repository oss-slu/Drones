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
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print(f'message received {m_decode}')
    #parseMessage(json.loads(m_decode), client)

#def parsemessage(message, client):
#    for role in message['mission_roles']:
#        file = open(f'./json_files/{role["role"]}.json')
#        data = json.load(file)
#        data['waypoints'] = []
#        #print(data['waypoints'])
#        for drone in role['drone_list']:
#            '''
#            # todo: demo code only - fix it properly for all roles 
#            print("data coming from the front end {}".format(drone))
#            if role["role"] == 'birds_eye_surveillance':
#                data['waypoints'].append(drone["hoverpoint"])
#            else:
#                data['waypoints'] = drone["waypoints"]
#            '''
#            print("sending this json {}".format(data));
#            client.publish(f'drone/{drone["id"]}/mission-spec', json.dumps(data))
#            with open(f'{drone["id"]}.json','w') as f:
#                json.dump(data,f)
#            f.close()

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
