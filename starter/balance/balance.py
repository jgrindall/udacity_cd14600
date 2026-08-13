# balance.py
from typing import Optional
from transaction.transaction_category import TransactionCategory
from abc import ABC, abstractmethod
from balance.base_types import BalanceObserverSubject, Command, Controller


class Balance(BalanceObserverSubject):
    """Singleton to track the balance."""
    _instance: Optional["Balance"] = None

    #always intialize the balance to 0, always int so dimes/pence are exact.
    _balance: int = 0

    _manager: Controller = Controller()

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
        Via a command so we can undo it

        Args:
            transaction (Transaction): The transaction to apply.
        """
        command = Command.from_transaction(transaction, self)    
        self._manager.execute_command(command)


    def undo(self):
        self._manager.undo()

    def redo(self):
        self._manager.redo()

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        # When reporting as string, convert to float
        float_balance = self._balance / 100 
        return f"Balance object with balance: {float_balance:.2f}"
    
