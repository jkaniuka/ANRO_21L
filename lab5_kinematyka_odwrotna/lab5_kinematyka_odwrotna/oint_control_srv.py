# Struktura wiadomości

# float64 time_of_move
# string type 
# float64 figure_param_a
# float64 figure_param_b
# ---
# string confirmation 


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
import json
import transforms3d

from interpolation_interfaces.srv import OpInvKin

class MinimalService(Node):


    def __init__(self):
        super().__init__('minimal_service')
        self.values = readDHfile()

        # Wektor pozycji początkowych w stawach
        self.start_positions = [2, -3, 2]

        self.srv = self.create_service(OpInvKin, 'interpolacja_op', self.interpolation_callback)  
        self.subscribtion = self.create_subscription(JointState, '/joint_states', self.initial_pose_callback, 10)

    def initial_pose_callback(self,msg):
        # Pobranie pozycji startowej w celu poprawnego rozpoczęcia zadawania trajektorii referencyjnej
        self.start_positions[0] = 2 + msg.position[0]
        self.start_positions[1] = -3 - msg.position[1]
        self.start_positions[2] = 2 + msg.position[2]
        print(self.start_positions[0])
        print(self.start_positions[1])
        print(self.start_positions[2])

    def interpolation_callback(self, request, response):
        print(self.start_positions[0])
        print(self.start_positions[1])
        print(self.start_positions[2])
        last_x = self.start_positions[2]
        last_y = self.start_positions[1]
        last_z = self.start_positions[0]

        d_values_from_DH = []

        for i, mark in enumerate(self.values.keys()):
            # przypisanie parametrów DH
            a, d, alpha, theta = self.values[mark]
            a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
            d_values_from_DH.append(d)

        # Początkowa pozycja układu współrzędnych (położenie + orientacja)
        # Orientacja nas nie interesuje ( poza tym jest przecież stała xD )
        # Początkowa pozycja z subscribera
                                               
        self.get_logger().info('Incoming request')


        sample_time = 0.1 # przykładowo co 0.1s wysyłamy wiadomość
        total_time = request.time_of_move
        steps = math.floor(total_time/sample_time) # całkowita liczba kroków do pętli

        # Obsługa markerów
        markerArray = MarkerArray()


        qos_profile = QoSProfile(depth=10)

        self.marker_pub = self.create_publisher(MarkerArray, '/marker_pose', qos_profile)
        marker = Marker()
        marker.header.frame_id = "base_link"

        marker.id = 0
        marker.action = Marker.DELETEALL
        markerArray.markers.append(marker)

        ##self.marker_pub.publish(markerArray)

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

        # Trajektoria prostokąt
        if(request.type == 'rectangle'):

            ob = 2*request.figure_param_a+ 2*request.figure_param_b

            j = int((request.figure_param_a/ob)*steps)
            k = int((request.figure_param_b/ob)*steps)
            print(steps)
            print(j)
            print(k)
            while(True):


                for i in range(1,steps+1):
                    print(self.start_positions[0])
                    print(self.start_positions[1])
                    print(self.start_positions[2])
                    qos_profile = QoSProfile(depth=10)
                    pose_publisher = self.create_publisher(PoseStamped, '/pose_op_interpolation', qos_profile)
                    poses = PoseStamped()
                    now = self.get_clock().now()
                    poses.header.stamp = ROSClock().now().to_msg()
                    poses.header.frame_id = "/base_link"

                    poses.pose.position.x = float(last_x)

                    if i < j:
                        poses.pose.position.y = self.start_positions[1] + ((-d_values_from_DH[1]+request.figure_param_a - self.start_positions[1])/(request.time_of_move/(steps/j)))*sample_time*i
                        last_y = poses.pose.position.y
                        poses.pose.position.z = float(last_z)
                        print(poses.pose.position.y)


                    if i >= j and i <= j+k:
                        poses.pose.position.y = float(last_y)

                        poses.pose.position.z = self.start_positions[0] + (((d_values_from_DH[0]+1)-request.figure_param_b  - self.start_positions[0])/(request.time_of_move/(steps/k)))*sample_time*(i-j)
                        last_z = poses.pose.position.z
                        print(poses.pose.position.z)
                    if i > j+k and i < 2*j+k:
                        poses.pose.position.z = float(last_z)

                        poses.pose.position.y = self.start_positions[1]+request.figure_param_a - ((-d_values_from_DH[1] - self.start_positions[1]+request.figure_param_a)/(request.time_of_move/(steps/j)))*sample_time*(i-j-k)
                        last_y = poses.pose.position.y
                        print(poses.pose.position.y)
                    if i >= j+k+j and i <= 2*j+2*k:
                        poses.pose.position.y = float(last_y)

                        poses.pose.position.z = self.start_positions[0]-request.figure_param_b  - (((d_values_from_DH[0]+1)  - self.start_positions[0]-request.figure_param_b)/(request.time_of_move/(steps/k)))*sample_time*(i-j-k-j)
                        last_z = poses.pose.position.z
                        print(poses.pose.position.z)

                    if i > 2*j+2*k:
                        poses.pose.position.y = float(last_y)
                        poses.pose.position.z = float(last_z)
                        break

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
                    ##self.marker_pub.publish(markerArray)


                    # Publikowanie pozycji układu współrzędnych
                    pose_publisher.publish(poses)


                    time.sleep(sample_time)
            
        # Trajektoria elipsa
        if request.type == 'ellipse':



            while(True):


                for i in range(1,steps+1):
                    qos_profile = QoSProfile(depth=10)
                    pose_publisher = self.create_publisher(PoseStamped, '/pose_op_interpolation', qos_profile)
                    poses = PoseStamped()
                    now = self.get_clock().now()
                    poses.header.stamp = ROSClock().now().to_msg()
                    poses.header.frame_id = "/base_link"

                    poses.pose.position.x = float(last_x)
                    poses.pose.position.y = self.start_positions[1] + request.figure_param_a*math.cos(2 * math.pi * (1/request.time_of_move) * sample_time * i)
                    poses.pose.position.z = self.start_positions[0] + request.figure_param_b*math.sin(2 * math.pi * (1/request.time_of_move) * sample_time * i)


                    


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
                    ##self.marker_pub.publish(markerArray)


                    # Publikowanie pozycji układu współrzędnych
                    pose_publisher.publish(poses)


                    time.sleep(sample_time)




        response.confirmation = 'Interpolacja zakończona'
        return response

# czytanie parametrów tablicy DH z pliku
def readDHfile():

    with open(os.path.join(
        get_package_share_directory('lab5_kinematyka_odwrotna'),'Tablica_MD-H.json'), 'r') as file:

        values = json.loads(file.read())

    return values



def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()

if __name__ == '__main__':
    main()