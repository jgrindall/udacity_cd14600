import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransaction(unittest.TestCase):

    def test_transaction_creation(self):
        t = Transaction(100, TransactionCategory.EXPENSE)
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, TransactionCategory.EXPENSE)

    def test_transaction_str(self):
        t = Transaction(50, TransactionCategory.INCOME)
        self.assertEqual(
            str(t),
            "Transaction($50, category='TransactionCategory.INCOME')")

    def test_transaction_equality(self):
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(20, TransactionCategory.EXPENSE)
        t3 = Transaction(30, TransactionCategory.EXPENSE)
        t4 = Transaction(30, TransactionCategory.INCOME)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)
        self.assertNotEqual(t1, t4)
        self.assertNotEqual(t3, t4)

        t5 = {"amount": 20, "category": TransactionCategory.EXPENSE}
        # Ensure that a Transaction is not equal to a dictionary with the same
        # data
        self.assertNotEqual(t1, t5)

    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            _t1 = Transaction("100", TransactionCategory.INCOME)
        with self.assertRaises(TypeError):
            _t2 = Transaction(100, "blahblah")


if __name__ == "__main__":
    unittest.main()
