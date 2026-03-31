import sqlite3, sys, os

file = sys.argv[1]
tags = sys.argv[2]

conn = sqlite3.connect('../data/photos.db')
c = conn.cursor()

c.execute("INSERT INTO photos (filename, tags) VALUES (?, ?)",
          (os.path.basename(file), tags))

conn.commit()
conn.close()

print("Inserted", file)
