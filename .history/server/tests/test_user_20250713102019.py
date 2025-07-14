import unittest
from server.models.user import User
from config import db
from run import app

class TestUser(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_set_password(self):
        with app.app_context():
            user = User(username='testuser')
            user.set_password('password')
            self.assertNotEqual(user.password_hash, 'password')

    def test_check_password(self):
        with app.app_context():
            user = User(username='testuser')
            user.set_password('password')
            self.assertTrue(user.check_password('password'))
            self.assertFalse(user.check_password('wrongpassword'))

if __name__ == '__main__':
    unittest.main()