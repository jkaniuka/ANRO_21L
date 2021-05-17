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


# Obsługa kinematyki odwrotnej

class ikin(Node):

	def __init__(self, DHdata):
		# DHdata to wartości d z tabeli DH
		
		super().__init__('ikin')

		# Parametry D z tabeli
		# Jest to tutaj, aby nie było parsowania z .json za każdym razem wywołania callback'u
		self.dh0 = DHdata[0];
		self.dh1 = DHdata[1];
		self.dh2 = DHdata[2];

		# Rozkazy dla węzła IKIN pochodzą z węzła interpolacji trajektorii w przestrzeni operacyjnej
		self.subscription = self.create_subscription(
			PoseStamped(),
			'/pose_op_interpolation',
			self.listener_callback,
			10)
		self.subscription  


	def listener_callback(self, msg):

		# Pobieramy wartości przesunięć w złączach
		joint1 = msg.position[0]
		joint2 = msg.position[1]
		joint3 = msg.position[2]



		# obsługa kinematyki odwrotnej
		# (x, y, z) -> położenie w przestrzeni kartezjańskiej
		x = self.dh2 - joint3
		y = -self.dh1 + joint2
		z = self.dh0 - joint1


		# Warningi
		if( not (x < 0 & x > -self.dh2)):
			self.get_logger().warn('Position out of limit')
		else if(not (y < 0 & y > -self.dh1)):
			self.get_logger().warn('Position out of limit')
		else if(not (z < 0 & z > -self.dh0)):
			self.get_logger().warn('Position out of limit')
		else:
			# Publikujemy na /joint_states TYLKO jeśli nie ma warningów
			qos_profile = QoSProfile(depth=10)
			self.joint_pub = self.create_publisher(JointState, '/joint_states', qos_profile)
			joint_state = JointState()
			now = self.get_clock().now()
			joint_state.header.stamp = now.to_msg()
			joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']
			joint_state.position = [x, y, z]
			
			self.joint_pub.publish(joint_state)



# czytanie parametrów tablicy DH z pliku
def readDHfile():

    with open(os.path.join(
        get_package_share_directory('lab5_kinematyka_odwrotna'),'Tablica_MD-H.json'), 'r') as file:

        values = json.loads(file.read())

        # Wektorr kolejnych wartości d z tabeli DH
       	d_values_from_DH = []


        for i, mark in enumerate(values.keys()):

            # przypisanie parametrów DH
            a, d, alpha, theta = values[mark]
            a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
            d_values_from_DH.append(d)


    return d_values_from_DH



def main(args=None):

	values = readDHfile()

	rclpy.init(args=args)

	ikin = ikin(values)
	rclpy.spin(ikin)

	ikin.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()

