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
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from PyKDL import *
import yaml



class Ikin(Node):

	def __init__(self):
		super().__init__('ikin')
		self.values = readDHfile()
		self.markerArray = MarkerArray()

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
		# Obsługa markerów
		
		qos_profile1 = QoSProfile(depth=10)
		self.marker_pub = self.create_publisher(MarkerArray, '/marker', qos_profile1)
		marker = Marker()
		marker.header.frame_id = "base_link"

		marker.id = 0
		marker.action = Marker.DELETEALL
		self.markerArray.markers.append(marker)

		self.marker_pub.publish(self.markerArray)

		marker.type = marker.SPHERE
		marker.action = marker.ADD
		marker.scale.x = 0.05
		marker.scale.y = 0.05
		marker.scale.z = 0.05
		marker.color.a = 1.0
		marker.color.r = 0.5
		marker.color.g = 0.5
		marker.color.b = 0.5



		for i, mark in enumerate(self.values.keys()):
			print(mark)

            # przypisanie parametrów DH
			a, d, alpha, theta = self.values[mark]
			a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
			d_values_from_DH.append(d)




		##obsługa kinematyki odwrotnej
		x =  joint3 -d_values_from_DH[2]
		y =  -(joint2 + d_values_from_DH[1]) 
		z =  joint1 - d_values_from_DH[0] - 1
		print("x", x)
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
		joint_state.position = [z, y, x]
		
		self.joint_pub.publish(joint_state)


		# Przypisanie wartości dla markerów
		marker.pose.position.x = 2 + float(x)
		marker.pose.position.y = -3 - float(y)
		marker.pose.position.z = 2 + float(z)

		# Obsługa tablicy markerów
		self.markerArray.markers.append(marker)

		id = 0
		for m in self.markerArray.markers:
			m.id = id
			id += 1

		#Publikowanie tablicy markerów
		self.marker_pub.publish(self.markerArray)
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

