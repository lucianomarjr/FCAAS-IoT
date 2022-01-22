from py_abac import Policy
from pymongo import MongoClient
from py_abac.storage.mongo import MongoStorage, MongoMigrationSet


class AccessControl:

    __usr = 'bdadmin'
    __psw = '111293'
    __client = MongoClient('192.168.1.150', 27017)
    __db = __client.sib
    __db.authenticate(__usr, __psw, source='admin')

    __storage = MongoStorage(__client, 'sib', collection='accesscontrol')
    #__storage2 = MongoStorage(__client, 'sib', collection='encryption')


    def save(self, policy_json: Policy):
        policy = Policy.from_json(policy_json)
        MongoStorage.add(policy)


    def getById(self, id: str):
        return MongoStorage.get(id).to_json()


    def getAll(self, limit: int, offset: int):
        data = MongoStorage.get_all(limit,offset)
        policies = []
        for d in data:
            policies.append(d.to_json())
        return policies


    def getForTarget(self, subjectId: str, resourceId: str, actionId: str):
        data = MongoStorage.get_for_target(subjectId, resourceId, actionId)
        policies = []
        for d in data:
            policies.append(d.to_json())
        return policies

    def getForTarResource(self, resourceId: str):
        data = MongoStorage.get_for_target('', resourceId, '')
        policies = []
        for d in data:
            policies.append(d.to_json())
        return policies

    def update(self, id: str, policy: Policy):
        policy.uid = id
        MongoStorage.update(policy)

    def delete(self, id: str):
        MongoStorage.delete(id)


class EncryptionPolicy:

    def __init__(self):
        __usr = 'bdadmin'
        __psw = '111293'
        __client = MongoClient('192.168.1.150', 27017)
        __db = __client.sib
        __db.authenticate(__usr, __psw, source='admin')

        self.policies = __db["encryption"]

    def getPolicies(self):
        policies_all = []
        for p in self.policies.find():
            policies_all.append(p)

    def getForTarget(self, tags:list):
        eval_policies = []
        priority = [3, 2, 1]
        try:
            for n in priority:
                for p in self.policies.find({"tags": tags, "priority": n}):
                    eval_policies.append(p)
        except:
            pass

        return eval_policies

    def save(self, policy: object):
        try:
            storage_policy = self.policies.insert_one(policy)
            print("Police saved! ID: {}.".format(storage_policy.inserted_id))
            return True

        except:
            return False

    def delete(self, id):
        try:
            self.policies.delete_one({"_id": id})
            print("Policy {} has deleted!".format(id))
        except:
            print("Policy not found!")
            return False

    @staticmethod
    def evaluationPolicies(eval_policies: list, context: dict):
        c = 0
        length = len(eval_policies)
        print("Quantidade de políticas a serem avaliadas: {}.".format(length))

        while c < length:
            policy = eval_policies[c]
            print("Policy analised: {}".format(policy.get("_id")))
            p_context = policy.get("context")
            flag = True
            while flag:
                c_count = 0
                for key, value in context.items():
                    itens = p_context[key]
                    if not itens == [] or value in itens:
                        c_count += 1
                        if c_count >= len(context):
                            return policy.get("c_infors")
                        else:
                            flag = False
            else:
                c += 1








