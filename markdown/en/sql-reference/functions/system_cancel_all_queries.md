Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$CANCEL\_ALL\_QUERIES

Cancels all active/running queries in the specified session.

See also:
:   [SYSTEM$CANCEL\_QUERY](/sql-reference/functions/system_cancel_query)

## Syntax

Copy code

```
SYSTEM$CANCEL_ALL_QUERIES( <session_id> )
```

## Arguments

`session_id`
:   Identifier for the session for which to cancel all queries. To obtain the ID for a session, log into the web interface as an account administrator (user with the ACCOUNTADMIN role) and go to:

    > **Account** [![Account tab](/static/images/screens/ui-navigation-account-icon.svg)](/static/images/screens/ui-navigation-account-icon.svg) » **Sessions**

## Usage notes

- A user can cancel their own running SQL operations using this SQL function. Canceling running operations executed by another user
  requires a role with one of the following privileges:

  - OWNERSHIP on the user who executed the operation.
  - OPERATE or OWNERSHIP on the warehouse that is running the operation (if applicable).

  Note that the ACCOUNTADMIN role is not necessarily granted any of these privileges.
- This function is not intended for canceling queries for a particular warehouse or user. Instead, use:

  - [ALTER WAREHOUSE … ABORT ALL QUERIES](/sql-reference/sql/alter-warehouse)
  - [ALTER USER … ABORT ALL QUERIES](/sql-reference/sql/alter-user)

## Examples

Copy code

```
SELECT SYSTEM$CANCEL_ALL_QUERIES(1065153872298);

+------------------------------------------+
| SYSTEM$CANCEL_ALL_QUERIES(1065153872298) |
|------------------------------------------|
| 1 cancelled.                             |
+------------------------------------------+
```

For a more detailed, working example, see [Canceling Statements](/user-guide/querying-cancel-statements).
