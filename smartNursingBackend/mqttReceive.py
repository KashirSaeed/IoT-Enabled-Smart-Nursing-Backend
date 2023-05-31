import paho.mqtt.client as paho
from paho import mqtt
import threading
import json
from smartNursingBackend.postData import postData
# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    data = {"activities":msg.payload.decode()}
    # print(type(data))
    # print(msg.payload)
    # print(msg.topic + " " + str(msg.qos) + " " + msg.payload.decode())
    try:
        postThread=threading.Thread(target=postData,args=(data,))
        postThread.start()
    except Exception as e:
        print("Error sending data to db" , e)
    return

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("iot-enabled", "sirsamyan")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("9de0b5ebb7c94ca2b0a8babceed188fa.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("activityDetection", qos=1)


# Start the MQTT loop to establish a connection and handle incoming messages
client.loop_start()

# Keep the receiver running to continue receiving messages
# while True:
#     pass
