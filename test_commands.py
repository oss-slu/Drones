import rospy
from mavros_msgs.msg import *
from mavros_msgs.srv import *

def setArm():
   rospy.wait_for_service('/mavros/cmd/arming')
   try:
       armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
       armService(True)
   except rospy.ServiceException:
       print("Service arm call failed")

def setDisarm():
   rospy.wait_for_service('/mavros/cmd/arming')
   try:
       armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
       armService(False)
   except rospy.ServiceException:
       print ("Service arm call failed")


if __name__ == "__main__":
   rospy.init_node('gapter_pilot_node', anonymous=True)
   rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, globalPositionCallback)
   velocity_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
