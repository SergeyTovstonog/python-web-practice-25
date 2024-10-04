import os
# Get environment variables from.env file
from dotenv import load_dotenv
load_dotenv()
DA
db_user = os.environ.get('DATABASE_USER', 'admin')
print(db_user)