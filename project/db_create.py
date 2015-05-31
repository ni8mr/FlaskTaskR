# project/db_create.py 

from views import db
from models import Task
from datetime import date


# Create the database and the db table
db.create_all()

# inserting dummy datas
db.session.add(Task("Finish this tutorial", date(2015, 3, 13), 10, 1)) 
db.session.add(Task("Finish Real Python", date(2015, 3, 13), 10, 1))

# commiting the changes
db.session.commit()

