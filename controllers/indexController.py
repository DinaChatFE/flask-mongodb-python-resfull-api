import json
import string
import random
from bson import json_util
from faker import Faker
from mongooseconnect import *
fake = Faker()


def fakeController():
    return fake


def loopDeleteAll(collection):
    collection.delete_many({})


def loopInsertAsMuch(collection, insertNumber=10):
    x = users_collection.find()
    listIbj = []
    for i in x:
        listIbj.append(i)

    randomcatch = random.randint(0, len(listIbj)-1)
    userselector = listIbj[randomcatch]
    print(listIbj[randomcatch])

    values = []
    for _ in range(insertNumber):
        value = {"name": fake.name(),
                 "address": fake.address(),
                 "user": userselector,
                 "comment": [{'user': userselector, 'comment': fake.name()}]
                 }
        values.append(value)

    collection.insert_many(values)


def randomName(N=7):
    return ''.join(random.choices(string.ascii_uppercase +
                                  string.digits, k=N))
