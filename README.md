# CRUD test task

## Installation
- `pip3 install pipenv`
- `pipenv install`
- `pipenv run flask db upgrade`
## Running
```
> FLASK_ENV=development pipenv run flask run
```
### Development
- Creating data migration from scratch:
```
pipenv run alembic -c ./migrations/alembic.ini revision -m 'demo data'
```