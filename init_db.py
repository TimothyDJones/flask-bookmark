import sqlite3

connection = sqlite3.connect('bookmarks.db')

with open('db_schema.sql') as f:
	connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO bookmarks (url, title, description) VALUES (?, ?, ?)",
	('https://google.com', 'Google', 'A popular search engine.'))
cur.execute("INSERT INTO bookmarks (url, title, description) VALUES (?, ?, ?)",
	('https://duckduckgo.com', 'DuckDuckGo', 'A privacy-focused search engine.'))

# Note: Must use comma in value list to make it a tuple.  See https://stackoverflow.com/a/16856730 for details.
cur.execute("INSERT INTO tags (name) VALUES (?)",
	('search',))
cur.execute("INSERT INTO tags (name) VALUES (?)",
	('privacy',))

connection.commit()
connection.close()
