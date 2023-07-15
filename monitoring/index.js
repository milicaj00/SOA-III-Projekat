import dotenv from "dotenv";
import express from "express";
import cors from "cors";
import mqtt from "mqtt";

dotenv.config();

let client;
const mqtt_url = process.env.MQTT_URL;
const mqtt_port = process.env.MQTT_PORT;

(async () => {
  client = mqtt.connect(`mtqq://${mqtt_url}:${mqtt_port}`);
  console.log("success");
})().catch((error) => {
  console.log("caught", error.message);
});

const app = express();
app.use(express.json());
app.use(cors());

client.on("connect", function () {
  try {
    client.subscribe("FISH-POND-SENSOR-DATA");
    // client.publish("sensordata", "Hello mqtt");
    console.log("subscribed");
  } catch (err) {
    console.log("err subscribe", err);
  }
});

client.on("message", function (topic, message) {
  // message is Buffer
  console.log(message.toString());

  const value = JSON.parse(message).readings[0].value;
  const name = JSON.parse(message).readings[0].name;

  console.log(`${name} is ${value}`);

  if (name === "nitrate") {
    if (value < 24) {
      sendAlert("red");
    } else {
      sendAlert("green");
    }
  }
});

async function sendAlert(color) {
  
  const url =
    "http://172.20.192.1:48082/api/v1/device/bcd18c02-b187-4f29-8265-8312dc5d794d/command/d6d3007d-c4ce-472f-a117-820b5410e498";

  try {
    const res = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ color }),
    });
    console.log(res);
  } catch (error) {
    console.log("error", error);
  }
}

client.on("error", function (err) {
  console.log("error", err);
  client.end();
});

app.listen(8080, () => {
  console.log("Server is listening on port 8080.");
});
