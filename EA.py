from socket import *
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def rsa_encryption(key, context):
    """
    Realiza a encriptação do contexto utilizando algoritmo RSA.
    input: chave pública e informações de contexto.
    output: contexto criptografado.
    """
    context = pickle.dumps(context)
    pu_key = RSA.importKey(key)
    cipher_rsa = PKCS1_OAEP.new(pu_key)
    c_context = cipher_rsa.encrypt(context)

    return c_context


def encryption_context(alg, key, context):

    print("Encryption Algorithm: {}".format(alg))

    if alg == 'rsa':
        c_context = rsa_encryption(key, context)
        return c_context

    elif alg == 'aes':
        print("Implementar AES!")

    elif alg == 'abe':
        print("Implementar AES!")

    else:
        msg = 'Nenhum algoritmo foi encontrado!'
        return msg


def send_context(context):
    host = 'localhost'
    port = 50004
    destination = (host, port)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(destination)
    print('Conectado ao AM!')
    context = pickle.dumps(context)
    sock.send(context)
    print('Context sent!')
    sock.close()

    return 1


def main():
    log = []
    host = 'localhost'
    port = 50005
    destination = (host, port)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(destination)
    sock.listen()

    while True:
        print('Waiting for requests...')
        connection, address = sock.accept()
        data = connection.recv(1024)
        data = pickle.loads(data)
        print(data)
        print(type(data))

        crypto_infor = data.get('crypto')
        crypto_alg = data.get('crypto').get('alg')
        crypto_key = data.get('crypto').get('key')

        context_infor = data.get('context')

        c_context = encryption_context(crypto_alg, crypto_key, context_infor)

        send_context(c_context)

if __name__ == '__main__':
    main()