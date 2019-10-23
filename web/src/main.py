# Load environment variables.
import os
from dotenv import load_dotenv
load_dotenv(os.getenv('ENV_FILE', '.env'))

# Create and Setup Flask Instance.
from flask import Flask, session
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'SECRET')

# Register blueprints
from views import general, auth, cars
app.register_blueprint(general.blueprint)
app.register_blueprint(auth.blueprint)
app.register_blueprint(cars.blueprint)

# Inject user into all templates
from producers import get_user
@app.context_processor
def inject_user():
    if session.get('token'):
        user = get_user(session.get('token'))
        if user:
            return { 'user': user }
    return {}

if __name__ == '__main__':
    # Run Flask
    app.run(debug=True, host='0.0.0.0')
