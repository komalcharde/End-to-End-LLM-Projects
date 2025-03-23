import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("student.db")

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Create the STUDENT table
cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME TEXT,
    CLASS TEXT,
    SECTION TEXT,
    MARKS INTEGER
);
""")

# Insert records into the STUDENT table (only if empty)
cursor.execute("SELECT COUNT(*) FROM STUDENT")
if cursor.fetchone()[0] == 0:  # Avoid duplicate insertions
    student_data = [
        ('Krish', 'cyber', 'A', 90),
        ('Komal', 'data science', 'B', 20),
        ('Kiran', 'cse', 'C', 70),
        ('Krupa', 'electrical', 'A', 30),
        ('Kri', 'data', 'A', 40)
    ]
    cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", student_data)
    connection.commit()

# Display inserted records
cursor.execute("SELECT * FROM STUDENT")
rows = cursor.fetchall()

if rows:
    print("Inserted records:")
    for row in rows:
        print(row)
else:
    print("No data found!")

# Close the connection
connection.close()
