# This Python file uses the following encoding: utf-8
#
# producer
#

import paho.mqtt.client as mqtt
import time
from datetime import datetime

broker_address="127.0.0.1"
broker_port=1883
topic_producer_default="producer/data"

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    print("message topic=", msg.topic)
    print("message qos=", msg.qos)
    print("message retain flag=", msg.retain)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

mqttc = mqtt.Client("client-001")
mqttc.on_message = on_message
mqttc.on_publish = on_publish

mqttc.connect(broker_address, broker_port, 60)

mqttc.loop_start()

for i in range(0, 10):
    print("---- " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ----", flush=True)
    values = [i for q in range(0,15)]
    array = bytearray(values)
    mqttc.publish(topic_producer_default, array, qos=0)

#while True:
#    print("1", flush=True)
#    time.sleep(1)

mqttc.disconnect()
mqttc.loop_stop()
