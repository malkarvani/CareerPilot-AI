from flask import Flask, render_template

from flask_login import LoginManager

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CONFIG
# =========================================================

from config import Config


# =========================================================
# DATABASE
# =========================================================

from models import db
from models.user import User


# =========================================================
# ROUTES
# =========================================================

from routes.auth import auth
from routes.dashboard import dashboard
from routes.profile import profile
from routes.roadmap import roadmap
from routes.resume import resume
from routes.chat import chat
from routes.job import job
from routes.portfolio import portfolio
from routes.certifications import certifications
from routes.interview import interview
from routes.resume_builder import resume_builder
from routes.admin import admin


# =========================================================
# CREATE FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# CONFIGURATION
# =========================================================

app.config.from_object(Config)


# =========================================================
# DATABASE
# =========================================================

db.init_app(app)


# =========================================================
# LOGIN MANAGER
# =========================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):

    try:

        return db.session.get(
            User,
            int(user_id)
        )

    except (
        TypeError,
        ValueError
    ):

        return None


# =========================================================
# BLUEPRINTS
# =========================================================

app.register_blueprint(auth)

app.register_blueprint(dashboard)

app.register_blueprint(profile)

app.register_blueprint(roadmap)

app.register_blueprint(resume)

app.register_blueprint(chat)

app.register_blueprint(job)

app.register_blueprint(portfolio)

app.register_blueprint(certifications)

app.register_blueprint(interview)

app.register_blueprint(resume_builder)

app.register_blueprint(admin)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )