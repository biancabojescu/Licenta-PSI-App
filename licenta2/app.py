import os
import psycopg2
from dotenv import load_dotenv
from flask import g, Flask, render_template

load_dotenv()
app = Flask(__name__)


@app.before_request
def before_request():
    g.db = psycopg2.connect(os.getenv("DATABASE_URL"))


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()
