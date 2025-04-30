from flask_mysqldb import MySQL
from config.config import Config
import MySQLdb

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = Config.DB_HOST
    app.config['MYSQL_USER'] = Config.DB_USER
    app.config['MYSQL_PASSWORD'] = Config.DB_PASSWORD
    app.config['MYSQL_DB'] = Config.DB_NAME
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    
    try:
        mysql.init_app(app)
        # Test connection
        with app.app_context():
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
    except MySQLdb.Error as e:
        raise RuntimeError(f"MySQL Connection Error: {str(e)}")