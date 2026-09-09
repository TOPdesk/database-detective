### Practice database creation

**Fast track**: In this field, you will create the database for Los Angeles Police Department, based on the physical model. You will also read about different options of a column like it can be `NULL` or not, `PRIMARY KEY`, `FOREIGN KEY`.  
If you are on the fast track, read and execute the script in the Solution section to build up the database for you.

**Exercise 1**: Build up tables and relations in your empty playground database based on the Physical model you created during [Practice database design](practice-database-design.md).

**Hints**:

* Define types.
* A primary key is commonly defined as `INT` (auto-incremented during an insert by the database), or a `UNIQUEIDENTIFIER`. An auto-incremented int can be built up by the `IDENTITY` keyword. `UNIQUEIDENTIFIER` can be defaulted by using the embedded function `NEWID()`, which returns a random uuid.
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
id INT IDENTITY NOT NULL,
first_name NVARCHAR(50) NULL,
last_name NVARCHAR(50) NULL,
date_of_birth DATE NULL,
CONSTRAINT pk_person_id PRIMARY KEY (id))

CREATE TABLE sample(
id INT IDENTITY NOT NULL,
place_collected NVARCHAR(200) NULL,
time_collected DATETIME2 NULL,
person_id INT NULL,
CONSTRAINT fk_sample_person FOREIGN KEY (person_id) REFERENCES person(id),
CONSTRAINT pk_sample_id PRIMARY KEY (id))

CREATE TABLE locus(
id INT IDENTITY NOT NULL,
name VARCHAR(20) NOT NULL,
CONSTRAINT locus_name_unique UNIQUE (name),
CONSTRAINT pk_locus_id PRIMARY KEY (id))

CREATE TABLE peak(
id INT IDENTITY NOT NULL,
locus_id INT NOT NULL,
sample_id INT NOT NULL,
value INT NOT NULL,
CONSTRAINT fk_peak_locus FOREIGN KEY (locus_id) REFERENCES locus(id),
CONSTRAINT fk_peak_sample FOREIGN KEY (sample_id) REFERENCES sample(id),
CONSTRAINT pk_peak_id PRIMARY KEY (id))
```
</details>

<!-- blank line -->
----
<!-- blank line -->

**Exercise 2**: Draw a diagram of your tables.

**Hints**:

* MS SQL offers a visual editor for this (can be generated from the existing tables): expand your database in Object explorer on the left, right click on Database Diagrams (click Yes if it's asking for permission), click on New Database Diagram. Select all your tables.
* A diagram is generated. Tables can be moved manually, and it can be configured what kind of data to show on it. 
* If you receive an error saying 'Could not obtain information about Windows NT group/user ..., error code 0x54b. (Microsoft SQL Server, Error: 15404)', then you bumped into a known issue with SQL Server. The reason is that for creating diagrams, the database owner must be a static user of the database, and cannot be a user logged in with Windows authentication. The workaround is: right click on the name of your database in Object Explorer, Properties, Files page on the left, set the owner by clicking on ... at end of the line, Browse..., and choose a normal user (which is not NT or ##MS, but can be sa on your own server), Ok, Ok, Ok. This can be changed back once you are not working with the diagrams anymore.
