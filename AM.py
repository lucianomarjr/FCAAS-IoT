"""
    Authorization Manager
    Este módulo:
    - recebe as requisições de contexto dos consumers;
    - extrai e formata os atributos;
    - envia mensagem de requisição ao PDA;
    - recebe resposta da solicitação e retorna para o consumer a mensagem criptografada ou a negação de acesso.
    envia mensagem ao

"""

from socket import *
import pickle
import json
from datetime import datetime


def get_subject(request):
    """
        Obtém os atributos referentes ao "subject" da requisição.
        Input: requisição
        Output: atributos de "subject" em json.
    """
    request = json.loads(request)

    sub_attr = {
        "id": request.get("subject").get("attributes").get("name"),
        "attributes": request.get("subject").get("attributes")
    }

    return sub_attr


def get_resource(request):
    """
            Obtém os atributos referentes ao "resource" da requisição.
            Input: requisição
            Output: atributos de "resource" em formato json.
        """

    request = json.loads(request)

    res_attr = {
        "id": request.get("resource").get("attributes").get("source"),
        "attributes": request.get("resource").get("attributes")
    }

    return res_attr


def get_request_context(request, address, port):
    """
        Obtém o contexto da solicitação.
        Input: requisição, socket de conexão do lado do emissor, endereço de porta.
        Output: contexto da requisição em formato json.
    """

    date_time = datetime.now()

    req_context = {
        "ip": address[0],
        "port": address[1],
        "time": date_time.strftime('%H:%M'),
        "date": date_time.strftime('%d/%m/%Y'),
        "connection": str(port),
        "device": 'qualquer um',
        "protocol": '1883'
    }

    return req_context


def access_composer(subject, resource, context):
    """
        Forma um objeto json a ser enviado para o PDA que será base para o Access Request.
        Input: objetos json com atributos.
        Output: objeto json no formato Access Request.
    """

    access_request = {
        "subject": subject,
        "resource": resource,
        "context": context,
        "action": {
            "id": 'get',
            "attributes": {'method': 'get'}
        }
    }

    return access_request


def main():
    host = 'localhost'
    port = 50003
    log = []

    while True:
        sock = socket(SOCK_DGRAM, AF_INET)
        sock.bind((host, port))
        print('AM is running! Waiting for requests...')
        data, address = sock.recvfrom(1024)
        print('Connection received from: IP {}, PORT {}.'.format(address[0],address[1]))

        request = data.decode()

        subject = get_subject(request)
        context = get_request_context(request)
        resource = get_resource(request)

        access_request = access_composer(subject, resource, context)


if __name__ == '__main__':
    main()

