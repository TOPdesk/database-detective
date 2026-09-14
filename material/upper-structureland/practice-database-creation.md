### Practice database creation

**Fast track**: In this field, you will create the database for Los Angeles Police Department, based on the physical model. You will also read about different options of a column like it can be `NULL` or not, `PRIMARY KEY`, `FOREIGN KEY`.  
If you are on the fast track, read and execute the script in the Solution section to build up the database for you.

**Exercise 1**: Build up tables and relations in your empty playground database based on the Physical model you created during [Practice database design](practice-database-design.md).

**Hints**:

* Define types.
* In SQLite, an auto-incrementing primary key is typically defined as `INTEGER PRIMARY KEY AUTOINCREMENT`.
* Use foreign keys to enforce relations between columns.
* Define `NULL/NOT NULL` for the columns.
* Many different solutions exist.
**Hints**:

* Use the Object explorer to check you achieved what you wanted. Table creation or any modification on the structure cannot be undone, but you can drop a table and recreate it anytime, if you always save your work into an sql file.

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
CREATE TABLE person(
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT NULL,
last_name TEXT NULL,
date_of_birth DATE NULL
)

CREATE TABLE sample(
id INTEGER PRIMARY KEY AUTOINCREMENT,
place_collected TEXT NULL,
time_collected DATETIME NULL,
person_id INTEGER NULL,
CONSTRAINT fk_sample_person FOREIGN KEY (person_id) REFERENCES person(id)
)

CREATE TABLE locus(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
CONSTRAINT locus_name_unique UNIQUE (name)
)

CREATE TABLE peak(
id INTEGER PRIMARY KEY AUTOINCREMENT,
locus_id INTEGER NOT NULL,
sample_id INTEGER NOT NULL,
value INTEGER NOT NULL,
CONSTRAINT fk_peak_locus FOREIGN KEY (locus_id) REFERENCES locus(id),
CONSTRAINT fk_peak_sample FOREIGN KEY (sample_id) REFERENCES sample(id)
)
```
</details>

<!-- blank line -->
----
<!-- blank line -->

**Exercise 2**: Draw a diagram of your tables.

**Hints**:

* Use a SQLite-capable client with schema visualization (for example, [SQLite View online App](https://www.sqliteview.com/app), [Letos](https://letos.org/) or [DB Browser for SQLite](https://sqlitebrowser.org/)) to inspect and diagram tables.
* A diagram is generated. Tables can be moved manually, and it can be configured what kind of data to show on it. 
* If your SQL client cannot generate diagrams automatically, export the schema and use a separate diagramming tool.
