from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLAlCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class BloglyModelTestCase(TestCase):
    '''Tests for model for users.'''


    def setUp(self):
        '''Clean up any existing users.'''

        User.query.delete()

    def tearDown(self):
        '''Clean up session.'''

        db.session.rollback()

    def test_fullname(self):
        test_user = User(first_name="Test", last_name="Person")
        self.assertEquals(test_user.full_name(), "Test Person")

    