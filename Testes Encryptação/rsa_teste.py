from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import pickle
import json
import base64
from pymongo import MongoClient


def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.public_key().export_key()

    with open('public_key.bin', 'wb') as file:
        file.write(public_key)

    with open('private_key.bin', 'wb') as file:
        file.write(private_key)


def encryption(data):
    key_file = open('public_key.bin').read()
    print(type(key_file))
    key = RSA.import_key(key_file)
    cipher_rsa = PKCS1_OAEP.new(key)

    data = data.encode()

    c_data = cipher_rsa.encrypt(data)

    return c_data


def save_key():

    usr = 'bdadmin'
    psw = '111293'
    client = MongoClient('192.168.1.150', 27017)
    db = client.crypto_test
    #db.authenticate(usr, psw, source='admin')

    keys = db['keys']

    key_file = open('private_key.bin', 'rb').read()

    register = {
        "_id": 1010,
        "key": key_file
    }

    #keys = db.keys

    result = keys.insert_one(register)

    return 1


def get_key(id=1010):
    usr = 'bdadmin'
    psw = '111293'
    client = MongoClient('192.168.1.150', 27017)
    db = client.crypto_test

    keys = db['keys']

    key = keys.find_one({'_id':id})
    key = key.get('key')

    # print(key)

    # print(type(key))

    return key


def decryption(data):
    #key_file = open('private_key.bin', 'rb').read()
    key_file = get_key()
    key = RSA.import_key(key_file)
    cipher_rsa = PKCS1_OAEP.new(key)

    text = cipher_rsa.decrypt(data)

    return text.decode()


def main():

    # generate_keys()

    #save_key()

    msg = 'Mensagem secreta'

    c_msg = encryption(msg)

    print(c_msg)

    text = decryption(c_msg)

    print(text)

    #key = get_key()



if __name__ == '__main__':
    main()