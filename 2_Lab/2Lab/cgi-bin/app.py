from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    # Отримуємо поточне значення лічильника з cookies
    count = int(request.cookies.get('form_count', 0))
    return render_template("form.html", count=count)

@app.route('/result', methods=['POST'])
def result():
    num1 = float(request.form["num1"])
    num2 = float(request.form["num2"])
    result = num1 + num2

    # Отримуємо поточне значення лічильника з cookies
    count = int(request.cookies.get('form_count', 0))
    count += 1

    # Встановлюємо нове значення лічильника в cookies
    resp = make_response(render_template('form.html', result=result, count=count))
    resp.set_cookie('form_count', str(count))
    return resp

@app.route('/delete_cookies')
def delete_cookies():
    # Видаляємо cookies, встановлюючи їх термін дії на минулий час і встановлюємо лічильник на 0
    resp = make_response(render_template('form.html', count=0))
    resp.set_cookie('form_count', '0', expires=0)
    return resp

if __name__ == "__main__":
    app.run(debug=True)
