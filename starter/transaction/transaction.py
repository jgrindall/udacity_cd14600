# transaction.py

from transaction.transaction_category import TransactionCategory


class Transaction:
    """Represents a financial transaction with an amount and category."""

    _metadata: dict

    def __init__(self, amount, category: TransactionCategory):
        self.amount = amount
        self.category = category
        self._metadata = {}
        if not isinstance(category, TransactionCategory):
            raise TypeError(
                f"Invalid category: {category}. "
                "Must be a TransactionCategory.")
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Invalid amount: {amount}. Must be a number.")

    def __str__(self):
        return f"Transaction(${self.amount}, category='{self.category}')"

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        return self.amount == other.amount and self.category == other.category

    def set_metadata(self, key, value):
        """Set a metadata key-value pair for the transaction."""
        self._metadata[key] = value
