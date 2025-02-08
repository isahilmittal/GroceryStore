import mysql.connector

def sql_connection():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='rootroot',  # Add your password if required
            host='127.0.0.1',
            database='GS'
        )
        return connection  # Return active connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
