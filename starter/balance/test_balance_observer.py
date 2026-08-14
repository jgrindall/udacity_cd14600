import unittest
from unittest.mock import patch

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, RecordingObserver, PrintObserver


class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        # 40 now
        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_edge_case(self):
        # logic is < not <=
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(
            Transaction(50, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(0, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(0.01, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_undo_redo(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.EXPENSE))
        # 40 now - triggererd!
        self.assertTrue(observer.alert_triggered)

        # Undo the last transaction (expense of 60)
        self.balance.undo()
        self.assertFalse(observer.alert_triggered)
        self.assertEqual(self.balance.get_balance(), 100)

        # Redo the last undone transaction (expense of 60)
        self.balance.redo()
        self.assertTrue(observer.alert_triggered)
        self.assertEqual(self.balance.get_balance(), 40)

    def test_undo_redo_and_reset_notify_with_no_transaction(self):
        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        observer = RecordingObserver()
        self.balance.register_observer(observer)
        self.balance.undo()
        self.assertEqual(observer.transactions, [None])
        self.balance.remove_observer(observer)

    def test_print_observer(self):
        with patch("builtins.print") as mocked_print:
            observer = PrintObserver()
            self.balance.register_observer(observer)
            self.balance.apply_transaction(
                Transaction(100, TransactionCategory.INCOME))
            mocked_print.assert_called_once_with("balance updated: 100.0")

    def test_removing(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.EXPENSE))
        # 40 now
        self.assertTrue(observer.alert_triggered)

        # Remove the observer and check that it no longer triggers
        self.balance.remove_observer(observer)
        self.balance.apply_transaction(
            Transaction(1000, TransactionCategory.INCOME))
        # Should still be True since we removed the observer!
        self.assertTrue(observer.alert_triggered)


if __name__ == "__main__":
    unittest.main()
