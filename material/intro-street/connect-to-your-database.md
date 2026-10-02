### Connect to your database

{% if variant == "duckdb" %}
For this workshop, we will use the DuckDB database engine.
It's small enough that it can run in your browser.
This avoids the need to do a lot of setup.

First, you need a copy of the database we will use.
Use the following download link and save the file somewhere you can find it back.
It is about 10Mb.

[Download](./dbadetective-v4-20261001.duckdb)

Next, open [shell.duckdb.org](https://shell.duckdb.org/), DuckDB's own browser-based SQL shell, and open the file you just downloaded there.
Here you will be able to browse the database, run queries through the SQL editor and see the results.
We will use [shell.duckdb.org](https://shell.duckdb.org/) throughout this workshop.

<!-- blank line -->
----
<!-- blank line -->

**Check your work:**

In the shell, you can look at the list of tables and browse their contents.

You can also write queries. Enter a query like:

<!-- sql-test: variant=duckdb; count=164 -->
```sql
SELECT COUNT(*) as count FROM person
```

And run it. This should give you a number as result (`164` for dbadetective-v4).
{% else %}
For this workshop, we will use a shared MS SQL Server database, through SQL Server Management Studio (SSMS).

First, make sure SSMS is installed. See [Intro to MS SQL Management Studio](https://wiki.topdesk.com/index.php?title=Intro_to_MS_SQL_Management_Studio) for installation instructions if you don't have it yet.

Next, connect to the server:

* Open SSMS, and in the "Connect to Server" dialog, enter the server name your workshop host gave you.
* Use the credentials your workshop host gave you (or Windows Authentication, if that's how your server is set up).
* Once connected, find the `dbadetective` database (or whichever name your host used) in the Object Explorer on the left. This is the crime database we'll be querying throughout the workshop.

<!-- blank line -->
----
<!-- blank line -->

**Check your work:**

Open a new query window against the `dbadetective` database, and enter a query like:

<!-- sql-test: variant=mssql; count=164 -->
```sql
SELECT COUNT(*) as count FROM person
```

And execute it. This should give you a number as result (`164` for dbadetective-v4).
{% endif %}
