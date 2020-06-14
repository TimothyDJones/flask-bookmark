# app.py
import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort

app = Flask(__name__)

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
