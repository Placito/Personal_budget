# Personal_budget

This project aims to allow the user to enter their monthly expenses and organize this data. The program must calculate the total expenses, the average expenses per category and identify the largest and smallest expenses. in python


to create this app I use PyQt5 - `pip install PyQt5`

Alembic Migrations Guide
This guide outlines the process of handling database migrations using Alembic for the Personal Budget project, specifically addressing SQLite limitations.

1. Setting Up Alembic
Initialize Alembic: `alembic init alembic`

    1.1. Configure alembic.ini:
        * Update the sqlalchemy.url to point to your database (e.g., sqlite:///dados.db).

    1.2. Define your models in the project's models.py or equivalent.

    1.3. Update alembic/env.py to include model imports and metadata: 
        * `` from your_project.models import Base
             target_metadata = Base.metadata ``

2. Creating and Applying Migrations
Generate a New Migration
2.1.  Create a migration script:

* ` alembic revision --autogenerate -m "migration_name" `

2.2 Review the migration file in alembic/versions/ for unsupported SQLite commands (e.g., ALTER TABLE):

* Unsupported Commands:
    * ALTER TABLE
    * Adding/removing columns

* Workaround:
    * Create a new table with the updated schema.
    * Migrate data from the old table to the new table.
    * Drop the old table and rename the new table.
    * Apply Migrations
    * Run migrations to apply schema changes: ` alembic upgrade head `