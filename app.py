from datetime import datetime, timedelta
from servers.PostCollection import PostCollection
from servers.UserCollection import UserCollection
from bson.objectid import ObjectId
from flask import Flask, request, jsonify, session
from flask.helpers import make_response
from decouple import config
import json
from controllers.indexController import *
from bson import json_util
from middleware.jwtToken import TokenRequire
import jwt

# initialized flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config("SECRET_KEY_JWT")

# print(config['SECRET_KEY'])


@app.route('/post/<id>', methods=['GET', 'POST', 'DELETE'])
@app.route('/post', methods=['GET', 'POST', 'DELETE'])
# ==========register middleware here==============
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


@app.route('/my-post', methods=['POST', 'GET'])
@TokenRequire.token_required
def myPost():
    if request.method == 'GET':
        return json_util.dumps({'data': PostCollection.get_individuals_posts(ObjectId("60d4110d1ea96237fdd821bb"))})


@app.route('/auth/register', methods=['POST', 'DELETE', 'GET'])
def register():
    if request.method == 'POST':
        usersloop = []
        for _ in range(20):
            usersloop.append(
                {'name': fakeController().name(), 'email': fakeController().email(), 'password': 'dina12345'})
        users_collection.insert_many(usersloop)
        return json.dumps({'message': 'user successfully register'})
    elif request.method == 'DELETE':
        users_collection.delete_many({})
        return json.dumps({'message': 'user successfully delete'})
    else:
        x = users_collection.find()
        return json_util.dumps(x)


@app.route("/auth/login", methods=['POST'])
def login():
    usersModule = UserCollection(
        email=request.json['email'], password=request.json['password'])

    foundUser = usersModule.is_credential_user()

    if foundUser:
        session['logged_in'] = True

        token = jwt.encode({
            'user':   str(usersModule.get_id()),
            # don't forget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])

        return jsonify({'message': "User successfully login", 'token': str(token)})

    else:
        return make_response({'message': 'Unable to connect'}, 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


if __name__ == "__main__":
    app.run(debug=True)
