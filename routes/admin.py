from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.user import User
from models.admin_activity import ActivityLog


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# =========================================================
# ADMIN PROTECTION
# =========================================================

def admin_required():

    if not current_user.is_authenticated:
        return redirect(
            url_for("auth.login")
        )

    if not current_user.is_admin:

        flash(
            "Admin access required.",
            "error"
        )

        return redirect(
            url_for("dashboard.home")
        )

    return None


# =========================================================
# HELPER - CREATE ACTIVITY LOG
# =========================================================

def log_activity(
    user_id=None,
    action="ADMIN_ACTION",
    description=None,
    endpoint=None,
    method=None
):

    activity = ActivityLog(
        user_id=user_id,
        action=action,
        description=description,
        endpoint=endpoint,
        method=method,
        ip_address=request.remote_addr
    )

    db.session.add(activity)


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@admin.route("/dashboard")
@login_required
def dashboard():

    check = admin_required()

    if check:
        return check

    total_users = User.query.count()

    admin_users = User.query.filter_by(
        is_admin=True
    ).count()

    normal_users = User.query.filter_by(
        is_admin=False
    ).count()

    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    recent_activities = ActivityLog.query.order_by(
        ActivityLog.created_at.desc()
    ).limit(100).all()

    return render_template(
        "admin.html",

        users=users,

        total_users=total_users,

        admin_users=admin_users,

        normal_users=normal_users,

        recent_activities=recent_activities,

        history_user=None
    )


# =========================================================
# USER HISTORY
# =========================================================

@admin.route("/user/<int:user_id>/history")
@login_required
def user_history(user_id):

    check = admin_required()

    if check:
        return check

    user = db.session.get(
        User,
        user_id
    )

    if not user:

        flash(
            "User not found.",
            "error"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    activities = ActivityLog.query.filter_by(
        user_id=user.id
    ).order_by(
        ActivityLog.created_at.desc()
    ).limit(200).all()

    # Get all users for sidebar/table
    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    # Keep dashboard statistics
    total_users = User.query.count()

    admin_users = User.query.filter_by(
        is_admin=True
    ).count()

    normal_users = User.query.filter_by(
        is_admin=False
    ).count()

    return render_template(
        "admin.html",

        users=users,

        total_users=total_users,

        admin_users=admin_users,

        normal_users=normal_users,

        recent_activities=activities,

        history_user=user
    )


# =========================================================
# DELETE USER
# =========================================================

@admin.route(
    "/user/<int:user_id>/delete",
    methods=["POST"]
)
@login_required
def delete_user(user_id):

    check = admin_required()

    if check:
        return check

    user = db.session.get(
        User,
        user_id
    )

    if not user:

        flash(
            "User not found.",
            "error"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    # -----------------------------------------------------
    # NEVER DELETE YOUR OWN ADMIN ACCOUNT
    # -----------------------------------------------------

    if user.id == current_user.id:

        flash(
            "You cannot delete your own admin account.",
            "error"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    deleted_name = user.name
    deleted_email = user.email
    deleted_user_id = user.id

    try:

        # -------------------------------------------------
        # SAVE DELETION HISTORY
        # -------------------------------------------------
        #
        # user_id is set to NULL because the User itself
        # is going to be deleted.
        #
        # The deleted user's information is preserved
        # inside description.
        # -------------------------------------------------

        activity = ActivityLog(
            user_id=None,

            action="USER_DELETED",

            description=(
                f"Deleted user: "
                f"{deleted_name} "
                f"({deleted_email}), "
                f"User ID: {deleted_user_id}"
            ),

            endpoint=request.path,

            method=request.method,

            ip_address=request.remote_addr
        )

        db.session.add(activity)

        # -------------------------------------------------
        # DELETE USER
        # -------------------------------------------------

        db.session.delete(user)

        db.session.commit()

        flash(
            f"User {deleted_name} was deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        print(
            "DELETE USER ERROR:",
            e
        )

        flash(
            "Could not delete the user. "
            "Please check the terminal for details.",
            "error"
        )

    return redirect(
        url_for("admin.dashboard")
    )


# =========================================================
# MAKE USER ADMIN
# =========================================================

@admin.route(
    "/user/<int:user_id>/make-admin",
    methods=["POST"]
)
@login_required
def make_admin(user_id):

    check = admin_required()

    if check:
        return check

    user = db.session.get(
        User,
        user_id
    )

    if not user:

        flash(
            "User not found.",
            "error"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    if user.is_admin:

        flash(
            f"{user.name} is already an admin.",
            "error"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    try:

        user.is_admin = True

        log_activity(
            user_id=user.id,

            action="USER_MADE_ADMIN",

            description=(
                f"{user.name} "
                f"({user.email}) "
                "was granted administrator access."
            ),

            endpoint=request.path,

            method=request.method
        )

        db.session.commit()

        flash(
            f"{user.name} is now an admin.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        print(
            "MAKE ADMIN ERROR:",
            e
        )

        flash(
            "Could not make this user an admin.",
            "error"
        )

    return redirect(
        url_for("admin.dashboard")
    )


# =========================================================
# REMOVE ADMIN
# =========================================================

@admin.route(
    "/user/<int:user_id>/remove-admin",
    methods=["POST"]
)
@login_required
def remove_admin(user_id):

    check = admin_required()

    if check:
        return check

    user = db.session.get(
        User,
        user_id
    )

    if not user:

        flash(
            "User not found.",
            "error"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    # -----------------------------------------------------
    # DON'T REMOVE YOUR OWN ADMIN ACCESS
    # -----------------------------------------------------

    if user.id == current_user.id:

        flash(
            "You cannot remove admin access from yourself.",
            "error"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    if not user.is_admin:

        flash(
            f"{user.name} is not an admin.",
            "error"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    try:

        user.is_admin = False

        log_activity(
            user_id=user.id,

            action="ADMIN_ACCESS_REMOVED",

            description=(
                f"Administrator access removed from "
                f"{user.name} ({user.email})."
            ),

            endpoint=request.path,

            method=request.method
        )

        db.session.commit()

        flash(
            f"Admin access removed from {user.name}.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        print(
            "REMOVE ADMIN ERROR:",
            e
        )

        flash(
            "Could not remove administrator access.",
            "error"
        )

    return redirect(
        url_for("admin.dashboard")
    )