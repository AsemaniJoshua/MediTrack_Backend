from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager

from Blueprint_app.models import User


# Load environment variables from the .env file
load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.secret_key = "Some Key"
    
    # db initialization
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Initializing Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    # Configure the unauthorized handler
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return "Unauthorized", 403
    
    
    # Enable CORS for the entire application
    CORS(app)
    
    # import and register blueprints
    from Blueprint_app.blueprints.core.routes import core
    from Blueprint_app.blueprints.users.routes import users
    from Blueprint_app.blueprints.medications.routes import medications
    from Blueprint_app.blueprints.appointments.routes import appointments
    from Blueprint_app.blueprints.medicalRecords.routes import medical_records

    app.register_blueprint(core, url_prefix="/")
    app.register_blueprint(users, url_prefix="/api/v1/users")
    app.register_blueprint(medications, url_prefix="/api/v1/medications")
    app.register_blueprint(appointments, url_prefix="/api/v1/appointments")
    app.register_blueprint(medical_records, url_prefix="/api/v1/medical_records")
    
    # db migrations
    migrate = Migrate(app, db)
    return app