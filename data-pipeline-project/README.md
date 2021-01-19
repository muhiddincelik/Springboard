# PYTHON & MySQL PROJECT  

## Introduction

>  The program code **[mysql_python_program.py](mysql_python_program.py)** resides in the main project folder.  The program connects to mysql and pushes the csv file data in **[data](data)** folder.

## HOW PROGRAM WORKS

The program is designed in OOP style. There is only one class: MySQLPython. All methods of this class uses the **connection** attribute of the class.

Methods:

	- get_db_connection(): Gets *user* and *password* info from the user input and connects to MySQL (host='localhost', port='3306'). Creates a database named **mysql_python**.
	
	- create_table(): creates ticket_sales table inside the mysql_python database using the table schema explained below.
	
	- load_third_party(): Insert the data in the [third_party_sales_1.csv](data/third_party_sales_1.csv) into the ticket_sales table.
	
	- query_popular_tickets(): Queries the ticket_sales table to get the most popular 3 events in the September and December 2020.
	
After user provides the user name and password, the driver code will create an instance of MySQLPython class and will call all methods of the class respectively. There should be 6 rows in the ticket_sales table in the mysql_python database in the MySQL of the hosting system. The logs about the results of the methods will also be written to the screen.

UML Class Diagram of the program resides in **[docs](docs)** folder, and it is also shown below:
![UML Class Diagram for Python & MySQL Program](docs/mysql_python.jpeg)



## SCHEMA OF THE TABLE   

		CREATE TABLE ticket_sales (
                                ticket_id INT,
                                trans_date DATE,
                                event_id INT,
                                event_name VARCHAR(50),
                                event_date DATE,
                                event_type VARCHAR(10),
                                event_city VARCHAR(20),
                                customer_id INT,
                                price DECIMAL,
                                num_tickets INT);

## LOGGING

For logging, the program utilizes the **[yaml log config file](docs/check.logging.yml)** which resides in **[docs](docs)** folder. Logger writes messages to both screen and **[check.log](logs/check.log)** file in the **[logs](logs)** folder. Following events are logged:

* Successful connection or error in the connection
* Creating the database
* Creating the ticket_sales table
* Number of inserted rows to the ticket_sales table
* Successful analysis query

