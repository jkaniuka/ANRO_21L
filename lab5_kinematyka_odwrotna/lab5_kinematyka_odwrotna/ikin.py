import os
import rclpy
import mathutils
from rclpy.node import Node
from rclpy.qos import QoSProfile
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformBroadcaster, TransformStamped
import json
from rclpy.clock import ROSClock
from PyKDL import *
import yaml



class Ikin(Node):

	def __init__(self):
		super().__init__('ikin')
		self.values = readDHfile()

		self.subscription = self.create_subscription(
			PoseStamped(),
			'/pose_op_interpolation',
			self.listener_callback,
			10)
		self.subscription  

	def send_warning(self):
		self.ikin.get_logger().warn('Nie można przejść do żądanego położenia z podwodu mechanicznych ograniczeń manipulatora')



	def listener_callback(self, msg):

		joint1 = msg.pose.position.z
		joint2 = msg.pose.position.y
		joint3 = msg.pose.position.x
		print("joint1: ", joint1)
		print("joint2: ", joint2)
		print("joint3: ", joint3)

		d_values_from_DH = []


		for i, mark in enumerate(self.values.keys()):
			print(mark)

            # przypisanie parametrów DH
			a, d, alpha, theta = self.values[mark]
			a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
			d_values_from_DH.append(d)




		##obsługa kinematyki odwrotnej
		x =  joint3 -2
		y =  -(joint2 +3) 
		z =  joint1 -2
		print("x",x)
		print("y", y)
		print("z", z)


		if( not ((x < 0) & (x > -d_values_from_DH[2]))):
			print("błąd")
			# send_warning()
		elif(not ((y < 0) & (y > -d_values_from_DH[1]))):
			print("błąd")
			# send_warning()
		elif(not ((z < 0) & (z > -d_values_from_DH[0]))):
			print("błąd")
			# send_warning()




		qos_profile = QoSProfile(depth=10)
		self.joint_pub = self.create_publisher(JointState, '/joint_states', qos_profile)
		joint_state = JointState()
		now = self.get_clock().now()
		joint_state.header.stamp = now.to_msg()
		joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']
		joint_state.position = [x, y, z]
		
		self.joint_pub.publish(joint_state)
		print("publik")


# czytanie parametrów tablicy DH z pliku
def readDHfile():

    with open(os.path.join(
        get_package_share_directory('lab5_kinematyka_odwrotna'),'Tablica_MD-H.json'), 'r') as file:

        values = json.loads(file.read())

    return values



def main(args=None):

	

	rclpy.init(args=args)

	ikin = Ikin()
	rclpy.spin(ikin)

	ikin.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()

