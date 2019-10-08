from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def get_register():
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

@app.route('/login')
def login():
    return render_template('login.html')
        
@app.route('/login', methods=['POST'])
def get_login():
    data = {
        'username' : request.form["username"],
        'password' : request.form["password"]
    }
    #username = request.form["username"]
    #password = request.form["password"]
    logging("Login Attempted: %s\n" %(data['username']))
    return "%s<br>%s"%(data['username'], data['password']) 

def logging(event):
    log_file = open("/srv/car-calendar/car-calendar-events.log", "a+")
    log_file.write(event)
    log_file.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')