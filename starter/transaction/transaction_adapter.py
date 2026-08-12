# transaction_adapter.py

"""
ExternalFreelanceIncome consists of:

self.amount = amount
self.invoice_id = invoice_id
self.description = description
self.typ = "income"  # fixed, since it’s always income
"""


from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TransactionAdapter:
    def __init__(self, external_transaction):
        self.external_transaction = external_transaction
        # eg. freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")

    def to_transaction(self):
        """Convert an external transaction to a standard Transaction."""
        # get the amount
        amount = self.external_transaction.amount
        # and use a real TransactionCategory. self.typ is always income, so we use INCOME!
        # throw away description and invoice_id
        return Transaction(amount, TransactionCategory.INCOME)
