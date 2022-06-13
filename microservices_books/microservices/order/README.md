### Create and activate virtual environment:
```shell
python -m venv .venv
source .venv/bin/activate
```
### Install:
```shell
pip install flask
pip install sqlalchemy flask-sqlalchemy
pip install flask-login
pip install flask-migrate 
```
### Run:
```shell
python app.py
flask run --reload
```
### Token:
```python
import secrets
secrets.token_urlsafe(16)
'yol_voq7'
```
### Migration:
    $ export FLASK_APP=app.py
    $ export FLASK_ENV=development
    $ flask run
    $ flask shell
```shell
export FLASK_APP=app.py
flask db init  # Initialize models (migrations dir)
flask db migrate  # Create database file user.db 
flask db upgrade   # Create table
```

