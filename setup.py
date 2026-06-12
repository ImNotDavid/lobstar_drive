from setuptools import find_packages, setup

package_name = 'lobstar_drive'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='winton',
    maintainer_email='davidcai918@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'drive_node = lobstar_drive.drive_node:main',
            'serial_bridge = lobstar_drive.serial_bridge:main',
            'joy_pub.py = lobstar_drive.joy_pub:main',
        ],
    },
)
