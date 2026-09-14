### Querying with tricky types

**Fast track**: In this field, you will learn how police writes queries on dates, how they calculate age with SQL functions, how to sort hits, and how to search on emptiness.  
If you are on the fast track and know about these, read the story line, exercises, solutions and notes only.

>
> Dick looked at the record of the suspicious guy they'd just found, and noticed his date of birth. 1957. 
> Something is wrong. He seems too old to be a murderer...
>

**Exercise 1**: Which people were born after 1997?

**Hints**:

* A condition can use different operators like `=`, `<`, `<=`, `>`, `>=`, `<>`.
* Filtering on dates is similar to filtering on texts: use quotes. Multiple recognizable formats 
are accepted by MS SQL in regards of the day-month-year order, and the SQL standard is YYYY-MM-DD. Make sure month and day are not 
mixed up. [(complete list of all possible format)](https://docs.microsoft.com/en-us/sql/t-sql/data-types/date-transact-sql?view=sql-server-ver15)

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
SELECT *
FROM person
WHERE date_of_birth >= '1998/01/01'
```
</details>

<details>
<summary>A few alternatives to the date</summary>
<p>
'01/01/1998'<br>
'1998-01-01'<br>
</p>
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 2**: The eyewitness said something about the *age* of the man, and not about the *birth date*. 
Let the query calculate it for every person.

**Hints**:

* There is a function called `GETDATE()` which returns the current date. Try this:
```sql
SELECT GETDATE()
```
* A calculated value like `GETDATE()` can be printed and used in a format of a column, by giving a name for it:
```sql
 SELECT GETDATE() AS currentdate
```
* There is another function called `DATEDIFF`, which has 3 parameters: a unit of time, a start date and an end date. It calculates the difference between 2 dates in the given time unit. Try this:
```sql
SELECT DATEDIFF(year, '1962-08-18', GETDATE())
```
* Both can be used combined with select from a table. So the name of a column can be passed as a parameter, and then it calculates the value for every selected row.
* There are a lot of functions implemented in MS SQL. There are so-called reference guides to find the one you need. See for example: [datediff in Microsoft's T-SQL documentation](https://docs.microsoft.com/en-us/sql/t-sql/functions/datediff-transact-sql)

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
SELECT *, DATEDIFF(year, date_of_birth, GETDATE()) FROM person
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 3**: Keep only person_id, first_name, last_name, date_of_birth and age to see the point.

**Hints**:

* Use `as age` to rename a column of the results to *age* or anything else. Especially useful when a column is calculated by a long formula, or when you want to refer to it in another part of the query, for example at ordering.

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
SELECT 
    person_id, 
    first_name, 
    last_name, 
    date_of_birth, 
    DATEDIFF(year, date_of_birth, GETDATE()) AS age 
FROM person
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 4**: I want to see the same people sorted by the age, from the youngest to the oldest.

**Hints**:

* To sort the results by a column, put `ORDER BY columnname` at the end of the query.
* By default `ORDER BY` returns an increasing list, but you can put `ASC` or `DESC` at the end to make ascending or descending explicit.

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
SELECT 
    person_id, 
    first_name, 
    last_name, 
    date_of_birth, 
    DATEDIFF(year, date_of_birth, GETDATE()) AS age 
FROM person 
ORDER BY age;
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 5**: Still too much... The eyewitness said she saw someone between 20 and 30 
years old, I'd like to see everyone with this age, with all their data, still ordered by age.

| **Note**    |
| ----------- |
| MS SQL does not allow usage of user-defined names of columns in the `WHERE` condition, as `WHERE` condition is parsed before the custom name of a column. Example: `SELECT first_name AS custom_name FROM person WHERE custom_name = 'Zelda'` -> this leads to a syntax error.|

<!-- blank line -->
----
<!-- blank line -->

**Exercise 5a**: Write a query for that. This time, you can repeat `DATEDIFF` calculation in the query as many times as it is needed. 

<details>
<summary>Check your results</summary>
<p>
22 rows expected.
</p>
</details>

<details>
<summary>Solution with repeated calculation</summary>

<!-- sql-test: rows=22 -->
```sql
SELECT *, DATEDIFF(year, date_of_birth, GETDATE()) AS age 
FROM person 
WHERE DATEDIFF(year, date_of_birth, GETDATE()) >= 20 AND DATEDIFF(year, date_of_birth, GETDATE()) <= 30
ORDER BY age
```

You may be wondering why it's not possible to refer to the `age` alias again in the `WHERE` clause. The answer is, that there is no good reason for this limitation. Oracle supports this, SQL Server doesn't.

Due to the repetition, it's not advisable to use this query in production. The next exercise shows a better way.
</details>

<!-- blank line -->
----
<!-- blank line -->

**Exercise 5b**: Make it more efficient: eliminate repetition of the calculation. SQL Server offers the so-called Common Table Expression (CTE) for this situation.

**Note**:

Here is an example of a Common Table Expression (CTE):
```sql
WITH name_of_the_query (name_of_column1, name_of_column2, name_of_column3) AS (
       SELECT a, b, any_function --this internal select is executable separately
       FROM table
)
SELECT * FROM name_of_the_query
WHERE name_of_column1 = 'something' AND name_of_column2 IS NULL
ORDER BY name_of_column3;
```

**Hint**:

* Pull out the calculation as a query, give a name to it and to its columns, and use it as a table with 
columns later in the query.

<details>
<summary>Solution</summary>

<!-- sql-test: rows=22 -->
```sql
WITH persons_with_age (first_name, last_name, age) AS (
       SELECT first_name, last_name, DATEDIFF(year, date_of_birth, GETDATE())
       FROM person
)
SELECT * FROM persons_with_age WHERE age >= 20 AND age <= 30
ORDER BY age;
```
</details>
<br />

<!-- blank line -->
----
<!-- blank line -->

**Exercise 6**: Ok, not bad, not bad. I see all kinds of hair colors and shoe sizes here, and males and females as well. Let's combine this query with the criteria the eyewitness said: age (between 20 and 30), shoe size (45), hair color (Black), gender (male). How many results do we get?

<details>
<summary>Check your results</summary>
<p>
0 row
</p>
</details>

<details>
<summary>Solution 1</summary>

<!-- sql-test: rows=0 -->
```sql
SELECT *, DATEDIFF(year, date_of_birth, GETDATE()) AS age 
FROM person 
WHERE is_male=1 AND hair='Black' AND shoe_size = 45 
AND DATEDIFF(year, date_of_birth, GETDATE()) >= 20 
AND DATEDIFF(year, date_of_birth, GETDATE()) < 30;
```
</details>


<details>
<summary>Solution 2</summary>

<!-- sql-test: rows=0 -->
```sql
WITH persons_with_age (first_name, last_name, age, is_male, hair, shoe_size) AS (
       SELECT first_name, last_name, DATEDIFF(year, date_of_birth, GETDATE()), is_male, hair, shoe_size
       FROM person
)
SELECT * FROM persons_with_age
WHERE age >= 20 AND age <= 30
AND is_male=1 AND hair='Black' AND shoe_size = 45
ORDER BY age;
```
</details>


>
> These data science guys are all full of pretenses. They pretend their database is so clean, so crisp, so full of all the answers... 
> But Dick knew better. "Your database is crap. Here, this person record. Hair color 'null', what the heck does that mean?"
> 
> The data scientist looked away in shame. "It seems we are missing some information about this person. His hair color was never properly entered into the system."
> Dick: "Well, how can you work like this? We're searching for a person with black hair. Could this be him, or not? I need answers, dang it"
> 

<!-- blank line -->
----
<!-- blank line -->

**Exercise 7**: Let's keep everyone who *can* be suspicious: the hair colour was either not recorded, or it is black; shoe size was either not recorded, or it is 45.

**Hints**:

* A column can be set to allow empty fields. The hair property of the person table are such.
* To filter on its emptiness or non-emptiness, use `IS NULL` or `IS NOT NULL`. This is not the same as the empty string: ''. Make experiments with it.
* Note that the shoe_size property also can be empty (check the table columns in the Object explorer). We are interested in people who have no recorded shoe size, so add this too to the criteria. 
* If you have both `AND` and `OR` in a `WHERE` condition, make sure they are grouped according to your needs:
in MS SQL `AND` has a higher preference than `OR`. If you want to change the default behaviour, or just want to make the grouping of conditions 
clear, use brackets like this: condition1 `AND` (condition2 `OR` condition3).

| **Note**    |
| ----------- |
| It's a common mistake to write `= NULL` in a query, but it will result in no hits. Use `IS NULL`. |

<details>
<summary>Result</summary>
<p>
1 row expected: Martin Walsh.
</p>
</details>

<details>
<summary>Solution 1</summary>

<!-- sql-test: rows=1; first_name=Martin; last_name=Walsh -->
```sql
SELECT *, DATEDIFF(year, date_of_birth, GETDATE()) AS age 
FROM person 
WHERE is_male=1 AND (hair='Black' OR hair IS NULL) AND (shoe_size = 45 OR shoe_size IS NULL) 
AND DATEDIFF(year, date_of_birth, GETDATE()) >= 20 
AND DATEDIFF(year, date_of_birth, GETDATE()) < 30;
```
</details>

<details>
<summary>Solution 2</summary>

<!-- sql-test: rows=1; first_name=Martin; last_name=Walsh -->
```sql
WITH persons_with_age (first_name, last_name, age, is_male, hair, shoe_size) AS (
    SELECT first_name, last_name, DATEDIFF(year, date_of_birth, GETDATE()), is_male, hair, shoe_size
    FROM person
)
SELECT * FROM persons_with_age
WHERE age >= 20 AND age <= 30
  AND is_male=1 AND (hair='Black' OR hair IS NULL) AND (shoe_size = 45 OR shoe_size IS NULL)
ORDER BY age;
```
</details>

<details>
<summary>Solution 3</summary>

<!-- sql-test: rows=1; first_name=Martin; last_name=Walsh -->
```sql
SELECT first_name, last_name, is_male, hair, shoe_size, personCalculatedValues.age
FROM person
CROSS APPLY (
    SELECT DATEDIFF(year, date_of_birth, GETDATE()) AS age
) AS personCalculatedValues
WHERE is_male = 1
AND (hair = 'Black' OR hair IS NULL)
AND (shoe_size = 45 OR shoe_size IS NULL)
AND personCalculatedValues.age >= 20 AND personCalculatedValues.age < 30
ORDER BY personCalculatedValues.age;
```

</details>

>
> Finally, a lucky break. Based on the database search, a suspect could be apprehended. 
> He was subsequently picked out in a line-up by the women who saw him fleeing the crime scene.
>
> Forensics still has work to do, find the murder weapon, compare the blade, match fingerprints.
> But Dick knew enough. In the interrogation room, he had looked the suspect in his stone-cold eyes.
> Forensics can only confirm what his gut already told him: this guy is a killer.
>
> Thanks for your assistence in catching a killer! But the job of a police detective never ends. Dick has already been called for the next case.
>
> To be continued ...
