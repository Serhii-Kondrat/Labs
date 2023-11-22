from flask import Flask, request, render_template, redirect, url_for, session, flash, make_response
from data import posts
import os 
from datetime import datetime
import json
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
user_cookies = {}

# Загрузка данных о пользователях из JSON-файла
with open('app/users.json', 'r') as users_file:
    users = json.load(users_file)
app.secret_key = '123456'


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

            if remember:
                # Якщо вибрано опцію "Remember me", можна зберегти в сесію
                session.permanent = True  # Зробити сесію перманентною

            return redirect(url_for('info'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)


   

# Создание страницы "info" с информацией для авторизованных пользователей
@app.route('/info', methods=['GET', 'POST'])
def info():
    if 'username' in session:
        username = session['username']
        message = None
        cookies = user_cookies

        if request.method == 'POST':
            if 'add_cookie' in request.form:
                cookie_key = request.form['cookie_key']
                cookie_value = request.form['cookie_value']
                cookie_expiry = int(request.form['cookie_expiry'])
                
                # Додавання нового кукі до словника
                user_cookies[cookie_key] = cookie_value

                response = make_response(redirect(url_for('info')))
                response.set_cookie(cookie_key, cookie_value, max_age=cookie_expiry)
                message = f'Кукі "{cookie_key}" було додано успішно.'

            if 'delete_cookie' in request.form:
                cookie_key = request.form['cookie_key']
                if cookie_key in user_cookies:
                    response = make_response(redirect(url_for('info')))
                    response.delete_cookie(cookie_key)
                    deleted_value = user_cookies.pop(cookie_key)  # Видаляємо кукі зі словника
                    message = f'Кукі "{cookie_key}" зі значенням "{deleted_value}" було видалено.'
            if 'change_password' in request.form:
                new_password = request.form['new_password']
                users[username] = new_password
                with open('app/users.json', 'w') as users_file:
                    json.dump(users, users_file)

                message = 'Пароль було змінено успішно.'

        return render_template('info.html', username=username, cookies=cookies, message=message)
    else:
        flash('Пожалуйста, войдите для доступа к этой странице', 'error')
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


#http://127.0.0.1:5000/query?name=admin&password=1234 or from form by post
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
    os_info = os.name  # Get the operating system name
    user_agent = request.headers.get("User-Agent")  # Get the user-agent from the request
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time

    return dict(os_info=os_info, user_agent=user_agent, current_time=current_time)



if __name__ == '__main__':
    app.run(debug=True)