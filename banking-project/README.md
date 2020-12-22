# OOP Programming: Bank Project

## Introduction

>  The Banking program code **[banking.py](banking.py)** resides in the main project folder.  The program mimics the core services of a bank: Checking Accounts, Saving Accounts, Credit Cards and Loans. For each of these services program captures the data and records to csv files in **[data](data)** folder.

## Part One: UML

UML Class Diagram of the program resides in **[docs](docs)** folder, and it is also shown below:
![UML Class Diagram for Banking Program](docs/Banking_UML_Class.jpeg)

## Part Two: How to Create Class Instances    

Examples to show initializing class objects and using methods if applicable.
### 1) Employee Instance ###  

**Creating an employee instance:**

	employee_instance = Employee(ssn: int, first_name: str, last_name: str, address: str)

**Note:** SSN argument should be an int with 9 digits and it should not had been used to create an employee instance before in the program.

After the employee instance created, the data about the employee instance is saved to **[employee.csv](data/employee.csv)**.
Example entries for employee.csv are shown below:

| index | ssn       | account_number |
|-------|-----------|----------------|
| 0     | 345678012 | 164147         |
| 1     | 123434347 | 130586         |

Currently, the employee class doesn't have any methods.

### 2) Checking Account Instance ###  

**Creating a checking account instance:**

	checking_account_instance = Checking(ssn: int, first_name: str, last_name: str, address: str)

**Note:** SSN argument should be an int with 9 digits and it should not had been used to create a checking account instance before in the program.

After the checking account instance created, the data about the checking account is saved to **[checking.csv](data/checking.csv)**.
Example entries for checking.csv are shown below:

| index | ssn       | account_number |
|-------|-----------|----------------|
| 0     | 345678012 | 164147         |
| 1     | 123434347 | 130586         |

**Calling checking account class methods on checking_account_instance:**

	checking_account_instance.withdraw(amount: Int) -> (Decreases checking_account_instance's balance attribute by 'amount'.) 

	checking_account_instance.deposit(amount: Int) -> (Increases checking_account_instance's balance attribute by 'amount'.) 
	
	del checking_account_instance -> (Deletes checking_account_instance and removes the related entry from checking.csv.) 

If 'deposit' or 'withdraw' methods of saving class are used, the transaction data is saved to **[account_transactions.csv](data/account_transactions.csv)**.
Example entries for account_transactions.csv are shown below:

| index | account_number | transaction_type | amount |
|-------|----------------|------------------|--------|
| 0     | 112486         | Debit            | -500   |
| 1     | 134022         | Credit           | 1200   |


### 3) Saving Account Instance ###  

**Creating a saving account instance:**

	saving_account_instance = Saving(ssn: int, first_name: str, last_name: str, address: str)

**Note:** SSN argument should be an int with 9 digits and it should not had been used to create a saving account instance before in the program.

After the saving account instance created, the data about the saving account is saved to **[saving.csv](data/saving.csv)**.
Example entries for saving.csv are shown below:

| index | ssn       | account_number |
|-------|-----------|----------------|
| 0     | 999666333 | 134022         |
| 1     | 123456789 | 155602         |

**Calling saving account class methods on saving_account_instance:**

	saving_account_instance.withdraw(amount: Int) -> (Decreases saving_account_instance's balance attribute by 'amount'.) 

	saving_account_instance.deposit(amount: Int) -> (Increases saving_account_instance's balance attribute by 'amount'.) 
	
	saving_account_instance.accrue_interest() -> (Increases saving_account_instance's balance attribute by 'balance' x 0.01.) 
	
	del saving_account_instance -> (Deletes saving_account_instance and removes the related entry from saving.csv.) 

If 'deposit', 'withdraw' or 'accrue_interest' methods of saving class are used, the transaction data is saved to **[account_transactions.csv](data/account_transactions.csv)**.
Example entries for account_transactions.csv are shown below:

| index | account_number | transaction_type | amount |
|-------|----------------|------------------|--------|
| 0     | 112486         | Debit            | -500   |
| 1     | 134022         | Credit           | 1200   |

### 4) Credit Card Instance ### 

**Creating a credit card instance:**

	credit_card_instance = CreditCard(ssn: int, first_name: str, last_name: str, address: str, limit: int)

**Note:** SSN argument should be an int with 9 digits and it should not had been used to create a creadit card instance before in the program.

After credit card instance created, the data about the credit card is saved to **[credit_card.csv](data/credit_card.csv)**.
Example entries for credit_card.csv are shown below:

| index | ssn       | credit_card_number |  limit |  expiration_date |  cvc |
|-------|-----------|--------------------|--------|------------------|------|
| 0     | 112233445 | 4234567890125150   | 1000   | 12-23            | 124  |
| 1     | 123412345 | 4234567890126800   | 900    | 12-23            | 168  |

**Calling credit card class methods on credit_card_instance:**

	credit_card_instance.pay_off(amount: Int) -> (Decreases credit_card_instance's balance attribute by 'amount'.) 

	credit_card_instance.purchase(amount: Int) -> (Increases credit_card_instance's balance attribute by 'amount'.) 

	del credit_card_instance -> (Deletes credit_card_instance and removes the related entry from credit_card.csv.) 

If 'pay_off' or 'purchase' methods of credit card class are used, the transaction data is saved to **[credit_card_transactions.csv](data/credit_card_transactions.csv)**.
Example entries for credit_card_transactions.csv are shown below:

| index | account_number   | transaction_type | amount |
|-------|------------------|------------------|--------|
| 0     | 4234567890125150 | Credit           | 100    |
| 1     | 4234567890125440 | Debit            | -500   |

### 5) Loan Instance ###

**Creating a loan instance:**

	loan_instance = CreditCard(ssn: int, first_name: str, last_name: str, address: str, loan_amount: int)

**Note:** SSN argument should be an int with 9 digits and it should not had been used to create a loan instance before in the program.

After loan instance created, the data about the loan is saved to **[loan.csv](data/loan.csv)**.
Example entries for loan.csv are shown below:

| index | ssn       | file_number | loan_amount |
|-------|-----------|-------------|-------------|
| 0     | 111222333 | 4506        | 2000        |
| 1     | 676776872 | 4800        | 23000       |

**Calling loan class methods on loan_instance:**

	loan_instance.pay_off(amount: Int) -> (Decreases loan_instance's remaining balance attribute by 'amount' whereas increasing amortized_balance attribute by 'amount'.)

**Note:** 'amount' should be equal or less than remaining_balance of the loan_instance.

If 'pay_off' method of loan class is used, the transaction data is saved to **[loan_transactions.csv](data/loan_transactions.csv)**. If a loan is fully paid off, del method is set to be called. Then the instance is deleted and related entry is removed from **[loan.csv](data/loan.csv)**.
Example entries for loan_transactions.csv are shown below:

| index | file_number | transaction_type | amount |
|-------|-------------|------------------|--------|
| 0     | 4484        | Credit           | 2000   |
| 1     | 3032        | Credit           | 1000   |

## Part Three: Logging

For logging, the program utilizes the **[yaml log config file](docs/check.logging.yml)** which resides in **[docs](docs)** folder. Logger writes messages to both screen and **[check.log](logs/check.log)** file in the **[logs](logs)** folder. Following events are logged:

* Creating an employee, saving, checking, credit card or loan instance successfully
* Attempt to create another employee, saving, checking, credit card or loan instance for a given SSN
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
