# Struktura wiadomości

# float64 joint1_goal
# float64 joint2_goal
# float64 joint3_goal
# float64 roll_goal
# float64 pitch_goal
# float64 yaw_goal
# float64 time_of_move
# string type - liniowa/wielomianowa
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
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import time
import math 
import transforms3d

from interpolation_interfaces.srv import OpInterpolation


class MinimalService(Node):


    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(OpInterpolation, 'interpolacja_op', self.interpolation_callback)  

    def interpolation_callback(self, request, response):

        # Początkowa pozycja układu współrzędnych (położenie + orientacja)
        start_positions = [0, 0, 0]
        start_orientation = [0, 0, 0]
                                               
        self.get_logger().info('Incoming request')


        sample_time = 0.1 # przykładowo co 0.1s wysyłamy wiadomość
        total_time = request.time_of_move
        steps = math.floor(total_time/sample_time) # całkowita liczba kroków do pętli

        # Obsługa markerów
        markerArray = MarkerArray()
        qos_profile = QoSProfile(depth=10)

        self.marker_pub = self.create_publisher(MarkerArray, '/marker', qos_profile)
        marker = Marker()
        marker.header.frame_id = "/base_link"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        marker.color.a = 0.5
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.pose.orientation.w = 1.0
        marker.pose.orientation.x = 1.0
        marker.pose.orientation.y = 1.0
        marker.pose.orientation.z = 1.0

        # Wyznaczenie współczynników dla metody wielomianowej
        if(request.type == 'polynomial'):

            # Współczynniki dla interpolacji położenia

            a0 = [start_positions[0], start_positions[1], start_positions[2]]
            a2 = [3*((request.joint1_goal - start_positions[0])/(request.time_of_move)**2),
            3*((request.joint2_goal - start_positions[1])/(request.time_of_move)**2),
            3*((request.joint3_goal - start_positions[2])/(request.time_of_move)**2)]
            a3 = [-2*((request.joint1_goal - start_positions[0])/(request.time_of_move)**3),
            -2*((request.joint2_goal - start_positions[1])/(request.time_of_move)**3),
            -2*((request.joint3_goal - start_positions[2])/(request.time_of_move)**3),]


            # Współczynniki dla interpolacji orientacji

            a0_rpy = [start_orientation[0], start_orientation[1], start_orientation[2]]
            a2_rpy = [3*((request.roll_goal - start_orientation[0])/(request.time_of_move)**2),
            3*((request.pitch_goal - start_orientation[1])/(request.time_of_move)**2),
            3*((request.yaw_goal - start_orientation[2])/(request.time_of_move)**2)]
            a3_rpy= [-2*((request.roll_goal - start_orientation[0])/(request.time_of_move)**3),
            -2*((request.pitch_goal - start_orientation[1])/(request.time_of_move)**3),
            -2*((request.yaw_goal - start_orientation[2])/(request.time_of_move)**3),]

        for i in range(1,steps+1):

            qos_profile = QoSProfile(depth=10)
            pose_publisher = self.create_publisher(PoseStamped, '/pose_op_interpolation', qos_profile)
            poses = PoseStamped()
            now = self.get_clock().now()
            poses.header.stamp = ROSClock().now().to_msg()
            poses.header.frame_id = "map"

            # Interpolacja liniowa
            if(request.type == 'linear'):

                # Położenie
                poses.pose.position.x = start_positions[0] + ((request.joint1_goal - start_positions[0])/request.time_of_move)*sample_time*i
                poses.pose.position.y = start_positions[1] + ((request.joint2_goal - start_positions[1])/request.time_of_move)*sample_time*i
                poses.pose.position.z = start_positions[2] + ((request.joint3_goal - start_positions[2])/request.time_of_move)*sample_time*i

                # Orientacja w RPY
                frame_roll = start_orientation[0] + ((request.roll_goal - start_orientation[0])/request.time_of_move)*sample_time*i
                frame_pitch = start_orientation[1] + ((request.pitch_goal - start_orientation[1])/request.time_of_move)*sample_time*i
                frame_yaw = start_orientation[2] + ((request.yaw_goal - start_orientation[2])/request.time_of_move)*sample_time*i

                

            # interpolacja wielomianowa
            if(request.type == 'polynomial'):
                # Położenie
                poses.pose.position.x = a0[0] + a2[0]*(sample_time*i)**2 + a3[0]*(sample_time*i)**3 
                poses.pose.position.y = a0[1] + a2[1]*(sample_time*i)**2 + a3[1]*(sample_time*i)**3 
                poses.pose.position.z = a0[2] + a2[2]*(sample_time*i)**2 + a3[2]*(sample_time*i)**3 


                # Orientacja RPY
                frame_roll = a0_rpy[0] + a2_rpy[0]*(sample_time*i)**2 + a3_rpy[0]*(sample_time*i)**3 
                frame_pitch = a0_rpy[0] + a2_rpy[0]*(sample_time*i)**2 + a3_rpy[0]*(sample_time*i)**3 
                frame_yaw = a0_rpy[0] + a2_rpy[0]*(sample_time*i)**2 + a3_rpy[0]*(sample_time*i)**3 

            # Przeliczenie na radiany do funkcji euler2quat
            frame_roll = frame_roll*math.pi/180
            frame_pitch = frame_pitch*math.pi/180
            frame_yaw = frame_yaw*math.pi/180





            # Konwersja z RPY na kwaternion
            ##quaternion = tf.transformations.quaternion_from_euler(frame_roll, frame_pitch, frame_yaw)
            quaternion = transforms3d.euler.euler2quat(frame_roll, frame_pitch, frame_yaw, axes='sxyz')
            poses.pose.orientation = Quaternion(w=quaternion[0], x=quaternion[1], y=quaternion[2], z=quaternion[3])




            # Przypisanie wartości dla markerów
            marker.pose.position.x = poses.pose.position.x
            marker.pose.position.y = poses.pose.position.y
            marker.pose.position.z = poses.pose.position.z

            

            # Obsługa tablicy markerów
            markerArray.markers.append(marker)

            id = 0
            for m in markerArray.markers:
                m.id = id
                id += 1

            #Publikowanie tablicy markerów
            self.marker_pub.publish(markerArray)


            # Publikowanie pozycji układu współrzędnych
            pose_publisher.publish(poses)

            



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