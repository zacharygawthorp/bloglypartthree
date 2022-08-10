from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLAlCHEMY_ECHO'] = False

app.config['Testing'] = True

db.drop_all()
db.create_all()


class BloglyViewsTestCase(TestCase):
    '''Tests for model for users.'''


    def setUp(self):
        '''Clean up any existing users.'''

        User.query.delete()

        test_user = User(first_name="Test", last_name="Person")
        db.session.add(test_user)
        db.session.commit()

        self.test_user_id = test_user.id

    def tearDown(self):
        '''Clean up session.'''

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Person', html)

    def test_root_redirect(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")
            
    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new_user")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_edit_user_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.test_user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)