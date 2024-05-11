import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, g
from db import db_conn
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'cheiaSecreta08.'


@app.route('/')
@app.route('/index')
def index():
    conn, cur = db_conn()
    return render_template('index.html', is_authenticated=session.get('is_authenticated', False))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    conn, cur = db_conn()

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return render_template('register.html', error="Passwords do not match")

    hashed_password = generate_password_hash(password)

    query = """INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"""
    cur.execute(query, (first_name, last_name, email, hashed_password))
    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('login'))


@app.route('/login_user', methods=['POST'])
def login_user():
    conn, cur = db_conn()

    email = request.form['email']
    password = request.form['password']

    cur.execute("SELECT id, password, is_auth FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if user:
        user_id, hashed_password, is_auth = user

        if check_password_hash(hashed_password, password):
            session['user_id'] = user_id
            session['is_authenticated'] = True

            cur.execute("UPDATE users SET is_auth = TRUE WHERE id = %s", (user_id,))
            conn.commit()

            return redirect(url_for('index'))
        else:
            return "Parola incorecta!", 403
    else:
        return "Utilizatorul nu exista!", 404

    cur.close()
    conn.close()


@app.route('/logout')
def logout():
    session.clear()  # Clears the session, logging out the user
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)