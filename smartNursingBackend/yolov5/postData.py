from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

def activityDetector(allActivities , oldActivities):
    print("----------------")
    currentObjectsCounter = getTotalObjectsNumber(allActivities)
    oldObjectsCounter = getTotalObjectsNumber(oldActivities)
    currentObjects = []
    oldObjects = []

    for i in range(currentObjectsCounter):
        currentObjects.append(getField(allActivities,i))    

    for i in range(oldObjectsCounter):
        oldObjects.append(getField(oldActivities,i))

    print("Current Objects:"+"    "+str(currentObjects))
    print("Old Objects:"+"    "+str(oldObjects))

    for i in range(currentObjectsCounter):
        if currentObjects[i] not in oldObjects:
            print("Oject to be inserted:"+"    "+str(currentObjects[i])) 
            postData(currentObjects[i])
    print("----------------")

def getTotalObjectsNumber(record):
    counter = 0
    for i in range(len(record)):
        if(record[i] == ","):
            counter = counter + 1
    return counter


def getField(record,position):
    idx=7
    firstspace=0
    naam=""
    while( firstspace < position+1 and idx < len(record)):
        if(record[idx] == ','):
            firstspace=firstspace+1
        elif(firstspace == position):
            naam=naam+record[idx]
        idx=idx+1
    return naam

def postData(objectName):
    # Create an InfluxDB client
    client = InfluxDBClient(url="https://us-east-1-1.aws.cloud2.influxdata.com", token="R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ==", org="1936be69c64da4d7")

    # Define the data to be written
    data = Point("objectDetection").tag("location", "hospital").field("object name",objectName).field("Blood pressure", 100.5).time(datetime.datetime.utcnow().isoformat() + 'Z').time(datetime.datetime.utcnow().isoformat() + 'Z')

    # Create a write API instance
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Write the data to the bucket
    write_api.write(bucket="Object Detection", record=data)

    # Close the write API
    write_api.close()
