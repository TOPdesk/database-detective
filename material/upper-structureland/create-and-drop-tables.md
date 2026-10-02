### Create and drop tables

{% if variant == "duckdb" %}
**Fast track**: In this field, you will learn how to create an own database, and the basic keywords for creating and dropping tables in DuckDB (`CREATE TABLE`, `DROP TABLE`).  
If you are on the fast track, just create your own database (Exercise 1) and execute creation and dropping once by copying the solution to your Query window. Read the framed notes as well.

**Exercise 1**: Create a new playground database, which you can use for the exercises in Upper-Structureland. Open a new, separate [shell.duckdb.org](https://shell.duckdb.org/) tab without loading the crime database file, so you get an empty database to experiment in, instead of mixing these exercises with the crime database tables.
{% else %}
**Fast track**: In this field, you will learn how to create an own database, and the basic keywords for creating and dropping tables in MS SQL (`CREATE TABLE`, `DROP TABLE`).  
If you are on the fast track, just create your own database (Exercise 1) and execute creation and dropping once by copying the solution to your Query window. Read the framed notes as well.

**Exercise 1**: Create a new playground database, which you can use for the exercises in Upper-Structureland. Prefix it with your own userid, so that it doesn’t get mixed with the others’ databases on the same server.
{% endif %}

<!-- blank line -->
----
<!-- blank line -->

**Exercise 2**: Open a query window, and create a person table first with the following columns: first_name, last_name and date_of_birth. Consider what kind of data will be stored in it. Birthdate may be empty.

**Hints**:

{% if variant == "duckdb" %}
* An example of creating a table is (and you need something very similar):
```sql
CREATE TABLE address(
  NUMBER INT NULL,
  street TEXT NOT NULL
)
```
* You can copy and paste this first, and execute it. There should be a success message. Check the newly created objects visually in [shell.duckdb.org](https://shell.duckdb.org/)'s table list.
* Every column has a type. Common DuckDB types are:
 * `INT` - integer number
 * `TEXT` - text value, of any length
 * `DATE` - only the date part without time
* Whether a property mandatory, is indicated by null/not null keywords per column (`NULL` means nullable, `NOT NULL` means it cannot be null).

<details>
<summary>Solution</summary>

<!-- sql-test: variant=duckdb -->
```sql
CREATE TABLE person(
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
date_of_birth DATE NULL
)
-- This is a comment, which does nothing. Used to add notes.<br>
```
</details>
<br />
{% else %}
* An example of creating a table is (and you need something very similar):
```sql
CREATE TABLE address(
  NUMBER INT NULL,
  street NVARCHAR(40) NOT NULL
)
```
* You can copy and paste this first, and execute it. There should be a success message. Check the newly created objects visually in the [Object explorer](https://wiki.topdesk.com/index.php?title=Intro_to_MS_SQL_Management_Studio&section=2#4._Explore_database_objects).
* Every column has a type. The most frequently used types in MS SQL are:
 * `INT` - integer number
 * `NVARCHAR` - text with a maximum length of 4000, default length: 1, define length like `NVARCHAR(40)`
 * `DATE` - only the date part without time
* Whether a property mandatory, is indicated by null/not null keywords per column (`NULL` means nullable, `NOT NULL` means it cannot be null).

<details>
<summary>Solution</summary>

<!-- sql-test: variant=mssql -->
```sql
CREATE TABLE person(
first_name NVARCHAR(50) NOT NULL,
last_name NVARCHAR(50) NOT NULL,
date_of_birth DATE NULL
)
-- This is a comment, which does nothing. Used to add notes.<br>
-- Instead of 50, any reasonable number is ok as length.<br>
```
</details>
<br />
{% endif %}

| **Note**    |
| ----------- |
| Before further progressing with the queries, it's worth to save the contents of the query window into an sql file, and regularly save. |

<!-- blank line -->
----
<!-- blank line -->

**Exercise 3**: Drop all your tables one by one (person, address if you have).

**Hint**:

* The basic structure of a `drop` query is:
```sql
 DROP tablename
```

{% if variant == "duckdb" %}
<details>
<summary>Solution</summary>

<!-- sql-test: variant=duckdb -->
```sql
DROP TABLE address;
DROP TABLE person
```
</details>
<br/>
{% else %}
<details>
<summary>Solution</summary>

<!-- sql-test: variant=mssql -->
```sql
DROP TABLE address
DROP TABLE person
```
</details>
<br/>
{% endif %}

| **Note**    |
| ----------- |
| While `DELETE` deletes the content of your table; `DROP` deletes the table itself. |

| **Note**    |
| ----------- |
| Try to execute drop tables again. You'll see error messages, but it doesn't do any harm. |
