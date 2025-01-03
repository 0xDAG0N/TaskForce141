import sqlite3

def create_db():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('todo_list.db')
        # Enable foreign key constraints
        conn.execute('PRAGMA foreign_keys = ON;')
        
        # Create Users table
        conn.execute('''   
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT 
            );    
        ''')

        # Create UserDetails table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS UserDetails (
            user_id INTEGER PRIMARY KEY,
            phone TEXT,
            preferences TEXT,
            address TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
            );
        ''')

        # Create Tags table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Tags (
            tag_id INTEGER PRIMARY KEY,
            name TEXT
            );
        ''')

        # Create Tasks table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Tasks (
            task_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            description TEXT,
            due_date DATE,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
            );
        ''')

        # Create TaskTags table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS TaskTags (
            task_id INTEGER,
            task TEXT,
            tag_id INTEGER,
            tag TEXT,
            FOREIGN KEY (task_id) REFERENCES Tasks(task_id),
            FOREIGN KEY (tag_id) REFERENCES Tags(tag_id),
            PRIMARY KEY (task_id, tag_id)
            );
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database created successfully!")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    create_db()
