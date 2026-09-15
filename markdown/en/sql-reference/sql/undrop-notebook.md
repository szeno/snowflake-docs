# UNDROP NOTEBOOK

Restores the most recent version of a dropped notebook.

See also:
:   [CREATE NOTEBOOK](/sql-reference/sql/create-notebook) , [ALTER NOTEBOOK](/sql-reference/sql/alter-notebook) , [DROP NOTEBOOK](/sql-reference/sql/drop-notebook) , [SHOW NOTEBOOKS](/sql-reference/sql/show-notebooks) , [DESCRIBE NOTEBOOK](/sql-reference/sql/desc-notebook)

## Syntax

Copy code

```
UNDROP NOTEBOOK <name>
```

## Parameters

`name`
:   Specifies the identifier for the notebook to restore. If the identifier contains spaces or special characters, the entire string must
    be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Notebooks can only be restored to the database and schema that contained the notebook at the time of deletion.
- If a notebook with the same name already exists, an error is returned.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Example

The following example restores the most recent version of a dropped notebook named `mynotebook` (this example builds on the examples
provided for [DROP NOTEBOOK](/sql-reference/sql/drop-notebook)):

Copy code

```
UNDROP NOTEBOOK mynotebook;
```

```
+--------------------------------------------+
| status                                     |
|--------------------------------------------|
| Notebook mynotebook successfully restored. |
+--------------------------------------------+
```
