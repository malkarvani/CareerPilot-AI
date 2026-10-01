from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from models import db
from models.user import User


auth = Blueprint(
    "auth",
    __name__
)


# =========================================================
# LOGIN
# =========================================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if current_user.is_authenticated:

        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("dashboard.home"))

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not email or not password:

            flash(
                "Please enter your email and password.",
                "error"
            )

            return render_template(
                "login.html"
            )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(password):

            login_user(user)

            # =================================================
            # ADMIN → ADMIN PANEL
            # =================================================

            if user.is_admin:

                return redirect(
                    url_for("admin.dashboard")
                )

            # =================================================
            # NORMAL USER → NORMAL DASHBOARD
            # =================================================

            return redirect(
                url_for("dashboard.home")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "login.html"
    )


# =========================================================
# REGISTER
# =========================================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    # Don't allow logged-in users to register again
    if current_user.is_authenticated:

        if current_user.is_admin:
            return redirect(
                url_for("admin.dashboard")
            )

        return redirect(
            url_for("dashboard.home")
        )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # -----------------------------------------------------
        # VALIDATION
        # -----------------------------------------------------

        if not name:

            flash(
                "Please enter your name.",
                "error"
            )

            return render_template(
                "register.html"
            )

        if not email:

            flash(
                "Please enter your email.",
                "error"
            )

            return render_template(
                "register.html"
            )

        if not password:

            flash(
                "Please enter a password.",
                "error"
            )

            return render_template(
                "register.html"
            )

        if len(password) < 6:

            flash(
                "Password must be at least 6 characters.",
                "error"
            )

            return render_template(
                "register.html"
            )

        if confirm_password and password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return render_template(
                "register.html"
            )

        # -----------------------------------------------------
        # CHECK EXISTING USER
        # -----------------------------------------------------

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return render_template(
                "register.html"
            )

        # -----------------------------------------------------
        # CREATE USER
        # -----------------------------------------------------

        user = User(
            name=name,
            email=email,
            is_admin=False
        )

        user.set_password(
            password
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Account created successfully. Please log in.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )