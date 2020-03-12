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

#if __name__ == "__main__":
#    print("dddddddddddddddddddddddddddddddddd")

for i in range(0, 10):
    print("---- " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ----", flush=True)
    mqttc.publish(topic_producer_default, "55555555555555555555555555555555555555", qos=0)

#while True:
#    print("11111111111111111111111111111", flush=True)
#    time.sleep(1)


mqttc.disconnect()
mqttc.loop_stop()

##
#last_idle = last_total = 0
#while True:
#    with open('/proc/stat') as f:
#        fields = [float(column) for column in f.readline().strip().split()[1:]]
#    idle, total = fields[3], sum(fields)
#    idle_delta, total_delta = idle - last_idle, total - last_total
#    last_idle, last_total = idle, total
#    utilisation = 100.0 * (1.0 - idle_delta / total_delta)

#    print('%5.1f%%' % utilisation)
#    mqttc.publish(topic_cpu_utilisation, utilisation, qos=0)
#    time.sleep(5)

#mqttc.disconnect()

#mqttc.loop_stop()
