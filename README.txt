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