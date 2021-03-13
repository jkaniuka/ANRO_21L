from setuptools import setup


package_name = 'turtle_keyboard'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='janek',
    maintainer_email='kan.jan@wp.pl',
    description='User-defined keys to move turtle',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'param_talker = turtle_keyboard.new_keys:main',
        ],
    },
)
