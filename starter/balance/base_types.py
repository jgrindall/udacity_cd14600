# base_types.py
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

if TYPE_CHECKING:
    from .balance import Balance


class IBalanceObserver(ABC):
    @abstractmethod
    def update(
            self,
            balance: "Balance",
            transaction: Transaction | None = None):
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
        if transaction.category == TransactionCategory.INCOME:
            return AddIncomeCommand(balance, transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            return AddExpenseCommand(balance, transaction.amount)
        else:
            raise ValueError(
                f"Unknown transaction category: {transaction.category}")


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


class HistoryManager:

    _history: list[Command]
    _pointer: int

    def __init__(self):
        self.reset()

    def reset(self):
        self._history = []
        # Points to the last executed command, one before the start for now
        self._pointer: int = -1

    def add(self, command: Command):
        # Discard any redo history if we are not at the end of the history.
        # eg  C1 C2 C3 C4 C5 C6 C7
        #            ^                         - discard C4 onwards
        self._history = self._history[:self._pointer + 1]
        self._history.append(command)
        self._pointer += 1

    def undo(self):
        if self._history and self._pointer >= 0:
            command_to_undo = self._history[self._pointer]
            command_to_undo.undo()
            # eg  C1 C2 C3 C4 C5 C6 C7
            #            ^
            # undo C3 and move pointer back to C2
            self._pointer -= 1
        else:
            raise Exception("No command to undo.")

    def redo(self):
        if self._history and self._pointer < len(self._history) - 1:

            # eg  C1 C2 C3 C4 C5 C6 C7
            #            ^
            # redo C4 and move pointer forward to C4

            self._pointer += 1
            command_to_redo = self._history[self._pointer]
            command_to_redo.execute()
        else:
            raise Exception("No command to redo.")
