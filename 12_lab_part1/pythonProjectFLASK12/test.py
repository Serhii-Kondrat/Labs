import unittest
from flask_testing import TestCase
from app import app
from __init__ import db, User
class TestAboutPage(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_about_page_status_code(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_about_page_content(self):
        response = self.client.get('/about')
        expected_phrase = 'Про мене'.encode('utf-8')
        self.assertIn(expected_phrase, response.data)
       
class TestRegistration(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_registration_page_status_code(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_registration_with_valid_data(self):
        data = {
            'name': 'test_user1',
            'password': 'test_password3',
            'email': 'test3@example.com',
            'about_me': 'Test about me3'
        }
        response = self.client.post('/register', data=data, follow_redirects=True)
        expected_phrase = 'Користувача успішно зареєстровано.'.encode('utf-8')
        self.assertIn(expected_phrase, response.data)
        
    def test_registration_with_invalid_data(self):
        data = {
            'name': '',
            'password': '',
            'email': 'test3@example.com',
            'about_me': 'Test about me3'
        }
        response = self.client.post('/register', data=data, follow_redirects=True)
        expected_phrase = 'Імя, пароль або email не можуть бути пустими.'.encode('utf-8')
        self.assertIn(expected_phrase, response.data)


class TestUserCRUDOperations(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Підключення до вашої тестової бази даних
        return app

    def setUp(self):
        db.create_all()  # Створення таблиць у тестовій базі даних

    def tearDown(self):
        db.session.remove()  # Закриття сесії після кожного тесту
        db.drop_all()  # Видалення таблиць після кожного тесту

    def test_create_user(self):
        # Тест створення користувача
        new_user = User(name='TestUser', password='TestPassword')
        db.session.add(new_user)
        db.session.commit()

        created_user = User.query.filter_by(name='TestUser').first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.name, 'TestUser')
        self.assertEqual(created_user.password, 'TestPassword')

    def test_read_user(self):
        # Тест читання користувача
        test_user = User(name='TestUser', password='TestPassword')
        db.session.add(test_user)
        db.session.commit()

        read_user = User.query.filter_by(name='TestUser').first()
        self.assertIsNotNone(read_user)
        self.assertEqual(read_user.name, 'TestUser')
        self.assertEqual(read_user.password, 'TestPassword')

    def test_update_user(self):
        # Тест оновлення користувача
        test_user = User(name='TestUser', password='TestPassword')
        db.session.add(test_user)
        db.session.commit()

        updated_user = User.query.filter_by(name='TestUser').first()
        updated_user.name = 'UpdatedUser'
        updated_user.password = 'UpdatedPassword'
        db.session.commit()

        modified_user = User.query.filter_by(name='UpdatedUser').first()
        self.assertIsNotNone(modified_user)
        self.assertEqual(modified_user.name, 'UpdatedUser')
        self.assertEqual(modified_user.password, 'UpdatedPassword')

    def test_delete_user(self):
        # Тест видалення користувача
        test_user = User(name='TestUser', password='TestPassword')
        db.session.add(test_user)
        db.session.commit()

        deleted_user = User.query.filter_by(name='TestUser').first()
        db.session.delete(deleted_user)
        db.session.commit()

        removed_user = User.query.filter_by(name='TestUser').first()
        self.assertIsNone(removed_user)
   
if __name__ == '__main__':
    unittest.main()
