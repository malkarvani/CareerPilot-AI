import os

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

from app import app
from models import db
from models.user import User


# Load .env
load_dotenv()


# ==========================================
# ADMIN CREDENTIALS
# ==========================================

ADMIN_EMAIL = os.getenv(
    "ADMIN_EMAIL",
    "malkarvani@gmail.com"
)

ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    "ShivMalkar2701"
)


# ==========================================
# CREATE / UPDATE ADMIN
# ==========================================

with app.app_context():

    user = User.query.filter_by(
        email=ADMIN_EMAIL
    ).first()

    if user:

        print("Admin email already exists.")

        # Update password
        user.password_hash = generate_password_hash(
            ADMIN_PASSWORD
        )

        # Make this account an admin
        user.is_admin = True

        # Make sure name exists
        if not user.name:
            user.name = "Admin"

        db.session.commit()

        print("Admin account updated successfully.")

    else:

        admin_user = User(
            name="Admin",
            email=ADMIN_EMAIL,
            password_hash=generate_password_hash(
                ADMIN_PASSWORD
            ),
            is_admin=True
        )

        db.session.add(admin_user)

        db.session.commit()

        print("Admin account created successfully.")


# ==========================================
# SHOW RESULT
# ==========================================

print()
print("==========================================")
print("       CareerAI Admin Account")
print("==========================================")
print("Email    :", ADMIN_EMAIL)
print("Password :", ADMIN_PASSWORD)
print("Admin    : True")
print("==========================================")