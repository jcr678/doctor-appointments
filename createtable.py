
import sqlite3

connection = sqlite3.connect('database.db')

#recreates table and reinitialized with initial values for the table
with open('createtable.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO doctor (firstName, lastName) VALUES (?, ?)",
            ('Julius', 'Hibbert')
            )

cur.execute("INSERT INTO doctor (firstName, lastName) VALUES (?, ?)",
            ('Algernop', 'Krieger')
            )

cur.execute("INSERT INTO doctor (firstName, lastName) VALUES (?, ?)",
            ('Nick', 'Riviera')
            )

connection.commit()
connection.close()
