import os
from ssl import PROTOCOL_TLSv1_2
import threading
from django.dispatch import receiver
from smartNursingBackend.signals import update_signal
from smartNursingBackend.settings import BASE_DIR, DEFAULT_WS_PORT
from SimpleWebSocketServer import SimpleWebSocketServer, SimpleSSLWebSocketServer, WebSocket
from threading import Event
import base64
import cv2
import numpy as np
import logging
import PIL.Image as Image
import io

from smartNursingBackend.yolov5.postData import postData
from .yolov5.detect import detect

# from .yolov5.detect


# from .model import *

logger = logging.getLogger()
detectObj=detect()


class WebSocketHandler(WebSocket):



    @staticmethod
    def sendBroadcast(msg):
        # Broadcast a message to connected clients
        for ws in WSServerWrapper.ws_server.connections.values():
            ws.sendMessage(msg)

    # Signal handling methods

    @staticmethod
    @receiver(update_signal)
    def onUpdateSignal(**kwargs):
        logger.info('Received a signal')
        msg = kwargs.get('msg', '')
        # Broadcast the message received from update_signal
        WebSocketHandler.sendBroadcast(msg)

    # WebSocket handling methods

    def handleMessage(self):
        # image_64_decoded = base64.b64decode(self.data) 
        # imageNp = np.frombuffer(image_64_decoded, dtype = np.uint8)
        # # print("adsf",type(image_64_decoded))
        # print("img data type",type(imageNp), "shape",imageNp.shape)
        # img.show()
        # nparr = np.fromstring(self.data, np.uint8)
        # newFrame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # cv2.imshow("s", newFrame)
        # img = cv2.imdecode(imageNp,cv2.IMREAD_COLOR) 
        # # print("frame",img.shape)
        
        # print(predict(img))

        print(self.data)
        # postThread=threading.Thread(target=postData.postData,args=(self.data,),daemon=True)
        # postThread.start()
        # postThread.quit()

    
        # detectObj.run(im0=img)
        # cv2.imshow("Frame",cv2.flip(img, 1) )   #show captured frame
        # cv2.waitKey(1)    
        
        
  
         
        # image_result = open('deer_decode.jpg', 'wb') # create a writable image and write the decoding result
        # image_result.write(self.data)

        # logger.info('Received msg "%s" from %s' % (self.data, self.address[0]))
        # print("message received",self.data)
        # self.sendMessage(self.data)  # Echo message back to client

    def handleConnected(self):
        logger.info('New client connected %s' % self.address[0])
        print("New client connected")

    def handleClose(self):
        logger.info('Client disconnected %s' % self.data)
        # closing all open windows
        cv2.destroyAllWindows()   


class WSServerWrapper():
    ws_started_event = Event()
    # NOTE: to use WSS, assuming the certificate and private key are in the base directory, switch the ws_server from SimpleWebSocketServer to SimpleSSLWebSocketServer.
    # ws_server = SimpleSSLWebSocketServer('', DEFAULT_WS_PORT, WebSocketHandler, certfile=os.path.join(BASE_DIR, 'cert.pem'), keyfile=os.path.join(BASE_DIR, 'key.pem'), version=PROTOCOL_TLSv1_2)
    ws_server = SimpleWebSocketServer('', DEFAULT_WS_PORT, WebSocketHandler)

    @staticmethod
    def run():
        logger.info('Starting WebSocket server')
        WSServerWrapper.ws_started_event.set()
        WSServerWrapper.ws_server.serveforever()
