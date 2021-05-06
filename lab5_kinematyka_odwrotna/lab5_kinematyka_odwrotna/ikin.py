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
		self.subscription  # prevent unused variable warning


	def listener_callback(self, msg):
		x=0
		y=0
		z=0


		##obsługa kinematyki odwrotnej




		qos_profile = QoSProfile(depth=10)
		self.joint_pub = self.create_publisher(JointState, '/joint_states', qos_profile)
		joint_state = JointState()
		now = self.get_clock().now()
		joint_state.header.stamp = now.to_msg()
		joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']
		joint_state.position = [x, y, z]
		
		self.joint_pub.publish(joint_state)




def main(args=None):
	rclpy.init(args=args)

	ikin = ikin()
	rclpy.spin(ikin)

	ikin.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()

