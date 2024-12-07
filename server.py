from flask import Flask, request, Response, jsonify, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)

data = {
    'temperature': 0,
    'humidity': 0,
    'light': 0
}

mqtt_server = '192.168.43.211'
port = 1883
data_topic = 'data/#'


@app.route("/")
def index():
    global data
    return render_template('index.html', temperature=data['temperature'], humidity=data['humidity'], light=data['light'])


def on_connect(client, userdata, flags, reason_code, properties):
    print(f'Connected with result code {reason_code}')
    client.subscribe(data_topic)

def on_message(client, userdata, msg):
    global data
    topic = msg.topic.split('/')[-1]
    data[topic] = int(str(msg.payload)[2:-1])
    print(f'{topic}: {str(msg.payload)}, {data[topic]}')
    socketio.emit("update", {topic: data[topic]})


if __name__=='__main__':
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(mqtt_server, port, 60)

    mqttc.loop_start()

    socketio.run('127.0.0.1', port=5000, debug=True)

