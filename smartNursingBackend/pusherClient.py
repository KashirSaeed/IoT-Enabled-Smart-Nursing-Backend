import json
import threading
import time
from pusher import Pusher
import pysher

from smartNursingBackend.postData import postData


def initPusher():
    global clientPusher
    clientPusher = pysher.Pusher('935efa930a4fab68ba80', 'ap2')
    clientPusher.connection.bind('pusher:connection_established', connectHandler)
    clientPusher.connect()
            
''' This function is called once pusher has successfully established a connection'''
def connectHandler(data):
    global channel
    channel = clientPusher.subscribe('activity-channel')
    channel.bind('activity', pusherCallback)

''' This function is called once pusher receives a new event '''
def pusherCallback(message):
    global counter
    data = json.loads(message)
    try:
        postThread=threading.Thread(target=postData,args=(data,))
        postThread.start()
    except Exception as e:
        print("Error sending data to db" , e)
    return
    
def killPusher():
    clientPusher.disconnect()
        