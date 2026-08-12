# balance_observer.py
from abc import ABC, abstractmethod
from balance.base_types import IBalanceObserver

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
