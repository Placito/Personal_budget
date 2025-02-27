# Personal_budget

    ## Overview

    Personal_budget is a Python application designed to help users manage their personal finances by entering monthly expenses, organizing data, calculating total expenses, determining the average expenses per category, and identifying the largest and smallest expenses. This application uses PyQt5 for the graphical user interface (GUI) and SQLAlchemy with SQLite as the database.


    ## Features

    * Enter monthly expenses.
    * Organize expenses by category.
    * Calculate the total expenses.
    * Find average expenses per category.
    * Identify the largest and smallest expenses.

    ## Installation

    Prerequisites
        To run this application, you need Python 3 and pip installed on your machine.

    1. Install Python 3
    2. Install pip (Python package manager): pip is usually installed with Python. If not, you can install it following this guide.
    
    ## Installing Required Packages
    The application uses PyQt5 for the UI and SQLAlchemy with Alembic for database migrations. You can install these dependencies by running the following command in your terminal:

    ```bash
    pip install -r requirements.txt
    ```

    ## Setting Up the Database

    The database for this application uses SQLite, which is a lightweight database included with Python. To set up Alembic for handling database migrations:

    1. Initialize Alembic: In your project directory, run the following command to initialize Alembic:

    ```bash
    alembic init alembic
    ```

    2. Configure Alembic: Update alembic.ini to point to your SQLite database. In the alembic.ini file, change the sqlalchemy.url setting to:

    ```bash
    sqlalchemy.url = sqlite:///dados.db
    ```

    ## Database Migrations with Alembic

        1. Creating and Applying Migrations
        Generate a New Migration
       
        ```bash
        alembic revision --autogenerate -m "migration_name"
        ```

        2. Review the Migration Script
        Review the migration script for any unsupported SQLite commands. Specifically, SQLite does not support ALTER TABLE for adding or removing columns.

        3. Workaround for SQLite
        Create a new table with the updated schema.
        Migrate the data from the old table to the new table.
        Drop the old table and rename the new table.

        4. Apply the Migrations
        To apply the migrations and update the database schema, run:

        ```bash
        alembic upgrade head
        ```

        ## Running the Application
        To run the application, execute the following command:

        ```bash
        python main.py
        ```


