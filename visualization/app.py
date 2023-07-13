import paho.mqtt.client as mqtt
import time
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime


broker_address  = "192.168.1.6"
topic           = "FISH-POND-SENSOR-DATA"
dbhost          = "192.168.1.6"
dbport          = 8086
dbuser          = "root"
dbpassword      = "password"
# dbname          = "sensordata"
#rAkkPznprMMsaFYknsbogdBxiaHpoP5vxq5VHwpKerhILR522lh_nhi1J0cb8iNc68Kzy1Rf6AviOF_77hFwDw==
token ='rAkkPznprMMsaFYknsbogdBxiaHpoP5vxq5VHwpKerhILR522lh_nhi1J0cb8iNc68Kzy1Rf6AviOF_77hFwDw=='
org = 'Jojobi'
bucket = 'FishPond'
dburl = "192.168.1.6:8086"

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
