from flask import Flask, request, render_template, redirect, url_for
from data import posts
import os 
from datetime import datetime

app = Flask(__name__)

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
