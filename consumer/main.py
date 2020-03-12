# This Python file uses the following encoding: utf-8
#
# consumer
#

import paho.mqtt.client as mqtt

broker_address="127.0.0.1"
broker_port=1883
topic_consumer_default="consumer/data"
topic_producer_default="producer/data"

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc), flush=True)

def on_message(mqttc, obj, msg):
    print("message received ", str(msg.payload.decode("utf-8")), flush=True)
    print("message topic=", msg.topic, flush=True)
    print("message qos=", msg.qos, flush=True)
    print("message retain flag=", msg.retain, flush=True)

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos), flush=True)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe

mqttc.connect(broker_address, broker_port, 60)
mqttc.subscribe(topic_producer_default, 0)

mqttc.loop_forever()
