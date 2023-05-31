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
    for obj in objects['activity']:
        random_number = random.randint(60, 100)
        data = Point("objectDetection").tag("location", "hospital").field("object name",obj).field("Blood pressure", random_number).time(datetime.datetime.utcnow().isoformat() + 'Z').time(datetime.datetime.utcnow().isoformat() + 'Z')
        write_api.write(bucket="Object Detection", record=data)

    return
