import os
import MySQLdb
import MySQLdb.cursors


conn = MySQLdb.connect(
    host=str(os.getenv('MYSQL_HOST')),
    port=int(os.getenv('MYSQL_PORT', 3306)),
    db=os.getenv('MYSQL_DB'),
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASS'),
    cursorclass=MySQLdb.cursors.DictCursor
)

db = conn.cursor()
