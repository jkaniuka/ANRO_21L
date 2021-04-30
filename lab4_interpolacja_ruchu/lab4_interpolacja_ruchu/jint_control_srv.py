# Struktura wiadomości

# float64 joint1_goal
# float64 joint2_goal
# float64 joint3_goal
# float64 time_of_move
# ---
# string confirmation - na koniec napisze, że komunikacja zakończona


import rclpy
from rclpy.node import Node
import os
import mathutils
from rclpy.qos import QoSProfile
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from rclpy.clock import ROSClock
from sensor_msgs.msg import JointState
import time
import math  

#import się nie udaje (w necie widziałem, że dodają customowy service do CMake.txt, a my mamy jednynie package.xml)
from lab4_interpolacja_ruchu.srv import Interpolation



class MinimalService(Node):



    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(Interpolation, 'interpolacja', self.interpolation_callback)  

    def interpolation_callback(self, request, response):

        # Pozycje początkowe w stawach
        start_positions = [0, 0, 0]
                                               
        self.get_logger().info('Incoming request')

        # Publisher dla Kartmana
        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        joint_state = JointState()
        now = self.get_clock().now()
        joint_state.header.stamp = now.to_msg()
        joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']


        sample_time = 0.1 # przykładowo co 0.1s wysyłamy wiadomość
        total_time = request.time_of_move
        steps = math.floor(total_time/sample_time) # całkowita liczba kroków do pętli

        for i in range(1,steps+1):
            joint1_next = start_positions[0] + ((request.joint1_goal - start_positions[0])/request.time_of_move)*sample_time*i
            joint2_next = start_positions[1] + ((request.joint2_goal - start_positions[1])/request.time_of_move)*sample_time*i
            joint3_next = start_positions[2] + ((request.joint3_goal - start_positions[2])/request.time_of_move)*sample_time*i


            joint_state.position = [float(joint1_next), float(joint2_next), float(joint3_next)]
            self.joint_pub.publish(joint_state)
            time.sleep(sample_time)



        response.confirmation = 'Interpolacja zakończona'
        return response





def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()

if __name__ == '__main__':
    main()