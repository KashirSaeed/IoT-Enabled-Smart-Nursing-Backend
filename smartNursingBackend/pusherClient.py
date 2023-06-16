import json
import threading
import time
from pusher import Pusher
import pysher
from smartNursingBackend.settings import logger
import datetime
from smartNursingBackend.postData import postData


def initPusher():
    logger.warning('Initialising Pusher '+str(datetime.datetime.now())+' hours!')
    global clientPusher
    try:
        clientPusher = pysher.Pusher('935efa930a4fab68ba80', 'ap2')
        clientPusher.connection.bind('pusher:connection_established', connectHandler)
        clientPusher.connect()
    except Exception as e:
        logger.warning("Error establishing Connection to Pusher"+str(datetime.datetime.now())+' hours!')

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
        logger.warning('Pushing Data over Pusher Channel '+str(datetime.datetime.now())+' hours!')
        postThread=threading.Thread(target=postData,args=(data,))
        postThread.start()
    except Exception as e:
        logger.warning("Error pushing data "+str(e)+str(datetime.datetime.now())+' hours!')
    return
    
def killPusher():
    logger.warning("Killing Pusher at "+str(datetime.datetime.now())+' hours!')
    try:
        clientPusher.disconnect()
    except Exception as e:
        logger.warning("Error killing Pusher "+str(e)+str(datetime.datetime.now())+' hours!')
        