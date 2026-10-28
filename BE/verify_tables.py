from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema = 'bookshop_dev'
        ORDER BY table_name
    """)
    for row in cursor.fetchall():
        print(row)
