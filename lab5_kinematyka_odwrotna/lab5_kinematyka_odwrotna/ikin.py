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

class Ikin(Node):

	def __init__(self, DHdata):
		# DHdata to wartości d z tabeli DH
		
		super().__init__('ikin')
		self.values = readDHfile()

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

	def send_warning(self):
		self.ikin.get_logger().warn('Nie można przejść do żądanego położenia z podwodu mechanicznych ograniczeń manipulatora')



	def listener_callback(self, msg):

<<<<<<< HEAD
		joint1 = msg.pose.position.z
		joint2 = msg.pose.position.y
		joint3 = msg.pose.position.x
		print("joint1: ", joint1)
		print("joint2: ", joint2)
		print("joint3: ", joint3)
=======
		# Pobieramy wartości przesunięć w złączach
		joint1 = msg.position[0]
		joint2 = msg.position[1]
		joint3 = msg.position[2]
>>>>>>> e28689091b115c9b1b8f9690b8f29cfe34e95109



<<<<<<< HEAD
		for i, mark in enumerate(self.values.keys()):
			print(mark)

            # przypisanie parametrów DH
			a, d, alpha, theta = self.values[mark]
			a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
			d_values_from_DH.append(d)
=======
		# obsługa kinematyki odwrotnej
		# (x, y, z) -> położenie w przestrzeni kartezjańskiej
		x = self.dh2 - joint3
		y = -self.dh1 + joint2
		z = self.dh0 - joint1

>>>>>>> e28689091b115c9b1b8f9690b8f29cfe34e95109

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



<<<<<<< HEAD
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


=======
# czytanie parametrów tablicy DH z pliku
def readDHfile():
>>>>>>> e28689091b115c9b1b8f9690b8f29cfe34e95109

    with open(os.path.join(
        get_package_share_directory('lab5_kinematyka_odwrotna'),'Tablica_MD-H.json'), 'r') as file:

<<<<<<< HEAD
		qos_profile = QoSProfile(depth=10)
		self.joint_pub = self.create_publisher(JointState, '/joint_states', qos_profile)
		joint_state = JointState()
		now = self.get_clock().now()
		joint_state.header.stamp = now.to_msg()
		joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']
		joint_state.position = [x, y, z]
		
		self.joint_pub.publish(joint_state)
		print("publik")
=======
        values = json.loads(file.read())

        # Wektorr kolejnych wartości d z tabeli DH
       	d_values_from_DH = []
>>>>>>> e28689091b115c9b1b8f9690b8f29cfe34e95109


        for i, mark in enumerate(values.keys()):

<<<<<<< HEAD
    with open(os.path.join(
        get_package_share_directory('lab5_kinematyka_odwrotna'),'Tablica_MD-H.json'), 'r') as file:
=======
            # przypisanie parametrów DH
            a, d, alpha, theta = values[mark]
            a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
            d_values_from_DH.append(d)
>>>>>>> e28689091b115c9b1b8f9690b8f29cfe34e95109


    return d_values_from_DH



def main(args=None):

	

	rclpy.init(args=args)

<<<<<<< HEAD
	ikin = Ikin()
=======
	ikin = ikin(values)
>>>>>>> e28689091b115c9b1b8f9690b8f29cfe34e95109
	rclpy.spin(ikin)

	ikin.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()

