import sqlite3
import create_db


def get_connection():
    """
    Function to connect to the database and enable foreign key constraints.
    """
    conn = sqlite3.connect('todo_list.db')
    conn.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key constraints
    return conn

# ====================== User ======================

def read_users():
    """
    Read all users from the Users table.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM Users")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error reading users: {e}")
        return []

def read_user(user_id):
    """
    Read a specific user from the Users table based on user_id.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error reading user: {e}")
        return None

def create_user(name, email):
    """
    Create a new user in the Users table."""
    try:
        with get_connection() as conn:
            cursor = conn.execute("INSERT INTO Users (name, email) VALUES (?, ?)", (name, email))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating user: {e}")
        return None

def update_user(user_id, name, email):
    """
    Update user details in the Users table based on user"""
    try:
        with get_connection() as conn:
            conn.execute("UPDATE Users SET name = ?, email = ? WHERE user_id = ?", (name, email, user_id))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating user: {e}")

def delete_user(user_id):
    """
    Delete user from the Users table based on user_id."""
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Cannot delete user due to associated records: {e}")
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")

# ====================== UserDetails ======================

def create_user_details(phone, preferences, address):
    """
    Create user details in the UserDetails table based on user_id."""
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO UserDetails (phone, preferences, address) VALUES (?, ?, ?)",
                (phone, preferences, address)
            )
            conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: Foreign key constraint failed - {e}")
    except sqlite3.Error as e:
        print(f"Error creating user details: {e}")

def read_user_details(user_id):
    """
    Read user details from the UserDetails table based on user_id."""
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM UserDetails WHERE user_id = ?", (user_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error reading user details: {e}")
        return None
    
def read_users_details():
    """
    Read all user details from the UserDetails table."""
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM UserDetails")
            users_details = cursor.fetchall()
            return users_details
    except sqlite3.Error as e:
        print(f"Error reading user details: {e}")
        return None

def update_user_details(user_id, phone, preferences, address):
    """
    Update user details in the UserDetails table based on user_id."""
    try:
        with get_connection() as conn:
            conn.execute("UPDATE UserDetails Set phone = ?, preferences = ?, address = ? WHERE user_id = ?", (phone, preferences, address, user_id))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating user details: {e}")


def delete_user_details(user_id):
    """
    Delete user details from the UserDetails table based on user_id.

    Parameters:
    user_id (int): The ID of the user to be deleted.

    Returns:
    None
    """
    try:
        conn = get_connection()
        conn.execute("DELETE FROM UserDetails WHERE user_id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# ====================== Tasks ======================

def create_task(user_id, description, due_date, status):
    """
    Create a new task in the Tasks table
    """
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO Tasks (user_id, description, due_date, status) VALUES (?, ?, ?, ?)",
                ( user_id, description, due_date, status)
            )
            conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: Foreign key constraint failed - {e}")
    except sqlite3.Error as e:
        print(f"Error creating task: {e}")

def read_tasks():
    """
    Read all tasks from the Tasks table."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM Tasks")
        tasks = cursor.fetchall()
    return tasks

def read_task(task_id):
    """
    Read a specific task from the Tasks table based on task_id."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM Tasks WHERE task_id = ?",(task_id,))
        task = cursor.fetchone()
    return task

def update_task(user_id,description, due_date, status, task_id):
    """
    Update a task in the Tasks table based on task_id."""
    with get_connection() as conn:
        conn.execute("UPDATE Tasks SET user_id = ?, description = ?, due_date = ?, status = ? WHERE task_id = ?", (user_id, description, due_date, status, task_id))
        conn.commit()

def delete_task(task_id):
    """
    Delete a task from the Tasks table based on task_id."""
    with get_connection() as conn:
        conn.execute("DELETE FROM Tasks WHERE task_id = ?", (task_id,))
        conn.commit()

def mark_task_as_complete(task_id):
    """
    Mark a task as complete in the Tasks table based on task_id."""
    with get_connection() as conn:
        conn.execute("UPDATE Tasks SET status = 'Complete' WHERE task_id = ?", (task_id,))
        conn.commit()

# ====================== Tags ======================

def create_tag(name):
    """
    Create a new tag in the Tags table.

    Parameters:
    name (str): The name of the tag to be created.

    Returns:
    None
    """
    try:
        conn = get_connection()
        conn.execute("INSERT INTO Tags (name) VALUES (?)", (name,))
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def read_tags():
    """
    Read all tags from the Tags table.

    Returns:
    list: A list of tuples containing tag details.
    """
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM Tags")
        tags = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        tags = []
    finally:
        conn.close()
    return tags

def read_tag(tag_id):
    """
    Retrieve a tag by tag_id from the Tags table.

    Parameters:
    tag_id (int): The ID of the tag.

    Returns:
    tuple: A tuple representing the tag (tag_id, tag_name) or None if not found.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM Tags WHERE tag_id = ?", (tag_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error reading tag: {e}")
        return None

def update_tag(tag_id, name):
    """
    Update a tag in the Tags table based on tag_id."""
    with get_connection() as conn:
        conn.execute("UPDATE Tags Set name = ? WHERE tag_id = ?", (name, tag_id))
        conn.commit()

def delete_tag(tag_id):
    """
    Delete a tag from the Tags table based on tag_id."""
    with get_connection() as conn:
        conn.execute("DELETE FROM Tags WHERE tag_id = ?", (tag_id,))
        conn.commit()

# ====================== TaskTags ======================

def create_task_tag_relation(task_id, tag_id):
    """
    Create a relation between a task and a tag in the TaskTags table."""
    with get_connection() as conn:
        task = read_task(task_id)[2]
        tag = read_tag(tag_id)[1]
        conn.execute("INSERT INTO TaskTags (task_id, tag_id, task, tag) VALUES (?, ?, ?, ?)", (task_id, tag_id, task, tag))
        conn.commit()

def read_tags_for_task(task_id):
    """
    Read all tags associated with a task from the TaskTags table."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM TaskTags WHERE task_id = ?",(task_id,))
        tags = cursor.fetchall()
    return [tag[2] for tag in tags]

def read_tasks_for_tag(tag_id):
    """
    Read all tasks associated with a tag from the TaskTags table."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM TaskTags WHERE tag_id = ?",(tag_id,))
        tasks = cursor.fetchall()
    return [task[0] for task in tasks]

def remove_tag_from_task(task_id):
    """
    Remove all tags associated with a task in the TaskTags table."""
    with get_connection() as conn:
        conn.execute("DELETE FROM TaskTags WHERE task_id = ? ", (task_id,))
        conn.commit()


    