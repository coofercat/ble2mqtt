from setuptools import setup

setup(
    name='ble2mqtt',
    version='0.1.0',    
    description='A simple Bluetooth Low Energy (BLE) beacon receiver that publishes to MQTT',
    url='https://github.com/coofercat/ble2mqtt',
    author='Ralph Bolton',
    author_email='null@example.com',
    license='GPL2',
    packages=['ble2mqtt', 'ble2mqtt.devices'],
    install_requires=['bluepy', 'paho-mqtt' ],

    classifiers=[
        'License :: OSI Approved :: GPL2',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    scripts=["bin/ble2mqtt"],
)

