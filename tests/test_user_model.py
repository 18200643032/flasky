import unittert
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = user(password = 'cat')
        self.asserTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = user(password = 'cat')
        with  self.assertRaises(AttributeError):
         
    def test_password_setter(self):
        u = user(password = 'cat')
        self.asserTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_setter(self):
        u = user(password = 'cat')
        u2 = user(password = 'cat')
        self.asserTrue(u.password_hash != u2.password_hash) 
