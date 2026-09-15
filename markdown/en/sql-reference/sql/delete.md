# DELETE

Remove rows from a table. You can use a WHERE clause to specify which rows should be removed. If you need to use a subquery(s) or
additional table(s) to identify the rows to be removed, specify the subquery(s) or table(s) in a USING clause.

Important

Unlike [TRUNCATE TABLE](/sql-reference/sql/truncate-table), this command does not delete the external file load history. If you delete rows
loaded into the table from a staged file, you cannot load the data from that file again unless you modify the file and stage it again.

## Syntax

Copy code

```
DELETE FROM <table_name>
            [ USING <additional_table_or_query> [, <additional_table_or_query> ] ]
            [ WHERE <condition> ]
```

## Required parameters

`table_name`
:   Specifies the table from which rows are removed.

## Optional parameters

`USING additional_table_or_query [, ... ]`
:   If you need to refer to additional tables in the WHERE clause to help identify the rows to be removed, then specify those table names in
    the USING clause. You can also use the USING clause to specify subqueries that identify the rows to be removed.

    If you specify a subquery, then put the subquery in parentheses.

    If you specify more than one table or query, use a comma to separate them.

`WHERE condition`
:   Specifies a condition to use to select rows for removal. If this parameter is omitted, all rows in the table are removed, but the table
    remains.

## Usage notes

- When deleting based on a JOIN (by specifying a `USING` clause), it is possible that a row in the target table joins against several
  rows in the `USING` table(s). If the DELETE condition is satisfied for any of the joined combinations, the target row is deleted.

  For example, given tables `tab1` and `tab2` with columns `(k number, v number)`:

  Copy code

  ```
  select * from tab1;

  -------+-------+
  k   |   v   |
  -------+-------+
  0   |   10  |
  -------+-------+

  Select * from tab2;

  -------+-------+
  k   |   v   |
  -------+-------+
  0   |   20  |
  0   |   30  |
  -------+-------+
  ```

  If you run the following query, the row in `tab1` is joined against both rows of `tab2`:

  Copy code

  ```
  DELETE FROM tab1 USING tab2 WHERE tab1.k = tab2.k
  ```

  Because at least one joined pair satisfies the condition, the row is deleted. As a result, after the statement completes, `tab1`
  is empty.

## Examples

Suppose that an organization that leases bicycles uses the following tables:

- The table named leased\_bicycles lists the bicycles that were leased out.
- The table named returned\_bicycles lists bicycles that have been returned recently. These bicycles need be removed from the table of
  leased bicycles.

Create tables:

> Copy code
>
> ```
> CREATE TABLE leased_bicycles (bicycle_id INTEGER, customer_id INTEGER);
> CREATE TABLE returned_bicycles (bicycle_id INTEGER);
> ```

Load data:

> Copy code
>
> ```
> INSERT INTO leased_bicycles (bicycle_ID, customer_ID) VALUES
>     (101, 1111),
>     (102, 2222),
>     (103, 3333),
>     (104, 4444),
>     (105, 5555);
> INSERT INTO returned_bicycles (bicycle_ID) VALUES
>     (102),
>     (104);
> ```

This example shows how to use the `WHERE` clause to delete a specified row(s). This example deletes by bicycle\_ID:

> Copy code
>
> ```
> DELETE FROM leased_bicycles WHERE bicycle_ID = 105;
> +------------------------+
> | number of rows deleted |
> |------------------------|
> |                      1 |
> +------------------------+
> ```

Show the data after the delete:

> Copy code
>
> ```
> SELECT * FROM leased_bicycles ORDER BY bicycle_ID;
> +------------+-------------+
> | BICYCLE_ID | CUSTOMER_ID |
> |------------+-------------|
> |        101 |        1111 |
> |        102 |        2222 |
> |        103 |        3333 |
> |        104 |        4444 |
> +------------+-------------+
> ```

This example shows how to use the `USING` clause to specify rows to be deleted. This `USING` clause specifies the returned\_bicycles
table, which lists the IDs of the bicycles to be deleted from the leased\_bicycles table. The `WHERE` clause joins the leased\_bicycles
table to the returned\_bicycles table, and the rows in leased\_bicycles that have the same bicycle\_ID as the corresponding rows in
returned\_bicycles are deleted.

> Copy code
>
> ```
> BEGIN WORK;
> DELETE FROM leased_bicycles 
>     USING returned_bicycles
>     WHERE leased_bicycles.bicycle_ID = returned_bicycles.bicycle_ID;
> TRUNCATE TABLE returned_bicycles;
> COMMIT WORK;
> ```

(To avoid trying to remove the same rows again in the future when it might be unnecessary or inappropriate, the returned\_bicycles table is
truncated as part of the same transaction.)

Show the data after the delete:

> Copy code
>
> ```
> SELECT * FROM leased_bicycles ORDER BY bicycle_ID;
> +------------+-------------+
> | BICYCLE_ID | CUSTOMER_ID |
> |------------+-------------|
> |        101 |        1111 |
> |        103 |        3333 |
> +------------+-------------+
> ```

Now suppose that another bicycle(s) is returned:

> Copy code
>
> ```
> INSERT INTO returned_bicycles (bicycle_ID) VALUES (103);
> ```

The following query shows a `USING` clause that contains a subquery (rather than a table) to specify which bicycle\_IDs to remove from
the leased\_bicycles table:

> Copy code
>
> ```
> BEGIN WORK;
> DELETE FROM leased_bicycles 
>     USING (SELECT bicycle_ID AS bicycle_ID FROM returned_bicycles) AS returned
>     WHERE leased_bicycles.bicycle_ID = returned.bicycle_ID;
> TRUNCATE TABLE returned_bicycles;
> COMMIT WORK;
> ```

Show the data after the delete:

> Copy code
>
> ```
> SELECT * FROM leased_bicycles ORDER BY bicycle_ID;
> +------------+-------------+
> | BICYCLE_ID | CUSTOMER_ID |
> |------------+-------------|
> |        101 |        1111 |
> +------------+-------------+
> ```
