# Load environment variables.
import os
from dotenv import load_dotenv
load_dotenv(os.getenv('ENV_FILE', '.env'))

# Create and Setup Flask Instance.
from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'SECRET')

from views import general, auth
app.register_blueprint(general.blueprint)
app.register_blueprint(auth.blueprint)

if __name__ == '__main__':
    # Run Flask
    app.run(debug=True, host='0.0.0.0')
