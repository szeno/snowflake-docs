# Account & session DDL

The following DDL commands are used to view and manage account-level and session operations, including:

- Viewing parameters at multiple levels in the system (account, session, object).
- Setting parameters at the account-level and within a session.
- Using a role, warehouse, database, or schema within a session.
- Using multi-statement transactions within a session.
- Setting and using SQL variables within a session.

## Account parameters & functions

|  |  |
| --- | --- |
| [ALTER ACCOUNT](/sql-reference/sql/alter-account) | For setting parameters at the account-level; can only be performed by users with the ACCOUNTADMIN role. |
| [SHOW FUNCTIONS](/sql-reference/sql/show-functions) | Displays system-defined functions, as well as any user-defined functions. |
| [SHOW PARAMETERS](/sql-reference/sql/show-parameters) | For viewing parameter settings for the account. |

Expand

Show lessSee more

## Accounts

|  |  |
| --- | --- |
| [CREATE ACCOUNT](/sql-reference/sql/create-account) | Used to create accounts in an organization. |
| [DROP ACCOUNT](/sql-reference/sql/drop-account) |  |
| [SHOW ACCOUNTS](/sql-reference/sql/show-accounts) | Lists the accounts in an organization. |
| [SHOW ORGANIZATION ACCOUNTS](/sql-reference/sql/show-organization-accounts) | Use SHOW ACCOUNTS instead. |
| [SHOW REGIONS](/sql-reference/sql/show-regions) |  |
| [UNDROP ACCOUNT](/sql-reference/sql/undrop-account) |  |

Expand

Show lessSee more

## Managed accounts

|  |  |
| --- | --- |
| [CREATE MANAGED ACCOUNT](/sql-reference/sql/create-managed-account) | Currently used to create [reader accounts](/user-guide/data-sharing-reader-create) for providers who wish to share data with non-Snowflake customers. |
| [DROP MANAGED ACCOUNT](/sql-reference/sql/drop-managed-account) |  |
| [SHOW MANAGED ACCOUNTS](/sql-reference/sql/show-managed-accounts) |  |

Expand

Show lessSee more

## Replication and failover/failback

|  |  |
| --- | --- |
| [ALTER CONNECTION](/sql-reference/sql/alter-connection) |  |
| [CREATE CONNECTION](/sql-reference/sql/create-connection) |  |
| [DROP CONNECTION](/sql-reference/sql/drop-connection) |  |
| [SHOW CONNECTIONS](/sql-reference/sql/show-connections) |  |
| [SHOW GLOBAL ACCOUNTS](/sql-reference/sql/show-global-accounts) | Deprecated. Use [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) instead. |
| [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) |  |
| [SHOW REPLICATION DATABASES](/sql-reference/sql/show-replication-databases) |  |

Expand

Show lessSee more

## Session parameters

|  |  |
| --- | --- |
| [ALTER SESSION](/sql-reference/sql/alter-session) | For setting parameters within a session; can be performed by any user. |
| [SHOW PARAMETERS](/sql-reference/sql/show-parameters) | For viewing parameter settings for the session (or account); can also be used to view parameter settings for a specified object. |

Expand

Show lessSee more

## Session context

|  |  |
| --- | --- |
| [USE ROLE](/sql-reference/sql/use-role) | Specifies the primary role to use in the session. |
| [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) | Specifies the secondary roles to use in the session. |
| [USE WAREHOUSE](/sql-reference/sql/use-warehouse) | Specifies the virtual warehouse to use in the session. |
| [USE DATABASE](/sql-reference/sql/use-database) | Specifies the database to use in the session. |
| [USE SCHEMA](/sql-reference/sql/use-schema) | Specifies the schema to use in the session (specified schema must be in the current database for the session). |

Expand

Show lessSee more

See also:
:   [Context functions](/sql-reference/functions-context)

## Queries

|  |  |
| --- | --- |
| [DESCRIBE RESULT](/sql-reference/sql/desc-result) | Describes the columns in the results from a specified query (must have been executed within the last 24 hours). |
| [SHOW LOCKS](/sql-reference/sql/show-locks) | For use with multi-statement transactions. |

Expand

Show lessSee more

## Session transactions

|  |  |
| --- | --- |
| [BEGIN](/sql-reference/sql/begin) | For use with multi-statement transactions. |
| [COMMIT](/sql-reference/sql/commit) | For use with multi-statement transactions. |
| [DESCRIBE TRANSACTION](/sql-reference/sql/desc-transaction) | Describes the state of the transaction (e.g. committed, rolled back, running), etc. |
| [ROLLBACK](/sql-reference/sql/rollback) | For use with multi-statement transactions. |
| [SHOW TRANSACTIONS](/sql-reference/sql/show-transactions) | Lists all running transactions. |

Expand

Show lessSee more

## SQL variables

|  |  |
| --- | --- |
| [SET](/sql-reference/sql/set) | For defining SQL variables in the session. |
| [SHOW VARIABLES](/sql-reference/sql/show-variables) | For showing SQL variables in the session. |
| [UNSET](/sql-reference/sql/unset) | For dropping SQL variables in the session. |

Expand

Show lessSee more
