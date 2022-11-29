# How to run

Add .env file and add env variables:
* SECRET_KEY=123891e2h812eh89e1h891wqwefgg78tv67st67
* ALLOWED_ORIGINS=*

Activate the venv using:
> python3 -m venv .venv

Activate venv:
> source .venv/bin/activate

Install the required dependencies using:
> pip install -r requirements.txt

After that, open your terminal and run python

Now that you're in python shell type in `from app import db` and `db.create_all()`, this will create tables in the database

Type in `flask run` to run the server
