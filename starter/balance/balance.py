# balance.py
from typing import Optional
from transaction.transaction_category import TransactionCategory
from abc import ABC, abstractmethod
from balance.base_types import BalanceObserverSubject


class Balance(BalanceObserverSubject):
    """Singleton to track the balance."""
    _instance: Optional["Balance"] = None

    #always intialize the balance to 0, always int so dimes/pence are exact.
    _balance: int = 0

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._balance = 0

    def reset(self):
        self._balance = 0
        # I suppose we might have a 'balance is 0' oberserver!
        self.notify(None)

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
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
            self.notify(transaction)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
            self.notify(transaction)
        else:
            raise ValueError(f"Unknown transaction category: {transaction.category}")

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        # When reporting as string, convert to float
        float_balance = self._balance / 100 
        return f"Balance object with balance: {float_balance:.2f}"
    
