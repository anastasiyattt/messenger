from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# <===========Создание базы данных===========> #
def get_db(): # Соединение с бд
    return sqlite3.connect('messenger.db')

def query_db(query, args=(), one=False):
    with get_db() as conn:
        pass

def init_db():
    pass

# <===========Пути которые наш сервер будет обслуживать===========> #

@app.route()
def login():
    pass

@app.route()
def chats():
    pass

@app.route('/chat/<username>')
def chat(username):
    pass

@app.route('/send', methods=['POST'])
def send():
    pass

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# <===========Запуск сервера из файла===========> #
if __name__ == '__main__':
    app.run(debug=True)