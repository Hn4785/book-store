from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT current_schema(), current_setting('search_path')")
    print("SCHEMA, SEARCH_PATH =", cursor.fetchone())
