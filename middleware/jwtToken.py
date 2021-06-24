from flask.app import Flask
import jwt
from flask import request, jsonify
from functools import wraps
from app import *
from decouple import config


class TokenRequire:

    def token_required(func):
        # decorator factory which invoks update_wrapper() method and passes decorated function as an argument

        @wraps(func)
        def decorated(*args, **kwargs):
            # arg whatever params, it will understand
            token = request.headers.get('authorization').split()[1]
            if not token:
                return jsonify({'Alert!': 'Token is missing!'}), 401

            try:

                data = jwt.decode(token, config('SECRET_KEY_JWT'))
            # You can use the JWT errors in exception
            # except jwt.InvalidTokenError:
            #     return 'Invalid token. Please log in again.'
                print(data)

            except:
                return jsonify({'Message': 'Invalid token'}), 403
            return func(*args, **kwargs)
        return decorated

    def store_token(usersModule):
        token = jwt.encode({
            'user':   str(usersModule.get_id()),
            # don't forget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return token
