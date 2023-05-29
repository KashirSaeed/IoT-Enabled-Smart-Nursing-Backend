import json
import threading
import time
from pusher import Pusher
import pysher

from smartNursingBackend.postData import postData


pusher = ''
clientPusher = ''

def initPusher():
    global pusher
    global clientPusher
    pusher = Pusher(app_id='1608704', key='935efa930a4fab68ba80', secret='44f2ebdd48cd40bf2ce9', cluster='ap2',  ssl=True)
    clientPusher = pysher.Pusher('935efa930a4fab68ba80', 'ap2')
    clientPusher.connection.bind('pusher:connection_established', connectHandler)
    clientPusher.connect()
            
''' This function is called once pusher has successfully established a connection'''
def connectHandler(data):
    global pusher
    global clientPusher
    channel = clientPusher.subscribe('activity-channel')
    channel.bind('activity', pusherCallback)

''' This function is called once pusher receives a new event '''
def pusherCallback(message):
    data = json.loads(message)
    print("Receiving Data from pusher",data['activity'])
    try:
        postThread=threading.Thread(target=postData,args=(data['activity'],), daemon=True)
        postThread.start()
    except Exception as e:
        print("Error sending data to db" , e)