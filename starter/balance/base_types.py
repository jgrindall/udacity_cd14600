# base_types.py
from abc import ABC, abstractmethod
from .balance import Balance
from transaction.transaction import Transaction

class IBalanceObserver(ABC):
    @abstractmethod
    def update(self, balance: Balance, transaction: Transaction | None = None):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class BalanceObserverSubject(ABC):

    _observers: list[IBalanceObserver] = []

    def __init__(self):
        self._observers: list[IBalanceObserver] = []

    def register_observer(self, observer: IBalanceObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: IBalanceObserver):
        self._observers.remove(observer)

    def notify(self, transaction=None):
        for observer in self._observers:
            observer.update(self, transaction)

