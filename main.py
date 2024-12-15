import network
import requests
import time
from machine import Pin, ADC
from simple import MQTTClient
import dht
import json

ssid = '-'
password = '-'

mqtt_server = '192.168.43.211'
client_id = 'esp32-1'

data_topic = 'data/' + client_id

temp_sensor = dht.DHT11(Pin(22))
soil_humidity_sensor = ADC(Pin(35))
light_sensor = ADC(Pin(34))

data = {
    'temperature': 0,
    'humidity': 0,
    'light': 0
}

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Connected to Wi-Fi:', wlan.ifconfig())


if __name__=='__main__':
    connect_to_wifi()

    client = MQTTClient(client_id, mqtt_server)
    client.connect()    

    print(f'Connected to MQTT server at: {mqtt_server}')

    while True:
        try:
            temp_sensor.measure()
            data['temperature'] = temp_sensor.temperature()
        except OSError as e:
            print('Failed to read temperature sensor.')
        data['humidity'] = soil_humidity_sensor.read_u16()
        data['light'] = light_sensor.read_u16()
       
        client.publish(data_topic, json.dumps(data))
        print(f'Temperature: {data['temperature']}\nHumidity: {data['humidity']}\nLight: {data['light']}\n')

        time.sleep(2)


