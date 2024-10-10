from datetime import datetime
import mongoengine as me


class User(me.Document):
    name = me.StringField(required=True)
    age = me.IntField(required=True, min_value=0)
    email = me.EmailField(required=True, unique=True)

    meta = {
        'collection': 'users_me'
    }


# Define the Post Document with a reference to User
class Post(me.Document):
# class Post(me.EmbeddedDocument):
    title = me.StringField(required=True)
    content = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
    author = me.ReferenceField(User, reverse_delete_rule=me.CASCADE)

    meta = {
        'collection': 'posts'
    }

# class User(me.Document):
#     name = me.StringField(required=True)
#     age = me.IntField(required=True)
#     posts = me.ListField(me.EmbeddedDocumentField(Post))
#     email = me.EmailField(required=True, unique=True)
#
#     meta = {
#         'collection': os.getenv('MONGO_COLLECTION', 'users')
#     }