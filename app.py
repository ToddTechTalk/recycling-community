from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT,
                user_name TEXT,
                timestamp DATETIME
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY,
                post_id INTEGER,
                content TEXT,
                user_name TEXT,
                timestamp DATETIME,
                FOREIGN KEY(post_id) REFERENCES posts(id)
            )
        ''')
    print("Database initialized")

# Index route
@app.route('/')
def index():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM posts')
        posts = cur.fetchall()
        post_replies = {}
        for post in posts:
            cur.execute('SELECT * FROM replies WHERE post_id = ?', (post[0],))
            post_replies[post[0]] = cur.fetchall()
    return render_template('index.html', posts=posts, post_replies=post_replies)

# Route for adding a new post
@app.route('/add', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    user_name = request.form['user_name']
    timestamp = datetime.now()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO posts (title, content, user_name, timestamp) VALUES (?, ?, ?, ?)', (title, content, user_name, timestamp))
        conn.commit()
    return redirect(url_for('index'))

# Route for adding a reply to a post
@app.route('/reply/<int:post_id>', methods=['POST'])
def add_reply(post_id):
    content = request.form['content']
    user_name = request.form['user_name']
    timestamp = datetime.now()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO replies (post_id, content, user_name, timestamp) VALUES (?, ?, ?, ?)', (post_id, content, user_name, timestamp))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
