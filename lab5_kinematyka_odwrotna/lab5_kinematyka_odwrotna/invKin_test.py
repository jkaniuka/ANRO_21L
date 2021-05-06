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
import sys

# ------------------------------------------------------------------

# Program rozwiązujący zadanie kinematyki odwrotnej korzystając z solvera KDL
# ( program służy wyłącznie do celów testowych )

# Wywołanie:
# python3 invKin_test.py x y z
# gdzie x, y, z to zadane położenie w przestrzeni 

#-------------------------------------------------------------------



def checkCalculations():



	values = readYAMLfile()


	#Kinematic chain
	chain = Chain()
	base_link__link_1 = Joint(Joint.TransZ) 
	frame1 = Frame(Rotation.RPY(values[0][0],values[0][1],values[0][2]),
		Vector(values[1][0],values[1][1],values[1][2])) 
	segment1 = Segment(base_link__link_1,frame1)
	chain.addSegment(segment1) 


	link_1__link_2 = Joint(Joint.TransY) 
	frame2 = Frame(Rotation.RPY(values[2][0],values[2][1],values[2][2]),
		Vector(values[3][0],values[3][1],values[3][2]))
	segment2=Segment(link_1__link_2,frame2)
	chain.addSegment(segment2)


	link_2__link_3 = Joint(Joint.TransY) 
	frame3 = Frame(Rotation.RPY(values[4][0],values[4][1],values[4][2]),
		Vector(values[5][0],values[5][1],values[5][2]))
	segment3=Segment(link_2__link_3,frame3)
	chain.addSegment(segment3)

	# Nie uwzględniamy na razie offsetu na narzędzie, bo możliwe, że jego długość ulegnie zmianie w trakcie prac


	# Inverse kinematics

	# Zadana pozycja narzędzia
	target_position_x = float(sys.argv[1])
	target_position_y = float(sys.argv[2])
	target_position_z = float(sys.argv[3])

	print("Inverse Kinematics")

	# Zakładamy, że na początku zmienne złączowe mają wartość zero
	joints_initial_positions = JntArray(3)
	joints_initial_positions[0] = 0.0
	joints_initial_positions[1] = 0.0
	joints_initial_positions[2] = 0.0




	
	vik=ChainIkSolverVel_pinv(chain)
	fk=ChainFkSolverPos_recursive(chain)
	ik=ChainIkSolverPos_NR(chain,fk,vik)
	desiredFrame=Frame(Vector(target_position_x, target_position_y, target_position_z))

	# Wyświelam pozycję zadaną
	print("Desired Position: ", desiredFrame.p)



	# Wyliczone wartości zmiennych złączowych
	q_out=JntArray(3)
	ik.CartToJnt(joints_initial_positions,desiredFrame,q_out)
	print("Joints positions: ", '[', q_out[0], q_out[1], q_out[2], ']')


def readYAMLfile():


	with open(os.path.join(
		get_package_share_directory('lab4_interpolacja'),'urdf_wartosci.yaml'), 'r') as file:

		data = yaml.load(file, Loader=yaml.FullLoader)

	my_data=[]

	joint1_RPY = data['row1']['j_rpy']
	joint1_Vector = data['row1']['j_xyz']
	joint2_RPY = data['row2']['j_rpy']
	joint2_Vector = data['row2']['j_xyz']
	joint3_RPY = data['row3']['j_rpy']
	joint3_Vector = data['row3']['j_xyz']

	my_data.extend((joint1_RPY,joint1_Vector,joint2_RPY,joint2_Vector,joint3_RPY,joint3_Vector))

	values = []
	for element in my_data:
		new_element = element.split()
		list_of_floats = [float(item) for item in new_element]
		values.append(list_of_floats)


	return values


if __name__ == '__main__':
	checkCalculations()




  