from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime
import time
import asyncio
oldActivities=""
client = InfluxDBClient(url="https://us-east-1-1.aws.cloud2.influxdata.com", token="R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ==", org="1936be69c64da4d7")
write_api = client.write_api(write_options=SYNCHRONOUS)
import random

# Generate a random integer between 1 and 10 (inclusive)


def postData(objects):
    global write_api
    # csv_array = objects['objects'].split(",")
    csv_array = objects['objects']
    print("Sending objects to Influx")
    for obj in csv_array:
        random_number = random.randint(40, 100)
        # heart_rate = random.randint(50,120)
        data = Point("objectDetection").tag("location", "hospital").field("object name",obj).field("Blood pressure", random_number).time(datetime.datetime.utcnow().isoformat() + 'Z').time(datetime.datetime.utcnow().isoformat() + 'Z')
        write_api.write(bucket="Object Detection", record=data)

    return
def sendActs(acts):
    global write_api
    data = acts['activity']
    print("Sending activities to Influx")
    for item in data:
        activity = item['activity']
        startTime = item['startTime']
        endTime = item['endTime']
        data = Point("activityDetection").tag("location", "hospital").field("Activity",activity).field("StartTime", startTime).field("EndTime",endTime).time(datetime.datetime.utcnow().isoformat() + 'Z').time(datetime.datetime.utcnow().isoformat() + 'Z')
        write_api.write(bucket="Object Detection", record=data)