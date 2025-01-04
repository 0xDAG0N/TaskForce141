"""
Enhanced Task Manager Application
"""

import sql
from art import *
from termcolor import colored
import inquirer
from prettytable import PrettyTable
import sys
import time
from playsound import playsound
from threading import Thread, Event
import pygame


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
    actions = [
        "Create User", "Update User", "Delete User", 
        "Fetch User", "Fetch All Users", "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="User Operations", choices=actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create User":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            sql.create_user(name, email)
            notify_user("User created!")
        elif action == "Update User":
            user_id = int(input("Enter user id: "))
            name = input("Enter new user name: ")
            email = input("Enter new user email: ")
            sql.update_user(user_id, name, email)
            notify_user("User updated!")
        elif action == "Delete User":
            user_id = int(input("Enter user id: "))
            sql.delete_user(user_id)
            notify_user("User deleted!")
        elif action == "Fetch User":
            user_id = int(input("Enter user id: "))
            user = sql.read_user(user_id)
            table_printer(user, ['ID', 'Name', 'Email'])
        elif action == "Fetch All Users":
            users = sql.read_users()
            table_printer(users, ['ID', 'Name', 'Email'])

# User Details Operations
def user_details_operations():
    actions = [
        "Create User Details", "Update User Details", 
        "Delete User Details", "View User Details", 
        "Fetch All User Details", "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="User Details Operations", choices=actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create User Details":
            phone = input("Enter phone number: ")
            preferences = input("Enter preferences: ")
            address = input("Enter address: ")
            sql.create_user_details(phone, preferences, address)
            notify_user("User details created!")
        elif action == "Update User Details":
            user_id = int(input("Enter user id: "))
            phone = input("Enter new phone number: ")
            preferences = input("Enter new preferences: ")
            address = input("Enter new address: ")
            sql.update_user_details(user_id, phone, preferences, address)
            notify_user("User details updated!")
        elif action == "Delete User Details":
            user_id = int(input("Enter user id: "))
            sql.delete_user_details(user_id)
            notify_user("User details deleted!")
        elif action == "View User Details":
            user_id = int(input("Enter user id: "))
            user_details = sql.read_user_details(user_id)
            table_printer(user_details, ['User ID', 'Phone', 'Preferences', 'Address'])
        elif action == "Fetch All User Details":
            users_details = sql.read_users_details()
            table_printer(users_details, ['User ID', 'Phone', 'Preferences', 'Address'])

# Task Operations
def task_operations():
    actions = [
        "Create Task", "Update Task", "Delete Task", 
        "Fetch Task", "Fetch All Tasks", "Mark Task as Complete", 
        "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="Task Operations", choices=actions)])['action']
        if action == "Back to Main Menu":
            break

        elif action == "Create Task":
            user_id = int(input("Enter user id: "))
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            status = input("Enter task status: ")
            sql.create_task(user_id, description, due_date, status)
            notify_user("Task created!")

        elif action == "Update Task":
            task_id = int(input("Enter task id: "))
            user_id = int(input("Enter new user id: "))
            description = input("Enter new task description: ")
            due_date = input("Enter new due date (YYYY-MM-DD): ")
            status = input("Enter new task status: ")
            sql.update_task(user_id, description, due_date, status, task_id)
            notify_user("Task updated!")

        elif action == "Delete Task":
            task_id = int(input("Enter task id: "))
            sql.delete_task(task_id)
            notify_user("Task deleted!")

        elif action == "Fetch Task":
            task_id = int(input("Enter task id: "))
            task = sql.read_task(task_id)
            table_printer(task, ['Task ID', 'User ID', 'Description', 'Due Date', 'Status'])

        elif action == "Fetch All Tasks":
            tasks = sql.read_tasks()
            table_printer(tasks, ['Task ID', 'User ID', 'Description', 'Due Date', 'Status'])

        elif action == "Mark Task as Complete":
            task_id = int(input("Enter task id: "))
            sql.mark_task_as_complete(task_id)
            notify_user("Task marked as complete!")

# Tag Operations
def tag_operations():
    actions = [
        "Create Tag", "Update Tag", "Delete Tag",
        "Fetch Tag", "Fetch All Tags", "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="Tag Operations", choices=actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create Tag":
                name = input("Enter tag name: ")
                sql.create_tag(name)
                notify_user("Tag created!")

        elif action == "Update Tag":
            tag_id = int(input("Enter tag id: "))
            name = input("Enter new tag name: ")
            sql.update_tag(tag_id, name)
            notify_user("Tag updated!")

        elif action == "Delete Tag":
            tag_id = int(input("Enter tag id: "))
            sql.delete_tag(tag_id)
            notify_user("Tag deleted!")

        elif action == "Fetch Tag":
            tag_id = int(input("Enter tag id: "))
            tag = sql.read_tag(tag_id)
            table_printer(tag, ['Tag ID', 'Name'])

        elif action == "Fetch All Tags":
            tags = sql.read_tags()
            table_printer(tags, ['Tag ID', 'Name'])

# Task-Tag Relations Operations
def task_tag_relations_operations():
    actions = [
        "Create Task Tag Relation", "Fetch Tags for Task",
        "Fetch Tasks for Tag", "remove_tag_from_task",
        "Back to Main Menu"
    ]
    while True:
        action = inquirer.prompt([inquirer.List("action", message="Tag Operations", choices=actions)])['action']
        if action == "Back to Main Menu":
            break
        elif action == "Create Task Tag Relation":
            task_id = int(input("Enter task id: "))
            tag_id = int(input("Enter tag id: "))
            sql.create_task_tag_relation(task_id, tag_id)
            notify_user("Tag assigned to task!")

        elif action == "Fetch Tags for Task":
            task_id = int(input("Enter task id: "))
            tags = sql.read_tags_for_task(task_id)
            print(tags)
            table = PrettyTable(['Task ID', 'Tag ID', 'Tag Name'])
            for tag in tags:
                tag_details = sql.read_tag(tag)
                table.add_row([task_id, tag_details[0], tag_details[1]])
            print(table)

        elif action == "Fetch Tasks for Tag":
            tag_id = int(input("Enter tag id: "))
            tasks = sql.read_tasks_for_tag(tag_id)
            
            table = PrettyTable(['Task ID', 'User ID', 'Description', 'Due Date', 'Status'])
            for task in tasks:
                task_details = sql.read_task(task)
                table.add_row([task_details[0], task_details[1], task_details[2], task_details[3], task_details[4]])
            print(table)

        elif action == "remove_tag_from_task":
            task_id = int(input("Enter task id: "))
            sql.remove_tag_from_task(task_id)
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
        actions = [
            "User Operations", "User Details Operations", 
            "Task Operations", "Tag Operations", 
            "Task-Tag Relations Operations", "Exit"
        ]
        action = inquirer.prompt([inquirer.List("action", message="Main Menu", choices=actions)])['action']
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
