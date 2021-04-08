from setuptools import setup
import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'lab3_kinematyka_prosta'

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
            'listener = lab3_kinematyka_prosta.NONKDL_DKIN:main',
        ],
    },
)
