

import mongooseconnect


class UserCollection:
    def __init__(self,  id=None, email=None, password=None):
        self.id = id,
        self.email = email,
        self.password = password

    def profile_user(self):
        data = mongooseconnect.users_collection.find_one({"_id": self.id})

        return (data)

    def all_profile():
        data = mongooseconnect.users_collection.find()
        return data

    def is_credential_user(self):
        # print(self.email[0], self.password)
        data = mongooseconnect.users_collection.find(
            {"email": self.email[0], 'password': self.password})
        listed = []
        for i in data:
            listed.append(i)
        self.id = listed[0]['_id']

        return listed != []

    def get_id(self):
        return self.id
