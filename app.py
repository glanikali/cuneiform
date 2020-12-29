# app.py

from cuneiform import app
from flask import render_template

@app.route('/')
def index():
    return render_template('home.html.j2')


if __name__ == '__main__':
    app.run(debug=True)
