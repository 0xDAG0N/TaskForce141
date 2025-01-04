# TaskForce141 ⚡
Effortlessly manage your tasks, organize them with tags, and keep track of user details—all with a powerful yet simple command-line interface.

## About TaskForce141
TaskForce141 is a Python tool designed to help users manage their tasks efficiently. It provides functionalities to create, update, delete, and fetch tasks, tags, and user details using a command-line interface.

- `create_db.py`: Script to create the SQLite database and tables.
- `main.py`: Main application script that provides a command-line interface for managing tasks, tags, and user details.
- `sql.py`: Contains functions to interact with the SQLite database.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/0xDAG0N/TaskForce141
    cd TaskForce141
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

    

3. Create the database:
    ```sh
    python create_db.py
    ```

## Usage

Run the main application:
```sh
python main.py
