# Zarys (pseudokod) serwisu do interpolacji trajektorii

# Trzeba stworzyć folder /srv w naszym pakiecie i tam zdefiniować strukturę komunikacji
# Proponuję następujące rozwiązanie:

# float64 joint1_goal
# float64 joint2_goal
# float64 joint3_goal
# float64 time_of_move
# ---
# String confirmation - na koniec napisze, że komunikacja zakończona

# Potem importujemy ten plik



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


class MinimalService(Node):



    def __init__(self):
        super().__init__('minimal_service')

        # Servis - nazwy z tutoriala, potem się zmieni :-)
        self.srv = self.create_service(AddThreeInts, 'add_three_ints', self.add_three_ints_callback)  

        # Subscriber poda nam początkowe położenia w stawach 
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.position_callback,
            10)
        self.subscription 


    # Funkcja zwraca wektor początkowych położeń w stawach
    def start_position_callback(self, msg):
        positions = []
        x = msg.position[0]
        y = msg.position[1]
        z = msg.position[2]
        positions.append(x)
        positions.append(y)
        positions.append(z)

        return positions


    # Teoria:

    # Wzór na interpolację liniową to

    # q(t)=q0+ (qf-q0)/tf

    # gdzie:
    # q(t) - położenie w chwili t
    # q0 - położenie początkowe z funkcji start_position_callback()
    # qf - położenie zadane podawane z linii komend przez klienta serwisu (jint)
    # tf - zadany czas ruchu

    def add_three_ints_callback(self, request, response):

        # Pobieramy położenia początkowe
        start_positions = start_position_callback(self)

        # Położenia zadane to kolejno:

        # request.joint1_goal
        # request.joint2_goal
        # request.joint3_goal

                                               
        self.get_logger().info('Incoming request')

        # Publisher dla kartmana
        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        joint_state = JointState()
        now = self.get_clock().now()
        joint_state.header.stamp = now.to_msg()
        joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']




        


        sample_time = 0.1 # przykładowo co 0.1s wysyłamy wiadomośc
        total_time = request.time_of_move
        steps = math.floor(total_time/sample_time) # całkowita liczba kroków do pętli




        for i in range(1,steps+1):
            joint1_next = start_positions[0] + ((request.joint1_goal - start_positions[0])/time_of_move)*sample_time*i
            joint2_next = start_positions[1] + ((request.joint2_goal - start_positions[1])/time_of_move)*sample_time*i
            joint3_next = start_positions[2] + ((request.joint3_goal - start_positions[2])/time_of_move)*sample_time*i


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