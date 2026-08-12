# balance_observer.py
from abc import ABC, abstractmethod

class IBalanceObserver(ABC):
    @abstractmethod
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        balance = balance.get_balance()
        print(f"balance updated: {balance}")


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        balance = balance.get_balance()
        if balance < self.threshold:
            print(f"Alert! Low balance: {balance} < {self.threshold}")
