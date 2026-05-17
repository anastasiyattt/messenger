from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# <===========Создание базы данных===========> #
def get_db(): # Соединение с бд
    return sqlite3.connect('messenger.db')


def query_db(query, args=(), one=False):
    with get_db() as conn:
        c = conn.cursor()
        c.execute(query,args)
        result = c.fetchall()
        return result[0] if(one and result) else result

def init_db():
    with get_db() as conn:
       c = conn.cursor()
       c.executescript('''
       CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);
       CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT, from_user TEXT NOT NULL, to_user TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, is_read INEGER DEFAULT 0);
       ''') 
init_db()

# <===========Пути которые наш сервер будет обслуживать===========> #

@app.route('/',methods=['GET','POST'])
def login():
   if request.method == 'POST':
       action = request.form.get('action')
       username = request.form['username']
       password = request.form['password']
       if action == 'login':
           user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', (username,password),one=True)
           if user:
               session['user'] = username
               return redirect(url_for('chats'))
        elif action == 'register':
            try:
                with get_db() as conn:
                    conn.execute('INSERT INTO users(username,password) VALUES (?,?)', (username,password))
                    session['user'] = username
                    return redirect(url_for('chats'))
            except sqlite3.IntegrityError:
                pass 
            return render_template('login.html')




@app.route('/chats')
def chats():
    pass

@app.route('/chat/<username>')
def chat(username):
    pass

@app.route('/send', methods=['POST'])
def send():
    if 'user' not in session:
        return redirect(url_for('login'))
    if content.strip():
        with get_db() as conn:  
            conn.execute('''
            INSERT INTO messages (from_user,to_user,content,is_read) VALUES(?,?,?,0)
            ''',session['user'],to_user, content)
            return redirect(url_for('chat'),username=to_user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# <===========Запуск сервера из файла===========> #
if __name__ == '__main__':
    app.run(debug=True)