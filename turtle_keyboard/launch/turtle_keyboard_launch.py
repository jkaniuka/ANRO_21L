from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():


    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

       Node(
            package='turtle_keyboard',
            executable='param_talker',
            name='my_publisher_node',
            output='screen',
            emulate_tty=True,
            prefix="gnome-terminal --",


        )
    ])
