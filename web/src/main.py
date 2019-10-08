import json
from flask import Flask, render_template, request
from amqp.producer import Producer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def get_register():
<<<<<<< HEAD
    data = {
        'email' : request.form["email"],
        'username' : request.form["username"],
        'password' : password = request.form["password"]
    }
    #email = request.form["email"]
    #username = request.form["username"]
    #password = request.form["password"]
    logging("Registration Attempted: %s\n" %(data['username']))
    return "%s<br>%s<br>%s"%(data['email'], data['username'], data['password']) 
=======
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    if not username:
        return 'Invalid username.'

    if not password:
        return 'Invalid password.'

    producer = Producer('12.12.0.2', 5672, '/', 'admin', 'adminpass', is_rpc=True)
    response = producer.produce('auth-queue-rpc', json.dumps({
        'action': 'register',
        'email': email,
        'username': username,
        'password': password
    }))

    logging("Registration Attempted: %s\n" % (username,))
    return 'Registered!'

>>>>>>> 647dc8ca33f9aac92b182561e3018dbb5ab8e12b

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def get_login():
<<<<<<< HEAD
    data = {
        'username' : request.form["username"],
        'password' : request.form["password"]
    }
    #username = request.form["username"]
    #password = request.form["password"]
    logging("Login Attempted: %s\n" %(data['username']))
    return "%s<br>%s"%(data['username'], data['password']) 
=======
    username = request.form["username"]
    password = request.form["password"]
    producer = Producer('12.12.0.2', 5672, '/', 'admin', 'adminpass', is_rpc=True)
    response = producer.produce('auth-queue-rpc', json.dumps({
        'action': 'login',
        'username': username,
        'password': password
    }))
    logging("Login Attempted: %s\n" % (username,))

    return json.loads(response)

>>>>>>> 647dc8ca33f9aac92b182561e3018dbb5ab8e12b

def logging(event):
    log_file = open("/srv/car-calendar/car-calendar-events.log", "a+")
    log_file.write(event)
    log_file.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
