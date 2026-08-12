# balance.py
from typing import Union, Optional
from transaction.transaction_category import TransactionCategory

class Balance:
    """Singleton to track the balance."""


    _instance = None

    #always intialize the balance to 0, always int so dimes/pence are exact.
    _balance: int = 0

    def __new__(cls):
        if cls._instance is None:
            print("No instance exists yet, making one")
            instance = super().__new__()
            cls._instance = instance
        else:
            print("Instance already exists")
        return cls._instance

    def __init__(self):
        self._balance = 0;

    def reset(self):
        self._balance = 0

    def add_income(self, amount):
        self._balance += amount

    def add_expense(self, amount):
        self._balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        pass

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        # When reporting as string, convert to float
        float_balance = self._balance / 100 
        return f"Balance object with balance: {float_balance:.2f}"
    
