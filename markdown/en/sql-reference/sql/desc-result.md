# DESCRIBE RESULT

Describes the columns in the result of a query.

Snowflake persists the result of a query for a period of time, after which the result is purged. The query can be from the current session or
any of your other sessions, including past sessions, as long as the limited period has not elapsed. This period is not adjustable. For
more details, see [Using Persisted Query Results](/user-guide/querying-persisted-results).

DESCRIBE can be abbreviated to DESC.

See also:
:   [LAST\_QUERY\_ID](/sql-reference/functions/last_query_id) (Context function) , [RESULT\_SCAN](/sql-reference/functions/result_scan) (Table function)

## Syntax

Copy code

```
DESC[RIBE] RESULT { '<query_id>' | LAST_QUERY_ID() }
```

## Parameters

`query_id` or `LAST_QUERY_ID()`
:   Specifies either the ID for a query you executed (within the last 24 hours in any session) or the
    [LAST\_QUERY\_ID](/sql-reference/functions/last_query_id) function, which returns the ID for a query within your current session.

## Usage notes

- To retrieve the ID for a specific query:
  - Locate the query ID in the web interface. The **History** [![History tab](/static/images/screens/ui-navigation-history-icon.svg)](/static/images/screens/ui-navigation-history-icon.svg) page lists the ID along with each query; however, note
    that you can only use this function for queries you have executed.
  - Execute the [QUERY\_HISTORY , QUERY\_HISTORY\_BY\_\*](/sql-reference/functions/query_history) table function, which returns a list of queries and their IDs; however,
    note that you can only use this function for queries you have executed.
  - If the query was executed in the current session, execute the [LAST\_QUERY\_ID](/sql-reference/functions/last_query_id) function. For example:

    Copy code

    ```
    SELECT LAST_QUERY_ID(-2);
    ```

    Note that this is equivalent to using LAST\_QUERY\_ID() as the input for DESC RESULT.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

Describe the columns in the result of the specified query from any of your sessions (within the previous 24 hours):

> Copy code
>
> ```
> DESC RESULT 'f2f07bdb-6a08-4689-9ad8-a1ba968a44b6';
> ```

Describe the columns in the results from your most recent query in the current session:

> Copy code
>
> ```
> SELECT * FROM boston_sales;
>
> +---------------+-------+-------+--------+-------------+---------------------+-------+
> | CITY          | ZIP   | STATE | SQ__FT | TYPE        | SALE_DATE           | PRICE |
> |---------------+-------+-------+--------+-------------+---------------------+-------|
> | MA-Lexington  | 40502 | MA    |    836 | Residential | 0016-01-25T00:00:00 | 59222 |
> | MA-Belmont    | 02478 | MA    |    852 | Residential | 0016-02-21T00:00:00 | 69307 |
> | MA-Winchester | 01890 | MA    |   1122 | Condo       | 0016-01-31T00:00:00 | 89921 |
> +---------------+-------+-------+--------+-------------+---------------------+-------+
>
> DESC RESULT LAST_QUERY_ID();
>
> +-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+
> | name      | type              | kind   | null? | default | primary key | unique key | check | expression | comment |
> |-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------|
> | CITY      | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    |
> | ZIP       | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    |
> | STATE     | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    |
> | SQ__FT    | NUMBER(38,0)      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    |
> | TYPE      | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    |
> | SALE_DATE | DATE              | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    |
> | PRICE     | NUMBER(38,0)      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    |
> +-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+
> ```
