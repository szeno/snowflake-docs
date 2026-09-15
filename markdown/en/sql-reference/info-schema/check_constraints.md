# CHECK\_CONSTRAINTS view

This Information Schema view displays a row for each [CHECK constraint](/sql-reference/constraints-overview#label-constraints-check)
defined in the specified or current database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CONSTRAINT\_CATALOG | VARCHAR | Database that the CHECK constraint belongs to. |
| CONSTRAINT\_SCHEMA | VARCHAR | Schema that the CHECK constraint belongs to. |
| CONSTRAINT\_TABLE | VARCHAR | Table or view that the CHECK constraint belongs to. |
| CONSTRAINT\_NAME | VARCHAR | Name of the constraint with the CHECK clause. |
| CHECK\_CLAUSE | VARCHAR | Condition enforced by the CHECK constraint. |

Expand

Show lessSee more

## Usage notes

The view only displays objects for which the current role for the session has been granted access privileges.

## Examples

Retrieve all of the CHECK constraints applied to tables in the `mydb` database:

Copy code

```
USE DATABASE mydb;

SELECT * FROM INFORMATION_SCHEMA.CHECK_CONSTRAINTS;
```
