# crud_operations_mongoengine.py

import os
from models import User, Post
from dotenv import load_dotenv
import mongoengine as me

# Load environment variables from .env file
load_dotenv()

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_DB = os.getenv('MONGO_DB', 'mydatabase')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'users_me')

import mongoengine as me
def connect_db():
    """Establishes a connection to the MongoDB database using MongoEngine."""
    try:
        me.connect(
            db=MONGO_DB,
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USER,
            password=MONGO_PASSWORD,
            authentication_source='admin'
        )
        print("MongoDB connection: SUCCESS")
    except me.ConnectionError as e:
        print(f"MongoDB connection: FAILED\nError: {e}")
        exit(1)

# --- CREATE Operations ---

def create_user(name, age, email):
    """Inserts a new user into the database."""
    try:
        user = User(name=name, age=age, email=email)
        user.save()
        print(f"Created User: {user.id}")
    except me.NotUniqueError:
        print(f"User with email '{email}' already exists.")
    except me.ValidationError as ve:
        print(f"Validation Error: {ve}")


def create_post(title, content, user_email):
    """Inserts a new post associated with a user."""
    try:
        user = User.objects(email=user_email).first()
        if not user:
            print(f"No user found with email '{user_email}'.")
            return
        post = Post(title=title, content=content, author=user)
        post.save()
        print(f"Created Post: {post.id} for User: {user.name}")
    except me.ValidationError as ve:
        print(f"Validation Error: {ve}")


def create_multiple_users(users_data):
    """Inserts multiple users into the database."""
    try:
        users = [User(**data) for data in users_data]
        User.objects.insert(users, load_bulk=False)
        print(f"Inserted {len(users)} users.")
    except me.NotUniqueError as e:
        print(f"Error inserting users: {e}")
    except me.ValidationError as ve:
        print(f"Validation Error: {ve}")


def create_multiple_posts(posts_data):
    """Inserts multiple posts into the database."""
    try:
        posts = []
        for data in posts_data:
            user = User.objects(email=data['user_email']).first()
            if not user:
                print(f"No user found with email '{data['user_email']}'. Skipping post '{data['title']}'.")
                continue
            post = Post(title=data['title'], content=data['content'], author=user)
            posts.append(post)
        Post.objects.insert(posts, load_bulk=False)
        print(f"Inserted {len(posts)} posts.")
    except me.ValidationError as ve:
        print(f"Validation Error: {ve}")


# --- READ Operations ---

def read_user_by_email(email):
    """Finds and returns a user by email."""
    user = User.objects(email=email).first()
    if user:
        print(f"Found User: {user.name}, Age: {user.age}, Email: {user.email}")
    else:
        print(f"No user found with email '{email}'.")


def read_all_users():
    """Retrieves and prints all users."""
    users = User.objects()
    print("All Users:")
    for user in users:
        print(f"- {user.name}, Age: {user.age}, Email: {user.email}")


def read_users_with_age_gte(age):
    """Finds and prints users with age greater than or equal to the specified value."""
    users = User.objects(age__gte=age)
    print(f"Users aged {age} and above:")
    for user in users:
        print(f"- {user.name}, Age: {user.age}, Email: {user.email}")


def read_posts_by_user(email):
    """Finds and prints all posts authored by a specific user."""
    user = User.objects(email=email).first()
    if not user:
        print(f"No user found with email '{email}'.")
        return
    posts = Post.objects(author=user)
    print(f"Posts by {user.name}:")
    for post in posts:
        print(f"- {post.title}: {post.content} (Created at: {post.created_at})")


# --- UPDATE Operations ---

def update_user_age(email, new_age):
    """Updates the age of a user identified by email."""
    user = User.objects(email=email).first()
    if not user:
        print(f"No user found with email '{email}'.")
        return
    user.update(set__age=new_age)
    print(f"Updated {user.name}'s age to {new_age}.")


def update_post_title(post_id, new_title):
    """Updates the title of a post identified by its ID."""
    post = Post.objects(id=post_id).first()
    if not post:
        print(f"No post found with ID '{post_id}'.")
        return
    post.update(set__title=new_title)
    print(f"Updated Post ID {post_id} title to '{new_title}'.")


def increment_user_age(email, increment=1):
    """Increments the age of a user by a specified value."""
    user = User.objects(email=email).first()
    if not user:
        print(f"No user found with email '{email}'.")
        return
    user.update(inc__age=increment)
    print(f"Incremented {user.name}'s age by {increment}.")


# --- DELETE Operations ---

def delete_user(email):
    """Deletes a user identified by email."""
    user = User.objects(email=email).first()
    if not user:
        print(f"No user found with email '{email}'.")
        return
    user.delete()
    print(f"Deleted User: {user.name}")


def delete_post(post_id):
    """Deletes a post identified by its ID."""
    post = Post.objects(id=post_id).first()
    if not post:
        print(f"No post found with ID '{post_id}'.")
        return
    post.delete()
    print(f"Deleted Post: {post.title}")


def delete_users_with_age_gte(age):
    """Deletes all users with age greater than or equal to the specified value."""
    users = User.objects(age__gte=age)
    count = users.count()
    users.delete()
    print(f"Deleted {count} user(s) aged {age} and above.")


def delete_posts_before_date(date):
    """Deletes all posts created before the specified date."""
    posts = Post.objects(created_at__lt=date)
    count = posts.count()
    posts.delete()
    print(f"Deleted {count} post(s) created before {date}.")


# --- ADDITIONAL OPERATIONS ---

def list_collections():
    """Lists all collections in the current database."""
    db = me.connection.get_db()
    collections = db.list_collection_names()
    print(f"Collections in '{MONGO_DB}':")
    for coll in collections:
        print(f"- {coll}")


def create_indexes():
    """Creates indexes on the collections."""
    # Creating index on User.email
    User.create_index('email')
    print("Created index on User.email")

    # Creating index on Post.created_at
    Post.create_index('created_at')
    print("Created index on Post.created_at")

    # Creating compound index on Post.title and Post.author
    Post.create_index([('title', 1), ('author', 1)])
    print("Created compound index on Post.title and Post.author")


def perform_aggregation():
    """Performs an aggregation to count users by age."""
    pipeline = [
        {"$match": {"age": {"$gte": 25}}},
        {"$group": {"_id": "$age", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = User._get_collection().aggregate(pipeline)
    print("Aggregation Result (User Count by Age):")
    for doc in result:
        print(f"Age: {doc['_id']}, Count: {doc['count']}")


def perform_post_aggregation():
    """Performs an aggregation to count posts by user."""
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = Post._get_collection().aggregate(pipeline)
    print("Aggregation Result (Post Count by User):")
    for doc in result:
        user = User.objects(id=doc['_id']).first()
        user_name = user.name if user else "Unknown"
        print(f"User: {user_name}, Post Count: {doc['count']}")


def list_databases():
    """Lists all databases in the MongoDB server."""
    dbs = me.connection.get_db().client.list_database_names()
    print("Databases:")
    for db in dbs:
        print(f"- {db}")


def list_all_users_and_posts():
    """Lists all users and their associated posts."""
    users = User.objects()
    for user in users:
        print(f"User: {user.name}, Email: {user.email}")
        posts = Post.objects(author=user)
        for post in posts:
            print(f"  - Post: {post.title}, Created at: {post.created_at}")


# --- MAIN FUNCTION ---

def main():
    """Main function to execute CRUD and additional operations."""
    connect_db()

    # --- CREATE Operations ---
    print("\n--- CREATE OPERATIONS ---")
    create_user(name="Alice", age=30, email="alice@example.com")
    create_user(name="Bob", age=25, email="bob@example.com")
    create_user(name="Charlie", age=35, email="charlie@example.com")

    create_post(title="Alice's First Post", content="Hello World!", user_email="alice@example.com")
    create_post(title="Bob's Thoughts", content="Today was a good day.", user_email="bob@example.com")
    create_post(title="Charlie's Adventures", content="Went hiking today.", user_email="charlie@example.com")

    # --- READ Operations ---
    print("\n--- READ OPERATIONS ---")
    read_user_by_email("alice@example.com")
    read_all_users()
    read_users_with_age_gte(30)
    read_posts_by_user("alice@example.com")

    # --- UPDATE Operations ---
    print("\n--- UPDATE OPERATIONS ---")
    update_user_age(email="alice@example.com", new_age=31)
    update_post_title(post_id=Post.objects(title="Alice's First Post").first().id, new_title="Alice's Updated Post")
    increment_user_age(email="bob@example.com", increment=2)

    # --- DELETE Operations ---
    print("\n--- DELETE OPERATIONS ---")
    delete_user(email="charlie@example.com")
    post_to_delete = Post.objects(title="Bob's Thoughts").first()
    if post_to_delete:
        delete_post(post_id=post_to_delete.id)
    delete_users_with_age_gte(35)

    # --- ADDITIONAL OPERATIONS ---
    print("\n--- ADDITIONAL OPERATIONS ---")
    list_databases()
    list_collections()
    # create_indexes()
    perform_aggregation()
    perform_post_aggregation()
    list_all_users_and_posts()

    # Close the connection
    me.disconnect()


if __name__ == "__main__":
    main()
