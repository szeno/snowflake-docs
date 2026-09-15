# USE *<object>*

Specifies the role, warehouse, database, or schema to use for the current session.

## USE commands

For specific syntax, usage notes, and examples, see:

- [USE ROLE](/sql-reference/sql/use-role)
- [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles)
- [USE WAREHOUSE](/sql-reference/sql/use-warehouse)
- [USE DATABASE](/sql-reference/sql/use-database)
- [USE SCHEMA](/sql-reference/sql/use-schema)

## Viewing the current session context

To view the current role, secondary roles, database, schema, and warehouse for the session, use the corresponding context functions.
For example:

Copy code

```
SELECT CURRENT_ROLE(),
       CURRENT_SECONDARY_ROLES(),
       CURRENT_WAREHOUSE(),
       CURRENT_DATABASE(),
       CURRENT_SCHEMA();
```

```
+----------------+--------------------------+---------------------+--------------------+------------------+
| CURRENT_ROLE() | CURRENT_SECONDARY_ROLES  | CURRENT_WAREHOUSE() | CURRENT_DATABASE() | CURRENT_SCHEMA() |
|----------------+--------------------------+---------------------+--------------------+------------------|
| SYSADMIN       | ALL                      | MYWH                | MYTESTDB           | PUBLIC           |
+----------------+--------------------------+---------------------+--------------------+------------------+
```

For more details, see [Context functions](/sql-reference/functions-context).
