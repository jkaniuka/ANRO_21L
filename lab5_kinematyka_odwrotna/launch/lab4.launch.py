import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node

def generate_launch_description():


    rviz_file_name = 'lab4_pose.rviz'
    rviz = os.path.join(
        get_package_share_directory('lab5_kinematyka_odwrotna'),
        rviz_file_name)

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(package = "tf2_ros", 
            executable = "static_transform_publisher",
            arguments = ['0', '0', '0', '0', '0', '0', '1', 'map', 'base_frame']),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-d', rviz]),
    ])