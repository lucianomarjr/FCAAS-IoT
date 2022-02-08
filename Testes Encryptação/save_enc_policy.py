from PMA import EncryptionPolicy
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def get_key_rsa(file):
    key_file = open(file).read()

    return key_file.encode()


def main():
    file = 'public_key.bin'

    key = get_key_rsa(file)

    print(type(key))

    tags = ['1883']
    ip = ['192.168.1.100', '127.0.0.1']
    port = ['1883']
    time = ['14:00']
    device = ['dev_1', 'dev_2']

    enc_policy = {
        "_id": 1,
        "tags": tags,
        "priority": 3,
        "context": {
            'ip': ip,
            'port': port,
            'time': time,
            'device': device,
        },
        "c_infors": {
            "alg": 'rsa',
            "key": key,
        }
    }

    policy = EncryptionPolicy()

    policy.save(enc_policy)


if __name__ == '__main__':
    main()