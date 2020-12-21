# OOP Programming: Bank Project

## Introduction

> This program mimics the core services of a bank: Checking Accounts, Saving Accounts, Credit Cards and Loans. For each of these services program captures the data and records to csv files in **[data](data)** folder.

## Part One: UML

UML Class Diagram of the program resides in **[docs](docs)** folder, and it is also shown below:
![UML Class Diagram for Banking Program](docs/Banking_UML_Class.jpeg)

## Part Two: How to Create Service Instances

Examples to show initializing class objects and using methods if applicable.
- 




## Part Three: Logging

For logging, the program utilizes the yaml log config file **[yaml log config file](docs/check.logging.yml)** which resides in **[docs](docs)** folder. Logger writes messages to both screen and **check.log** file in the **[logs](logs)** folder. Following events are logged:

* Creating an employee, saving, checking, credit card or loan instance successfully
* Attempt to create another employee, saving, checking, credit card or loan instance for a given ssn
* Succesfully executing deposit method for saving and checking instances
* Succesfully executing withdraw method for saving and checking instances
* Insufficient funds to execute withdraw method for saving and checking classes
* Deleting a saving, checking, creadit card or loan instance
* Succesfully executing accrue_interest method on a saving instance
* Succesfully executing pay_off or purchase methods on a credit card instance
* Succesfully executing pay_off method on a loan instance
* Attempt to make an excess pay-off payment on a loan instance

## Part Three: User Inputs Schema
When the program is executed, the users are directed to choose among menu items and they are required to enter the necessary information to get a service. Using user inputs, class instances are created as expected. User menu is depicted below:
![User Menu Design for Banking Program](docs/Banking_User_Menu_Diagram.jpeg)
