from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

# Модель користувача
class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

# Схема Marshmallow для серіалізації та десеріалізації об'єктів User
class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Дані користувачів (тимчасово для прикладу)
users_data = {
    1: User(1, 'john_doe', 'john.doe@example.com'),
    2: User(2, 'jane_doe', 'jane.doe@example.com')
}

# Базовий клас для ендпоінтів користувачів
class UserResource(Resource):
    def get(self, user_id):
        user = users_data.get(user_id)
        if user:
            return user_schema.dump(user)
        return {'message': 'User not found'}, 404

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username cannot be blank', required=True)
        parser.add_argument('email', type=str, help='Email cannot be blank', required=True)
        args = parser.parse_args()

        user = users_data.get(user_id)
        if user:
            user.username = args['username']
            user.email = args['email']
            return user_schema.dump(user)
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = users_data.pop(user_id, None)
        if user:
            return {'message': 'User deleted successfully'}
        return {'message': 'User not found'}, 404

# Ендпоінт для отримання списку користувачів
class UsersResource(Resource):
    def get(self):
        return users_schema.dump(list(users_data.values()))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username cannot be blank', required=True)
        parser.add_argument('email', type=str, help='Email cannot be blank', required=True)
        args = parser.parse_args()

        user_id = max(users_data.keys()) + 1
        new_user = User(user_id, args['username'], args['email'])
        users_data[user_id] = new_user
        return user_schema.dump(new_user), 201

# Додаємо ендпоінти до API
api.add_resource(UserResource, '/api/user/<int:user_id>')
api.add_resource(UsersResource, '/api/users')

# Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'User API'})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Основний маршрут для HTML-сторінки
@app.route('/')
def ap():
    return render_template('test.html')

@app.route('/ap')
def home():
    return render_template('home.html')

# Запускаємо сервер
if __name__ == '__main__':
    app.run(debug=True)
