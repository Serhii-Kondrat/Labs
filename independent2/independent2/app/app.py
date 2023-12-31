from flask import Flask, request, render_template, redirect, url_for, session, flash, make_response, jsonify
import os 
from datetime import datetime
import json
from forms import LoginForm,  UpdateAccountForm
from __init__ import db, User, RegUser, Post
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restful import Api, Resource, reqparse, fields,  marshal_with



app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
api = Api(app)
user_cookies = {}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  
app.config['SQLALCHEMY_BINDS'] = {
    'reg': 'sqlite:///reg.db'
}
UPLOAD_FOLDER = 'app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

current_directory = os.path.dirname(__file__)
users_file_path = os.path.join(current_directory, 'users.json')


with open(users_file_path, 'r') as users_file:
    users = json.load(users_file)
app.secret_key = '123456'

todos = [
    {"id": 1, "task": "Приклад завдання", "status": "В процесі"},
    {"id": 2, "task": "Інше завдання", "status": "Виконано"}
]
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)




@app.route("/independent_test")
def independent_test():
    return render_template("indepedent_test.html")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Будь ласка, увійдіть для доступу до цієї сторінки', 'error')
            return redirect(url_for('new_login'))
        return f(*args, **kwargs)
    return decorated_function


post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
}

class IndependentAPI(Resource):
    @marshal_with(post_fields)
    def get(self, post_id=None):
        if post_id:
            
            post = Post.query.get(post_id)
            if not post:
                return {'message': 'Post not found'}, 404
            return post, 200
        else:
         
            all_independent = Post.query.all()
            return all_independent, 200

    @marshal_with(post_fields)
    def post(self):
        
        title = request.json['title']
        content = request.json['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return new_post, 201

    @marshal_with(post_fields)
    def put(self, post_id):
      
        post = Post.query.get(post_id)
        if not post:
            return {'message': 'Post not found'}, 404

        post.title = request.json.get('title', post.title)
        post.content = request.json.get('content', post.content)
        db.session.commit()
        return post, 200

    def delete(self, post_id):
       
        post = Post.query.get(post_id)
        if not post:
            return {'message': 'Post not found'}, 404

        db.session.delete(post)
        db.session.commit()
        return {'message': 'Post deleted'}, 200


api.add_resource(IndependentAPI, '/api/independent', '/api/independent/<int:post_id>', endpoint='independent_api')




@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    username = session.get('username')
    form = UpdateAccountForm()

    if username:
        user = RegUser.query.filter_by(RegName=username).first()

        if user:
            if form.validate_on_submit():
                user.RegName = form.username.data
                user.email = form.email.data
                user.about_me = form.about_me.data  
                user.RegPassword = form.password.data  
                db.session.commit()  
                flash('Your account has been updated!', 'success')
                return redirect(url_for('account'))

            form.username.data = user.RegName
            form.email.data = user.email
            form.about_me.data = user.about_me  
            form.password.data = user.RegPassword  

            return render_template('account.html', user=user, form=form)

    flash('Please log in to access this page', 'error')
    return redirect(url_for('new_login'))


@app.route('/new_login', methods=['GET', 'POST'])
def new_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = RegUser.query.filter_by(RegName=username).first()

        if user and user.RegPassword == password:
            flash('Успішний вхід', 'success')
           
            session['username'] = username
            session['email'] = user.email
          
            access_token = create_access_token(identity=username)
            session['access_token'] = access_token

            user.last_seen = datetime.utcnow()
            db.session.commit()

            return redirect(url_for('home'))
        else:
            flash('Невірне ім\'я користувача або пароль', 'error')

    return render_template('NewLogin.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        about_me = request.form.get('about_me')  
        

        if name and password and email:
            new_reg_user = RegUser(
                RegName=name,
                RegPassword=password, 
                email=email,
                about_me=about_me 
            )
            db.session.add(new_reg_user)
            db.session.commit()
            flash('Користувача успішно зареєстровано.', 'success')
            return redirect(url_for('get_todos'))
        else:
            flash('Ім\'я, пароль або email не можуть бути пустими.', 'error')

    return render_template("reg.html")


@app.route('/change_profile_picture', methods=['POST'])
@login_required
def change_profile_picture():
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file.filename != '':
    
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

         
            username = session.get('username')
            if username:
                user = RegUser.query.filter_by(RegName=username).first()
                if user:
                    user.image_file = filename
                    db.session.commit()
                    flash('Фото профілю змінено успішно.', 'success')
                    return redirect(url_for('account'))

    flash('Помилка при зміні фото профілю.', 'error')
    return redirect(url_for('account'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        if username in users and users[username] == password:
            flash('Login successful', 'success')
            session['username'] = username

            if not remember:
                return redirect(url_for('home'))
            
            session.permanent = True
            return redirect(url_for('info'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)

   


   
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Выход выполнен успешно', 'success')
    return redirect(url_for('new_login'))


@app.route("/")
@login_required
def index():
    return render_template("home.html")

@app.route('/home')
@login_required
def home():
    return render_template("home.html")
@app.route('/page1')
def page1():
    return render_template("page1.html")

@app.route('/page2')
def page2():
    return render_template("page2.html")

@app.route('/page3')
def page3():
    return render_template("page3.html")






@app.context_processor
def utility_processor():
    os_info = os.name  
    user_agent = request.headers.get("User-Agent")  
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

    return dict(os_info=os_info, user_agent=user_agent, current_time=current_time)



if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port=8080)