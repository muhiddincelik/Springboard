import yaml
import logging.config
import logging
import random
import pandas as pd

with open('..\\docs\\check.logging.yml', "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


class IdRange:
    def __init__(self):
        """
        Class of id ranges to generate ids for employees, customers and accounts.
        """
        self.employee_id_range = list(range(500, 1000))
        self.customer_id_range = list(range(1, 250))
        self.account_number_range = list(range(100000, 200000))

        # Shuffling the id lists to get a randomized list of possible ids
        random.shuffle(self.employee_id_range)
        random.shuffle(self.customer_id_range)
        random.shuffle(self.account_number_range)


class Person:
    """
    Parent class for employees and customers.
    """
    def __init__(self, ssn, first_name, last_name, address):
        self.ssn = ssn
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    @property
    def fullname(self):
        """
        Returns the full name of Person class.
        """
        return f'{self.first_name} {self.last_name}'

    @property
    def address(self):
        """
        Returns the address of Person class.
        """
        return f'Address of {self.fullname}: {self._address}'

    @address.setter
    def address(self, new_address):
        self._address = new_address
        logger.debug(f'{self.fullname}\'s address has been set.')


class Customer(Person):
    def __init__(self, ssn, first_name, last_name, address):
        super().__init__(ssn, first_name, last_name, address)
        self.customer_id = IdRange().customer_id_range.pop()


class Employee(Person):
    def __init__(self, ssn, first_name, last_name, address):
        """
        Initiates Employee instance and registers it to employee.csv after checking the database for a given ssn.
        """

        df = pd.read_csv('..\\data\\employee.csv')
        ssn_list = df['ssn'].tolist()
        if ssn in ssn_list:
            logger.debug(f'Attempt to hire an existing employee with ssn {ssn}.')
            raise ValueError('Employee is already in the database!')
        else:
            super().__init__(ssn, first_name, last_name, address)
            self.employee_id = IdRange().employee_id_range.pop()
            record = pd.DataFrame(self.__dict__, index=[len(ssn_list)])
            record.to_csv('..\\data\\employee.csv', mode='a', header=False)
            logger.debug(f'Employee({self.employee_id}) has been hired.')


class Account:
    def __init__(self):
        """
        Parent class for checking and saving accounts.
        """
        self.balance = 0
        self.account_number = IdRange().account_number_range.pop()

    def deposit(self, amount):
        """
        Increases the balance by amount and adds this transaction to transactions.csv.
        """
        self.balance += amount
        record_dict = {'account_number': self.account_number, 'transaction_type': 'Credit', 'amount': amount}
        df = pd.read_csv('..\\data\\transactions.csv')
        record = pd.DataFrame(record_dict, index=[len(df.index)])
        record.to_csv('..\\data\\transactions.csv', mode='a', header=False)
        logger.debug(f'Deposit for account {self.account_number}. Balance is {self.balance}.')

    def withdraw(self, amount):
        """
        Decreases the balance by amount if funds is sufficient and adds this transaction to transactions.csv.
        """
        if self.balance - amount < 0:
            logger.debug(f'Insufficient funds for withdrawal for account {self.account_number}.')
            pass
        else:
            self.balance -= amount
            record_dict = {'account_number': self.account_number, 'transaction_type': 'Debit', 'amount': -amount}
            df = pd.read_csv('..\\data\\transactions.csv')
            record = pd.DataFrame(record_dict, index=[len(df.index)])
            record.to_csv('..\\data\\transactions.csv', mode='a', header=False)
            logger.debug(f'Withdrawal for account {self.account_number}. New balance is {self.balance}.')


class Checking(Account, Customer):
    """
    Initiates checking account instance and registers it to checking.csv.
    """
    def __init__(self, ssn, first_name, last_name, address):
        df = pd.read_csv('..\\data\\checking.csv')
        ssn_list = df['ssn'].tolist()
        if ssn in ssn_list:
            logger.debug(f'Attempt to open duplicate checking account with ssn {ssn}.')
            raise ValueError('Customer has already a checking account!')
        else:
            Customer.__init__(self, ssn, first_name, last_name, address)
            Account.__init__(self)
            record_dict = {'ssn': self.ssn, 'account_number': self.account_number}
            record = pd.DataFrame(record_dict, index=[len(ssn_list)])
            record.to_csv('..\\data\\checking.csv', mode='a', header=False)
            logger.debug(f'{self.fullname}\'s checking account({self.account_number}) is now active.')

    def __del__(self):
        """
        Deletes the checking account instance, and removes account from checking.csv
        """
        try:
            checking_df = pd.read_csv('..\\data\\checking.csv')
            checking_df = checking_df[checking_df['ssn'] != self.ssn]
            checking_df.to_csv('..\\data\\checking.csv', mode='w', header=True, index=False)
            logger.debug(f'Checking account {self.account_number} has been closed.')
        except:
            pass


class Saving(Account, Customer):
    """
    Initiates saving account instance and registers it to saving.csv.
    """
    def __init__(self, ssn, first_name, last_name, address, interest_rate):
        df = pd.read_csv('..\\data\\saving.csv')
        ssn_list = df['ssn'].tolist()
        if ssn in ssn_list:
            logger.debug(f'Attempt to open duplicate saving account with ssn {ssn}.')
            raise ValueError('Customer has already a saving account!')

        else:
            Customer.__init__(self, ssn, first_name, last_name, address)
            Account.__init__(self)
            self.interest_rate = interest_rate
            record_dict = {'ssn': self.ssn, 'account_number': self.account_number} # Create record
            record = pd.DataFrame(record_dict, index=[len(ssn_list)])              # Convert the record into DataFrame
            record.to_csv('..\\data\\saving.csv', mode='a', header=False)          # Append the record to the base file.
            logger.debug(f'{self.fullname}\'s saving account({self.account_number}) is now active.')

    def accrue_interest(self):
        """
        Applies interest rate to the balance, and adds it to the balance.
        Also adds this transaction to transactions.csv.
        """
        interest_gain = self.balance * self.interest_rate # Calculate the interest increment
        self.balance += interest_gain                     # Add interest increment to the balance

        record_dict = {'account_number': self.account_number,                # Create new record as a dictionary
                       'transaction_type': 'Credit',
                       'amount': interest_gain}
        df = pd.read_csv('..\\data\\transactions.csv')
        record = pd.DataFrame(record_dict, index=[len(df.index)])            # Convert record dictionary into DataFrame
        record.to_csv('..\\data\\transactions.csv', mode='a', header=False)  # Append the record to the base file.
        logger.debug(f'Accrual is done for account {self.account_number}. Balance is {self.balance}.')

    def __del__(self):
        """
        Deletes the saving account instance, and removes account from saving.csv
        """
        try:
            saving_df = pd.read_csv('..\\data\\saving.csv')
            saving_df = saving_df[saving_df['ssn'] != self.ssn]
            saving_df.to_csv('..\\data\\saving.csv', mode='w', header=True, index=False)

            logger.debug(f'Saving account {self.account_number} has been closed.')
        except:
            pass


if __name__ == '__main__':
    s = Employee(2342348, 'First', 'Customer', 'Palo Alto')
    s.address = 'San Jose'
    del s

