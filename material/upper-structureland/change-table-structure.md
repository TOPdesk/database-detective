### Change table structure

**Fast track**: In this field, you will practice how to add a new column to an existing table by using `ALTER TABLE`.  
If you are on the fast track, read and execute the Solution to make the change, and read the framed note.

**Exercise 1**: Add a new column called weight_kg to the person table, without dropping and recreating the table.

**Hints**:

* Changing the table structure can be done by using `ALTER TABLE`, which has the following format:

```SQL
ALTER TABLE <tablename>
ADD <columnname> <columntype> <nullability>
```

<details>
<summary>Solution</summary>

<!-- sql-test -->
```sql
ALTER TABLE person
ADD number_of_siblings INT NULL
```
</details>

<br />

| **Note**    |
| ----------- |
| `ALTER TABLE` is a very diverse command, it can change/add new columns, change types, nullability, rename columns etc. | 

**Exercise 2**: Check the new structure visually in the Schema Visualization, and check the table content.
