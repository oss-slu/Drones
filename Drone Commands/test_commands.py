import rospy
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from geometry_msgs.msg import PoseStamped

def stateCallback(self, msg):
        self.state = msg

def setArm():
   rospy.wait_for_service('/mavros/cmd/arming')
   print("armed")
   try:
       armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
       armService(True)
   except rospy.ServiceException:
       print("Service arm call failed")

def setDisarm():
   rospy.wait_for_service('/mavros/cmd/arming')
   print("disarmed")
   try:
       armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
       armService(False)
   except rospy.ServiceException:
       print ("Service arm call failed")

def setOffboardMode():
	rospy.wait_for_service('mavros/set_mode')
	print("offboarded")
	try:
		flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
		flightModeService(custom_mode='OFFBOARD')
	except rospy.serviceException:
		print ("Service set_mode call failed")

def commandList():
	commands = ['arm', 'disarm', 'exit']
	while (not rospy.is_shutdown()):
		for command in commands:
			if command == 'arm':
				print("arming")
				setOffboardMode()
			elif command == 'disarm':
				print("disarming")
				setDisarm()
			elif command == 'exit':
				print("exit")
			 

if __name__ == "__main__":
   rospy.init_node('gapter_pilot_node', anonymous=True)
   rospy.Subscriber('mavros/state', State, stateCallback)
   velocity_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
   
   commandList()
   
   #/mavros/global_position/raw/fix"
