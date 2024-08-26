from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return jsonify({"message": "Hello, Dockerized Flask with PostgreSQL and Poetry!"})

@app.route('/check-db')
def check_db():
    try:
        # Try to make a simple query to the database
        db.session.execute(text('SELECT 1'))
        return jsonify({"db_connection": "successful"})
    except Exception as e:
        return jsonify({"db_connection": "failed", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
