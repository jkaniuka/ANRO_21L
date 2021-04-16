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



class NonKdl_dkin(Node):


    def __init__(self):
        super().__init__('NonKdl_dkin')

        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.listener_callback,
            10)
        self.subscription


    def listener_callback(self, msg):

        values = readDHfile()
        T = []

        for i, mark in enumerate(values.keys()):

            a, d, alpha, theta = values[mark]
            a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
            # przekształcenia macierzowe
            translation_z = mathutils.Matrix.Translation((0, 0, d+msg.position[i]))
            rotation_z = mathutils.Matrix.Rotation(theta, 4, 'Z')
            translation_x = mathutils.Matrix.Translation((a, 0, 0))
            rotation_x =mathutils.Matrix.Rotation(alpha,4,  'X')

            # przemnożenie macierzy
            m = translation_x @ rotation_x @ translation_z @ rotation_z 
            T.append(m)


        T_02 = T[0] @ T[1] @ T[2] 
        xyz = T_02.to_translation()
        rpy = T_02.to_euler()
        qua = rpy.to_quaternion()
        
        qos_profile = QoSProfile(depth=10)
        pose_publisher = self.create_publisher(PoseStamped, '/pose_stamped', qos_profile)


        poses = PoseStamped()
        now = self.get_clock().now()
        poses.header.stamp = ROSClock().now().to_msg()
        poses.header.frame_id = "base_link"

        poses.pose.position.x = xyz[0]
        poses.pose.position.y = xyz[1]
        poses.pose.position.z = xyz[2]+1
        poses.pose.orientation = Quaternion(w=qua[0], x=qua[1], y=qua[2], z=qua[3])

        pose_publisher.publish(poses)



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