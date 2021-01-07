# Environment Creation/ Package install:

Anaconda version 4.9.2 was used to setup the environment
```
conda create --name cuneiform python=3.7.9
```

# Package Install

```
pip install -r requirements.txt
```

# Environment activation

```
conda activate cuneiform
```

# Environment Variables for Development

The following environment variables need to be set in a .env file in the root directory
```
DEBUG=True
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=EnterYourSecretKeyHere
GOOGLE_API_KEY=YourGoogleApiKeyHere
```


# DB Initialization:

The ```FLASK_APP``` environment variable must be set, then run the following command
```
flask db init
```

# DB Migrations:

The following command is  used for simpler DB Migrations:
```
flask db migrate -m "message"
flask db upgrade
```
As SQLite is used as the DB for this project, dropping columns in DB migration is more nuanced
Before running a migration, edit the migration script.


# Testing:

To run the test tests, run the following command from the root directory of the project
```
python -m pytest tests/
```
from the root directory of the project



# Run development server to serve the Flask application:

```
flask run
```