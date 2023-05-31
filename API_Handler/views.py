# example/views.py
from datetime import datetime
from django.http import HttpResponse
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json

# import datetime
# import the logging library
# import logging
# Get an instance of a logger
# logger = logging.getLogger(__name__)
# creating .log file per day
# from logging.handlers import TimedRotatingFileHandler
# logname = "logs/logsContainer.log"
# handler = TimedRotatingFileHandler(logname, when="midnight", backupCount=30)
# handler.suffix = "%Y%m%d"
# logger.addHandler(handler)



def index(request):
    # logger.warning('Homepage was accessed at '+str(datetime.now())+' hours!')
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)


# Declaring an object with parameters initialised
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
org = "1936be69c64da4d7"
token = "R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ=="
bucket = "Object Detection"
client = InfluxDBClient(url=url, token=token, org=org)

def count_influx(request):

    query = f'from(bucket:"{bucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "objectDetection")|> count()'
    result = client.query_api().query(query)
    try:
        response = result[0].records[0].values['_value']
    except:
        response = 0
    return HttpResponse(response)

def fetch_from_influx(request):

    query = f'from(bucket:"{bucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "objectDetection")|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")|> sort(columns: ["_time"], desc: true)|>limit(n: 10)'

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
