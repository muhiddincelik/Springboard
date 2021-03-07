import mysql.connector
import time
import yaml
import logging.config
import logging

# Read from the logging config file
with open("docs\\check.logging.yml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


class MySQLPython:
    def __init__(self):
        self.connection = None

    def get_db_connection(self):
        try:
            self.connection = mysql.connector.connect(user=input('Please enter the user name: '),     # user name
                                                      password=input('Please enter the password: '),  # password
                                                      host='localhost',
                                                      port='3306')
            logger.info("Connection is successful!")

        except Exception as error:
            logger.error("Error while connecting to database for job tracker", error)

        cursor = self.connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS mysql_python")  # Drop the ticket_sales table in case it exists
        cursor.execute("CREATE DATABASE mysql_python")          # Create mysql_python database
        logger.info("DATABASE mysql_python has been created!")
        return self.connection

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("USE mysql_python")                   # Ensuring to use mysql_python database
        cursor.execute("DROP TABLE IF EXISTS ticket_sales")  # Drop the ticket_sales table in case it exists
        time.sleep(0.02)

        # DDL syntax to create the ticket_sales table with desired fields and field types
        query = """CREATE TABLE ticket_sales (
                                ticket_id INT,
                                trans_date DATE,
                                event_id INT,
                                event_name VARCHAR(50),
                                event_date DATE,
                                event_type VARCHAR(10),
                                event_city VARCHAR(20),
                                customer_id INT,
                                price DECIMAL,
                                num_tickets INT)"""

        cursor.execute(query)
        logger.info("TABLE ticket_sales has been created!")
        cursor.close()

    def load_third_party(self, file_path_csv='data/third_party_sales_1.csv'):
        cursor = self.connection.cursor()
        query = "INSERT INTO ticket_sales VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # Create values format

        # [Iterate through the CSV file and execute insert query]
        n = 0  # define a counter variable for row count
        with open(file_path_csv, 'r') as csv_file:
            for line in csv_file.readlines():
                cursor.execute(query, tuple(cell for cell in line.split(',')))  # insert each row as a tuple
                n += 1                                                          # add each row count to n

        self.connection.commit()                                                # Commit the changes
        logger.info(f"{n} rows have been inserted to the ticket_sales table.")
        cursor.close()

    def query_popular_tickets(self):
        # query to get the most popular 3 events in the September and December 2020
        sql_statement = """SELECT
                                event_name
                            FROM ticket_sales
                            WHERE YEAR(event_date) = 2020 AND MONTH(event_date) IN (9, 10)
                            GROUP BY 1
                            ORDER BY SUM(num_tickets) DESC
                            LIMIT 3"""
        cursor = self.connection.cursor()

        # Execute sql_statement and fetch all rows
        cursor.execute(sql_statement)
        records = cursor.fetchall()

        # Close the cursor and log the query event
        cursor.close()
        logger.info(f"Query is successful. {len(records)} rows have been returned.")

        # Creating a more readable format for teh desired analysis result
        result = """Here are the most popular 3 events in September and October 2020:
                1) {}
                2) {}
                3) {}"""

        # Return the result with accessing cell values from the records tuple list.
        return print(result.format(records[0][0], records[1][0], records[2][0]))


if __name__ == '__main__':
    """The driver code will create a MySQLPython class and will call all the class methods respectively,
       executing desired tasks using class attributes and the default function arguments."""
    m = MySQLPython()
    m.get_db_connection()
    m.create_table()
    m.load_third_party()
    m.query_popular_tickets()