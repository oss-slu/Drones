#!/usr/bin/env python
# ROS python API
import rospy
import socket
import json

# 3D point & Stamped Pose msgs
from geometry_msgs.msg import Point, PoseStamped
# import all mavros messages and services
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from pymavlink import mavutil

# Flight modes class
# Flight modes are activated using ROS services
class fcuModes:
    def __init__(self):
        pass

    def setTakeoff(self):
    	rospy.wait_for_service('mavros/cmd/takeoff')
    	try:
    		takeoffService = rospy.ServiceProxy('mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL)
    		takeoffService(altitude = 1)
    	except rospy.ServiceException, e:
    		print ("Service takeoff call failed: %s")

    def setArm(self):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
            armService(True)
        except rospy.ServiceException, e:
            print ("Service arming call failed: %s")

    def setDisarm(self):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
            armService(False)
        except rospy.ServiceException, e:
            print ("Service disarming call failed: %s")

    def setStabilizedMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='STABILIZED')
        except rospy.ServiceException, e:
            print ("service set_mode call failed: %s. Stabilized Mode could not be set.")

    def setOffboardMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='OFFBOARD')
        except rospy.ServiceException, e:
            print ("service set_mode call failed: %s. Offboard Mode could not be set.")

    def setAltitudeMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='ALTCTL')
        except rospy.ServiceException, e:
            print ("service set_mode call failed: %s. Altitude Mode could not be set.")

    def setPositionMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='POSCTL')
        except rospy.ServiceException, e:
            print ("service set_mode call failed: %s. Position Mode could not be set.")

    def setAutoLandMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='AUTO.LAND')
        except rospy.ServiceException, e:
               print ("service set_mode call failed: %s. Autoland Mode could not be set.")

class Controller:
    # initialization method
    def __init__(self):
        # Drone state
        self.state = State()
        # Instantiate a setpoints message
        self.sp = PoseStamped()
        # We will fly at a fixed altitude for now. Altitude setpoint, [meters]
        self.ALT_SP = 1
        # update the setpoint message with the required altitude
        self.sp.pose.position.z = self.ALT_SP
        # Step size for position update
        self.STEP_SIZE = 2.0
	# Fence. We will assume a square fence for now
        self.FENCE_LIMIT = 5.0
        # A Message for the current local position of the drone
        self.local_pos = Point(0.00, 2, 1)
        # initial values for setpoints
        self.sp.pose.position.x = 0.00
        self.sp.pose.position.y = -2.00

    # Callbacks
    ## local position callback
    def posCb(self, msg):
        self.local_pos.x = msg.pose.position.x
        self.local_pos.y = msg.pose.position.y
        self.local_pos.z = msg.pose.position.z

    ## Drone State callback
    def stateCb(self, msg):
        self.state = msg

    ## Update setpoint message
    def updateSp(self):
        self.sp.pose.position.x = self.local_pos.x
        self.sp.pose.position.y = self.local_pos.y

    def x_dir(self):
    	self.sp.pose.position.x = self.local_pos.x + 5
    	self.sp.pose.position.y = self.local_pos.y

    def neg_x_dir(self):
    	self.sp.pose.position.x = self.local_pos.x - 5
    	self.sp.pose.position.y = self.local_pos.y

    def y_dir(self):
    	self.sp.pose.position.x = self.local_pos.x
    	self.sp.pose.position.y = self.local_pos.y + 5

    def neg_y_dir(self):
    	self.sp.pose.position.x = self.local_pos.x
    	self.sp.pose.position.y = self.local_pos.y - 5


# Main function
def main():

    # initiate node
    rospy.init_node('setpoint_node', anonymous=True)

    # flight mode object
    modes = fcuModes()

    # controller object
    cnt = Controller()

    # ROS loop rate
    rate = rospy.Rate(30.0)

    # Subscribe to drone state
    rospy.Subscriber('mavros/state', State, cnt.stateCb)

    # Setpoint publisher    
    sp_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=1)

    # Make sure the drone is armed
    while not cnt.state.armed:
        modes.setArm()
        rate.sleep()

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 37020))
    while True:
        print ("**** .120 waiting for bcast command")
        data, addr = client.recvfrom(1024)
        if data is not None:
            jsonData = json.loads(data)
            cmd = jsonData["uid-bcast"]["cmd"]
            if cmd == "start":
                print ("**** .120 recieved bcast command start.")
                break

    # We need to send few setpoint messages, before we activate OFFBOARD mode, so it takes effect
    k=0
    while k<100:
        sp_pub.publish(cnt.sp)
        rate.sleep()
        k = k + 1

    # activate OFFBOARD mode
    modes.setOffboardMode()
    print ("---- offboard mode triggered")

    # calculate the total offboard run time-duration
    last_request = rospy.Time.now() + rospy.Duration(90)

    # ROS main loop
    while not rospy.is_shutdown():
        if last_request < rospy.Time.now():
            break
        sp_pub.publish(cnt.sp)
        #print "----published---- x:%f ,y:%f, z:%f"%(cnt.sp.position.x,cnt.sp.position.y,cnt.sp.position.z)
    	rate.sleep()

    # activate auto land mode
    modes.setAutoLandMode()
    print ("---- auto-land mode triggered")
    rospy.sleep(10)

    # trigger disarm command
    modes.setDisarm()
    print ("---- disarmed")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
