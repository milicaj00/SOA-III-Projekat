import csv
import requests
import json
import time


edgexip = 'localhost'
humval = 40
tempval = 23

data = []

with open("./FishPond.csv") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
          data.append(row)



if __name__ == "__main__":

    sensorTypes = [
            "pH",
            "ammonia",
            "nitrate",
            ]

    with open("./FishPond.csv") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
  
            url = 'http://%s:49986/api/v1/resource/Fish_pond_sensor_cluster_03/pH' % edgexip
            payload = float(row['pH'])
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

            url = 'http://%s:49986/api/v1/resource/Fish_pond_sensor_cluster_03/ammonia' % edgexip
            payload = float(row['AMMONIA'])
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

            url = 'http://%s:49986/api/v1/resource/Fish_pond_sensor_cluster_03/nitrate' % edgexip
            payload = int(row['NITRATE'])
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

            url = 'http://%s:49986/api/v1/resource/Fish_pond_sensor_cluster_03/temperature' % edgexip
            payload = int(float(row['TEMPERATURE']))
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
            print(response)

            print('Sent data: ', row['pH'], row['AMMONIA'], row['NITRATE'])
            time.sleep(5)
