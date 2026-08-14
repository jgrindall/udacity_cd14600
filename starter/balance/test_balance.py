import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestBalance(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_initial_balance(self):
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_singleton_instance(self):
        balance1 = Balance.get_instance()
        balance2 = Balance.get_instance()
        self.assertIs(balance1, balance2)

    def test_add_income(self):
        self.balance.add_income(100)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_formatting_of_balance(self):

        self.assertEqual(
            self.balance.summary(),
            "Balance object with balance: 0.00")

        self.balance.add_income(100)
        self.balance.add_expense(30)
        self.assertEqual(
            self.balance.summary(),
            "Balance object with balance: 70.00")

        self.balance.add_income(0.01)
        self.assertEqual(
            self.balance.summary(),
            "Balance object with balance: 70.01")

        self.balance.add_income(0.000001)
        self.assertEqual(
            self.balance.summary(),
            "Balance object with balance: 70.01")

        self.balance.reset()
        self.assertEqual(
            self.balance.summary(),
            "Balance object with balance: 0.00")

        self.balance.add_expense(30)
        self.assertEqual(
            self.balance.summary(),
            "Balance object with balance: -30.00")

    def test_add_expense(self):
        self.balance.add_expense(40)
        self.assertEqual(self.balance.get_balance(), -40)

    def test_apply_transaction_income(self):
        t = Transaction(150, TransactionCategory.INCOME)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 150)

    def test_apply_transaction_expense(self):
        t = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), -60)

    def test_apply_transaction_invalid_category(self):
        class FakeCategory:
            pass
        with self.assertRaises(TypeError):
            _t = Transaction(100, FakeCategory())

    def test_reset(self):
        self.balance.add_income(100)
        self.balance.add_expense(50)
        self.balance.reset()
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_single(self):
        with self.assertRaises(RuntimeError):
            _b = Balance()


if __name__ == "__main__":
    unittest.main()
