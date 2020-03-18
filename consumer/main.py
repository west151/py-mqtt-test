# This Python file uses the following encoding: utf-8
#
# consumer
#

import paho.mqtt.client as mqtt
import configparser
import os
from datetime import datetime

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc), flush=True)

def on_message(mqttc, obj, msg):
    #print("message received ", str(msg.payload.decode("utf-8")), flush=True)
    array = bytearray(msg.payload)
    print("message received [0]: ", array[0], flush=True)
    print("message received len: ", len(array), flush=True)

    print("message topic =", msg.topic, flush=True)
    print("message qos =", msg.qos, flush=True)
    print("message retain flag =", msg.retain, flush=True)
    print("**********************************************", flush=True)

def on_publish(mqttc, obj, mid):
    print("---- " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ----", flush=True)
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos), flush=True)

# create a config file
def create_config(path):
    config = configparser.ConfigParser()
    config.add_section("broker")
    config.set("broker", "address", "127.0.0.1")
    config.set("broker", "port", "1883")
    config.add_section("topics")
    config.set("topics", "producer", "consumer/data")
    config.set("topics", "consumer", "producer/data")

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
    path = "consumer.ini"

    broker_address = get_setting(path, 'broker', 'address')
    broker_port = int(get_setting(path, 'broker', 'port'))
    topic_consumer_default = get_setting(path, 'topics', 'consumer')
    topic_producer_default = get_setting(path, 'topics', 'producer')

    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_publish = on_publish

    mqttc.connect(broker_address, broker_port, 60)
    mqttc.subscribe(topic_consumer_default, 0)

    mqttc.loop_forever()
