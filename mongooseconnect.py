import pymongo
from decouple import config


client = pymongo.MongoClient(config("KEY"))
db = client['mydb']
users_collection = db['users']
post_collection = db['posts']
comments_collection = db['comments']
