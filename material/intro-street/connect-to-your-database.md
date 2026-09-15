### Connect to your database

For this workshop, we will use the SQLite database engine. 
It's small enough that it can run in your browser.
This avoids the needs to do a lot of setup.

First, you need a copy of the database we will use. 
Use the following download link and save the file somewhere you can find it back.
It is less than 7Mb.

[Download](./dbadetective-v4-20260915.sqlite)

Next, upload the database again on [sqliteview.com](https://www.sqliteview.com/).
Here you will be able to browse the database, run queries through the "SQL Query Editor" and see the results. 
We will use [sqliteview.com](https://www.sqliteview.com/) throughout this workshop.

<!-- blank line -->
----
<!-- blank line -->

**Check your work:**

In sqliteview, you can look at the list of the tables in the sidebar on the left. You can browse their contents.

You can also write queries. Open the "SQL Query Editor" (item on the left), and enter a query like:

<!-- sql-test: count=164 -->
```sql
SELECT COUNT(*) as count FROM person
```

And click the "Run SQL" Button. This should give you a number as result (`164` for dbadetective-v4).

