import random
import time
import json
import pickle

from paho.mqtt import client as mqtt_client


def temp_generator():
    temperature = random.uniform(35, 40)
    temperature = "{:.2f}".format(temperature)
    return temperature


def location_generator():
    location = {'longitude': '31.01670',
                'latitude': '-298500'}

    return location


def connect_mqtt(client_id, broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client


def publish(client, data, topic):
    msg_count = 0
    c = True
    while c:
        time.sleep(5)
        publication = client.publish(topic, data, retain=True)
        status = publication[0]

        if status == 0:
            print(f"Send `{data}` to topic `{topic}`")
            c = False

        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def main():
    broker = '192.168.1.150'
    port = 1883
    client_id = ''
    username = 'luciano'
    password = '12345'

    client = connect_mqtt(client_id, broker, port)
    client.loop_start()

    temperature = temp_generator()
    location = location_generator()
    location = pickle.dumps(location)

    topic_temp = 'sensor_1/temperature'
    topic_loc = 'sensor_1/location'

    publish(client, temperature, topic_temp)
    publish(client, location,  topic_loc)


if __name__ == '__main__':
    main()
