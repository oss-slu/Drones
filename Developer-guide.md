#Controlling a Swarm of Drones Developer Guide 
v1 Apr 25, 2023

##Table of Contents
*Requirements
*Hardware Requirements
*VR Control System
*Drones
*Control System
*Software Requirements
*VR Control System
*Drones
*Control System
*Installation Steps
*Control System and Drone OS Installation
*Drone Physical Installation
*How to Use MQTT
*Master Pi and Drones
*Unity
*Notes
*How to Use QGroundControl
*How to Setup VR
*VR Headset
*Desktop
*Notes
*Putting Everything Together


##Requirements 

###Hardware Requirements 
*VR Control System
*Oculus Quest 1 or 2 headset and controllers
*USC Type-C to USB Type-C cable 

###Drones
*Raspberry Pi 3 (Drone Pi)
*MicroSD card
*Pixhawk 4 mini
*Pixhawk 4 mini GPS attachment 
*3 cell 11.1V lithium ion battery pack 
*2.4GHz Aircraft Receiver
*Lumenier motors 

###Control System
*Laptop or desktop 
*Router 
*Raspberry Pi 3 (Master Pi)
*Monitor 
*HDMI cable 
*MicroUSB to USB cable 
*12W power source

##Software Requirements
*Source Code: https://github.com/oss-slu/Drones

##VR Control System
*Meta Quest mobile application
*Unity Hub desktop application 
*Oculus desktop application 

##Drones 
*Raspberry Pi OS (Legacy)
*Python 3.7
*Mavsdk
*Mavproxy
*Mosquitto MQTT
*Paho Mqtt

##Control System 
*QGroundControl desktop application
*Raspberry Pi OS (Legacy)
*Python 3.7
*Mavsdk
*Mavproxy
*Mosquitto MQTT


##Installation Steps 
Control System and Drone OS Installation 
*The following steps should be followed for the Master Pi and each drone’s Raspberry Pi*

###Install the Raspberry Pi OS
Download the Raspberry Pi Imager from: https://www.raspberrypi.com/software/
Run the imager and select the Raspberry Pi OS (Legacy) from the other OS options, insert and format a microSD card, then select write. 



###On each Raspberry Pi, install the following:
Python 3.7 
https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/
Mavsdk
https://mavsdk.mavlink.io/main/en/python/quickstart.html
Mavproxy
https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html#linux
Mosquitto MQTT
https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-debian-10
Paho MQTT (this only needs to be downloaded on the drones)
http://www.steves-internet-guide.com/into-mqtt-python-client/

##Drone Physical Installation
Connect the Pixhawk 4 mini to the Raspberry Pi through UART&ITC B using pins 1 or 2 (red wire), 3 (yellow wire), 4 (blue wire), and 5 (black wire)



###Connect the GPS to the Pixhawk 4 mini using the GPS Module Port 

Ensure that the battery pack is properly charged. Do not overcharge or plug in the battery until you are ready to fly the drone. It is imperative that you do not overcharge the battery. 


##How to Use MQTT

###Master Pi and Drones
Turn on the Master Pi
In the terminal, get the IP address using the command: hostname -I
Ex. IP address 192.168.1.117
Initialize the Master Pi broker with the command: mosquitto_sub -h [IP_address] -t [topic_name]
Ex. mosquitto_sub -h 192.168.1.117 -t drone
Turn on a Drone Raspberry Pi and connect it to the same network as the Master Pi
Publish a test message using the command: mosquitto_pub -h [IP_address] -t [topic_name[ -m [“message”]
Ex. mosquitto_pub -h 192.168.1.117 -t drone -m “test message”
Unity 
On the computer running Unity (see instructions below) download the M2Mqtt library
https://www.nuget.org/api/v2/package/M2Mqtt/4.3.0
Rename the downloaded file extension from ".nupkg" to ".zip" and extract its contents
Locate the appropriate M2Mqtt DLLs in your files
Navigate to the "lib\net45" folder in the extracted package
Copy the "M2Mqtt.Net.dll" file
Import M2Mqtt into your Unity project by pasting the copied file into your Unity project's "Assets" folder

###Notes 
You can SSH into the drone’s Pi on another computer using the following command: ssh [username]@[IP address]
VR1sender.py and VR2sender.py are test scripts mimicking what the VR headsets send to the Master Pi

##How to Use QGroundControl 
Download the QGroundControl desktop application onto a computer 
Open QGroundControl 
Connect the Pixhawk 4 mini to the computer using the MicroUSB to USB cable. The top left corner on QGroundControl should say connected. 
You can also use telemetry to connect the computer and Pixhawk if you have the hardware for it
Adjust settings by clicking on the Q in the top left corner -> vehicle setup 
Summary: boxes must not have a red dot in the upper right corner
Airframe: Quadrotor x 
Select Lumenier QAV250 from dropdown menu

###Sensors: calibrate all sensors
Ex. Compass calibration requires you to rotate the Pixhawk in six directions
Again, all sensors need calibrated, gyroscope, acceloremeter, etc. 

###Power: (change as needed according to your battery)
Source: Power Module
Number of Cells (in Series): 3
Empty Voltage (per cell): 3.50 V
Full Voltage (per cell): 4.05 V
Voltage divider: calculate 
		
*Parameters:
MAVlink: MAV_0_RATE 57600 B/s
*Additional settings may need to be adjusted based on your hardware and wiring of the drone*




##How to Setup VR
*All devices must be connected to the same network*
VR Headset 
Download the Oculus desktop application and sign into your Meta account 
Go to devices and add headset 
Select Quest or Quest 2 depending on your headset 
Use the USB Type-C to USB Type-C cable to connect the headset 
You can also use wifi to connect the headset 

##Desktop 
Install Unity Hub on your desktop 
In Unity Hub, install 2020.3.47f1 LTS 
During the installation, you must check all of the boxes for Android and Windows build support 
Put Oculus in developer mode 
Install Meta Quest mobile application
Sign in with the same Meta account as your Oculus 
Create and join an organization 
Go to devices -> headset settings -> developer mode and turn on Developer Mode
Open VR code on Unity Editor using Unity Hub and the 2020.3.47f1 editor version 
Go to file -> build settings and switch platform to Android 
Texture Compression should be set to ASTC 
ETC2 fallback should be set to 32-bit
Choose the Oculus device from the Run Device dropdown menu 
Select Build And Run to send the VR code to the Oculus 
Notes
If you want to open Unity Hub from the VR device:
Go to settings -> Quest Link and turn on the link
Choose the application you want to open 



##Putting Everything Together
###Drone
Connect the Pixhawk 4 mini to the Raspberry Pi situated on each drone 
Set up a power source on each drone (battery or outlet)
Connect the drone’s Pixhawk to QGroundControl and calibrate

###MasterPi
Turn on the Master Pi and run the broker using MQTT
Subscribe the drone to the Master Pi using MQTT 

###VR Headset
Turn on the VR headset and connect the headset to a computer or phone 
Open the VR code through Unity on your computer or through the headset
Build and Run the VR code to send to the headset 
Select the drone(s) and command that you want to execute via the VR 
















