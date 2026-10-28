from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT current_user, current_schema(), current_setting('search_path')")
    print("Connection:", cursor.fetchone())

    cursor.execute("SELECT schema_name FROM information_schema.schemata ORDER BY schema_name")
    print("Schemas:", cursor.fetchall())

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    print("Public tables:", cursor.fetchall())

    cursor.execute("SELECT has_database_privilege(current_user, current_database(), 'CREATE')")
    print("Can create schema:", cursor.fetchone()[0])
