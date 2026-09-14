### Basic querying

**Fast track**: In this field, you will learn how police formulates queries from English text by using `SELECT`, `WHERE`, `OR` and `AND` keywords.  
If you already know this part of SQL, you can save time by reading only the story line, the exercises, the solutions and the framed tricks and notes.

>
> Chapter 1: The Suspect's Description
> ==
> 
> Rain was falling and slowly washed away the blood in the gutter. 
> The forensic team was making photos and preparing to take away the body for autopsy. 
> Such a shame, this young fellow had his whole life ahead of him. But now that's over. A knife through the chest will do that to you.
>
> Simmons was interviewing bystanders. "Dick, come quick. I think we've got something". 
> Anderson was surprised, usually interviews didn't produce quick results like that. 
> But the man had some useful news. Apparently a woman saw a man fleeing the crime scene. 
> She saw him clearly running accross the street into the park. 
> 
> Tall, male, black hair, between 20 and 30 years old. It's not much to go on, but it's 
> enough to search the forensic database and make a list of suspects. 
> Dick took out his phone and made a call. It's time for the geeks from the data science 
> department to stop playing tetris and start doing something useful.
>
> ![Simmons interviewing bystanders](images/Ready1-800.jpg)
>

**Exercise 1**: Make a list of people.

**Hints**:  

* Choose a table which seems to store people.
* The basic structure of a select query is:
```sql
SELECT * FROM tablename
```
where `*` means you'll see every column, but you can replace it with a list of comma separated column names.
* Whenever you need examples, check the SQLite documentation, or search online for SQLite-specific query examples.
<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
SELECT * FROM person
```
</details>
<br />

| **Note**    |
| ----------- |
| SQL is case insensitive. Although it's not a very strong recommendation, convention says you should use uppercase characters for SQL keywords. It's useful because this makes the keywords stand apart from the table and column names.|

<!-- blank line -->
----
<!-- blank line -->

**Exercise 2**: Which hair colors does the police know about? 

**Hints**:

* If you just query for the hair column of the person table, you see a hair color as many times as many person has that hair color. To remove all the duplicate values from the result, use the `DISTINCT` keyword after `SELECT`.

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
SELECT DISTINCT hair FROM person
```
</details>
<br />

**Exercise 3**: Make a list of persons with black hair.

| **Trick**   |
| ----------- |
| You can have multiple commands in the Query window, just select the commands you want to run, and then Execute/F5 will execute only that one (otherwise everything). Details: <a href="https://wiki.topdesk.com/wiki/Intro_to_MS_SQL_Management_Studio#6._Handle_multiple_queries_in_the_editor">Handle multiple queries in the editor</a>.|

**Hints**:

* `WHERE` condition can be added to the query: `SELECT * FROM tablename WHERE columnname = value`
* Text values need to be quoted like this: 'blue'.

<details>
<summary>Check your results</summary>
<p>
The query should return 50 rows.
</p>
</details>

<details>
<summary>Solution</summary>

<!-- sql-test: rows=50 -->
```sql
SELECT * FROM person WHERE hair = 'Black'
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 4**: Make a list of persons that are male.

**Hints**:

* Yes/no values are often stored as 0 (meaning No) or 1 (meaning Yes), as it's very effective (needs just 1 bit).
* Numbers don't need quoting in queries.

<details>
<summary>Check your results</summary>
<p>
The query should return 81 rows.
</p>
</details>

<details>
<summary>Solution</summary>

<!-- sql-test: rows=81 -->
```sql
SELECT * FROM person WHERE is_male=1
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 5**: Let's see who are the black haired males.

**Hints**:

* Conditions can be combined by logical operators: `AND`, `OR`:
```sql
  SELECT * FROM tablename WHERE condition1 AND condition2
  SELECT * FROM tablename WHERE condition1 OR condition2
```
* Consider the meaning of `AND` and `OR`. In the English language, `AND` and `OR` can mean the same thing, so it doesn't help:
 * 'Gimme every Ben and Otto!'
 * 'I don't care if he is a Ben or an Otto, give me!'
* The condition you write is evaluated for every row. So you want to construct a condition, which is true for males, and true for people with black hair, but not for people with blond hair.

<details>
<summary>Check your results</summary>
<p>
The query should return 25 rows.
</p>
</details>

<details>
<summary>Solution</summary>

<!-- sql-test: rows=25 -->
```sql
SELECT * FROM person
WHERE is_male=1 AND hair='Black'
```
</details>

| **Note**    |
| ----------- |
| The order of the results doesn't depend on how you wrote the conditions, but depends on the order they are stored in the table.|

> Our story continues...
>
> Dick sipped his coffee, simultaneously scaldingly hot and disgustingly bitter. But it was still better than no coffee.
> Unfortunately, it turned out the list of suspects from the database was quite long. Too long. He doesn't have time to chase
> up half of New York. The description was not specific enough. Ugh. Dick started to feel a headache coming up.
> 
> But this investigation was not over yet. 
>
> Forensics found more, in the fresh mud near the park. A set of hasty footprints. From the pictures,
> made hurriedly before the rain washed everything away, forensics determined that the suspect had shoe size 45!

<!-- blank line -->
----
<!-- blank line -->

**Exercise 6**: Add an extra condition to your query from the previous exercise, to check for shoe size.

<details>
<summary>Check your results</summary>
<p>
The query should return 1 person: Neil Davis.
</p>
</details>

<details>
<summary>Solution</summary>

<!-- sql-test: rows=1; first_name=Neil; last_name=Davis -->
```sql
SELECT * FROM person
WHERE is_male=1 AND hair='Black' AND shoe_size = 45
```
</details>

> Did we find the killer? Our story continues in the next section "Querying with tricky types"