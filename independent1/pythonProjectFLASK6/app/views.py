from flask import request, render_template, redirect, url_for, make_response, session
from app import app
from data import posts


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

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

#http://127.0.0.1:5000/query?name=admin&password=1234


@app.route('/query', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if name == "admin" and password == "1234":
            return redirect(url_for("home"))
    return render_template("my_form.html")

#http://127.0.0.1:5000/setcookie?userId=101
@app.route('/setcookie', methods=["GET"])
def cookie():
    if request.args.get("userId"):
        user_value = request.args.get("userId") #101
        session["userId"] = user_value
        resp = make_response(f"Hi, set cookie {user_value}")
        resp.set_cookie("userId", user_value)
        return resp
    print(session.get("userId"))
    userId = request.cookies.get("userId")
    if not userId:
        userId = session.get("userId")

    return render_template("read_cookie.html", userID=userId)

@app.route('/clearcookie', methods=["GET"])
def clear_cookie():
    resp = make_response(f"Hi, delete  ")
    # resp.set_cookie("userId", "", expires=0)
    resp.delete_cookie("userId")
    return resp

@app.route('/clearsession', methods=["GET"])
def clear_session():
    session.pop("userId")
    return redirect(url_for("home"))