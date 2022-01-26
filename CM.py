from socket import *
import pickle
from paho.mqtt import client as mqtt_client
import paho.mqtt.subscribe as subscribe
import json
from datetime import datetime


def get_context(request):
    """
    Obtém as informações de contexto a partir do Context Broker.
    input: requisição recebida do AM com especificação do contexto solicitado.
    output: informações de contexto em formato json.
    """

    source = request.get('source')
    context_data = {}
    data = request.get('context')

    for n in data:
        topic = '{}/{}'.format(source, n)
        broker = '192.168.1.150'
        port = 1883
        client_id = 'cm_client'
        userdata = 'qualquer dado'

        try:
            print('Getting context...')
            msg = subscribe.simple(topic, qos=0, hostname=broker, retained=True)
            c_msg = msg.payload.decode()
            context_data[n] = c_msg
            continue

        except ConnectionRefusedError:
            return -1

    return context_data


def context_compose(context, data):
    """
    Monta a mensagem de contexto a ser enviada para o EA.
    input: contexto obtido do CB e requisição de contexto recebida do AM.
    output: mensagem de contexto em formato json.
    """

    context_response = {
        'source': data.get('source'),
        'destination': data.get('destination'),
        'crypto': data.get('crypto'),
        'context': context
    }

    return context_response


def send_context(context):
    """
    Envia mensagem com contexto para o EA.
    input: mensagem de contexto
    output:nada
    """

    host = 'localhost'
    port = 50005
    destination = (host, port)

    context = pickle.dumps(context)
    sock = socket(AF_INET, SOCK_STREAM)

    try:
        sock.connect(destination)
        sock.send(context)

    except ConnectionRefusedError:
        return -1

    print("Context sent to EA!")
    return 1


def main():
    log = []
    host = 'localhost'
    port = 50006

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()

    while True:
        print('Waiting for requests...')
        connection, address = sock.accept()
        data = connection.recv(1024)
        data = pickle.loads(data)

        context = get_context(data)

        context_response = context_compose(context, data)

        send_context(context_response)


if __name__ == '__main__':
    main()
