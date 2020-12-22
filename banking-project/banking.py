import yaml
import logging.config
import logging
import random
import pandas as pd
import datetime
import sys
import time

with open("docs\\check.logging.yml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


class IdRange:
    """
    Class of id ranges to generate ids for employees, customers and accounts.
    """

    def __init__(self):
        """
        Defining id range attributes
        """
        self._employee_id_range = list(range(500, 1000))
        self._customer_id_range = list(range(1, 250))
        self._account_number_range = list(range(100000, 200000))
        self._loan_file_number_range = list(range(3000, 5000))
        self._credit_card_number_first_part = '423456789012'
        self._credit_card_number_last_part = list(range(5000, 7000))
        self._credit_card_cvc = list(range(111, 222))
        self._credit_card_expiration = '{0}/{1}'.format(str(datetime.datetime.now().month),  # Create expiration date
                                                        str(datetime.datetime.now().year + 3))

        # Shuffling the id list attributes to get a randomized list of possible ids
        random.shuffle(self._employee_id_range)
        random.shuffle(self._customer_id_range)
        random.shuffle(self._account_number_range)
        random.shuffle(self._credit_card_cvc)
        random.shuffle(self._credit_card_number_last_part)
        random.shuffle(self._loan_file_number_range)

    @property
    def employee_id_range(self):
        return self._employee_id_range

    @property
    def customer_id_range(self):
        return self._customer_id_range

    @property
    def account_number_range(self):
        return self._account_number_range

    @property
    def credit_card_cvc(self):
        return self._credit_card_cvc

    @property
    def credit_card_number_first_part(self):
        return self._credit_card_number_first_part

    @property
    def credit_card_number_last_part(self):
        return self._credit_card_number_last_part

    @property
    def loan_file_number_range(self):
        return self._loan_file_number_range

    @property
    def credit_card_expiration(self):
        return self._credit_card_expiration


class Person:
    """
    Parent class for employees and customers.
    """
    def __init__(self, ssn, first_name, last_name, address):
        # Enforce argument data types and limitations
        if len(str(ssn)) != 9:
            raise ValueError('Invalid SSN!')
        elif not first_name.isalpha():
            raise ValueError('Invalid First Name!')
        elif not first_name.isalpha():
            raise ValueError('Invalid Last Name!')
        else:
            self._ssn = ssn
            self._first_name = first_name
            self._last_name = last_name
            self._address = address

    @property
    def _fullname(self):
        """
        Returns the full name of Person class.
        """
        return f'{self._first_name} {self._last_name}'

    @property
    def address(self):
        """
        Returns the address of Person class.
        """
        return f'Address of {self._fullname}: {self._address}'

    @address.setter
    def address(self, new_address):
        self._address = new_address


class Customer(Person):
    def __init__(self, ssn, first_name, last_name, address):
        super().__init__(ssn, first_name, last_name, address)
        self._customer_id = IdRange().customer_id_range.pop()


class Employee(Person):
    def __init__(self, ssn, first_name, last_name, address):
        """
        Initiates Employee instance and registers it to employee.csv after checking the database for a given ssn.
        """
        df = pd.read_csv('data\\employee.csv')
        ssn_list = df['ssn'].tolist()
        if ssn in ssn_list:
            logger.debug(f'Attempt to hire an existing employee with ssn {ssn}.')
            raise ValueError('Employee is already in the database!')
        else:
            super().__init__(ssn, first_name, last_name, address)
            self._employee_id = IdRange().employee_id_range.pop()
            record = pd.DataFrame(self.__dict__, index=[len(ssn_list)])
            record.to_csv('data\\employee.csv', mode='a', header=False)
            logger.debug(f'Employee({self._employee_id}) has been hired.')


class Account:
    def __init__(self):
        """
        Parent class for checking and saving accounts.
        """
        self._balance = 0
        self._account_number = IdRange().account_number_range.pop()

    def deposit(self, amount):
        """
        Increases the balance by amount and adds this transaction to account_transactions.csv.
        """
        self._balance += amount
        record_dict = {'account_number': self._account_number, 'transaction_type': 'Credit', 'amount': amount}
        df = pd.read_csv('data\\account_transactions.csv')
        record = pd.DataFrame(record_dict, index=[len(df.index)])
        record.to_csv('data\\account_transactions.csv', mode='a', header=False)
        logger.debug(f'Deposit for account {self._account_number}. Balance is {self._balance}.')
        time.sleep(0.05)

    def withdraw(self, amount):
        """
        Decreases the balance by amount if funds is sufficient and adds this transaction to account_transactions.csv.
        """
        # Check available funds
        if self._balance - amount < 0:
            logger.debug(f'Insufficient funds for withdrawal for account {self._account_number}.')
            time.sleep(0.05)
            pass
        else:
            self._balance -= amount
            record_dict = {'account_number': self._account_number, 'transaction_type': 'Debit', 'amount': -amount}
            df = pd.read_csv('data\\account_transactions.csv')
            record = pd.DataFrame(record_dict, index=[len(df.index)])
            record.to_csv('data\\account_transactions.csv', mode='a', header=False)
            logger.debug(f'Withdrawal for account {self._account_number}. New balance is {self._balance}.')
            time.sleep(0.05)


class Checking(Account, Customer):
    """
    Initiates checking account instance and registers it to checking.csv.
    """

    def __init__(self, ssn, first_name, last_name, address):
        df = pd.read_csv('data\\checking.csv')
        ssn_list = df['ssn'].tolist()
        if ssn in ssn_list:
            logger.debug(f'Attempt to open duplicate checking account with ssn {ssn}.')
            raise ValueError('Customer has already a checking account!')
        else:
            Customer.__init__(self, ssn, first_name, last_name, address)
            Account.__init__(self)
            self._min_avg_daily_balance = 1500
            record_dict = {'ssn': self._ssn, 'account_number': self._account_number}
            record = pd.DataFrame(record_dict, index=[len(ssn_list)])
            record.to_csv('data\\checking.csv', mode='a', header=False)
            logger.debug(f'{self._fullname}\'s checking account({self._account_number}) is now active.')
            time.sleep(0.05)

    def __del__(self):
        """
        Deletes the checking account instance, and removes account from checking.csv
        """
        try:
            checking_df = pd.read_csv('data\\checking.csv')
            checking_df = checking_df[checking_df['ssn'] != self._ssn]
            checking_df.to_csv('data\\checking.csv', mode='w', header=True, index=False)
            logger.debug(f'Checking account {self._account_number} has been closed.')
            time.sleep(0.05)
        except ImportError:
            pass


class Saving(Account, Customer):
    """
    Initiates saving account instance and registers it to saving.csv.
    """

    def __init__(self, ssn, first_name, last_name, address):
        # Check the database to prevent duplicate saving accounts for a given ssn
        df = pd.read_csv('data\\saving.csv')
        ssn_list = df['ssn'].tolist()
        if ssn in ssn_list:
            logger.debug(f'Attempt to open duplicate saving account with ssn {ssn}.')
            raise ValueError('Customer has already a saving account!')

        else:
            Customer.__init__(self, ssn, first_name, last_name, address)
            Account.__init__(self)
            self.interest_rate = 0.01
            record_dict = {'ssn': self._ssn, 'account_number': self._account_number}  # Create record
            record = pd.DataFrame(record_dict, index=[len(ssn_list)])  # Convert the record into DataFrame
            record.to_csv('data\\saving.csv', mode='a', header=False)  # Append the record to the base file.
            logger.debug(f'{self._fullname}\'s saving account({self._account_number}) is now active.')
            time.sleep(0.05)

    def accrue_interest(self):
        """
        Applies interest rate to the balance, and adds it to the balance.
        Also adds this transaction to account_transactions.csv.
        """
        interest_gain = self._balance * self.interest_rate  # Calculate the interest increment
        self._balance += interest_gain  # Add interest increment to the balance

        record_dict = {'account_number': self._account_number,  # Create new record as a dictionary
                       'transaction_type': 'Credit',
                       'amount': interest_gain}
        df = pd.read_csv('data\\account_transactions.csv')
        record = pd.DataFrame(record_dict, index=[len(df.index)])  # Convert record dictionary into DataFrame
        record.to_csv('data\\account_transactions.csv', mode='a', header=False)  # Append the record to the base file.
        logger.debug(f'Accrual is done for account {self._account_number}. Balance is {self._balance}.')
        time.sleep(0.05)

    def __del__(self):
        """
        Deletes the saving account instance, and removes account from saving.csv
        """
        try:
            saving_df = pd.read_csv('data\\saving.csv')
            saving_df = saving_df[saving_df['ssn'] != self._ssn]
            saving_df.to_csv('data\\saving.csv', mode='w', header=True, index=False)
            logger.debug(f'Saving account {self._account_number} has been closed.')
            time.sleep(0.05)
        except ImportError:
            pass


class CreditCard(Customer):
    """
    Initiates credit card instance and registers it to credit_card.csv.
    """

    def __init__(self, ssn, first_name, last_name, address, limit):
        # Check the database to prevent duplicate credit cards for a given ssn
        df = pd.read_csv('data\\credit_card.csv')
        ssn_list = df['ssn'].tolist()
        if ssn in ssn_list:
            logger.debug(f'Attempt to get additional credit card with ssn {ssn}.')
            raise ValueError('Customer already has a credit card!')
        else:
            Customer.__init__(self, ssn, first_name, last_name, address)
            self._balance = 0  # Credit card initial balance is declared.
            self._limit = limit
            self._cvc = IdRange().credit_card_cvc.pop()
            self._expiration_date = IdRange().credit_card_expiration
            self._credit_card_number = "{0}{1}".format(IdRange().credit_card_number_first_part,  # C.C. Number assigned
                                                       str(IdRange().credit_card_number_last_part.pop()))
            record_dict = {'ssn': self._ssn,
                           'credit_card_number': self._credit_card_number,  # Create record
                           'limit': self._limit,
                           'expiration_date': self._expiration_date,
                           'cvc': self._cvc}
            record = pd.DataFrame(record_dict, index=[len(ssn_list)])  # Convert the record into DataFrame
            record.to_csv('data\\credit_card.csv', mode='a', header=False)  # Append the record to the base file.
            logger.debug(f'{self._fullname}\'s credit card ({self._credit_card_number}) is now active.')
            time.sleep(0.05)

    def pay_off(self, amount):
        """
        Decreases the credit card balance by amount and adds this transaction to credit_card_transactions.csv.
        """
        self._balance -= amount
        record_dict = {'credit_card_number': self._credit_card_number, 'transaction_type': 'Credit', 'amount': amount}
        df = pd.read_csv('data\\credit_card_transactions.csv')
        record = pd.DataFrame(record_dict, index=[len(df.index)])
        record.to_csv('data\\credit_card_transactions.csv', mode='a', header=False)
        logger.debug(f'Pay off for credit card {self._credit_card_number}. Current balance is {self._balance}.')
        time.sleep(0.05)

    def purchase(self, amount):
        """
        Increases the balance by amount if limit is sufficient,
        and adds this transaction to credit_card_transactions.csv.
        """
        # Check the limit before purchase
        if self._balance + amount > self._limit:
            logger.debug(f'Insufficient limit to make purchase for credit card {self._credit_card_number}.')
            pass
        else:
            self._balance += amount
            record_dict = {'credit_card_number': self._credit_card_number, 'transaction_type': 'Debit',
                           'amount': -amount}
            df = pd.read_csv('data\\credit_card_transactions.csv')
            record = pd.DataFrame(record_dict, index=[len(df.index)])
            record.to_csv('data\\credit_card_transactions.csv', mode='a', header=False)
            logger.debug(f'Purchase on credit card {self._credit_card_number}. New balance is {self._balance}.')
            time.sleep(0.05)

    def __del__(self):
        """
        Deletes the credit card instance, and removes credit card from credit_card.csv
        """
        try:
            df = pd.read_csv('data\\credit_card.csv')
            df = df[df['ssn'] != self._ssn]
            df.to_csv('data\\credit_card.csv', mode='w', header=True, index=False)
            logger.debug(f'Credit card {self._credit_card_number} has been closed.')
            time.sleep(0.05)
        except ImportError:
            pass


class Loan(Customer):
    """
    Initiates Loan instance and registers it to loan.csv.
    """

    def __init__(self, ssn, first_name, last_name, address, loan_amount):
        # Check the database to prevent duplicate loan files for a given ssn
        df = pd.read_csv('data\\loan.csv')
        ssn_list = df['ssn'].tolist()
        if ssn in ssn_list:
            logger.debug(f'Attempt to get additional loan with ssn {ssn}.')
            raise ValueError('Customer already has an open loan file!')

        # If there is no record in the database for the given ssn, create the Loan instance.
        else:
            Customer.__init__(self, ssn, first_name, last_name, address)
            self._amortized_balance = 0  # Loan initial amortized balance is declared.
            self._loan_amount = loan_amount
            self._remaining_balance = self._loan_amount - self._amortized_balance
            self._file_number = IdRange().loan_file_number_range.pop()
            # Create the record and write to the database
            record_dict = {'ssn': self._ssn,
                           'file_number': self._file_number,
                           'amount': self._loan_amount}

            record = pd.DataFrame(record_dict, index=[len(ssn_list)])  # Convert the record into DataFrame
            record.to_csv('data\\loan.csv', mode='a', header=False)  # Append the record to the base file.
            logger.debug(f'{self._fullname}\'s loan (file_number: {self._file_number}) has been approved.')
            time.sleep(0.05)

    def pay_off(self, amount):
        """
        Increases the loan amortized balance by amount and adds this transaction to loan_transactions.csv.
        """
        # Check over-payment
        if self._amortized_balance + amount > self._loan_amount:
            logger.debug(f'Excess payment for loan {self._file_number}. Please pay ${self._remaining_balance} or less.')
            pass
        else:
            self._amortized_balance += amount
            self._remaining_balance -= amount
            record_dict = {'file_number': self._file_number, 'transaction_type': 'Credit', 'amount': amount}
            df = pd.read_csv('data\\loan_transactions.csv')
            record = pd.DataFrame(record_dict, index=[len(df.index)])
            record.to_csv('data\\loan_transactions.csv', mode='a', header=False)
            logger.debug(f'Pay off for loan {self._file_number}. Total amortized balance is {self._amortized_balance}.')
            time.sleep(0.05)

        if self._remaining_balance == 0:
            # Remove the loan record from database if it is paid off totally, then delete the instance.
            df = pd.read_csv('data\\loan.csv')
            df = df[df['ssn'] != self._ssn]
            df.to_csv('data\\loan.csv', mode='w', header=True, index=False)
            logger.debug(f'Loan {self._file_number} has been closed.')
            time.sleep(0.05)
            del self


if __name__ == '__main__':
    '''Driver code is designed to get inputs from the user to interact with the program.'''

    print('WELCOME TO XYZ BANKING INC!')
    while True:  # Enabling user to be able to return to main menu

        # Main Menu Items
        print('''What kind of service are you interested in now? 
            1 - Open a Checking Account
            2 - Open a Saving Account
            3 - Get a Loan
            4 - Get a Credit Card
            5 - Exit''')

        selection = input('Please enter the number code of the service you want to get: ')  # Main Menu User Input
        try:
            if selection == '1':   # Creating a Checking Account
                input_ssn = int(input('Please enter your ssn: '))
                input_first_name = input('Please enter your first name: ')
                input_last_name = input('Please enter your last name: ')
                input_address = input('Please enter your address: ')
                c = Checking(input_ssn, input_first_name, input_last_name, input_address)

                while True:  # Enables user to stay in checking account sub-menu after getting a service
                    print('''Which service do you want to get for your checking account?
                        11 - Deposit to Your Checking Account
                        12 - Withdraw from Your Checking Account
                        13 - Close Your Checking Account
                        14 - Return to Main Menu''')

                    checking_sub_selection = input('Please enter the number code of the service you want to get: ')

                    if checking_sub_selection == '11':  # deposit method will be called
                        checking_deposit_amount = input('Please enter the amount you want to deposit: ')
                        try:
                            c.deposit(int(checking_deposit_amount))
                            continue
                        except ValueError:
                            print('Invalid selection!')
                            continue
                    elif checking_sub_selection == '12':   # withdraw method will be called
                        checking_withdraw_amount = input('Please enter the amount you want to withdraw: ')
                        try:
                            c.withdraw(int(checking_withdraw_amount))
                            continue
                        except ValueError:
                            print('Invalid selection!')
                            continue
                    elif checking_sub_selection == '13':   # del method will be called
                        del c
                        break
                    elif checking_sub_selection == '14':  # Returns to Main Menu
                        break
                    else:
                        print('Invalid selection!')
                    continue

            elif selection == '2':  # Creating a Saving Account
                input_ssn = int(input('Please enter your ssn: '))
                input_first_name = input('Please enter your first name: ')
                input_last_name = input('Please enter your last name: ')
                input_address = input('Please enter your address: ')
                s = Saving(input_ssn, input_first_name, input_last_name, input_address)

                while True:  # Enables user to stay in saving account sub-menu after getting a service
                    print('''Which service do you want to get for your saving account?
                        21 - Deposit to Your Saving Account
                        22 - Withdraw from Your Saving Account
                        23 - Calculate interest for Your Savings
                        24 - Close Your Saving Account
                        25 - Return to Main Menu''')

                    saving_sub_selection = input('Please enter the number code of the service you want to get: ')

                    if saving_sub_selection == '21':  # deposit method will be called
                        saving_deposit_amount = input('Please enter the amount you want to deposit: ')
                        try:
                            s.deposit(int(saving_deposit_amount))
                            continue
                        except ValueError:
                            print('Invalid selection!')
                            continue
                    elif saving_sub_selection == '22':  # withdraw method will be called
                        saving_withdraw_amount = input('Please enter the amount you want to withdraw: ')
                        try:
                            s.withdraw(int(saving_withdraw_amount))
                            continue
                        except ValueError:
                            print('Invalid selection!')
                            continue
                    elif saving_sub_selection == '23':  # accrue_interest method will be called
                        s.accrue_interest()
                    elif saving_sub_selection == '24':  # del method will be called
                        del s
                        break
                    elif saving_sub_selection == '25':  # Returns to Main Menu
                        break
                    else:
                        print('Invalid selection!')
                    continue

            elif selection == '3':  # Creating a Loan
                input_ssn = int(input('Please enter your ssn: '))
                input_first_name = input('Please enter your first name: ')
                input_last_name = input('Please enter your last name: ')
                input_address = input('Please enter your address: ')
                input_loan_amount = input('Please enter the loan amount you want to get: ')

                try:
                    input_loan_amount = int(input_loan_amount)
                except ValueError:
                    print('Invalid loan amount')
                loan = Loan(input_ssn, input_first_name, input_last_name, input_address, input_loan_amount)

                while True:  # Enables user to stay in loan sub-menu after getting a service
                    print('''Which service do you want to get for your loan?
                        31 - Make payment for your loan!
                        32 - Return to Main Menu''')

                    loan_sub_selection = input('Please enter the number code of the service you want to get: ')

                    if loan_sub_selection == '31':  # pay_off method will be called
                        saving_payment_amount = input('Please enter the amount you want to pay: ')
                        try:
                            loan.pay_off(int(saving_payment_amount))
                            continue
                        except ValueError:
                            print('Invalid selection!')
                            continue
                    elif loan_sub_selection == '32':  # Returns to Main Menu
                        break
                    else:
                        print('Invalid selection!')
                    continue
            elif selection == '4':  # Creating a Credit Card
                input_ssn = int(input('Please enter your ssn: '))
                input_first_name = input('Please enter your first name: ')
                input_last_name = input('Please enter your last name: ')
                input_address = input('Please enter your address: ')
                input_limit = input('Please enter desired limit: ')

                try:
                    input_limit = int(input_limit)
                except ValueError:
                    print('Invalid limit')
                    continue

                cc = CreditCard(input_ssn, input_first_name, input_last_name, input_address, input_limit)

                while True:  # Enables user to stay in credit card sub-menu after getting a service
                    print('''Which service do you want to get for your credit card?
                        41 - Make Payment to Your Credit Card
                        42 - Make Purchase With Your Credit Card
                        43 - Close Your Credit Card
                        44 - Return to Main Menu''')

                    credit_card_sub_selection = input('Please enter the number code of the service you want to get: ')

                    if credit_card_sub_selection == '41':  # pay_off method will be called.
                        credit_card_payment_amount = input('Please enter the amount you want to pay: ')
                        try:
                            credit_card_payment_amount = int(credit_card_payment_amount)
                        except ValueError:
                            print('Invalid selection!')
                            continue
                        cc.pay_off(credit_card_payment_amount)
                        continue

                    elif credit_card_sub_selection == '42':  # purchase method will be called.
                        credit_card_purchase_amount = input('Please enter the amount you want to purchase: ')
                        try:
                            cc.purchase(int(credit_card_purchase_amount))
                            continue
                        except ValueError:
                            print('Invalid selection!')
                            continue

                    elif credit_card_sub_selection == '43':  # del method will be called.
                        del cc
                        break

                    elif credit_card_sub_selection == '44':  # Returns to Main Menu
                        break

                    else:
                        print('Invalid selection!')
                    continue

            elif selection == '5':  # Exits the program
                sys.exit()

            else:
                print('Invalid selection!')

        except ValueError:
            print('Invalid selection!')

