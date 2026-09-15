### Create and drop tables

**Fast track**: In this field, you will learn how to create your own database, and the basic keywords for creating and dropping tables in SQLite (`CREATE TABLE`, `DROP TABLE`).  
If you are on the fast track, just create your own database (Exercise 1) and execute creation and dropping once by copying the solution to your Query window. Read the framed notes as well.

**Exercise 1**: Create a new playground database, which you can use for the exercises in Upper-Structureland. In SQLiteView "Close" your current database and then select "Load sample DB".

<!-- blank line -->
----
<!-- blank line -->

**Exercise 2**: Open a query window, and create a person table first with the following columns: first_name, last_name and date_of_birth. Consider what kind of data will be stored in it. Birthdate may be empty.

**Hints**:

* An example of creating a table is (and you need something very similar):
```sql
CREATE TABLE address(
  NUMBER INT NULL,
  street TEXT NOT NULL
)
```
* You can copy and paste this first, and execute it. There should be a success message.
* Every column has a type. Common SQLite types are:
 * `INT` - integer number
 * `TEXT` - text value
 * `DATE` - only the date part without time
* Whether a property mandatory, is indicated by null/not null keywords per column (`NULL` means nullable, `NOT NULL` means it cannot be null).

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
CREATE TABLE person(
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
date_of_birth DATE NULL
)
-- This is a comment, which does nothing. Used to add notes.
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 3**: Drop all your tables one by one (person, address if you have).

**Hint**:

* The basic structure of a `drop` query is:
```sql
 DROP tablename
```

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
DROP TABLE address
DROP TABLE person
```
</details>
<br/>

| **Note**    |
| ----------- |
| While `DELETE` deletes the content of your table; `DROP` deletes the table itself. The interface of SQLiteView confusingly (and incorrectly) talks about "deleting" a table. |
