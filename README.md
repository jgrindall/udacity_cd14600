# Run the app

> cd starter
> python3 -m main.py

Final balance: 1375.0



# Run the tests

> cd starter
> python3 -m unittest discover
or
> pytest


# Command pattern 

* I chose the Command Pattern, with a HistoryManager

* It seems a good fit since undo/redo seems a natural thing to perform with transactions

* Eg. when a mistake has been made

* It improves scalablilty primarily through the

```
Command::from_transaction
```
 
method. When a new kind of transaction is added we don't need to touch the Balance class.

We could have added a Factory but that seems a bit overkill, so I made it a class method.

* The HistoryManager stores a list of Commands

* Each Command wraps a transaction

* Each Command has undo and redo

* I decided to pass None as the "transaction" when received by an observer, which I think makes sense since there are no extra transactions.

* It improves flexibiliy since we have control over how a Command wraps a transaction.
It's a bit more future-proof than the original code which was just 
type=INCOME -> add
type=EXPENSE -> subtract

* I've added tests for the HistoryManager class. See test_balance_manager.py

* Testability is improved since we have clear separation of concerns. You can create a HistoryManager using any class that extends Command, so it can be tested separately from a Balance.  In fact I decided to remove the command.execute() code (it used to be in the Manager). I put it back in the Balanace to keep this clean.





# Reflection

The design patterns used in this application are:

* Observer
* Command
* Singleton
* Adapter

Observer improves the design by allowing us to listen to changes in an object oriented way.
New observers can be added simply and, as long as they implement the interface, we are guaranteed that they will fire.
They are quite pluggable and can be easily combined.

Adapter allows us to interface in a simple way with the 'real world' - allowing us to use our code unchanged with slightly different input that doesnt' 100% fit the shape of our classes.

The Singleton pattern lets us guarantee one balance instance.
I'm not convinced it is a good fit, since it requires lots of "reset" calls to ensure it stays clean.

The Command pattern is explained above. Commands wrap transactions and the HistoryManager allows undo/redo.

One trade-off I made was that the observers receive None. I considered allowing a transaction to have a correspoding reverse transaction when undone.

So Transaction(50, TransactionCategory.INCOME) -> undo -> get reverse transaction -> Transaction(50, TransactionCategory.INCOME_UNDO) or Transaction(50, TransactionCategory.EXPENSE) or perhaps
(50, TransactionCategory.EDIT)

It gets a bit complicated since then I would have to notify observers using these but I would have to be careful not to wrap these in a COmmand and insert them into the HistoryManager array!

In the end I decided that None is acceptable.

