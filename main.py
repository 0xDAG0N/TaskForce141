"""
Enhanced Task Manager Application
"""

import sql
import sqlite3
from art import *
from termcolor import colored
import inquirer
from prettytable import PrettyTable
import sys
import time
from playsound import playsound
from threading import Thread, Event
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame  # it is important to import pygame after that


# Utility Functions
def notify_user(message):
    art = text2art(message)
    print(colored(art, 'green'))

def table_printer(data, columns):
    table = PrettyTable(columns)
    if type(data) == tuple:
        table.add_row(data)
    else:
        for row in data:
            table.add_row(row)
    print(table)

# Initialize pygame mixer
pygame.mixer.init()

def play_sound(stop_event):
    pygame.mixer.music.load('media/typing.wav')
    pygame.mixer.music.play(-1)  # Loop the sound indefinitely
    while not stop_event.is_set():
        time.sleep(0.1)  # Check the stop event periodically
    pygame.mixer.music.stop()

def typing_effect_with_sound(text, delay=0.05):
    stop_event = Event()
    sound_thread = Thread(target=play_sound, args=(stop_event,))
    sound_thread.start()
    
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    
    stop_event.set()
    sound_thread.join()  # Ensure the sound thread finishes before exiting the function
    print()

# User Operations
def user_operations():
    user_actions = [
        "Create User", "Update User", "Delete User", 
        "Fetch User", "Fetch All Users", "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="User Operations", choices=user_actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create User":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            try:
                sql.create_user(name, email)
            except sqlite3.Error as e:
                print(f"Error creating user: {e}")
            else:
                notify_user("User created!")
        elif action == "Update User":
            try:
                user_id = int(input("Enter user id: "))
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
                continue  # Go back to the beginning of the loop
            name = input("Enter new user name: ")
            email = input("Enter new user email: ")
            try:
                sql.update_user(user_id, name, email)
            except sqlite3.Error as e:
                print(f"Error updating user: {e}")
            else:
                notify_user("User updated!")
        elif action == "Delete User":
            try:
                user_id = int(input("Enter user id: "))
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
                continue  # Go back to the beginning of the loop
            try:
                sql.delete_user(user_id)
            except sqlite3.Error as e:
                print(f"Error deleting user: {e}")
            else:
                notify_user("User deleted!")
        elif action == "Fetch User":
            try:
                user_id = int(input("Enter user id: "))
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
                continue  # Go back to the beginning of the loop
            user = sql.read_user(user_id)
            if user:
                table_printer(user, ['ID', 'Name', 'Email'])
            else:
                print(f"No user found with ID {user_id}")
        elif action == "Fetch All Users":
            users = sql.read_users()
            if users:
                table_printer(users, ['ID', 'Name', 'Email'])
            else:
                print("No users found.")

# User Details Operations
def user_details_operations():
    user_details_actions = [
        "Create User Details", "Update User Details", 
        "Delete User Details", "View User Details", 
        "Fetch All User Details", "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="User Details Operations", choices=user_details_actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create User Details":
            try:
                user_id = int(input("Enter user id: "))
                phone = input("Enter phone number: ")
                preferences = input("Enter preferences: ")
                address = input("Enter address: ")
                sql.create_user_details(user_id, phone, preferences, address)  # Assuming create_user_details takes user_id
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
            except sqlite3.Error as e:
                print(f"Error creating user details: {e}")
            else:
                notify_user("User details created!")
        elif action == "Update User Details":
            try:
                user_id = int(input("Enter user id: "))
                phone = input("Enter new phone number: ")
                preferences = input("Enter new preferences: ")
                address = input("Enter new address: ")
                sql.update_user_details(user_id, phone, preferences, address)
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
            except sqlite3.Error as e:
                print(f"Error updating user details: {e}")
            else:
                notify_user("User details updated!")
        elif action == "Delete User Details":
            try:
                user_id = int(input("Enter user id: "))
                sql.delete_user_details(user_id)
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
            except sqlite3.Error as e:
                print(f"Error deleting user details: {e}")
            else:
                notify_user("User details deleted!")
        elif action == "View User Details":
            try:
                user_id = int(input("Enter user id: "))
                user_details = sql.read_user_details(user_id)
                if user_details:
                    table_printer(user_details, ['User ID', 'Phone', 'Preferences', 'Address'])
                else:
                    print(f"No user details found for user ID {user_id}")
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
        elif action == "Fetch All User Details":
            users_details = sql.read_users_details()
            if users_details:
                table_printer(users_details, ['User ID', 'Phone', 'Preferences', 'Address'])
            else:
                print("No user details found.")

# Task Operations
def task_operations():
    task_actions = [
        "Create Task", "Update Task", "Delete Task", 
        "Fetch Task", "Fetch All Tasks", "Mark Task as Complete", 
        "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="Task Operations", choices=task_actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create Task":
            try:
                user_id = int(input("Enter user id: "))
                description = input("Enter task description: ")
                due_date = input("Enter due date (YYYY-MM-DD): ")
                status = input("Enter task status: ")
                sql.create_task(user_id, description, due_date, status)
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
            except sqlite3.Error as e:
                print(f"Error creating task: {e}")
            else:
                notify_user("Task created!")
        elif action == "Update Task":
            try:
                task_id = int(input("Enter task id: "))
                user_id = int(input("Enter new user id: "))
                description = input("Enter new task description: ")
                due_date = input("Enter new due date (YYYY-MM-DD): ")
                status = input("Enter new task status: ")
                sql.update_task(user_id, description, due_date, status, task_id)
            except ValueError:
                print("Invalid input. Please enter integers for task ID and user ID.")
            except sqlite3.Error as e:
                print(f"Error updating task: {e}")
            else:
                notify_user("Task updated!")
        elif action == "Delete Task":
            try:
                task_id = int(input("Enter task id: "))
                sql.delete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter an integer for task ID.")
            except sqlite3.Error as e:
                print(f"Error deleting task: {e}")
            else:
                notify_user("Task deleted!")
        elif action == "Fetch Task":
            try:
                task_id = int(input("Enter task id: "))
                task = sql.read_task(task_id)
                if task:
                    table_printer(task, ['Task ID', 'User ID', 'Description', 'Due Date', 'Status'])
                else:
                    print(f"No task found with ID {task_id}")
            except ValueError:
                print("Invalid input. Please enter an integer for task ID.")
        elif action == "Fetch All Tasks":
            tasks = sql.read_tasks()
            if tasks:
                table_printer(tasks, ['Task ID', 'User ID', 'Description', 'Due Date', 'Status'])
            else:
                print("No tasks found.")
        elif action == "Mark Task as Complete":
            try:
                task_id = int(input("Enter task id: "))
                sql.mark_task_as_complete(task_id)
            except ValueError:
                print("Invalid input. Please enter an integer for task ID.")
            except sqlite3.Error as e:
                print(f"Error marking task as complete: {e}")
            else:
                notify_user("Task marked as complete!")

# Tag Operations
def tag_operations():
    tag_actions = [
        "Create Tag", "Update Tag", "Delete Tag",
        "Fetch Tag", "Fetch All Tags", "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="Tag Operations", choices=tag_actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create Tag":
            try:
                name = input("Enter tag name: ")
                sql.create_tag(name)
            except sqlite3.Error as e:
                print(f"Error creating tag: {e}")
            else:
                notify_user("Tag created!")
        elif action == "Update Tag":
            try:
                tag_id = int(input("Enter tag id: "))
                name = input("Enter new tag name: ")
                sql.update_tag(tag_id, name)
            except ValueError:
                print("Invalid input. Please enter an integer for tag ID.")
            except sqlite3.Error as e:
                print(f"Error updating tag: {e}")
            else:
                notify_user("Tag updated!")
        elif action == "Delete Tag":
            try:
                tag_id = int(input("Enter tag id: "))
                sql.delete_tag(tag_id)
            except ValueError:
                print("Invalid input. Please enter an integer for tag ID.")
            except sqlite3.Error as e:
                print(f"Error deleting tag: {e}")
            else:
                notify_user("Tag deleted!")
        elif action == "Fetch Tag":
            try:
                tag_id = int(input("Enter tag id: "))
                tag = sql.read_tag(tag_id)
                if tag:
                    table_printer(tag, ['Tag ID', 'Name'])
                else:
                    print(f"No tag found with ID {tag_id}")
            except ValueError:
                print("Invalid input. Please enter an integer for tag ID.")
        elif action == "Fetch All Tags":
            tags = sql.read_tags()
            if tags:
                table_printer(tags, ['Tag ID', 'Name'])
            else:
                print("No tags found.")

# Task-Tag Relations Operations
def task_tag_relations_operations():
    task_tag_actions = [
        "Create Task Tag Relation", "Fetch Tags for Task",
        "Fetch Tasks for Tag", "remove_tag_from_task",
        "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="Tag Operations", choices=task_tag_actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create Task Tag Relation":
            try:
                task_id = int(input("Enter task id: "))
                tag_id = int(input("Enter tag id: "))
                sql.create_task_tag_relation(task_id, tag_id)
            except ValueError:
                print("Invalid input. Please enter integers for task ID and tag ID.")
            except sqlite3.Error as e:
                print(f"Error assigning tag to task: {e}")
            else:
                notify_user("Tag assigned to task!")
        elif action == "Fetch Tags for Task":
            try:
                task_id = int(input("Enter task id: "))
                tags = sql.read_tags_for_task(task_id)
                if tags:
                    table = PrettyTable(['Task ID', 'Tag ID', 'Tag Name'])
                    for tag in tags:
                        tag_details = sql.read_tag(tag)
                        table.add_row([task_id, tag_details[0], tag_details[1]])
                    print(table)
                else:
                    print(f"No tags found for task ID {task_id}")
            except ValueError:
                print("Invalid input. Please enter an integer for task ID.")
        elif action == "Fetch Tasks for Tag":
            try:
                tag_id = int(input("Enter tag id: "))
                tasks = sql.read_tasks_for_tag(tag_id)
                if tasks:
                    table = PrettyTable(['Task ID', 'User ID', 'Description', 'Due Date', 'Status'])
                    for task in tasks:
                        task_details = sql.read_task(task)
                        table.add_row([task_details[0], task_details[1], task_details[2], task_details[3], task_details[4]])
                    print(table)
                else:
                    print(f"No tasks found for tag ID {tag_id}")
            except ValueError:
                print("Invalid input. Please enter an integer for tag ID.")
        elif action == "remove_tag_from_task":
            try:
                task_id = int(input("Enter task id: "))
                sql.remove_tag_from_task(task_id)
            except ValueError:
                print("Invalid input. Please enter an integer for task ID.")
            except sqlite3.Error as e:
                print(f"Error unassigning tag from task: {e}")
            else:
                notify_user("Tag unassigned from task!")

# Main Function
def main():
    notify_user("Task Force 141")
    typing_effect_with_sound(">>> Welcome, Operator, to TaskForce141 <<<")
    typing_effect_with_sound("Mission Objective: Dominate your tasks with precision and speed.")
    typing_effect_with_sound("Created by Dagon, for those who never back down.")
    typing_effect_with_sound("Intel HQ: https://github.com/0xDAG0N/TaskForce141")
    print()

    while True:
        main_actions = [
            "User Operations", "User Details Operations", 
            "Task Operations", "Tag Operations", 
            "Task-Tag Relations Operations", "Exit"
        ]
        action = inquirer.prompt([inquirer.List("action", message="Main Menu", choices=main_actions)])['action']
        if action == "Exit":
            print(text2art("Goodbye!"))
            break
        elif action == "User Operations":
            user_operations()
        elif action == "User Details Operations":
            user_details_operations()
        elif action == "Task Operations":
            task_operations()
        elif action == "Tag Operations":
            tag_operations()
        elif action == "Task-Tag Relations Operations":
            task_tag_relations_operations()

if __name__ == '__main__':
    main()