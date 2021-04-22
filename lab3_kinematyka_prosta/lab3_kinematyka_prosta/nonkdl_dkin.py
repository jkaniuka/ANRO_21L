from math import sin, cos, pi
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
import time


class NonKdl_dkin(Node):


    def __init__(self):
        super().__init__('NonKdl_dkin')

        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.listener_callback,
            10)
        # timer_period = 0.1  # czas w sekundach
        # self.timer = self.create_timer(timer_period, self.listener_callback)
        self.subscription


    def listener_callback(self, msg):

        # pobranie parametrów DH
        values = readDHfile()
        T = []

        for i, mark in enumerate(values.keys()):

            # przypisanie parametrów DH
            a, d, alpha, theta = values[mark]
            a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)

            # przekształcenia macierzowe
            
            # msg.position[i] jest <= 0, d+msg.position to aktualne wysunięcie danego członu do przodu
            # względem końca poprzedniego członu
            translation_z = mathutils.Matrix.Translation((0, 0, d+msg.position[i]))
            rotation_z = mathutils.Matrix.Rotation(theta, 4, 'Z')
            translation_x = mathutils.Matrix.Translation((a, 0, 0))
            rotation_x =mathutils.Matrix.Rotation(alpha,4,  'X')

            # przemnożenie macierzy
            m = translation_x @ rotation_x @ translation_z @ rotation_z 
            T.append(m)


        T_02 = T[0] @ T[1] @ T[2] 
        # wyznaczenie pozycji koncówki
        xyz = T_02.to_translation()
        # wyznaczenie orientacji końcówki
        rpy = T_02.to_euler()
        qua = rpy.to_quaternion()
        
        # stworzenie tematu pose_stamped_nonkdl
        qos_profile = QoSProfile(depth=10)
        pose_publisher = self.create_publisher(PoseStamped, '/pose_stamped_nonkdl', qos_profile)

        #utworzenie wiadomości
        pose = PoseStamped()
        now = self.get_clock().now()
        pose.header.stamp = ROSClock().now().to_msg()
        pose.header.frame_id = "base_link"

        # zapis informacji o pozycji do wiadomości
        pose.pose.position.x = xyz[0]+0.05
        pose.pose.position.y = xyz[1]
        pose.pose.position.z = xyz[2]+1
        pose.pose.orientation = Quaternion(w=qua[0], x=qua[1], y=qua[2], z=qua[3])
        # publikowanie wiadomości na temacie pose_stamped_nonkdl
        pose_publisher.publish(pose)



# czytanie parametrów tablicy DH z pliku
def readDHfile():

    with open(os.path.join(
        get_package_share_directory('lab3_kinematyka_prosta'),'Tablica_MD-H.json'), 'r') as file:

        values = json.loads(file.read())

    return values



def main(args=None):
    rclpy.init(args=args)

    nonkdl = NonKdl_dkin()
    rclpy.spin(nonkdl)

    nonkdl.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()