# CREATE INTEGRATION

Creates a new integration in the system or replaces an existing integration. An integration is a Snowflake object that provides an
interface between Snowflake and third-party services.

See also:
:   [ALTER INTEGRATION](/sql-reference/sql/alter-integration), [DROP INTEGRATION](/sql-reference/sql/drop-integration), [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] <integration_type> INTEGRATION [ IF NOT EXISTS ] <object_name>
  [ <integration_type_params> ]
  [ COMMENT = '<string_literal>' ]
```

Where `integration_type_params` are specific to the integration type.

For specific syntax, usage notes, and examples, see:

- [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)
- [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration)
- [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration)
- [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration)
- [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration)
- [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)

## General usage notes

- `OR REPLACE` and `IF NOT EXISTS` clauses are mutually exclusive; they cannot both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
