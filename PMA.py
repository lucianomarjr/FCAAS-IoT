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
    __storage2 = MongoStorage(__client, 'sib', collection='encryption')