# crud_operations.py

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection details from environment variables
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_DB = os.getenv('MONGO_DB', 'mydatabase')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'users')

def get_client():
    """Establishes and returns a MongoDB client."""
    try:
        client = MongoClient(
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USER,
            password=MONGO_PASSWORD,
            authSource='admin'
        )
        # Verify connection
        client.admin.command('ismaster')
        print("MongoDB connection: SUCCESS")
        return client
    except ConnectionFailure:
        print("MongoDB connection: FAILED")
        exit(1)

def get_collection(client):
    """Returns the specified collection from the database."""
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    return collection

# --- CREATE Operations ---

def create_single_document(collection, document):
    """Inserts a single document into the collection."""
    result = collection.insert_one(document)
    print(f"Inserted document with _id: {result.inserted_id}")

def create_multiple_documents(collection, documents):
    """Inserts multiple documents into the collection."""
    result = collection.insert_many(documents)
    print(f"Inserted documents with _ids: {result.inserted_ids}")

# --- READ Operations ---

def read_one_document(collection, query):
    """Finds and returns one document matching the query."""
    document = collection.find_one(query)
    print("Find one:", document['name'])

def read_all_documents(collection):
    """Finds and prints all documents in the collection."""
    print("Find all users:")
    for doc in collection.find():
        print(doc)

def read_with_filter(collection, query):
    """Finds and prints documents matching the filter query."""
    print(f"Users matching {query}:")
    for doc in collection.find(query):
        print(doc)

# --- UPDATE Operations ---

def update_one_document(collection, query, update):
    """Updates a single document matching the query."""
    result = collection.update_one(query, update)
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")

def update_multiple_documents(collection, query, update):
    """Updates multiple documents matching the query."""
    result = collection.update_many(query, update)
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")

# --- DELETE Operations ---

def delete_one_document(collection, query):
    """Deletes a single document matching the query."""
    result = collection.delete_one(query)
    print(f"Deleted {result.deleted_count} document.")

def delete_multiple_documents(collection, query):
    """Deletes multiple documents matching the query."""
    result = collection.delete_many(query)
    print(f"Deleted {result.deleted_count} documents.")

# --- ADDITIONAL OPERATIONS ---

def list_databases(client):
    """Lists all databases."""
    print("Databases:")
    for db_name in client.list_database_names():
        print(f" - {db_name}")

def list_collections(db):
    """Lists all collections in the specified database."""
    print(f"Collections in '{db.name}':")
    for coll in db.list_collection_names():
        print(f" - {coll}")

def create_indexes(collection):
    """Creates indexes on the collection."""
    index_name = collection.create_index("email")
    print(f"Created index: {index_name}")

    compound_index = collection.create_index([("name", 1), ("age", -1)])
    print(f"Created compound index: {compound_index}")

def perform_aggregation(collection):
    """Performs an aggregation pipeline."""
    pipeline = [
        {"$match": {"age": {"$gte": 25}}},
        {"$group": {"_id": "$age", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

    print("Aggregation result:")
    for doc in collection.aggregate(pipeline):
        print(doc)

def main():
    """Main function to execute CRUD and additional operations."""
    client = get_client()
    collection = get_collection(client)

    # --- CREATE ---
    user = {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    }
    create_single_document(collection, user)

    users = [
        {"name": "Bob", "age": 25, "email": "bob@example.com"},
        {"name": "Charlie", "age": 35, "email": "charlie@example.com", "address": "NY"},
        {"name": "Diana", "age": 22, "email": "diana@example.com", "url": "http://example.com"},
        {"name": "Eve", "age": 28, "email": "eve@example.com"}
    ]
    create_multiple_documents(collection, users)

    # --- READ ---
    read_one_document(collection, {"name": "Alice"})
    read_all_documents(collection)
    read_with_filter(collection, {"age": {"$gte": 30}})
    #
    # # --- UPDATE ---
    update_one_document(collection, {"name": "Alice"}, {"$set": {"age": 31}})
    update_multiple_documents(collection, {"age": {"$lt": 30}}, {"$inc": {"age": 1}})
    read_all_documents(collection)
    # #
    # # # --- DELETE ---
    delete_one_document(collection, {"name": "Bob"})
    delete_multiple_documents(collection, {"age": {"$gte": 35}})

    # # --- ADDITIONAL OPERATIONS ---
    list_databases(client)
    list_collections(client[MONGO_DB])
    create_indexes(collection)
    perform_aggregation(collection)
    #
    # # Close the client connection
    client.close()

if __name__ == "__main__":
    main()
