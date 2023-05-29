from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

oldActivities=""
client = InfluxDBClient(url="https://us-east-1-1.aws.cloud2.influxdata.com", token="R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ==", org="1936be69c64da4d7")
write_api = client.write_api(write_options=SYNCHRONOUS)


def  postData(objects):
    global write_api
    print("DATA REACHED" , objects)
    # data = Point("objectDetection").tag("location", "hospital").field("object name",objects).field("Blood pressure", 100.5).time(datetime.datetime.utcnow().isoformat() + 'Z').time(datetime.datetime.utcnow().isoformat() + 'Z')
    # write_api.write(bucket="Object Detection", record=data)
