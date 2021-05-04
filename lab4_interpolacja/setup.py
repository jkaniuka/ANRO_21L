from setuptools import setup
import os
from glob import glob
from setuptools import setup
from setuptools import find_packages
package_name = 'lab4_interpolacja'

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
        (os.path.join('share', package_name), glob('lab4_interpolacja/*')),
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
            'service = lab4_interpolacja.jint_control_srv:main',
            'client = lab4_interpolacja.jint:main',
            'publ = lab4_interpolacja.joint_st_publ_kin:main', 
            'service2 = lab4_interpolacja.oint_control_srv:main',
            'client2 = lab4_interpolacja.oint:main',
        ],
    },
)
