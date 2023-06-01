from django.shortcuts import render
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.views import APIView
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
# Create your views here.
from django.http import HttpResponse
import datetime
# import the logging library
import logging

from django.http import HttpResponse
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json

# import datetime
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

# ---------Credentials of influxdb-------------
bucket = "Users"
org = "1936be69c64da4d7"
token = "R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
measurement = "User"

# --------------Posting the data in influxdb-----------
@csrf_exempt
def postUserData(request):
    # ----------Using global variable---------
    global bucket
    global org
    global token
    global url
    global measurement
    # -----------Parameters send from frontend----------
    data = json.loads(request.body)
    myUsername = data.get('myUsername')
    myEmail = data.get('myEmail')
    myPassword = data.get('myPassword')
    isAuthenticatedByGoogle = data.get('isAuthenticatedByGoogle')

    # -------------Create an InfluxDB client------------
    client = InfluxDBClient(url=url, token=token, org=org)
    # ----------Query for checking whether user with same email exist--------
    query_api = client.query_api()
    query = f'from(bucket:"{bucket}")|> range(start: -1y)|> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}" )'
    # ----------append data in array-----------
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    # --------checking wether user with same email exist or not---------- 
    if(len(results) == 0 ):
        # ----------code for posting data----------
        # Define the data to be written
        data = Point(measurement).field("isAuthenticatedByGoogle", isAuthenticatedByGoogle).field("username", myUsername).tag("email",myEmail).field("password", myPassword).time(datetime.datetime.utcnow().isoformat() + 'Z')
        # Create a write API instance
        write_api = client.write_api(write_options=SYNCHRONOUS)
        # Write the data to the bucket
        write_api.write(bucket=bucket, record=data)
        # Close the write API
        write_api.close()
        print("--------------user registered successfully------------")
        response = json.dumps(data, default=str)
        return JsonResponse(response,safe=False)
    print("--------------Already Exist User------------")
    return JsonResponse({"response":"Already Exist User"},safe=False)
    

def getSpecificUser(request, *args, **kwargs):
    # --------using glpbal variables--------
    global bucket
    global org
    global token
    global url
    global measurement
    # -----------Parameters send from frontend----------
    myEmail = kwargs['email']
    myPassword = kwargs['password']
    isAuthenticatedByGoogle = kwargs['isAuthenticatedByGoogle']

    # ---------making connection to influxdb-----------
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    if(isAuthenticatedByGoogle == "false"):
        # -----------query for reading data--------
        query_api = client.query_api()    
        query = f'from(bucket:"{bucket}") \
        |> range(start: -1y) \
        |> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}"   and r._field == "password"  and r._value == "{myPassword}" )'

    elif(isAuthenticatedByGoogle == "true"):
        # -----------query for reading data--------
        query_api = client.query_api()    
        query = f'from(bucket:"{bucket}") \
        |> range(start: -1y) \
        |> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}" )'

    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    print(results)
    if(len(results) == 0 ):
        return JsonResponse({"response":"false"},safe=False)
    else:
        return JsonResponse({"response":"true"},safe=False)


# @csrf_exempt
# def addingUsertype(request , *args, **kwargs)  :
#     print("I am in--------")
#     usertype = kwargs['usertype']
    
#     client = InfluxDBClient(url="https://us-east-1-1.aws.cloud2.influxdata.com", token="R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ==", org="1936be69c64da4d7")

#     # Write API instance
#     write_api = client.write_api(write_options=SYNCHRONOUS)

#     # Prepare the data update
#     measurement = 'User'
#     # tags = {'email': 'umairahmedpaki7@gmail.com' }
#     # fields = {'usertype': usertype}
#     # timestamp = '2023-05-28T09:49:20.980Z'

#     # Construct the data point with the new field
#     point  =Point(measurement).tag("email", 'umairahmedpaki7@gmail.com').field('usertype', usertype).time('2023-05-28T10:19:49.889Z')

#     # Write the data point to InfluxDB
#     write_api.write(bucket='Users', record=point)

#     # Close the InfluxDB client
#     client.close()
   
#     return JsonResponse({},safe=False)
# example/views.py
# from datetime import datetime

def index(request):
    logger.warning('Homepage was accessed at '+str(datetime.now())+' hours!')
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
databucket = "Object Detection"
client = InfluxDBClient(url=url, token=token, org=org)

def count_influx(request):

    query = f'from(bucket:"{databucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "objectDetection")|> count()'

    result = client.query_api().query(query)
    try:
        response = result[0].records[0].values['_value']
    except:
        response = 0
    return HttpResponse(response)

def fetch_from_influx(request):

    query = f'from(bucket:"{databucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "objectDetection")|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")|> sort(columns: ["_time"], desc: true)|>limit(n: 10)'

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
