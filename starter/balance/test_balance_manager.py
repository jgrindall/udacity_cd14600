import unittest

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

from balance.balance import Balance
from balance.base_types import Command, HistoryManager


class TestBalanceManager(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_manager_state(self):
        c = HistoryManager()
        self.assertEqual(c._pointer, -1)
        cmd1 = Command.from_transaction(
            Transaction(
                100,
                TransactionCategory.INCOME),
            self.balance)
        c.add(cmd1)
        self.assertEqual(c._pointer, 0)
        cmd2 = Command.from_transaction(
            Transaction(
                100,
                TransactionCategory.INCOME),
            self.balance)
        c.add(cmd2)
        self.assertEqual(c._pointer, 1)

    def test_manager_undo(self):
        c = HistoryManager()
        self.assertEqual(c._pointer, -1)
        cmd1 = Command.from_transaction(
            Transaction(
                100,
                TransactionCategory.INCOME),
            self.balance)
        cmd2 = Command.from_transaction(
            Transaction(
                100,
                TransactionCategory.INCOME),
            self.balance)
        c.add(cmd1)
        c.add(cmd2)
        c.undo()
        self.assertEqual(c._pointer, 0)
        self.assertEqual(len(c._history), 2)
        cmd3 = Command.from_transaction(
            Transaction(
                100,
                TransactionCategory.INCOME),
            self.balance)
        c.add(cmd3)
        self.assertEqual(c._pointer, 1)
        # it gets overwritten, so the history length should be 2 not 3
        self.assertEqual(len(c._history), 2)

    def test_manager_reset(self):
        c = HistoryManager()
        cmd1 = Command.from_transaction(
            Transaction(
                100,
                TransactionCategory.INCOME),
            self.balance)
        cmd2 = Command.from_transaction(
            Transaction(
                100,
                TransactionCategory.INCOME),
            self.balance)
        c.add(cmd1)
        c.add(cmd2)
        c.reset()
        self.assertEqual(c._pointer, -1)
        self.assertEqual(len(c._history), 0)

    def test_undo(self):
        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.balance.apply_transaction(
            Transaction(50, TransactionCategory.EXPENSE))
        self.balance.undo()
        self.assertEqual(self.balance.get_balance(), 100)
        self.balance.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_redo(self):
        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.balance.apply_transaction(
            Transaction(50, TransactionCategory.EXPENSE))
        self.balance.undo()
        self.balance.redo()
        self.assertEqual(self.balance.get_balance(), 50)
        self.balance.undo()
        self.balance.redo()
        self.assertEqual(self.balance.get_balance(), 50)

    def test_throws(self):
        with self.assertRaises(Exception):
            self.balance.undo()  # No transactions to undo
        with self.assertRaises(Exception):
            self.balance.redo()  # No transactions to redo

    def test_throws_extra(self):
        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.balance.apply_transaction(
            Transaction(50, TransactionCategory.EXPENSE))
        self.balance.undo()
        self.balance.undo()
        with self.assertRaises(Exception):
            self.balance.undo()  # No transactions to undo

    def test_overwrite_redo_history(self):
        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.balance.apply_transaction(
            Transaction(50, TransactionCategory.EXPENSE))
        self.balance.undo()  # Undo the expense
        # New transaction should have cleared the redo history, so 50 has gone
        self.balance.apply_transaction(
            Transaction(30, TransactionCategory.EXPENSE))
        with self.assertRaises(Exception):
            self.balance.redo()  # Redo should fail because the redo history was overwritten

    def test_order(self):
        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.balance.apply_transaction(
            Transaction(80, TransactionCategory.INCOME))
        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.INCOME))
        self.balance.apply_transaction(
            Transaction(40, TransactionCategory.INCOME))

        self.assertEqual(self.balance.get_balance(), 280)

        self.balance.undo()
        self.balance.undo()
        self.balance.undo()
        self.balance.undo()
        self.assertEqual(self.balance.get_balance(), 0)
        self.balance.redo()
        self.assertEqual(self.balance.get_balance(), 100)
        self.balance.redo()
        self.assertEqual(self.balance.get_balance(), 180)
        self.balance.redo()
        self.assertEqual(self.balance.get_balance(), 240)
        self.balance.redo()
        self.assertEqual(self.balance.get_balance(), 280)

    def test_reset_clears_history(self):

        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.balance.apply_transaction(
            Transaction(50, TransactionCategory.EXPENSE))
        self.balance.reset()

        # all gone!
        with self.assertRaises(Exception):
            self.balance.undo()  # No transactions to undo after reset
        with self.assertRaises(Exception):
            self.balance.redo()  # No transactions to redo after reset


if __name__ == "__main__":
    unittest.main()
