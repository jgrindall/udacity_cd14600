import unittest

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver


class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        print("Running test_alert_triggers_on_low_balance")
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        #40 now
        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)
        
        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_edge_case(self):
        # logic is < not <=
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(50, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(0, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(0.01, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_undo_redo(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        #40 now - triggererd!
        self.assertTrue(observer.alert_triggered)

        # Undo the last transaction (expense of 60)
        self.balance.undo()
        self.assertFalse(observer.alert_triggered)
        self.assertEqual(self.balance.get_balance(), 100)

        # Redo the last undone transaction (expense of 60)
        self.balance.redo()
        self.assertTrue(observer.alert_triggered)
        self.assertEqual(self.balance.get_balance(), 40)

    def test_removing(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        #40 now
        self.assertTrue(observer.alert_triggered)

        # Remove the observer and check that it no longer triggers
        self.balance.remove_observer(observer)
        self.balance.apply_transaction(Transaction(1000, TransactionCategory.INCOME))
        self.assertTrue(observer.alert_triggered)  # Should still be True since we removed the observer!


if __name__ == "__main__":
    unittest.main()
