import os
import sqlite3


# =========================================================
# FIND DATABASE
# =========================================================

DATABASE_CANDIDATES = [
    "careerai.db",
    "app.db",
    "database.db",
    os.path.join("instance", "careerai.db"),
    os.path.join("instance", "app.db"),
    os.path.join("instance", "database.db"),
]


database_path = None

for path in DATABASE_CANDIDATES:
    if os.path.exists(path):
        database_path = path
        break


if database_path is None:

    print("❌ Could not find the SQLite database.")

    print("\nI checked:")

    for path in DATABASE_CANDIDATES:
        print("   ", os.path.abspath(path))

    print("\nFind the .db file in your CareerAI project and")
    print("add its path to DATABASE_CANDIDATES.")

    raise SystemExit(1)


print("=" * 60)
print("CareerAI Database Fix")
print("=" * 60)

print(f"\nDatabase found:")
print(os.path.abspath(database_path))


# =========================================================
# CONNECT
# =========================================================

connection = sqlite3.connect(database_path)

cursor = connection.cursor()


# =========================================================
# CHECK ACTIVITY_LOGS TABLE
# =========================================================

cursor.execute(
    "SELECT name FROM sqlite_master "
    "WHERE type='table' AND name='activity_logs'"
)

table_exists = cursor.fetchone()


if not table_exists:

    print("\n⚠ activity_logs table does not exist.")

    print("Creating activity_logs table...")

    cursor.execute(
        """
        CREATE TABLE activity_logs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            action VARCHAR(200),
            description TEXT,
            endpoint VARCHAR(200),
            method VARCHAR(20),
            ip_address VARCHAR(100),
            created_at DATETIME
        )
        """
    )

    connection.commit()

    print("✅ activity_logs table created.")

else:

    print("\n✅ activity_logs table exists.")

    # -----------------------------------------------------
    # GET EXISTING COLUMNS
    # -----------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(activity_logs)"
    )

    columns = cursor.fetchall()

    existing_columns = {
        column[1]
        for column in columns
    }

    print("\nExisting columns:")

    for column in existing_columns:
        print("   ✓", column)


    # =====================================================
    # ADD MISSING COLUMNS
    # =====================================================

    required_columns = {

        "action": "VARCHAR(200)",

        "description": "TEXT",

        "endpoint": "VARCHAR(200)",

        "method": "VARCHAR(20)",

        "ip_address": "VARCHAR(100)",

        "created_at": "DATETIME",

    }


    for column_name, column_type in required_columns.items():

        if column_name not in existing_columns:

            print(
                f"\n➕ Adding missing column: {column_name}"
            )

            cursor.execute(
                f"""
                ALTER TABLE activity_logs
                ADD COLUMN {column_name} {column_type}
                """
            )

            print(
                f"   ✅ {column_name} added."
            )

        else:

            print(
                f"   ✓ {column_name} already exists."
            )


    connection.commit()


# =========================================================
# VERIFY
# =========================================================

cursor.execute(
    "PRAGMA table_info(activity_logs)"
)

final_columns = cursor.fetchall()


print("\n" + "=" * 60)
print("FINAL activity_logs TABLE")
print("=" * 60)


for column in final_columns:

    print(
        f"{column[1]:20} {column[2]}"
    )


# =========================================================
# CLOSE
# =========================================================

connection.close()


print("\n" + "=" * 60)
print("✅ DATABASE FIX COMPLETED")
print("=" * 60)

print(
    "\nNow restart CareerAI with:"
)

print(
    "    python app.py"
)

print(
    "\nThen open:"
)

print(
    "    http://127.0.0.1:5000/admin/dashboard"
)