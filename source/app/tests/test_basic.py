import unittest
from app import create_app, db
from app.models import User, DataPoint


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_user_registration(self):
        response = self.client.post('/auth/register', data={
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_data_point_creation(self):
        user = User(username='test', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        point = DataPoint(x=1.0, y=2.0, label=0, user_id=user.id)
        db.session.add(point)
        db.session.commit()

        self.assertEqual(DataPoint.query.count(), 1)