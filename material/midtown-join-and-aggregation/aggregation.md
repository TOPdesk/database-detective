### Aggregation

**Fast track**: In this field, you will learn how aggregation like `GROUP BY` and `SUM` is working via examples.  
If you are on the fast track, check out the story line and the exercises with their solutions by executing them in your database.

> Chapter 3: The motive
> ==
>
> One Sunday afternoon, water reservoir, central park. Forensics agents were
> swarming around the crowded crime scene, like a school of fish. 
> "Simmons, walk me through" said Dick. - "The body was found by 
> a boy and his father, who were spending their bi-weekly Sunday visitation rights
> here in the park. They were driving a radio-controlled model boat, and it bumped 
> into the body as it was floating just below the surface".
>
> Simmons continued: "The body was identified as Vern Jameson, 25 years old, student at NYU.
> It looks like he might have been strangled, but the coroner will know more."
> Strangled? That usually meant an impulsive crime, hot with passion or anger. 
> "All right, let's talk to his room mates, see if we can trace his last steps". 
>
> At the dormitory, Anderson & Simmons were greeted by three students, two girls and a boy.
> They described Vern as a quiet, introverted boy who was a bit odd, but wouldn't hurt a fly.
> "Can you think of anybody who might have hurt Vern?" The students could not think of anybody.
> "Was he acting strangely lately?" One boy thought it was odd that he seemed to have more money lately.
> He was always working long hours, working shifts at the bar downstairs to make ends meet. 
> But over the past weeks he bought a new mac book, a brand new racing bike, while he was spending less
> time working at the bar.
> 
> "This newfound wealth is suspicious, don't you think, Simmons?"
> "Yessir, I'll take a look at his financial records"
>
> ![Thoughtful Anderson](images/Ready2-800.jpg)
>

**Prerequisite**: Make sure you are still connected to the database which is already prepared for you. If unsure, refer back to: [Connect to your database](../intro-street/connect-to-your-database.md).

| **Note**    |
| ----------- |
| In our model transfer.iban received the money, and transfer.contra_iban is who sent the money. |

<details>
  <summary>Whenever you need to remember the entity relations, check out the Entity-Relationship Diagram here.</summary>
  <p>
  <a href="images/dba_detective_database_structure.png"><img src="images/dba_detective_database_structure.png" alt="Entity Relationship Diagram"/></a>
  </p>
</details>

<!-- blank line -->
----
<!-- blank line -->


**Exercise 1**: First find the bank account of the victim, by his name: Vern Jameson. To find this in one query, you'll need to follow the relation from person to account_person, and then on to account.

<details>
<summary>The bank account of our victim</summary>
<p>US48BANK830816901</p>
</details>

<details>
<summary>Solution</summary>

<!-- sql-test: rows=1; iban=US48BANK830816901 -->
```sql
SELECT * FROM person p
JOIN account_person ap ON ap.person_id = p.person_id
JOIN account a ON a.iban = ap.iban
WHERE p.first_name = 'Vern' AND p.last_name = 'Jameson'
```
</details>

<details>
<summary>An equivalent solution</summary>

<!-- sql-test: rows=1; IBAN=US48BANK830816901 -->
```sql
SELECT * FROM account_person ap 
JOIN person p ON p.person_id = ap.person_id
WHERE last_name='Jameson' AND first_name='Vern'
```
</details>

<!-- blank line -->
----
<!-- blank line -->

**Exercise 2**: Calculate the sum of money transferred to our victim, grouped by the contra account.
Which contra party transferred the most money to this account?

**Hints**:

* There are aggregating operations like `SUM`. Aggregation in a sense that it takes multiple rows, and returns one as a result.
* General syntax: `SELECT SUM(a-number-type-column) FROM table`. This returns only 1 number, so it aggregates the hits into one.
* It's usually used combined with `GROUP BY` like this: `SELECT SUM(a-number-type-column), another-column FROM table GROUP BY another-column`. 
This takes the distinct (different) values from the group-by column, and to every group returns 1 row. The aggregated value is calculated within 1 group.

| **Note**    |
| ----------- |
| The most frequent aggregate functions are `SUM`, `COUNT`, `MIN`, `MAX`, `AVG`. | 

<details>
<summary>Check your results</summary>
<p>There were 9 contra parties sending money to US48BANK830816901.</p>
<p>The contra account that transferred the most is US81BANK2096431873.</p>
</details>

<details>
<summary>Solution</summary>

<!-- sql-test: rows=9; contra_IBAN=US81BANK2096431873 -->
```sql
SELECT contra_IBAN, SUM(amount) AS SUM
  FROM transfer
  WHERE IBAN = 'US48BANK830816901'
  GROUP BY contra_IBAN
  ORDER BY SUM DESC
```
</details>

| **Note**    |
| ----------- |
| Putting arbitrary columns in the column list (like `SELECT cluster_id`) would throw an error. This is not surprising, as many rows are aggregated in that one line, and only the group by column and the aggregated column has one single value in the group. When there is a `GROUP BY` in a query, every field in the column list must be either aggregated, or listed in `GROUP BY`.| 


<!-- blank line -->
----
<!-- blank line -->

**Exercise 3**: Take the answer from Exercise 2, and write a join query to find the name of the person holding the contra account. Who should the police invite to the station for further investigation?

<details>
<summary>The name</summary>
<p>Peter Patrelli</p>
</details>

<details>
<summary>Solution</summary>

<!-- sql-test: rows=1; first_name=Peter; last_name=Patrelli -->
```sql
SELECT * FROM account_person AS ap
JOIN person AS p ON ap.person_id = p.person_id
WHERE ap.IBAN = 'US81BANK2096431873'
```
</details>

<!-- blank line -->
----
<!-- blank line -->

>
> Did we find our murderer? Continue with 'Complex joins' to find out!
> 