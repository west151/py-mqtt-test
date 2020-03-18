# This Python file uses the following encoding: utf-8
#
# producer
#

import paho.mqtt.client as mqtt
import configparser
import os
from datetime import datetime

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    print("message topic=", msg.topic)
    print("message qos=", msg.qos)
    print("message retain flag=", msg.retain)

def on_publish(mqttc, obj, mid):
    print("---- " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ----", flush=True)
    print("mid: " + str(mid))

# create a config file
def create_config(path):
    config = configparser.ConfigParser()
    config.add_section("broker")
    config.set("broker", "address", "127.0.0.1")
    config.set("broker", "port", "1883")
    config.add_section("topics")
    config.set("topics", "producer", "producer/data")

    with open(path, "w") as config_file:
        config.write(config_file)

# returns the config object
def get_config(path):
    if not os.path.exists(path):
       create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config

# print out a setting
def get_setting(path, section, setting):
    config = get_config(path)
    value = config.get(section, setting)
    msg = "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value
    )

    print(msg)
    return value

if __name__ == "__main__":
    path = "producer.ini"

    broker_address = get_setting(path, 'broker', 'address')
    broker_port = int(get_setting(path, 'broker', 'port'))

    topic_producer_default = get_setting(path, 'topics', 'producer')

    # MQTT
    mqttc = mqtt.Client("producer-001")
    mqttc.on_message = on_message
    mqttc.on_publish = on_publish
    mqttc.connect(broker_address, broker_port, 60)
    mqttc.loop_start()

    for i in range(0, 10):
        values = [i for q in range(0,15)]
        array = bytearray(values)
        mqttc.publish(topic_producer_default, array, qos=0)

    #while True:
    #    print("1", flush=True)
    #    time.sleep(1)

    mqttc.disconnect()
    mqttc.loop_stop()
