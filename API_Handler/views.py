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
# ------------Get an instance of a logger------------
logger = logging.getLogger(__name__)
# -----------creating .log file per day--------
from logging.handlers import TimedRotatingFileHandler
logname = "logs/logsContainer.log"
handler = TimedRotatingFileHandler(logname, when="midnight", backupCount=30)
handler.suffix = "%Y%m%d"
logger.addHandler(handler)

# ---------Credentials of influxdb-------------
databucket = "Users"
# databucket = "Object Detection"
org = "1936be69c64da4d7"
token = "R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
measurement = "User"
client = InfluxDBClient(url=url, token=token, org=org)

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
    query = f'from(bucket:"{databucket}")|> range(start: -1y)|> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}" )'
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
        data = Point(measurement).tag("isAuthenticatedByGoogle", isAuthenticatedByGoogle).field("username", myUsername).tag("email",myEmail).tag("password", myPassword).time(datetime.datetime.utcnow().isoformat() + 'Z')
        # Create a write API instance
        write_api = client.write_api(write_options=SYNCHRONOUS)
        # Write the data to the bucket
        write_api.write(bucket=databucket, record=data)
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
        query = f'from(bucket:"{databucket}") \
        |> range(start: -1y) \
        |> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}"   and r.password == "{myPassword}"  and r.isAuthenticatedByGoogle == "{isAuthenticatedByGoogle}"  )' 
  

    elif(isAuthenticatedByGoogle == "true"):
        # -----------query for reading data--------
        query_api = client.query_api()    
        query = f'from(bucket:"{databucket}") \
        |> range(start: -1y) \
        |> filter(fn:(r) => r._measurement == "{measurement}" and r.email == "{myEmail}" and r.isAuthenticatedByGoogle == "{isAuthenticatedByGoogle}"  )'
        

        
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




# --------------

import threading

# Define a function to be executed in the separate thread
def my_function():
    # Your code goes here...
    import schedule
    import time
    def job():
        print("I'm working...")
    schedule.every().day.at("14:50").do(job)
    
    def job_with_argument(name):
        print(f"I am {name}")

    schedule.every(10).seconds.do(job_with_argument, name="Peter")

    while True:
        schedule.run_pending()
        time.sleep(1)
    print("Running in the separate thread.")

# Create a thread object with your function
my_thread = threading.Thread(target=my_function)

# Start the thread
my_thread.start()