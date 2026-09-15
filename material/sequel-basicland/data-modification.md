### Data modification

**Fast track**: In this field, you will learn how police database guys maintain the database by using `UPDATE`, `INSERT`, `DELETE` keywords in multiple lines together, and how do they create and restore their database.  
If you are familiar with the topic, read the story line, exercises and solutions only.

> While Dick is just sitting in his room smoking and thinking, the database guys are busy with maintaining the
> data. Whenever they receive a shoe size or a complete person data which was unknown, they update or insert
> the relevant records.

**Exercise 1**: Before doing any change on the database, make a backup of the database. This is a 
saved copy of the database in a file, which can be used to restore (put back) the data which are in it at the moment of creation of the backup. For SQLite all that is needed is to copy the `*.sqlite` to another file, e.g. `*_backup.sqlite`). Restoring it then simply copying the `_backup.sqlite` over the original file.

<!-- blank line -->
----
<!-- blank line -->

**Exercise 2**: Set the hair color of Kira Murray to Black in the person table, and check if you managed to update it.

**Hints**:

* The basic structure of an update query is:
```sql
 UPDATE tablename
 SET columnname = newvalue
 WHERE condition
```
* `WHERE` condition is especially important for updates: it works without conditions as well: updates all fields! Most of the time this is not what you want.
* Format of the `WHERE` condition is the same as in a `SELECT`. 
* In Basicland we go with the default *transaction* setting. It means that every query you run, takes effect immediately in the database, and cannot be reverted. This setting can be changed, but unnecessary for now.
* See examples in SQLite documentation, or in Google.
* To check it, use a select query with the same where condition.

<details>
<summary>Solution</summary>

<!-- sql-test: rows=1 -->
```sql
UPDATE person
SET hair = 'Black'
WHERE first_name = 'Kira' AND last_name = 'Murray';

SELECT * FROM person
WHERE first_name = 'Kira' AND last_name = 'Murray';
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 3a**: Hans Klein and Cindy Klein are a brother and a sister, and they changed 
their last names to Kleiner, and want to do the change in the database.

In this exercise, do it in 3 steps, so that you see what's going on:

1. write a query to get the ids of the 2 person records to update
1. do the update
1. check your work with another query

**Hints**:

* You can filter on uuid similar to how you filtered on any text.
* You can use ```OR``` condition or ```IN``` as well: ```IN ('uuid1', 'uuid2')```.

<details>
<summary>Solution</summary>

<!-- sql-test: rows=2 -->
```sql
SELECT * FROM person
WHERE (first_name = 'Hans'
OR first_name = 'Cindy') AND last_name = 'Klein';

UPDATE person
SET last_name = 'Kleiner'
WHERE person_id IN ('398e6049-79cb-5b4e-9b36-e8c685e8543b', '73cfed84-eef9-864f-bbc2-51d1a1c0b897');

SELECT * FROM person
WHERE person_id IN ('398e6049-79cb-5b4e-9b36-e8c685e8543b', '73cfed84-eef9-864f-bbc2-51d1a1c0b897');
```
</details>
<br />

| **Note**    |
| ----------- |
|This is simple and safe, but not performing very well because of the separate queries. If the query gets into production environment, always keep performance in mind. See Exercise 3b.|

**Exercise 3b**: Change the query on a way that it's better performance-wise, so it's suitable to be included in the detective application. 

1. first, rename them manually back to Klein
1. write a single query to do the update 

<details>
<summary>Rename to Klein</summary>

<!-- sql-test -->
```sql
UPDATE person
SET last_name = 'Klein'
WHERE person_id IN ('398e6049-79cb-5b4e-9b36-e8c685e8543b', '73cfed84-eef9-864f-bbc2-51d1a1c0b897')
```
</details>
<br />

<details>
<summary>Single-query solution</summary>

<!-- sql-test -->
```sql
UPDATE person SET last_name = 'Kleiner' 
WHERE (first_name = 'Hans' OR first_name = 'Cindy') AND last_name = 'Klein'; 
```
</details>
<br />

| **Note**    |
| ----------- |
|When you do the same update from an application, performance becomes an issue. If you did a select first and then an update, the intermediate result set can be huge in memory in case of many records. It's a good practice to do that in one single query.|

<!-- blank line -->
----
<!-- blank line -->

**Exercise 4**: Add two new people to the person table, so that it looks like:

| first_name | last_name | date_of_birth | weight_kg | shoe_size |
| --------   | --------  | --------      | --------  | --------  |
| Otto       | Herz      | '1988-02-19'  | 112       | NULL      |
| Kathie     | Herz      | '1989-12-29'  | 64        | 39        |

**Hints**:

* An example of insert data into a table is (and you need something very similar):
```sql
INSERT INTO tablename (column1, column2, ...)
  VALUES (value1, value2, ...)
```
* A date can be inserted in a format like '1900-01-01'
* Every mandatory field has to be added, otherwise database will throw an error. Experiment with it.
* For SQLite, use explicit UUID strings for person_id values.
* You can create the two rows with 2 separate insert statement or by just 1 combined insert:
```sql
INSERT INTO tablename (column1, column2, ...) VALUES
  (value1, value2, ...),
  (valueA, valueB, ...)
```

<details>
<summary>Solution 1</summary>

<!-- sql-test -->
```sql
INSERT INTO person (person_id, first_name, last_name, weight_kg, date_of_birth)
  VALUES ('30e4f1df-cf4a-4b13-8f8a-d2fef53f7c41', 'Otto', 'Herz', 112, '1988-02-19')
INSERT INTO person (person_id, first_name, last_name, weight_kg, date_of_birth, shoe_size)
  VALUES ('8b6f9570-0358-4d16-9ac4-223670a85f49', 'Kathie', 'Herz', 64, '1989-12-29', 39)
```
</details>

<details>
<summary>Solution 2</summary>

<!-- sql-test -->
```sql
INSERT INTO person (person_id, first_name, last_name, weight_kg, date_of_birth, shoe_size) VALUES
  ('30e4f1df-cf4a-4b13-8f8a-d2fef53f7c41', 'Otto', 'Herz', 112, '1988-02-19', NULL),
  ('8b6f9570-0358-4d16-9ac4-223670a85f49', 'Kathie', 'Herz', 64, '1989-12-29', 39)
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 5**: It turned out they are twins, and Otto's birth date was wrong in the database. 
Set it to same as Kathie's, without explicitly putting the date.

* Use the result of a select in the update statement:
```sql
UPDATE tablename
SET column = (SELECT column FROM tablename WHERE condition)
WHERE condition
```
* Construct first the inner select. Make sure it returns only 1 value, which would fit as a value in the column to set in the ```update```.

<details>
<summary>Check solution with this select</summary>

<!-- sql-test -->
```sql
SELECT * FROM person WHERE 
(first_name = 'Otto' AND last_name = 'Herz') OR
(first_name = 'Kathie' AND last_name = 'Herz')
```
</details>

<details>
<summary>Solution</summary>

```sql
UPDATE person
SET date_of_birth = (SELECT date_of_birth FROM person WHERE first_name = 'Kathie' AND last_name = 'Herz')
WHERE first_name = 'Otto' AND last_name = 'Herz'
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

>
> The WiFi cafe is crowded, but nobody is paying attention to the shadowy figure in the 
> far corner typing away on his laptop. Otto Herz, notorious hacker and most wanted person,
> had gained access to the police database. Now, 
> with just a few commands on his keyboard, he could make himself disappear.
>

**Exercise 6**: Delete Otto from the person table.

**Hints**:

* The basic structure of a delete query is:
```sql
DELETE FROM tablename
  WHERE condition
```
* Without a `WHERE` condition everything gets deleted from the table, but not the table itself. 
So don't forget to add a `WHERE` condition.
* There are cases when a record cannot be deleted, because it has a reference on the record in another table or maybe within the same table. The database can enforce this kind of dependency between records. Now not this is the case.

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
DELETE FROM person
WHERE (first_name = 'Otto' AND last_name = 'Herz')
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 7**: It turned out the registration office was attacked by hackers, and sent wrong data to other offices. Restore the database you had before the changes.

**Hints**:

* If you are using the database on your disk, restore it by taking your backup file and copy it over your database .sqlite file.
* In SQLite Viewer App, Close the database and re-import the original file that you Downloaded in the Connect to your Database section.
