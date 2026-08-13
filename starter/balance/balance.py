# balance.py
from typing import Optional

from transaction.transaction import Transaction

from balance.base_types import BalanceObserverSubject, Command, HistoryManager


class Balance(BalanceObserverSubject):
    """Singleton to track the balance."""
    _instance: Optional["Balance"] = None

    #always intialize the balance to 0
    _balance: float = 0.0

    #manage the undo/redo stack
    _manager: HistoryManager = HistoryManager()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._balance = 0.0

    def reset(self):
        self._balance = 0.0
        # I suppose we might have a 'balance is 0' observer!
        self.notify(None)
        # clear the undo/redo history
        self._manager.reset()

    def add_income(self, amount):
        print("Adding income:", amount)
        self._balance += amount
        print("New balance:", self._balance)

    def add_expense(self, amount):
        print("Adding expense:", amount)
        self._balance -= amount
        print("New balance:", self._balance)

    def apply_transaction(self, transaction: Transaction):
        command = Command.from_transaction(transaction, self)  
        print(f"Executing command: {command.__class__.__name__} with amount: {getattr(command, 'amount', 'N/A')}")
        command.execute()
        self._manager.add(command)
        self.notify(transaction)

    def undo(self):
        # Undo the last transaction and notify observers
        self._manager.undo()
        self.notify(None)

    def redo(self):
        # Redo the last undone transaction and notify observers
        self._manager.redo()
        self.notify(None)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        # When reporting as string, convert to float
        return f"Balance object with balance: {self._balance:.2f}"
    
