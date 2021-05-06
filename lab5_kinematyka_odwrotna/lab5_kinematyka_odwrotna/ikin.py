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



class ikin(Node):

	def __init__(self):
		super().__init__('ikin')

		self.subscription = self.create_subscription(
			PoseStamped(),
			'/pose_op_interpolation',
			self.listener_callback,
			10)
		self.subscription  


	def listener_callback(self, msg):

		joint1 = msg.position[1]
		joint2 = msg.position[2]
		joint3 = msg.position[3]

		d_values_from_DH = []


        for i, mark in enumerate(values.keys()):

            # przypisanie parametrów DH
            a, d, alpha, theta = values[mark]
            a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
            d_values_from_DH.append(d)




		##obsługa kinematyki odwrotnej
		x = d_values_from_DH[2] - joint3
		y = -d_values_from_DH[1] + joint2
		z = d_values_from_DH[0] - joint1


		if( not (x < 0 & x > -d_values_from_DH[2])):
			send_warning()
		else if(not (y < 0 & y > -d_values_from_DH[1])):
			send_warning()
		else if(not (z < 0 & z > -d_values_from_DH[0])):
			send_warning()




		qos_profile = QoSProfile(depth=10)
		self.joint_pub = self.create_publisher(JointState, '/joint_states', qos_profile)
		joint_state = JointState()
		now = self.get_clock().now()
		joint_state.header.stamp = now.to_msg()
		joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']
		joint_state.position = [x, y, z]
		
		self.joint_pub.publish(joint_state)

	def send_warning(self):
		self.ikin.get_logger().warn('Nie można przejść do żądanego położenia z podwodu mechanicznych ograniczeń manipulatora')


# czytanie parametrów tablicy DH z pliku
def readDHfile():

    with open(os.path.join(
        get_package_share_directory('lab4_kinematyka_odwrotna'),'Tablica_MD-H.json'), 'r') as file:

        values = json.loads(file.read())

    return values



def main(args=None):

	values = readDHfile()

	rclpy.init(args=args)

	ikin = ikin()
	rclpy.spin(ikin)

	ikin.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()

