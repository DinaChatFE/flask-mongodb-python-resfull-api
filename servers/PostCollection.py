import mongooseconnect


class PostCollection:
    def get_individuals_posts(id):
        return mongooseconnect.post_collection.find({'user._id': id})
