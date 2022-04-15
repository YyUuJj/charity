from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', title='Charity')

@app.route("/registration")
def registration():
    return render_template('registration.html', title='Регистрация')

@app.route('/login')
def login():
    return render_template('login.html', title="Вход")

if __name__ == "__main__":
    print("Запускаем сайт...")
    app.run(debug=True)
    print("Сайт отключен...")