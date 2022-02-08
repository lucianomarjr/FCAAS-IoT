from socket import *
import time
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pymongo import MongoClient
import base64


# def get_key(context_request):
#     usr = 'bdadmin'
#     psw = '111293'
#     client = MongoClient('192.168.1.150', 27017)
#     db = client.encryption_keys
#     db.authenticate(usr, psw, source='admin')
#     keys = db['consumer_1']
#
#     key = []
#
#     for p in keys.find({"context": context_request}):
#         key.append(p)
#         print(key)
#
#     dec_key = key[0]


def get_attributes():
    filename = 'Attributes/request_001.json'
    with open(filename) as file:
        content = file.read()

    return content


def context_request(attributes):
    host = 'localhost'
    port = 50003
    server = (host, port)

    sock = socket(AF_INET, SOCK_DGRAM)

    try:
        sock.connect(server)
        print("Connection status: OK!")
        msg = pickle.dumps(attributes)
        sock.send(msg)

        print("Context request sent!")

        response = sock.recv(1024)

        return response

    except ConnectionRefusedError:
        return -1


def decryption(context):
    file = 'Testes Encryptação/private_key.bin'
    key_file = open(file).read()
    key = RSA.import_key(key_file)
    cipher_rsa = PKCS1_OAEP.new(key)

    data = cipher_rsa.decrypt(context)

    return pickle.loads(data)


def main():
    log = []
    count = 0

    while count <= 2:
        attributes = get_attributes()
        context = context_request(attributes)
        print('A mensagem recebida: {}'.format(context))
        msg = decryption(context)
        print('A mensagem descriptografada: {}'.format(msg))

        print('Context: ')
        for item, value in msg.items():
            print('{} : {}'.format(item, value))

        time.sleep(10)
        count += 1


if __name__ == '__main__':
    main()