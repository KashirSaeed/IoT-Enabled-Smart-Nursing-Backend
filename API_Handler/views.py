from django.shortcuts import render
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import influxdb_client
# Create your views here.
from django.http import HttpResponse
import datetime
import logging
import threading
import schedule
import time
import os

newLogFileNamesArray = []
from influxdb_client import InfluxDBClient, Point



# ------------Get an instance of a logger------------
logger = logging.getLogger(__name__)
# -----------creating .log file per day--------
from logging.handlers import TimedRotatingFileHandler
logname = "logs/logsContainer.log"
handler = TimedRotatingFileHandler(logname, when="midnight", backupCount=30)
handler.suffix = "%Y%m%d"
logger.addHandler(handler)


# ---------Credentials of influxdb-------------
databucket = "Object Detection"
bucket = "Object Detection"
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

    if(len(results) == 0 ):
        return JsonResponse({"response":"false"},safe=False)
    else:
        access_token=create_access_token(myEmail)
        
        return JsonResponse({"response":"true","token":access_token},safe=False)


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



def firstThread():
    def job():
        global newLogFileNamesArray
        newLogFileNamesArray = readDataFromFile('logFileNames.txt')
        if(len(newLogFileNamesArray) != 0):
            for i in range(len(newLogFileNamesArray)):
                print("logs\{}".format(newLogFileNamesArray[i]))
                infile = r"logs\{}".format(newLogFileNamesArray[i])
                with open(infile) as f:
                    f = f.readlines()
                logsArray=[]
                for index, item in enumerate(f):
                    logsArray.append(item)
                    print(item)
                    postData(item)
                print(logsArray)
            deleteDataFromFile('logFileNames.txt')
        
    schedule.every().day.at("00:02").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    print("Running in the separate thread.")

def secondThread():
    global newLogFileNamesArray
    # Define the directory to monitor
    directory = 'logs'
    # Get the initial list of files in the directory
    initial_files = os.listdir(directory)
    while True:
        # Wait for a certain time interval
        time.sleep(5)  # Adjust the interval as per your requirement
        # Get the updated list of files in the directory
        updated_files = os.listdir(directory)
        # Find the difference between the initial and updated file lists
        new_files = list(set(updated_files) - set(initial_files))
        # Check if any new files are generated
        if new_files:
            for file in new_files:
                print(f"New file generated: {file}")
                # newLogFileNamesArray.append(file)
                writeDataToFile('logFileNames.txt',file)
        # Update the initial file list for the next iteration
        initial_files = updated_files
    print("Running in the separate thread.")

# Create a thread object with your function
myThread1 = threading.Thread(target=firstThread)
myThread2 = threading.Thread(target=secondThread)

# Start the thread
myThread1.start()
myThread2.start()

def postData(logsData):
    global client
    # Define the data to be written
    data = Point("logs").field("logs",logsData).time(datetime.datetime.utcnow().isoformat() + 'Z')
    # Create a write API instance
    write_api = client.write_api(write_options=SYNCHRONOUS)
    # Write the data to the bucket
    write_api.write(bucket="Logs", record=data)
    # Close the write API
    write_api.close()

def hello_reader(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    return HttpResponse("<h1>Created Django Application </h1>")

def writeDataToFile(fileName,data):
    with open(fileName, 'a') as f:
        f.write(data)
        f.write('\n')

def readDataFromFile(fileName):
    file = open(fileName, 'r')
    array=[]
    while True:
        line = file.readline()
        if not line:
            break
        array.append(line[:-1])
    return array
    file.close()

def deleteDataFromFile(fileName):
    open(fileName , 'w').close()
    



def fetch_images_ids(request):
    query = f'from(bucket:"{databucket}")|> range(start: -30d)|> filter(fn: (r) => r._measurement == "ImagesOnDrive")|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")|> sort(columns: ["_time"], desc: true)|>limit(n: 10)'
    result = client.query_api().query(query)
    json_result=[]
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
