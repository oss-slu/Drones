#Controlling a Swarm of Drones Developer Guide 
v1 Apr 25, 2023

## Table of Contents
* Requirements
* Hardware Requirements
* VR Control System
* Drones
* Control System
* Software Requirements
* VR Control System
* Drones
* Control System
* Installation Steps
* Control System and Drone OS Installation
* Drone Physical Installation
* How to Use MQTT
* Master Pi and Drones
* Unity
* Notes
* How to Use QGroundControl
* How to Setup VR
* VR Headset
* Desktop
* Notes
* Putting Everything Together


## Requirements 

### Hardware Requirements 
* VR Control System
* Oculus Quest 1 or 2 headset and controllers
* USC Type-C to USB Type-C cable 

### Drones
* Raspberry Pi 3 (Drone Pi)
* MicroSD card
* Pixhawk 4 mini
* Pixhawk 4 mini GPS attachment 
* 3 cell 11.1V lithium ion battery pack 
* 2.4GHz Aircraft Receiver
* Lumenier motors 

### Control System
* Laptop or desktop 
* Router 
* Raspberry Pi 3 (Master Pi)
* Monitor 
* HDMI cable 
* MicroUSB to USB cable 
* 12W power source

## Software Requirements
* Source Code: https://github.com/oss-slu/Drones

### VR Control System
* Meta Quest mobile application
* Unity Hub desktop application 
* Oculus desktop application 

### Drones 
* Raspberry Pi OS (Legacy)
* Python 3.7
* Mavsdk
* Mavproxy
* Mosquitto MQTT
* Paho Mqtt

### Control System 
* QGroundControl desktop application
* Raspberry Pi OS (Legacy)
* Python 3.7
* Mavsdk
* Mavproxy
* Mosquitto MQTT


## Installation Steps 
### Control System and Drone OS Installation 
*The following steps should be followed for the Master Pi and each drone’s Raspberry Pi*

### Install the Raspberry Pi OS
Download the Raspberry Pi Imager from: https://www.raspberrypi.com/software/
Run the imager and select the Raspberry Pi OS (Legacy) from the other OS options, insert and format a microSD card, then select write. 



### On each Raspberry Pi, install the following:
* Python 3.7  https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/
* Mavsdk https://mavsdk.mavlink.io/main/en/python/quickstart.html
* Mavproxy https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html#linux
* Mosquitto MQTT https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-debian-10
* Paho MQTT ***Drones Only*** http://www.steves-internet-guide.com/into-mqtt-python-client/


## Drone Physical Installation
Connect the Pixhawk 4 mini to the Raspberry Pi through UART&ITC B using pin 1 or 2 (*only one*) **red wire**, 3 **yellow wire**, 4 **blue wire**, and 5 **black wire**
If this step confuses you, look up documentation for raspberrypi uart ports, or click this link: https://raspberrypi.stackexchange.com/questions/104464/where-are-the-uarts-on-the-raspberry-pi-4 

### Connect the GPS to the Pixhawk 4 mini using the GPS Module Port 

Ensure that the battery pack is properly charged. Do not overcharge or plug in the battery until you are ready to fly the drone. It is imperative that you do not overcharge the battery as it could lead to damaged components. 

## How to Use MQTT

### Master Pi and Drones
1. Turn on the Master Pi
2. In the terminal, get the IP address using the command: hostname -I (Ex. IP address 192.168.1.117)
3. Initialize the Master Pi broker with the command: mosquitto_sub -h [IP_address] -t [topic_name]
4. Ex. mosquitto_sub -h 192.168.1.117 -t drone
5. Turn on a Drone Raspberry Pi and connect it to the same network as the Master Pi
6. Publish a test message using the command: mosquitto_pub -h [IP_address] -t [topic_name[ -m [“message”]
Ex. mosquitto_pub -h 192.168.1.117 -t drone -m “test message”

### Unity 
1. On the computer running Unity (see instructions below) download the M2Mqtt library https://www.nuget.org/api/v2/package/M2Mqtt/4.3.0
2. Rename the downloaded file extension from ".nupkg" to ".zip" and extract its contents
3. Locate the appropriate M2Mqtt DLLs in your files
4. Navigate to the "lib\net45" folder in the extracted package
5. Copy the "M2Mqtt.Net.dll" file
6. Import M2Mqtt into your Unity project by pasting the copied file into your Unity project's "Assets" folder

### Notes 
You can SSH into the drone’s Pi on another computer using the following command: ssh [username]@[IP address]
VR1sender.py and VR2sender.py are test scripts mimicking what the VR headsets send to the Master Pi


## How to Use QGroundControl 
1. Download the QGroundControl desktop application onto a computer 
2. Open QGroundControl 
3. Connect the Pixhawk 4 mini to the computer using the MicroUSB to USB cable. The top left corner on QGroundControl should say connected. 
4. You can also use telemetry to connect the computer and Pixhawk if you have the hardware for it
5. Adjust settings by clicking on the Q in the top left corner -> vehicle setup 
6. Summary: boxes must not have a red dot in the upper right corner
7. Airframe: Quadrotor x (*choose whatever model works best with your current drone design*) 
8. Select Lumenier QAV250 from dropdown menu

### Sensors: calibrate all sensors
Ex. Compass calibration requires you to rotate the Pixhawk in six directions
Again, all sensors need calibrated, gyroscope, acceloremeter, etc. 

### Power: *change as needed according to your battery*
Source: Power Module
Number of Cells (in Series): 3
Empty Voltage (per cell): 3.50 V
Full Voltage (per cell): 4.05 V
Voltage divider: calculate 
		
* Parameters:
MAVlink: MAV_0_RATE 57600 B/s
*Additional settings may need to be adjusted based on your hardware and wiring of the drone*


## How to Setup VR
*All devices must be connected to the same network*
1. You'll need a VR Headset (duh)
2. Download the Oculus desktop application and sign into your Meta account 
3. Go to devices and add headset 
4. Select Quest or Quest 2 depending on your headset 
5. Use the USB Type-C to USB Type-C cable to connect the headset 
*You can also use wifi to connect the headset* 


## Desktop 
1. Install Unity Hub on your desktop 
2. In Unity Hub, install 2020.3.47f1 LTS 
3. During the installation, you must check all of the boxes for Android and Windows build support 
4. Put Oculus in developer mode 
5. Install Meta Quest mobile application
6. Sign in with the same Meta account as your Oculus 
7. Create and join an organization 
8. Go to devices -> headset settings -> developer mode and turn on Developer Mode
9. Open VR code on Unity Editor using Unity Hub and the 2020.3.47f1 editor version 
10. Go to file -> build settings and switch platform to Android 
11. Texture Compression should be set to ASTC 
12. ETC2 fallback should be set to 32-bit
13. Choose the Oculus device from the Run Device dropdown menu 
14. Select Build And Run to send the VR code to the Oculus 
### **Notes**
#### If you want to open Unity Hub from the VR device:
* Go to settings -> Quest Link and turn on the link
* Choose the application you want to open 


## Putting Everything Together

### Drone
Connect the Pixhawk 4 mini to the Raspberry Pi situated on each drone 
Set up a power source on each drone (battery or outlet)
Connect the drone’s Pixhawk to QGroundControl and calibrate

### MasterPi
Turn on the Master Pi and run the broker using MQTT
Subscribe the drone to the Master Pi using MQTT 

### VR Headset
Turn on the VR headset and connect the headset to a computer or phone 
Open the VR code through Unity on your computer or through the headset
Build and Run the VR code to send to the headset 
Select the drone(s) and command that you want to execute via the VR 
















