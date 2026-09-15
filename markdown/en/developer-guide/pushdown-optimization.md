# Pushdown Optimization and Data Visibility

Through the pushdown optimization, Snowflake helps make query processing faster and more efficient by filtering rows. However, due to the
way filters can be reordered, pushdown can expose data that you might not want to be visible.

This topic describes pushdown and how it can expose sensitive data. To prevent sensitive data from becoming visible, you can make a
UDF secure as described in [Protecting Sensitive Information with Secure UDFs and Stored Procedures](/developer-guide/secure-udf-procedure).

## What is Pushdown?

Pushdown improves performance by filtering out unneeded rows as early as possible during query processing. Pushdown can also reduce memory
consumption. However, pushdown can allow confidential data to be exposed indirectly.

Consider the following query:

Copy code

```
SELECT col1
  FROM tab1
  WHERE location = 'New York';
```

One approach to processing the query is:

1. Read all rows from the table into memory (i.e. execute the FROM clause).
2. Scan the rows in memory, filtering out any rows that do not match `New York` (i.e. execute the WHERE clause).
3. Select `col1` from the rows still remaining in memory (i.e. execute the SELECT list).

You can think of this as a “load first, filter later” strategy, which is straight-forward, but inefficient.

It’s usually more efficient to filter as early as possible. Early filtering is called “pushing the filter down deeper into the query plan”,
or simply “pushdown”.

In example query above, it would be more efficient to tell the table-scanning code not to load records that don’t match the WHERE clause. This
doesn’t save filtering time (every row’s location must still be read once), but it can save considerable memory and reduce subsequent processing
time because there are fewer rows to process.

In some cases, you can process the data even more efficiently. For example, suppose that the data is partitioned by state (i.e. all the data
for New York is in one micro-partition, all the data for Florida is in another micro-partition, and so on). In this scenario:

- Snowflake does not need to store all the rows in memory.
- Snowflake does not need to read all the rows.

We loosely define this as another form of “pushdown”.

The principle of “pushing down the filters” applies to a wide range of queries. Often, the filter that is the most selective (screens out
the most data) is pushed deepest (executed earliest) to reduce the work that the remaining query must do.

Pushdown can be combined with other techniques, such as clustering (sorting/ordering the data), to reduce the amount of irrelevant data that
needs to be read, loaded, and processed.

## Example of Indirect Data Exposure Through Pushdown

The following example shows one way that pushdown could indirectly result in the exposure of underlying details about a query. This example
focuses on views, but the same principles apply to UDFs.

Suppose there is a table that stores information about patients:

> Copy code
>
> ```
> CREATE TABLE patients
>   (patient_ID INTEGER,
>    category VARCHAR,      -- 'PhysicalHealth' or 'MentalHealth'
>    diagnosis VARCHAR
>    );
>
> INSERT INTO patients (patient_ID, category, diagnosis) VALUES
>   (1, 'MentalHealth', 'paranoia'),
>   (2, 'PhysicalHealth', 'lung cancer');
> ```

There are two views, one of which shows mental health information and one of which shows physical health information:

> Copy code
>
> ```
> CREATE VIEW mental_health_view AS
>   SELECT * FROM patients WHERE category = 'MentalHealth';
>
> CREATE VIEW physical_health_view AS
>   SELECT * FROM patients WHERE category = 'PhysicalHealth';
> ```

Most users don’t have direct access to the table. Instead, users are assigned one of two roles:

- `MentalHealth`, which has privileges to read from `mental_health_view`, or
- `PhysicalHealth`, which has privileges to read from `physical_health_view`.

Now suppose that a doctor with privileges only on physical health data wants to know whether there are currently any mental health patients
in the table. The doctor can construct a query similar to the following:

> Copy code
>
> ```
> SELECT * FROM physical_health_view
>   WHERE 1/IFF(category = 'MentalHealth', 0, 1) = 1;
> ```

This query is equivalent to:

> Copy code
>
> ```
> SELECT * FROM patients
>   WHERE
>     category = 'PhysicalHealth' AND
>     1/IFF(category = 'MentalHealth', 0, 1) = 1;
> ```

There are (at least) two methods that Snowflake can use to process this query.

- Method 1:

  1. Read all the rows in the patients table.
  2. Apply the view’s security filter (i.e. filter out the rows for which the category is not `PhysicalHealth`).
  3. Apply the WHERE clause in the query (i.e. filter based on `WHERE 1/IFF(category = 'MentalHealth', 0, 1) = 1`).
- Method 2 changes the order of the filters, so that the query executes as follows:

  1. Read all the rows in the patients table.
  2. Apply the WHERE clause in the query (i.e. filter based on `WHERE 1/IFF(category = 'MentalHealth', 0, 1) = 1`).
  3. Apply the view’s security filter (i.e. filter out the rows for which the category is not `PhysicalHealth`).

Logically, these two sequences seem equivalent; they return the same set of rows. However, depending on how selective these two filters are,
one order of processing might be faster, and Snowflake’s query planner might choose the plan that executes faster.

Suppose that the optimizer chooses the second plan, in which the clause `WHERE 1/IFF(category = 'MentalHealth', 0, 1) = 1` is executed
before the security filter. If the patients table has any rows in which `category = 'MentalHealth'`, then the `IFF` function returns
0 for that row, and the clause effectively becomes `WHERE 1/0 = 1`, so the statement causes a divide-by-zero error. The user with
`physical_health_view` privileges does not see any rows for people with mental health issues, but can deduce that at least one person in the
mental health category exists.

Note that this technique does not always result in exposing underlying details; it relies heavily on the choices that the query planner makes,
as well as on how the views (or UDFs) are written. But this example shows that a user can deduce information about rows that the user cannot
view directly.
