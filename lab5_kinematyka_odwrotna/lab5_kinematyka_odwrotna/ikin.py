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
		
		# Obsługa markerów
		self.markerArray = MarkerArray()
		qos_profile1 = QoSProfile(depth=10)
		self.marker_pub = self.create_publisher(MarkerArray, '/marker', qos_profile1)
		self.marker = Marker()
		self.marker.header.frame_id = "base_link"
		self.marker.id = 0
		self.marker.action = Marker.DELETEALL
		self.markerArray.markers.append(self.marker)
		self.marker_pub.publish(self.markerArray)
		self.count = 0
		self.MARKERS_MAX = 1000

		self.subscription = self.create_subscription(
			PoseStamped(),
			'/pose_op_interpolation',
			self.listener_callback,
			10)
		self.subscription  

		self.last_x_val = 0
		self.last_y_val = 0
		self.last_z_val = 0






	def send_warning(self):
		self.ikin.get_logger().warn('Nie można przejść do żądanego położenia z podwodu mechanicznych ograniczeń manipulatora')



	def listener_callback(self, msg):

		joint1 = msg.pose.position.z
		joint2 = msg.pose.position.y
		joint3 = msg.pose.position.x

		d_values_from_DH = []
		# Obsługa markerów
		self.marker.type = self.marker.SPHERE
		self.marker.action = self.marker.ADD
		self.marker.scale.x = 0.05
		self.marker.scale.y = 0.05
		self.marker.scale.z = 0.05
		self.marker.color.a = 1.0

		for i, mark in enumerate(self.values.keys()):
            # przypisanie parametrów DH
			a, d, alpha, theta = self.values[mark]
			a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
			d_values_from_DH.append(d)


		##obsługa kinematyki odwrotnej
		x =  joint3 -d_values_from_DH[2] - 0.05
		y =  -(joint2 + d_values_from_DH[1]) 
		z =  joint1 - d_values_from_DH[0] - 1

		# Przygotowanie publishera
		qos_profile = QoSProfile(depth=10)
		self.joint_pub = self.create_publisher(JointState, '/joint_states', qos_profile)
		joint_state = JointState()
		now = self.get_clock().now()
		joint_state.header.stamp = now.to_msg()
		joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']
		print(x)
		print(y)
		print(z)

		if( not ((x <= 0) & (x > -d_values_from_DH[2])) or 
			not ((y <= 0) & (y > -d_values_from_DH[1])) or
			not ((z <= 0) & (z >= -d_values_from_DH[0]))):

			self.get_logger().warn("Position is out of range")
			joint_state.position = [float(self.last_z_val), float(self.last_y_val), float(self.last_x_val)]
			self.joint_pub.publish(joint_state)

			# Obsługa tablicy markerów
			self.marker.color.r = 0.9
			self.marker.color.g = 0.0
			self.marker.color.b = 0.0
			self.marker.pose.position.x = d_values_from_DH[2] + 0.05 + float(x)
			self.marker.pose.position.y = -d_values_from_DH[1] - float(y)
			self.marker.pose.position.z = d_values_from_DH[0] +1 + float(z)

			if(self.count > self.MARKERS_MAX):
				pass
				# self.markerArray.markers.pop(0)
			
			self.count += 1
			self.markerArray.markers.append(self.marker)

			id = 0
			for m in self.markerArray.markers:
				m.id = id
				id += 1

			#Publikowanie tablicy markerów
			self.marker_pub.publish(self.markerArray)
		else:

			joint_state.position = [z, y, x]
			self.last_x_val = x
			self.last_y_val = y
			self.last_z_val = z
			
			self.joint_pub.publish(joint_state)

			# Obsługa tablicy markerów
			self.marker.color.r = 0.0
			self.marker.color.g = 1.0
			self.marker.color.b = 0.0
			
			# Przypisanie wartości dla markerów
			self.marker.pose.position.x = d_values_from_DH[2] + 0.05 + float(x)
			self.marker.pose.position.y = -d_values_from_DH[1] - float(y)
			self.marker.pose.position.z = d_values_from_DH[0] +1 + float(z)

			if(self.count > self.MARKERS_MAX):
				self.markerArray.markers.pop(0)
			
			self.count += 1

			self.markerArray.markers.append(self.marker)

			id = 0
			for m in self.markerArray.markers:
				m.id = id
				id += 1

			#Publikowanie tablicy markerów
			self.marker_pub.publish(self.markerArray)

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

