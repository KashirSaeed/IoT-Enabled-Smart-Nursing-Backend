from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import datetime
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def hello_reader(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    return HttpResponse("<h1>Created Django Application </h1>")


from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
import json

def fetch_from_influx(request):
    # pass request as arg

    # Extract data from request
    # measurement = request.GET.get('measurement')
    # tag_key = request.GET.get('tag_key')
    # tag_value = request.GET.get('tag_value')
    # field_key = request.GET.get('field_key')
    # field_value = request.GET.get('field_value')
    # timestamp = request.GET.get('timestamp')
    # start_time = request.GET.get('start_time')
    # end_time = request.GET.get('end_time')

    # Set up the InfluxDB client
    url = "https://us-east-1-1.aws.cloud2.influxdata.com"
    org = "1936be69c64da4d7"
    token = "R4yVXBDI84LlpaZijvjNMrhl-8m-67S_gUNhON9CXISLLSEwKP4Oaeykw8UaF-wq5rQs4_kismihsVNBCC3vVQ=="
    bucket = "Object Detection"

    # Declaring an object with parameters initialised
    client = InfluxDBClient(url=url, token=token, org=org)

    # for writing to influxDB
    # write_api = client.write_api(write_options=SYNCHRONOUS)

    # Define the query to write data to DB
    # data = Point(measurement)\
    #     .tag(tag_key, tag_value)\
    #     .field(field_key, field_value)\
    #     .time(timestamp)

    # Write the data to InfluxDB Cloud
    # write_api.write(bucket=bucket, record=data)

    # defining the query to read data
    # query = f'from(bucket:"{bucket}")|> range(start: -1y)|> filter(fn:(r) => r._measurement == "object_detection")|> filter(fn:(r) => r.location == "hospital")|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
    query = f'from(bucket:"{bucket}")|> range(start: -1y)|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'

    # Alternate way to define query
    # query = f'from(bucket: "{bucket}")\
    # |> range(start: {start_time}, stop: {end_time})\
    # |> filter(fn: (r) => r["_measurement"] == "{measurement}")\
    # |> filter(fn: (r) => r["_field"] == "{field_key}")\
    # |> filter(fn: (r) => r["{tag_key}"] == "{tag_value}")\
    # |> filter(fn: (r) => r["_value"] == {field_value}) \
    # |> limit(n: 100)'
    
    #executing the query through query_api instance
    # query_api = client.query_api()
    # tables = query_api.query(query)
    # for table in tables:
    #     for record in table.records:
    #         print(str(record["_time"]) + " - " + record.get_measurement() + " " + record.get_field() + "=" + str(record.get_value()))

    # result = client.query_api().query_data_frame(query)
    result = client.query_api().query(query)
    # json_data = ''.join([df.to_json(orient='records') for df in result])
    # json_data = '[' + ','.join(json_data.split()) + ']'
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
