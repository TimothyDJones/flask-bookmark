# app.py
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_the_secret_key!'

def get_db_connection():
	conn = sqlite3.connect('bookmarks.db')
	conn.row_factory = sqlite3.Row
	return conn

def get_bookmark(bookmark_id):
	conn = get_db_connection()
	bookmark = conn.execute('SELECT * FROM bookmarks WHERE id = ?',
			(bookmark_id, )).fetchone()
	conn.close()
	if bookmark is None:
		abort(404)
	return bookmark

@app.route("/")
def index():
	conn = get_db_connection()
	bookmarks = conn.execute('SELECT * FROM bookmarks').fetchall()
	conn.close()
	return render_template("index.html", bookmarks=bookmarks)

@app.route("/<int:bookmark_id>")
def bookmark(bookmark_id):
	bookmark = get_bookmark(bookmark_id)
	return render_template('bookmark.html', bookmark=bookmark)

@app.route("/create", methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
		url = request.form['url']
		title = request.form['title']
		description = request.form['description']

		if not url:
			flash_message('URL is required!')
		elif  not title:
			flash_message('Title is required!')
		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO bookmarks (url, title, description) VALUES (?, ?, ?)',
				(url, title, description))
			conn.commit()
			conn.close()
			return redirect(url_for('index'))

	return render_template('create.html')
