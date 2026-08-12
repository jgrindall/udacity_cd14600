# balance_observer.py
from abc import ABC, abstractmethod
from balance.base_types import IBalanceObserver
from transaction.transaction import Transaction

class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction: Transaction | None = None):
        """Print balance update message."""
        balance = balance.get_balance()
        print(f"balance updated: {balance}")


class LowBalanceAlertObserver(IBalanceObserver):

    alert_triggered: bool = False
    threshold: int

    def __init__(self, threshold):
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction: Transaction | None = None):
        """Alert if balance drops below threshold."""
        balance = balance.get_balance()
        if balance < self.threshold:
            print(f"Alert! Low balance: {balance} < {self.threshold}")
            self.alert_triggered = True

