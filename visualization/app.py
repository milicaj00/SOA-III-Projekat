import paho.mqtt.client as mqtt
import time
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

broker_address = os.getenv('broker_address')
topic = os.getenv('topic')
dburl = os.getenv('dburl')
dbhost = os.getenv('dbhost')
dbuser = os.getenv('dbuser')
dbpassword = os.getenv('dbpassword')
token = os.getenv('token')
org = os.getenv('org')
bucket = os.getenv('bucket')


def influxDBconnect():
    influxDBConnection = InfluxDBClient(url = dburl, token=token, org=org)
    return influxDBConnection

def influxDBwrite(device, sensorName, sensorValue):

    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
   
    write_api = influxDBConnection.write_api(write_options=SYNCHRONOUS)
    p = Point('measurements').tag("gateway", device).time(timestamp).field(sensorName, sensorValue)
    write_api.write(bucket=bucket, org=org, record=p)
    



def on_message(client, userdata, message):
    payload = message.payload.decode()
    message = json.loads(payload)
    print(message)

    for entry in message["readings"]:
       
        device      = entry["device"]
        sensorName  = entry["name"]
        sensorValue = entry["value"]

        
        influxDBwrite(device, sensorName, sensorValue)




influxDBConnection = influxDBconnect()

print("Creating new instance ...")
client = mqtt.Client("sub1") #create new instance
client.on_message=on_message #attach function to callback
# client.username_pw_set("mqttUser", "mqttPass")

print("Connecting to broker ...")
client.connect(broker_address, 1883) #connect to broker
print("...done")

client.loop_start()

while True:
    client.subscribe(topic)
    time.sleep(1)

client.loop_stop()
