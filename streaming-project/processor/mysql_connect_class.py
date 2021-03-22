import mysql.connector
import time


# Create a class to connect to and interact with MySql
class MySQLPython:
    def __init__(self):
        self.connection = None

    def get_db_connection(self):
        try:
            self.connection = mysql.connector.connect(user='root',     # user name
                                                      password='root1234',  # password
                                                      host='localhost',
                                                      port='3306')
            print("Connection is successful!")

        except Exception as error:
            print("Error while connecting to database for job tracker", error)

        cursor = self.connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS logs")          # Drop the logs table in case it exists
        cursor.execute("CREATE DATABASE logs")                  # Create logs database
        cursor.execute("DROP DATABASE IF EXISTS dim_users")     # Drop the dim_users table in case it exists
        cursor.execute("CREATE DATABASE dim_users")             # Drop the dim_users table in case it exists
        print("DATABASE log has been created!")

        return self.connection

    # Method to create logs tables where Spark will write logs into
    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("USE logs;")                        # Ensuring to use logs database
        cursor.execute("DROP TABLE IF EXISTS good_logs;")  # Drop the good_logs table in case it exists
        cursor.execute("DROP TABLE IF EXISTS bad_logs;")   # Drop the bad_logs table in case it exists
        cursor.execute("DROP TABLE IF EXISTS suspicious_logs;")   # Drop the suspicious_logs table in case it exists
        time.sleep(0.2)

        # DDL syntax to create the good_logs table with desired fields and field types
        create_good_query = """CREATE TABLE good_logs (
                                event_id VARCHAR(32),
                                account_id INT,
                                event_type VARCHAR(15),
                                device VARCHAR(15),
                                location_country VARCHAR(5),
                                event_timestamp TIMESTAMP,
                                status VARCHAR(15)
                                )"""

        cursor.execute(create_good_query)

        # DDL syntax to create the bad_logs table with desired fields and field types
        create_bad_query = """CREATE TABLE bad_logs (
                                event_id VARCHAR(50),
                                account_id VARCHAR(50),
                                event_type VARCHAR(50),
                                device VARCHAR(15),
                                location_country VARCHAR(50),
                                event_timestamp VARCHAR(50),
                                status VARCHAR(15)
                                )"""

        cursor.execute(create_bad_query)

        # DDL syntax to create the suspicious_logs table with desired fields and field types
        create_suspicious_query = """CREATE TABLE suspicious_logs (
                                    event_id VARCHAR(50),
                                    account_id INT,
                                    event_type VARCHAR(50),
                                    device VARCHAR(15),
                                    location_country VARCHAR(50),
                                    event_timestamp TIMESTAMP,
                                    status VARCHAR(15)
                                    )"""

        cursor.execute(create_suspicious_query)
        cursor.close()

    # Method to user dimension table where Spark will read the users data from
    def create_dim_table(self):
        cursor = self.connection.cursor()
        cursor.execute("USE dim_users;")               # Ensuring to use dim_users database
        cursor.execute("DROP TABLE IF EXISTS users;")  # Drop the users table in case it exists
        time.sleep(0.2)

        # DDL syntax to create the users table with desired fields and field types
        create_dim_query = """CREATE TABLE users (
                                account_id VARCHAR(15),
                                device VARCHAR(15);
                                )"""

        # Insert some sample data into users table
        insert_users = """INSERT INTO (users)
                        VALUES
                        ("1", "ANDROID"),
                        ("2", "ANDROID"),
                        ("3", "ANDROID"),
                        ("4", "ANDROID"),
                        ("5", "ANDROID"),
                        ("6", "ANDROID"),
                        ("7", "ANDROID"),
                        ("8", "ANDROID"),
                        ("9", "ANDROID"),
                        ("10", "ANDROID");
                        """
        cursor.execute(create_dim_query)
        cursor.execute(insert_users)
        cursor.close()
