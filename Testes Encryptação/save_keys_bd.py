from pymongo import MongoClient
import pickle


def save_key(key, alg, context):
    usr = 'bdadmin'
    psw = '111293'
    client = MongoClient('192.168.1.150', 27017)
    db = client.encryption_keys

    register = {
        'key': key.encode(),
        'context': context,
        'alg': alg
    }

    key_reg = db.private_keys.insert_one(register)

    #key_reg = db.private_keys.find_one({'context': "1"})

    return key_reg


def get_key(file):
    key = open(file).read()

    return key


# def get_key(context_request):
#     usr = 'bdadmin'
#     psw = '111293'
#     client = MongoClient('192.168.1.150', 27017)
#     db = client.encryption_keys
#     db.authenticate(usr, psw, source='admin')
#     keys = db['consumer_1']

def main():
    file = 'private_key.bin'
    key = get_key(file)

    context = "1"
    alg = 'rsa'
    key_storage = save_key(key, alg, context)

    print(key)


if __name__ == '__main__':
    main()