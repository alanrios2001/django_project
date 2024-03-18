A python-django project.

1. Clone project
2. Install poetry
   ```cmd
   pip install poetry
   ```
3. Install dependencies using poetry
   ```cmd
   poetry install
   ```
4. Create db mysql
5. edit env vars, by creating .secrets.toml file, copy settings.toml and change the values with the data to connect the db.
7. Run migrations in order to create db tables
   ```cmd
   poetry run python manage.py migrate
   ```
8. run server and verify if django is running
   ```cmd
   poetry run python manage.py runserver
   ```
