from flask import Flask, request, render_template, redirect, url_for, session, flash, make_response, jsonify
from data import posts
import os 
from datetime import datetime
import json
from forms import LoginForm, FeedbackForm
from __init__ import db, User, Feedback


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
user_cookies = {}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  


current_directory = os.path.dirname(__file__)
users_file_path = os.path.join(current_directory, 'users.json')

# Загрузка данных о пользователях из JSON-файла
with open(users_file_path, 'r') as users_file:
    users = json.load(users_file)
app.secret_key = '123456'

todos = [
    {"id": 1, "task": "Приклад завдання", "status": "В процесі"},
    {"id": 2, "task": "Інше завдання", "status": "Виконано"}
]

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    feedback_form = FeedbackForm()
    if feedback_form.validate_on_submit():
        feedback_text = feedback_form.feedback.data
        new_feedback = Feedback(text=feedback_text)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Відгук успішно додано.', 'success')
        return redirect(url_for('feedback'))

    feedbacks = Feedback.query.all()
    return render_template("feedback.html", feedback_form=feedback_form, feedbacks=feedbacks)
@app.route('/todos/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    password = request.form.get('password')
    
    if name and password:
        # Create a new User instance and add it to the database
        new_user = User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Користувача успішно додано до бази даних.', 'success')
    else:
        flash('Ім\'я та пароль не можуть бути пустими.', 'error')

    return redirect(url_for('get_todos'))
@app.route('/todos', methods=['GET'])
def get_todos():
    users = User.query.all()  # Отримання списку користувачів з бази даних
    return render_template("todos.html", users=users)

@app.route('/todos/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Користувача успішно видалено.', 'success')
    else:
        flash('Користувача не знайдено.', 'error')

    return redirect(url_for('get_todos'))
@app.route('/todos/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if user:
        new_name = request.form.get('new_name')
        new_password = request.form.get('new_password')
        
        if new_name:
            user.name = new_name
        if new_password:
            user.password = new_password

        db.session.commit()
        flash('Зміни збережено успішно.', 'success')
    else:
        flash('Користувача не знайдено.', 'error')

    return redirect(url_for('get_todos'))
# Шлях для додавання нового завдання
@app.route('/todos/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    status = request.form.get('status')
    new_todo = {"id": len(todos) + 1, "task": task, "status": status}
    todos.append(new_todo)
    return redirect(url_for('get_todos'))

# Шлях для редагування завдання
@app.route('/todos/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    task = request.form.get('task')
    status = request.form.get('status')
    for todo in todos:
        if todo['id'] == todo_id:
            todo['task'] = task
            todo['status'] = status
            break
    return redirect(url_for('get_todos'))

# Шлях для видалення завдання
@app.route('/todos/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
            break
    return redirect(url_for('get_todos'))
# Создание страницы "login" с формой для входа
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

   

# Создание страницы "info" с информацией для авторизованных пользователей
@app.route('/info', methods=['GET', 'POST'])
def info():
    if 'username' in session:
        username = session['username']
        cookies = user_cookies
        message = None

        if request.method == 'POST':
            if 'add_cookie' in request.form:
                cookie_key = request.form['cookie_key']
                cookie_value = request.form['cookie_value']
                cookie_expiry = int(request.form['cookie_expiry'])
                
                user_cookies[cookie_key] = cookie_value

                response = make_response(redirect(url_for('info')))
                response.set_cookie(cookie_key, cookie_value, max_age=cookie_expiry)
                flash(f'Cookie "{cookie_key}" було додано успішно.', 'success')

            if 'delete_cookie' in request.form:
                cookie_key = request.form['cookie_key']
                if cookie_key in user_cookies:
                    response = make_response(redirect(url_for('info')))
                    response.delete_cookie(cookie_key)
                    deleted_value = user_cookies.pop(cookie_key)
                    flash(f'Cookie "{cookie_key}" зі значенням "{deleted_value}" було видалено.', 'success')

            if 'change_password' in request.form:
                new_password = request.form['new_password']
                users[username] = new_password
                with open('app/users.json', 'w') as users_file:
                    json.dump(users, users_file)
                flash('Пароль було змінено успішно.', 'success')

        return render_template('info.html', username=username, cookies=cookies, message=message)
    else:
        flash('Будь ласка, увійдіть для доступу до цієї сторінки', 'error')
        return redirect(url_for('login'))
    
# Додавання ендпоінту для видалення кукі
@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    cookie_key = request.form['cookie_key']
    if cookie_key in user_cookies:
        deleted_value = user_cookies.pop(cookie_key)  # Видаляємо кукі зі словника
        message = f'Кукі "{cookie_key}" зі значенням "{deleted_value}" було видалено.'
        flash(message, 'success')
    return redirect(url_for('info'))
# Добавьте обработку выхода
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Выход выполнен успешно', 'success')
    return redirect(url_for('login'))

my_skills = [
    "Навик ходити",
    "Навик їсти",
    "Навик спати",
    "Навик читати",]

@app.route('/skills')
@app.route('/skills/<int:id>')
def display_skills(id=None):
    if id is not None:
        # Якщо передано id, відобразіть навичку зі списку за цим id
        if 0 <= id < len(my_skills):
            skill = my_skills[id]
            return render_template("skills.html", skills=[skill])
        else:
            return "Немає навички з таким id"
    else:
        # Якщо id не передано, відобразіть всі навички і їх загальну кількість
        total_skills = len(my_skills)
        return render_template("skills.html", skills=my_skills, total=total_skills)

@app.route('/tables')
def tables():
    return render_template("tables.html")
@app.route('/skills')
def skills():
    return render_template("skills.html")
@app.route("/")
def index():
    return render_template("home.html")

@app.route('/home')
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

@app.route('/post/')
@app.route('/post/<int:idx>')
def post(idx=None):
    if idx is not None:
        return render_template("post.html", posts=posts, idx=idx)
    else:
        return render_template("posts.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/main')
def main():
    return redirect(url_for("home"))


@app.route('/query', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        method = request.method
    else:
        name = request.args.get("name")
        password = request.args.get("password")
        method = request.method
    return render_template("my_form.html", name=name, password=password, method=method)
@app.context_processor
def utility_processor():
    os_info = os.name  
    user_agent = request.headers.get("User-Agent")  
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

    return dict(os_info=os_info, user_agent=user_agent, current_time=current_time)



if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)