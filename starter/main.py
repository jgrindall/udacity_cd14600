"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction_category import TransactionCategory


def main():
    
    balance = Balance.get_instance()

    obs1 = LowBalanceAlertObserver(threshold=50)
    balance.register_observer(obs1)

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # Apply all transactions to balance
    for t in all_transactions:
        balance.apply_transaction(t)

    print("Final balance:", balance.get_balance())
    assert balance.get_balance() == 1375, f"Expected balance to be 1375, but got {balance.get_balance()}"

if __name__ == "__main__":
    main()
