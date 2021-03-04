import datetime
import mysql.connector
import time


class Tracker(object):
    """
    job_id, job_status, updated_time
    """
    def __init__(self, job_name, current_date):
        self.job_name = job_name
        self.current_date = current_date

    def assign_job_id(self):
        job_id = self.job_name + "_" + str(self.current_date)
        return job_id

    def get_db_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(  # user=input('Please enter the user name: '),     # user name
                                                   # password=input('Please enter the password: '),  # password
                                                 user='root',
                                                 password='Metin34.2027',
                                                 host='localhost',
                                                 port='3306')

        except Exception as error:
            print("Error while connecting to database for job tracker", error)

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS spark")          # Create spark database
        cursor.execute("USE spark")
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS job_tracker (job_id VARCHAR(100) PRIMARY KEY,
                                                                job_status VARCHAR(300),
                                                                updated_time DATETIME)""")
        return connection

    def update_job_status(self, status):
        job_id = self.assign_job_id()
        print(f"Job ID Assigned: {job_id}")
        update_time = datetime.datetime.now()
        connection = self.get_db_connection()
        connection.autocommit = True
        cursor = connection.cursor()
        time.sleep(1)
        cursor.execute("USE spark")
        update_ddl = f"""
                        REPLACE INTO spark.job_tracker VALUES ('{job_id}','{status}','{update_time}')
                        """
        try:
            cursor.execute(update_ddl)
            return print(f"Status of job {job_id} has been updated!")
        except Exception as e:
            print(f"Error updating job status: {e}")
        return

    def get_job_status(self, job_id):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("USE spark")
        get_ddl = f"SELECT job_status FROM spark.job_tracker WHERE job_id = '{job_id}'"
        try:
            cursor.execute(get_ddl)
            record = cursor.fetchall()
            if len(record) > 0:
                result = record[0][0]
                return print(f"Status of {job_id}: {result}")
            else:
                raise ValueError("There is no matching job_id!")
        except Exception as e:
            print(f"Error getting job status: {e}")



