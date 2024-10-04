# app.py

import logging
from sqlalchemy import create_engine, select, func, and_, or_, update
from sqlalchemy.orm import sessionmaker, joinedload, selectinload, subqueryload
from models import Base, User, Post
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from db_config import engine, Session

# Configure logging to display SQL statements
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)  # Set to DEBUG for more details

def create_tables():
    """
    Drops all existing tables and creates new ones based on the models.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Database tables created.")

def create_users(session):
    """
    Adds new users to the database.
    """
    print("\n=== CREATE Users ===")
    users = [
        User(name="Alice", email="alice@example.com", age=30),
        User(name="Bob", email="bob@example.com", age=25),
        User(name="Charlie", email="charlie@example.com", age=35),
    ]
    session.add_all(users)
    session.commit()
    print("Added Users: Alice, Bob, Charlie")
    return users  # Return users for reference

def create_posts(session, users):
    """
    Adds new posts associated with users to the database.
    """
    print("\n=== CREATE Posts ===")
    posts = [
        Post(title="First Post", content="Hello World!", author_id=users[0].id),
        Post(title="Second Post", content="SQLAlchemy is awesome!", author_id=users[1].id),
        Post(title="Third Post", content="Python programming tips", author_id=users[0].id),
    ]
    session.add_all(posts)
    session.commit()
    print("Added Posts: First Post, Second Post, Third Post")

def display_users(session):
    """
    Displays all users and their associated posts.
    """
    users = session.execute(select(User).options(selectinload(User.posts))).all()
    print(users)
    for user in users:
        print(f"User: {user[0].name}, Email: {user[0].email}, Age: {user[0].age}")
        for post in user[0].posts:
            print(f"\tPost: {post.title} - {post.content}")
    users = session.execute(select(User).options(selectinload(User.posts))).scalars().all()
    print(users)
    print("\nCurrent Users and Their Posts:")
    for user in users:
        print(f"User: {user.name}, Email: {user.email}, Age: {user.age}")
        for post in user.posts:
            print(f"\tPost: {post.title} - {post.content}")

def display_posts(session):
    """
    Displays all posts and their authors.
    """
    posts = session.execute(select(Post).options(joinedload(Post.author))).scalars().all()
    print("\nCurrent Posts and Their Authors:")
    for post in posts:
        print(f"Post: {post.title}, Content: {post.content}, Author: {post.author.name}")

def read_users_with_eager_loading(session):
    """
    Demonstrates different eager loading strategies.
    """
    print("\n=== READ Operations with Eager Loading ===")

    # Using joinedload
    print("\nQuerying users with their posts using joinedload:")
    users_with_posts_joined = session.execute(
        select(User).options(joinedload(User.posts)).order_by(User.id)
    ).unique().scalars().all()

    for user in users_with_posts_joined:
        print(f"User: {user.name}")
        for post in user.posts:
            print(f"\tPost: {post.title} - {post.content}")

    # Using selectinload
    print("\nQuerying users with their posts using selectinload:")
    users_with_posts_selectin = session.execute(
        select(User).options(selectinload(User.posts)).order_by(User.id)
    ).scalars().all()

    for user in users_with_posts_selectin:
        print(f"User: {user.name}")
        for post in user.posts:
            print(f"\tPost: {post.title} - {post.content}")

    # Using subqueryload
    print("\nQuerying users with their posts using subqueryload:")
    users_with_posts_subquery = session.execute(
        select(User).options(subqueryload(User.posts)).order_by(User.id)
    ).scalars().all()

    for user in users_with_posts_subquery:
        print(f"User: {user.name}")
        for post in user.posts:
            print(f"\tPost: {post.title} - {post.content}")

def read_users_with_lazy_loading(session):
    """
    Demonstrates lazy loading by accessing related objects without specifying eager loading strategies.
    """
    print("\n=== READ Operations with Lazy Loading ===")

    # Fetch all users without eager loading
    query = select(User).order_by(User.id)
    users = session.execute(query).scalars().all()

    for user in users:
        print(f"User: {user.name}, Email: {user.email}, Age: {user.age}")
        # Accessing posts triggers a separate query for each user's posts (lazy loading)
        for post in user.posts:
            print(f"\tPost: {post.title} - {post.content}")

def perform_aggregation(session):
    """
    Demonstrates various aggregation functions.
    """
    print("\n=== Aggregation Functions ===")
    #
    print("\nUsing COUNT():")
    # Count the number of users
    user_count = session.execute(select(func.count(User.id))).scalar()
    print("Number of users:", user_count)

    print("\nUsing SUM():")
    # Sum of ages of all users
    total_age = session.execute(select(func.sum(User.age))).scalar()
    print("Sum of ages:", total_age)

    print("\nUsing AVG():")
    # Average age of users
    average_age = session.execute(select(func.avg(User.age))).scalar()
    print("Average age:", average_age)

    print("\nUsing MIN():")
    # Minimum age of users
    min_age = session.execute(select(func.min(User.age))).scalar()
    print("Minimum age:", min_age)

    print("\nUsing MAX():")
    # Maximum age of users
    max_age = session.execute(select(func.max(User.age))).scalar()
    print("Maximum age:", max_age)

def perform_logical_queries(session):
    """
    Demonstrates the usage of logical operators in queries.
    """
    print("\n=== Logical Operators ===")

    print("\nUsing and_():")
    # Using and_ to filter results
    and_users = session.execute(
        select(User).where(and_(User.age >= 25, User.age <= 35)).options(selectinload(User.posts))
    ).scalars().all()
    print("Users aged between 25 and 35:")
    for user in and_users:
        print(f"User: {user.name}, Age: {user.age}")

    print("\nUsing or_():")
    # Using or_ to filter results
    or_users = session.execute(
        select(User).where(or_(User.name == "Alice", User.name == "Charlie")).options(subqueryload(User.posts))
    ).scalars().all()
    print("Users named Alice or Charlie:")
    for user in or_users:
        print(f"User: {user.name}, Email: {user.email}")

def update_user(session, user_name, new_age):
    """
    Updates the age of a user specified by name.
    """
    print("\n=== UPDATE Operations ===")
    try:
        user = session.execute(
            select(User).where(User.name == user_name)
        ).scalar_one()
        # session.execute(update(User).where(User.name == user_name))
        print(f"Before Update: {user.name}'s Age: {user.age}")
        user.age = new_age
        session.commit()
        print(f"After Update: {user.name}'s Age: {user.age}")
    except NoResultFound:
        print(f"{user_name} not found for update.")
    except MultipleResultsFound:
        print("Multiple users found with the same name.")

def update_post(session, post_title, new_content):
    """
    Updates the content of a post specified by title.
    """
    try:
        post = session.execute(
            select(Post).where(Post.title == post_title)
        ).scalar_one()
        print(f"Before Update: '{post.title}' Content: {post.content}")
        post.content = new_content
        session.commit()
        print(f"After Update: '{post.title}' Content: {post.content}")
    except NoResultFound:
        print(f"Post titled '{post_title}' not found for update.")

def delete_user(session, user_name):
    """
    Deletes a user specified by name.
    """
    print("\n=== DELETE Operations ===")
    try:
        user = session.execute(
            select(User).where(User.name == user_name)
        ).scalar_one()
        session.delete(user)
        session.commit()
        print(f"Deleted User: {user_name}")
    except NoResultFound:
        print(f"{user_name} not found for deletion.")

def delete_post(session, post_title):
    """
    Deletes a post specified by title.
    """
    try:
        post = session.execute(
            select(Post).where(Post.title == post_title)
        ).scalar_one()
        session.delete(post)
        session.commit()
        print(f"Deleted Post: {post_title}")
    except NoResultFound:
        print(f"Post titled '{post_title}' not found for deletion.")

def final_read_operations(session):
    """
    Displays the final state of users and posts after all CRUD operations.
    """
    print("\n=== Final READ Operations ===")

    # Final state of users
    print("\nFinal Users and Their Posts:")
    final_users = session.execute(select(User).options(selectinload(User.posts))).scalars().all()
    for user in final_users:
        print(f"User: {user.name}, Email: {user.email}, Age: {user.age}")
        for post in user.posts:
            print(f"\tPost: {post.title} - {post.content}")

    # Final state of posts
    print("\nFinal Posts and Their Authors:")
    final_posts = session.execute(select(Post).options(joinedload(Post.author))).scalars().all()
    for post in final_posts:
        print(f"Post: {post.title}, Content: {post.content}, Author: {post.author.name}")

def main():
    """
    Main function to execute CRUD operations sequentially.
    """
    # Create tables
    create_tables()

    # Start a session
    with Session() as session:
        # CREATE Operations
        users = create_users(session)
        create_posts(session, users)

        # # Display current data
        # display_users(session)
        # display_posts(session)

    with Session() as session:
        # READ Operations with Lazy Loading
        read_users_with_lazy_loading(session)

        # READ Operations with Eager Loading
        read_users_with_eager_loading(session)
    #
    #     # Aggregation Functions
        perform_aggregation(session)
    #
    #     # Logical Operators
    #     perform_logical_queries(session)
    #
    # with Session() as session:
    #     # UPDATE Operations
    #     update_user(session, "Alice", 31)
    #     update_post(session, "Second Post", "SQLAlchemy makes database interactions seamless!")
    #
    #     # Display updated data
    #     display_users(session)
    #     display_posts(session)
    #
    #     # DELETE Operations
    #     delete_user(session, "Charlie")
    #     delete_post(session, "First Post")
    #
    #     # Display data after deletions
    #     display_users(session)
    #     display_posts(session)
    #
    #     # Final READ Operations
    #     # final_read_operations(session)

if __name__ == "__main__":
    main()
