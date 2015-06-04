# project/test.py 

import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'



class AllTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()


    # executed after to each test
    def tearDown(self):
        db.drop_all()


    ##############  helper methods   ##################


    # method for testing if any un-rregistered User is going to login
    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)

    # method for testing if registered user can login (form validation)
    def register(self, name, email, password, confirm):
        return self.app.post('register/', data=dict(name=name, email=email, password=password,\
            confirm=confirm), follow_redirects=True)

    # method for testing if logged in user can logout
    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    
    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
            name= 'Go to the bank.',
            due_date = '02/05/2014',
            priority = '1',
            posted_date = '02/04/2014',
            status = '1'
            ), follow_redirects = True)





    
    ######### test begins here ##############
    
    # testing if form is present in login page
    def test_form_is_present_on_login_page(self):
        response = self.app.get('/') # catching the response from sending a GET request to '/'
        # assertEqual(first,second,msg=None)- Test the first and second are equal. 
        # If the values do not compare equal, the test will fail.
        self.assertEqual(response.status_code, 200) # 200 - OK. It means that the request was recieved and understood and is being processed.
        # assertIn(first,second, msg=None)- Test the first is (or is not) in second.
        self.assertIn(b'Please sign in to access your task list',\
            response.data)


    # testing if un-registered users cannot login
    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data) 

    # testing if registered user can login (form validation)
    def test_users_can_login(self):
        self.register('Afzalur','afzalur@east_colony.com', 'python', 'python')
        response = self.login('Afzalur', 'python')
        self.assertIn(b'Welcome!', response.data)

    # testing with some bad data in case of form validation
    def test_invalid_form_data(self):
        self.register('Michael', 'michael@gmail.com', 'python', 'python')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

    # testing if form is present on register page
    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.', response.data)

    # testing if user can register (another kind of form validation)
    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Michael', 'michael@realpython.com', 'python', 'python')
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    # Testing the Error Handling while registering
    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Michael', 'michael@python.com', 'python', 'python')
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Michael', 'michael@python.com', 'python', 'python'
        )
        self.assertIn(
            b'That username and/or email already exist.',
            response.data
        )

    # Testing if users can logout (We will make sure that only logged in users can log out)
    # if anyone is not logged in, he/she should be redirected to the homepage.
    def test_logged_in_users_can_logout(self):
        self.register('Fletcher', 'Fletcher@gmail.com', 'python', 'python')
        self.login('Fletcher', 'python')
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)
    
    # testing if the user can access the task page
    def test_logged_in_users_can_access_tasks_page(self):
        self.register('Reza vai', 'n.f.r@gmail.com', 'python', 'python')
        self.login('Reza vai', 'python')
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects = True)
        self.assertIn(b'You need to login first.', response.data)

    # testing if the user can add task
    def test_users_can_add_tasks(self):
        self.create_user('Michael', 'michael_herman@gmail.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects = True)
        response = self.create_task()
        self.assertIn(b'New entry was succesfully posted. Thanks.', response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user('Office', 'officeport@gmail.com', 'python')
        self.login('Office', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name = 'Go to the bank',
            due_date = '',
            priority = '1',
            posted_date = '02/05/2015',
            status = '1'
            ), follow_redirects = True)
        self.assertIn(b'This field is required', response.data)

    # testing if users can complete tasks
    def test_users_can_complete_tasks(self):
        self.create_user('Office', 'officeport@gmail.com', 'python')
        self.login('Office', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'The task is complete. Nice.', response.data)

    # testing if users can delete tasks
    def test_users_can_delete_tasks(self):
        self.create_user('Office', 'officeport@gmail.com', 'python')
        self.login('Office', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    # testing the (one-to-many relationship), i.e. if a user A adds a task,
    # only user A can update and/or delete that task.
    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Office', 'officeport@gmail.com', 'python')
        self.login('Office', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Michael', 'michael_herman@gmail.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects = True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(b'The task is complete. Nice.', response.data)


if __name__ == '__main__':
    unittest.main()

# unittest.main() provides a command line interface to the test script
# the interface represents the result
        

     
