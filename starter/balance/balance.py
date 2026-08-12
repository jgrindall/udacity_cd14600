# balance.py
from typing import Optional
from transaction.transaction_category import TransactionCategory
from abc import ABC, abstractmethod

class Observer(ABC):
    @property
    def logger(self):
        return self._logger

    def __init__(self, logger: object | None = None):
        self._logger = logger

    @abstractmethod
    def update(self, message: str):
        pass


class ObserverSubject(ABC):

    _observers: list[Observer] = []

    def __init__(self):
        self._observers: list[Observer] = []

    def register_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)



class Balance(ObserverSubject):
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
    
