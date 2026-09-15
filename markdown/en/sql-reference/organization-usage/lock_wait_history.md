Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# LOCK\_WAIT\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view includes the history of [transactions](/sql-reference/transactions) that wait on locks.
For details, see [Analyzing blocked transactions with the LOCK\_WAIT\_HISTORY view](/sql-reference/transactions#label-analyzing-blocked-transactions).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| OBJECT\_ID | NUMBER | Internal/system-generated identifier for the blocking object (such as a table) on which the transaction is waiting for a lock. |
| --- | --- | --- |
| LOCK\_TYPE | VARCHAR | Type of lock. Valid values are `PARTITION`, `STREAM`, `TABLE`, and `ROW`. `ROW` is shown for hybrid table locks. |
| OBJECT\_NAME | VARCHAR | Identifier for the object (such as a table) on which the transaction is waiting for a lock. `ROW` is shown for hybrid table locks. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the object on which the transaction is waiting for a lock. `0` is shown for hybrid tables. |
| SCHEMA\_NAME | VARCHAR | Identifier for the schema of the object on which the transaction is waiting for a lock. NULL is shown for `ROW` locks. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database of the object on which the transaction is waiting for a lock. |
| DATABASE\_NAME | VARCHAR | Identifier for the database of the object on which the transaction is waiting for a lock. |
| QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement that is waiting on the lock. |
| TRANSACTION\_ID | NUMBER | Internal/system-generated [identifier for the transaction](/sql-reference/transactions#label-transaction-id) with the statement that is waiting on the lock. Can be joined with the [query history](/sql-reference/organization-usage/query_history) for additional details about the statements in the transaction. |
| REQUESTED\_AT | TIMESTAMP\_LTZ | Timestamp when the lock was requested by the transaction waiting for the lock. |
| ACQUIRED\_AT | TIMESTAMP\_LTZ | Timestamp when the lock was acquired by the transaction holding the lock. |
| BLOCKER\_QUERIES | VARIANT | JSON array of objects. Each object is a blocker query with the following properties:   - `is_snowflake`: TRUE if the query is a background process run by Snowflake (e.g., automatic maintenance of   materialized views). - `query_id`: Query ID of the current statement in the blocker transaction that blocked the statement. Empty if   `is_snowflake` is true. - `transaction_id`: ID of the blocker transaction. Empty if `is_snowflake` is true.   There may be up to 20 objects in this array. |

Expand

Show lessSee more

## Usage notes

- The first blocker query ID that is returned in the `blocker_queries` array is the ID of the query that was being executed
  in the transaction that holds the lock when the transaction waiting for the lock started waiting.
  Note that it is possible that queries prior to that query in the blocker transaction also acquired the lock and should be investigated.
- Each row in the output represents a transaction waiting on a lock. Note that there may be other transactions ahead
  of that transaction, waiting on the same lock.

## Examples

Find all the blocked transactions that requested locks within the past 24 hours:

Copy code

```
SELECT account_name, query_id, object_name, transaction_id, blocker_queries
  FROM snowflake.organization_usage.alert_history.lock_wait_history
  WHERE requested_at >= DATEADD('hours', -24, CURRENT_TIMESTAMP());
```

For additional examples, see [Analyzing blocked transactions with the LOCK\_WAIT\_HISTORY view](/sql-reference/transactions#label-analyzing-blocked-transactions).
