from bson.objectid import ObjectId
from flask import Flask, request
from mongooseconnect import *
import json
from controllers.indexController import *
from bson import json_util

# initialized flask app
app = Flask(__name__)


@app.route('/post/<id>', methods=['GET', 'POST', 'DELETE'])
@app.route('/post', methods=['GET', 'POST', 'DELETE'])
def index(id=None):
    if(request.method == 'POST'):
        loopInsertAsMuch(collection=post_collection)
        return json.dumps({'message': 'Post successfully'})
    elif request.method == 'DELETE':
        loopDeleteAll(post_collection)
        return json.dumps({'message': 'delete successfully'})
    else:
        if id == None:
            data = post_collection.find()
            return json_util.dumps({'data': data})
        else:
            data = post_collection.find_one({'_id': ObjectId(id)})
            return json_util.dumps({'data': data})


@app.route('/auth/register', methods=['POST', 'DELETE', 'GET'])
def register():
    if request.method == 'POST':
        usersloop = []
        for i in range(20):
            usersloop.append(
                {'name': fakeController().name(), 'email': fakeController().email()})
        users_collection.insert_many(usersloop)
        return json.dumps({'message': 'user successfully register'})
    elif request.method == 'DELETE':
        users_collection.delete_many({})
        return json.dumps({'message': 'user successfully delete'})
    else:
        # this is how we can find one params
        # x = users_collection.find(
        #     {'_id': ObjectId('60d4110d1ea96237fdd821b0')})
        x = users_collection.find()
        return json_util.dumps(x)
