SMART POT

Server implemented in Pyhton using Flask, in server.py:
    -> MQTT client subscribed to data/ topic, where all devices send sensor data; it 
       updates the global data dictionary with new data from each received message;
    -> data is displayed on the root page, defined in index.html; data is periodically
       requested from the exposed API, at the /update route, to account for new incoming
       data from the Smart Pots;
    -> index.html includes a JavaScript script that defines 3 graphics and corresponding
       plugins using Chart.js, and the fetchDataAndUpdate() function which sends requests
       to the API and then updates the charts' elements with the new data.


ESP32 code in main.py:
    -> using the MQTT client implementation in simple.py;
    -> using dht library for temperature sensor, and simple ADC readings for the humidity
       sensor and photoresistor;
    -> initiate WiFi connection, then read data from sensors in a loop and publish messages
       to the data/<device_id> topic for the server to receive.

       

