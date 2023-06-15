from django.shortcuts import render
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import influxdb_client
from django.http import HttpResponse
import datetime
import logging
from smartNursingBackend.settings import logger
# -------Array containing names of .log files----------
newLogFileNamesArray = []

# ------------Get an instance of a logger------------
# logger = logging.getLogger(__name__)
# -----------creating .log file per day--------
from logging.handlers import TimedRotatingFileHandler
logname = "logs/logsContainer.log"
handler = TimedRotatingFileHandler(logname, when="midnight", backupCount=30)
handler.suffix = "%Y%m%d"
logger.addHandler(handler)


# ---------Credentials of influxdb-------------
databucket = "Object Detection"
org = "1936be69c64da4d7"
token = "R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
measurement = "User"
client = InfluxDBClient(url=url, token=token, org=org)

    
def index(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    now = datetime.datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

def count_influx(request):
    logger.warning('Count sent  '+str(datetime.datetime.now())+' hours!')
    query = f'from(bucket:"{databucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "objectDetection")|> count()'
    result = client.query_api().query(query)
    try:
        response = result[0].records[0].values['_value']
    except:
        response = 0
    return HttpResponse(response)


def fetch_from_influx(request):
    logger.warning('Accessing objects '+str(datetime.datetime.now())+' hours!')
    try:
        query = f'from(bucket:"{"databucket"}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "objectDetection")|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")|> sort(columns: ["_time"], desc: true)|>limit(n: 10)'
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
        
        return JsonResponse(json_result,safe=False)
    except:
        logger.warning("Error in fetching data from influx" + str(datetime.datetime.now())+' hours!')





