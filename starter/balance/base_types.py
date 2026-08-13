# base_types.py
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from starter import transaction
from starter.transaction import transaction
from transaction.transaction import Transaction

if TYPE_CHECKING:
    from .balance import Balance

class IBalanceObserver(ABC):
    @abstractmethod
    def update(self, balance: "Balance", transaction: Transaction | None = None):
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



class Command(ABC):

    @property
    def balance(self):
        return self._balance

    def __init__(self, balance):
        self._balance = balance

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @classmethod
    def from_transaction(cls, transaction: Transaction, balance: "Balance"):
        """Factory method to create a command based on the category."""
        if transaction.category == "INCOME":
            return AddIncomeCommand(balance, transaction.amount)
        elif transaction.category == "EXPENSE":
            return AddExpenseCommand(balance, transaction.amount)
        else:
            raise ValueError(f"Unknown transaction category: {transaction.category}")
    


class AddIncomeCommand(Command):
    def __init__(self, balance, amount: int):
        super().__init__(balance)
        self.amount = amount

    def execute(self):
        self._balance.add_income(self.amount)

    def undo(self):
        self._balance.add_expense(self.amount)



class AddExpenseCommand(Command):
    def __init__(self, balance, amount: int):
        super().__init__(balance)
        self.amount = amount

    def execute(self):
        self._balance.add_expense(self.amount)

    def undo(self):
        self._balance.add_income(self.amount)


class Controller:
    def __init__(self):
        self._history: list[Command] = []

    def execute_command(self, command: Command):
        command.execute()
        self._history.append(command)
        return self

    def undo(self):
        if self._history:
            last_command = self._history.pop()
            last_command.undo()

    def redo(self):
        if self._history:
            last_command = self._history[-1]
            last_command.execute()


