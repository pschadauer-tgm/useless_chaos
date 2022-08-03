# sidb (SImple DataBase)

Probably the worst sql-like database ever written. sidb is an embedded database written in python. Yes, I know python isn't really embeddable.

## Why it sucks

* No indexes
* No `ALTER TABLE`
* No `DELETE`
* Very non-compliant SQL
* Extremely slow
* Only 3 data types (`INTEGER`, `BOOLEAN`, `STRING`)
* No prepared Statements
* No joins, even though every sql-like db needs them
* Bad code
* No unit tests
* No basic math operations
* No transactions
* Don't ask about ACID
* No string literals it will just interpret symbols as strings if they aren't a keyword

and a lot more

## Why it is good

It is great for small python projects, that want to use a terrible sql like database. That is because a sql query returns an iterator which itself returns tuples of the result.

## Should you use it?

No

# The repl

`sql.py` provides a simple repl. It supports these commands:

* sql like commmands: `CREATE TABLE`, `INSERT INTO` and `SELECT`
* custom commands: `.tables` (lists all tables) and `.desc <table>` (describes a table)

every command needs to end with a semicolon (`;`) or else it throw a weird exception.
