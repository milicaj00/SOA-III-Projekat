import dotenv from "dotenv";
import express from "express";
import cors from "cors";
import mqtt from "mqtt";

dotenv.config();

let client;

(async () => {
  client = mqtt.connect("mtqq://192.168.1.6:1883");
  // mqtt.connect(this.host, { username: this.username, password: this.password });
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
//   client.end();
});

client.on("error", function (err) {
  console.log("error", err);
});

app.listen(8080, () => {
  console.log("Server is listening on port 8080.");
});
