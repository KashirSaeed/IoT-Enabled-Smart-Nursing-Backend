from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
# creating .log file per day
from logging.handlers import TimedRotatingFileHandler
logname = "logs/logsContainer.log"
handler = TimedRotatingFileHandler(logname, when="midnight", backupCount=30)
handler.suffix = "%Y%m%d"
logger.addHandler(handler)

def hello_reader(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    return HttpResponse("<h1>Created Django Application </h1>")


from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json

def fetch_from_influx(request):

    # Set up the InfluxDB client
    url = "https://us-east-1-1.aws.cloud2.influxdata.com"
    org = "1936be69c64da4d7"
    token = "R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ=="
    bucket = "Object Detection"
    # Declaring an object with parameters initialised
    client = InfluxDBClient(url=url, token=token, org=org)
    query = f'from(bucket:"{bucket}")|> range(start: -1y)|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'

    # result = client.query_api().query_data_frame(query)
    result = client.query_api().query(query)
    json_result = []
    for table in result:
        for record in table.records:
            # Get timestamp from FluxRecord object
            record_time = record.get_time().strftime('%Y-%m-%dT%H:%M:%SZ')
            record_values = record.values
            # Add time field to record_values dictionary
            record_values['time'] = record_time
            json_result.append(record_values)

    # Return the JSON object as a web response
    response = json.dumps(json_result, default=str)
    
    # Return a success response
    return JsonResponse(response,safe=False)
