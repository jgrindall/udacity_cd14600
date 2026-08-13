# Purpose of this Folder

This folder should contain the scaffolded project files to get a student started on their project. This repo will be added to the Classroom for students to use, so please do not have any solutions in this folder.


You will start with a provided skeleton codebase and implement core components using classic object-oriented design patterns. The project requires you to apply three required patterns and one additional pattern of your choice. Each pattern must be implemented in Python and integrated into the working finance manager application.

Required Steps
Required Steps

1. Implement a Singleton Balance class
Ensure only one instance of the balance manager exists across the application using the Singleton pattern.
DONE



2. Complete the Transaction class
Finish the Transaction class using an enum to represent the transaction type (INCOME, EXPENSE).
?
DONE


3. Implement the Adapter pattern
Complete a TransactionAdapter class that converts external freelance income (with invoice ID and project details) into a compatible Transaction object.

DONE



4. Implement the Observer pattern
Create and register a LowBalanceAlertObserver that gets notified and triggers an alert when the user’s balance falls below a defined threshold and PrintBalance Observer that gets triggered when there is a change in the balance.
DONE


5. Choose and Implement One Additional Pattern (Student’s Choice)
You will select one additional design pattern to implement from the course curriculum:

Students must document:

Why they chose this pattern
Where it fits into the app
How it improves flexibility, testability, or scalability

DONE



6. Write Unit Tests
Create unit tests for the Balance, Transaction, Adapter, Observer, and any custom pattern implementation.



7. Run and Demonstrate the Application
Use the provided main.py script to simulate the app.



8. Reflect and Document
Include a short reflection explaining:



The four design patterns used
How each improved the design
Any trade-offs encountered during implementation

Break Down Tests
test_balance.py → Verifies correct implementation of the Singleton Balance class.


test_transaction.py → Confirms transactions update balances correctly.


test_transaction_adapter.py → Ensures external income data is correctly adapted into Transaction objects.


test_balance_observer.py → Validates that low-balance alerts are triggered at the correct threshold.

