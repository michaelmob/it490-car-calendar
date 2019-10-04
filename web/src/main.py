from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    data = {
        'example': 'This is how to pass a variable to a template.'
    }
    return render_template('login.html', **data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
