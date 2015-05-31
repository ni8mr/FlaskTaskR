# project/_config.py

import os

# grabbing the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
#USERNAME = 'admin'
#PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_precious'

# defining the full path for the database
DATABASE_PATH = os.path.join(basedir,DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH


# URI= Uniform Resource Identifier- is a string of characters used to identify a name of a resource.
# We are telling sqlalchemy, where to access the database. 
