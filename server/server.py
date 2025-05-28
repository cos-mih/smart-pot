from flask import Flask, request, Response, jsonify, render_template
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

data = {
    'temperature': 0,
    'humidity': 0,
    'light': 0
}

mqtt_server = 'localhost'
port = 1883
data_topic = 'data/#'


@app.route("/")
def index():
    global data
    return render_template('index.html', temperature=data['temperature'], humidity=data['humidity'], light=data['light'])

@app.route("/update")
def get_data():
    return jsonify(data)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f'Connected with result code {reason_code}')
    client.subscribe(data_topic)

def on_message(client, userdata, msg):
    global data
    device_id = msg.topic.split('/')[-1]
    json_data = json.loads(msg.payload)
    data['temperature'] = json_data.get('temperature', data['temperature'])
    data['humidity'] = json_data.get('humidity', data['humidity'])
    data['light'] = json_data.get('light', data['light'])

    print(f'{device_id}: {json_data}')


if __name__=='__main__':
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(mqtt_server, port, 60)

    mqttc.loop_start()

    app.run('127.0.0.1', port=5000, debug=True)

