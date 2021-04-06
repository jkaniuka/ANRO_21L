from setuptools import setup
import os
from glob import glob
from setuptools import setup
from setuptools import find_packages
package_name = 'lab2_manipulator'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.py')),
        (os.path.join('share', package_name), glob('urdf/*')),
        (os.path.join('share', package_name), glob('lab2_manipulator/*.rviz'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='przemek',
    maintainer_email='przemekdaniel@interia.eu',
    description='Wizualizacja manipulatora',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'state_publisher = lab2_manipulator.state_publisher:main'
        ],
    },
)
