Controlling a Swarm of Drones User Guide v1 Apr 30, 2023

Table of Contents How to Setup VR and Desktop VR Headset Desktop Notes
Usage

This guide is intended to help any users, regardless of their background
or skill level, use our software. For detailed directions and software
or hardware troubleshooting, refer to the Developers Guide.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ How to Setup VR and Desktop \*All
devices must be connected to the same network\* VR Headset  1. Download
the Oculus desktop application and sign into your Meta account 2. Go to
devices and add headset  1. Select Quest or Quest 2 depending on your
headset 2. Use the USB Type-C to USB Type-C cable to connect the headset
 1. You can also use wifi to connect the headset

Desktop  1. Install Unity Hub on your desktop

2\. In Unity Hub, install 2020.3.47f1 LTS  1. During the installation,
you must check all of the boxes for Android and Windows build support 3.
Put Oculus in developer mode  1. Install Meta Quest mobile application
2. Sign in with the same Meta account as your Oculus 3. Create and join
an organization 4. Go to devices -\> headset settings -\> developer mode
and turn on Developer Mode

4\. Open VR code on Unity Editor using Unity Hub and the 2020.3.47f1
editor version  1. Go to file -\> build settings and switch platform to
Android 2. Texture Compression should be set to ASTC 3. ETC2 fallback
should be set to 32-bit 4. Choose the Oculus device from the Run Device
dropdown menu 5. Select Build And Run to send the VR code to the Oculus
Notes If you want to open Unity Hub from the VR device: 1. Go to
settings -\> Quest Link and turn on the link 2. Choose the application
you want to open

Usage Once you have the VR device set up, the application open, and
everything ready to go, you should be able to look around and see a
virtual environment through the VR headset. In this environment, you
should be able to see a simulation of your drones (which will be on the
floor to begin) and a layout of buttons. If you don't see this, you may
have to look around in different directions until you find it. Once you
see it and are standing in front of it, you should be able to use the
buttons to send commands to the drone. On the right side, you'll see a
panel of buttons that allow you to select or unselect the drones. You
can use your hand to click on the drone you want to select or unselect.
If the drone button has an orange outline, then it is selected,
otherwise it is unselected. After this, you can go ahead and click one
of the buttons up above that will send a command to the selected drones.
Our project currently only has the takeoff and land buttons working. If
the drone is on the ground, then it will not be able to execute the land
button, and if it's in the air then it won't be able to execute the
takeoff function.
