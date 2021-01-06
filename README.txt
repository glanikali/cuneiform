Environment Creation/ Package install:

conda create --name cuneiform python=3.7.9




Package Install

pip install -r requirements.txt
conda activate cuneiform




DB Migrations:

set FLASK_APP=cuneiform.py
flask db init

flask db migrate -m "message"

- note to drop columns in SQLite it is a bit more nuanced
- 	- have to edit the migration script actually
	- https://www.youtube.com/watch?v=CxCK1DkikgA&ab_channel=PrettyPrinted

flask db upgrade



Testing:

To run the test, run 
```
python -m pytest tests/
```
from the root directory of the project




Set the file that contains the Flask application and specify that the development environment should be used:

```sh
(venv) $ export FLASK_APP=app.py
(venv) $ export FLASK_ENV=development
```

Run development server to serve the Flask application:

```sh
(venv) $ flask run
```

Docker Build Command:
```
docker build -t cuneiform .
```

Docker run command:
```
docker run -d -p 5000:5000 cuneiform
```