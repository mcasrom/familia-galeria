import sqlite3
conn = sqlite3.connect('../data/photos.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS photos (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 filename TEXT,
 tags TEXT
)
''')

conn.commit()
conn.close()
print("DB initialized")
