Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$CANCEL\_QUERY

Cancels the specified query (or statement) if it is currently active/running.

See also:
:   [SYSTEM$CANCEL\_ALL\_QUERIES](/sql-reference/functions/system_cancel_all_queries)

## Syntax

Copy code

```
SYSTEM$CANCEL_QUERY( <query_id> )
```

## Arguments

`query_id`
:   Identifier for the query to cancel. To obtain the ID for a query executed within the last 14 days, log into the web interface and go to the **History** [![History tab](/static/images/screens/ui-navigation-history-icon.svg)](/static/images/screens/ui-navigation-history-icon.svg) page.

## Usage notes

- A user can cancel their own running SQL operations using this SQL function. Canceling running operations executed by another user
  requires a role with one of the following privileges:

  - OWNERSHIP on the user who executed the operation.
  - OPERATE or OWNERSHIP on the warehouse that is running the operation (if applicable).
  - ACCOUNTADMIN role.
- For a query run by a [task](/user-guide/tasks-intro), canceling running operations requires a role with one of the following privileges:

  - OPERATE or OWNERSHIP on the task that is running the operation.
  - ACCOUNTADMIN role.
- Snowflake query IDs are UUID text strings with hyphens, which are special characters, so the strings must be escaped by using single quotes.
- This function is not intended for canceling queries for a particular warehouse or user. Instead, use:

  - [ALTER WAREHOUSE … ABORT ALL QUERIES](/sql-reference/sql/alter-warehouse)
  - [ALTER USER … ABORT ALL QUERIES](/sql-reference/sql/alter-user)

## Examples

Copy code

```
SELECT SYSTEM$CANCEL_QUERY('d5493e36-5e38-48c9-a47c-c476f2111ce5');

+-------------------------------------------------------------+
| SYSTEM$CANCEL_QUERY('D5493E36-5E38-48C9-A47C-C476F2111CE5') |
|-------------------------------------------------------------|
| query [d5493e36-5e38-48c9-a47c-c476f2111ce5] terminated.    |
+-------------------------------------------------------------+
```
