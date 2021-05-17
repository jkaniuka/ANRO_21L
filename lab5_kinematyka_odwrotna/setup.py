from setuptools import setup
import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'lab5_kinematyka_odwrotna'

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
        (os.path.join('share', package_name), glob('lab5_kinematyka_odwrotna/*')),
        (os.path.join('share', package_name), glob('*.json')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='przemek',
    maintainer_email='przemekdaniel@interia.eu',
    description='TODO: Package description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'service = lab5_kinematyka_odwrotna.jint_control_srv:main',
            'client = lab5_kinematyka_odwrotna.jint:main',
            'publ = lab5_kinematyka_odwrotna.joint_st_publ_kin:main', 
            'service2 = lab5_kinematyka_odwrotna.oint_control_srv:main',
            'client2 = lab5_kinematyka_odwrotna.oint:main',
            'ikin = lab5_kinematyka_odwrotna.ikin:main'
        ],
    },
)
