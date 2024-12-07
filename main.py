import network
import requests
import time
from machine import Pin, ADC
from simple import MQTTClient
import dht

ssid = ''
password = ''

mqtt_server = ''
client_id = 'esp32-1'

temp_topic = 'data/temperature'
soil_topic = 'data/humidity'
light_topic = 'data/light'

temp_sensor = dht.DHT11(Pin(22))
soil_humidity_sensor = ADC(Pin(35))

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
            temp = temp_sensor.temperature()
            client.publish(temp_topic, f'{temp}')
            print(f'Temperature: {temp}\n')
        except OSError as e:
            print('Failed to read temperature sensor.')


        humidity = soil_humidity_sensor.read_u16()
        client.publish(soil_topic, f'{humidity}')
        print(f'Soil humidity: {humidity}')

        time.sleep(2)

    client.disconnect()
