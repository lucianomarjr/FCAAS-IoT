from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.memory import MemoryStorage
from PMA import AccessControl
from PMA import EncryptionPolicy as Crypto
from socket import *
import pickle


def access_compose(data, infor):
    request = {
        'subject': data.get('subject'),
        'context': data.get('context'),
        'action': data.get('action'),
        'resource': {
            'id': data.get('resource').get('id'),
            'attributes': {
                'source': data.get('resource').get('attributes').get('source'),
                'name': infor
            }
        }
    }

    return request


def accessEvaluation(request):
    print("Access Control evaluation...")
    storage = MemoryStorage()

    sib = AccessControl()
    tar_sub = request.get("subject").get("id")
    tar_res = request.get("resource").get("id")
    #tar_action = request.get("action").get("id")
    tar_action = 'get'

    print(tar_sub, tar_res, tar_action)

    policies = sib.getForTarget(tar_sub, tar_res, tar_action, True)
    #policies = sib.getForTarResource(tar_res)

    print("Polices has recovered!")
    print("Access control policies analyzed: {}.".format(len(policies)))

    for p in policies:
        policy = Policy.from_json(p)
        storage.add(policy)

    pdp = PDP(storage)

    print("Evaluating policies...")

    context_infors = request.get("resource").get('attributes').get('name')

    for n in context_infors:
        request = access_compose(request, n)

        access_request = AccessRequest.from_json(request)

        if pdp.is_allowed(access_request):
            continue
        else:
            print("Access Denied!")
            return "Deny", 401

    print("Access Allowed!")
    return "Allow", 200


def cryptoCheck(request):

    print("Encryption policies evaluation...")
    tags = []

    policies = Crypto()
    tag = request.get("port")
    tags.append(tag)

    storage = policies.getForTarget(tags)

    evaluation = policies.evaluationPolicies(storage, request)

    return evaluation


def cryptoContext(request):
    context = {
        "ip": request.get("ip"),
        "port": request.get("protocol"),
        "time": request.get("time"),
        "device": request.get("device")
    }

    return context


def main():
    host = 'localhost'
    port = 50000

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    print('PDA is running...')

    while True:
        print('Waiting for requests...')
        connection, address = sock.accept()
        print('Connection received from: ' + str(address[0]))
        data = connection.recv(1024)
        data = pickle.loads(data)

        evaluation = accessEvaluation(data)

        permission = evaluation[0]

        if permission != 'Allow':
            connection.send(permission.encode())
        else:
            crypto_context = cryptoContext(data.get("context"))
            crypto_infor = cryptoCheck(crypto_context)
            print(crypto_infor)
            crypto_infor = pickle.dumps(crypto_infor)
            connection.send(crypto_infor)
            print("Evaluation results sent to AM!")


if __name__ == '__main__':
    main()
