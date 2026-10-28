from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT
            current_schema(),
            current_setting('search_path'),
            to_regclass('auth_user'),
            to_regclass('public.auth_user')
    """)
    print("RESULT:", cursor.fetchone())
