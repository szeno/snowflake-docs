# DROP SEQUENCE

Removes a sequence from the current/specified schema.

See also:
:   [CREATE SEQUENCE](/sql-reference/sql/create-sequence) , [ALTER SEQUENCE](/sql-reference/sql/alter-sequence) , [SHOW SEQUENCES](/sql-reference/sql/show-sequences) , [DESCRIBE SEQUENCE](/sql-reference/sql/desc-sequence)

## Syntax

Copy code

```
DROP SEQUENCE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Parameters

`name`
:   Specifies the identifier of the sequence to drop.

    If the sequence identifier is not fully-qualified (in the form of `db_name.schema_name.sequence_name` or
    `schema_name.sequence_name`), the command looks for the sequence in the current schema for the session.

`CASCADE | RESTRICT`
:   Snowflake allows the keywords `CASCADE` and `RESTRICT` syntactically, but does not act on them. For example,
    dropping a sequence with the `CASCADE` keyword does not actually drop a table that uses the sequence.
    Dropping a sequence with the `RESTRICT` keyword does not issue a warning if a table is still using the sequence.

## Usage notes

- To drop a sequence, you must be using a role that has ownership privilege on the sequence.
- After dropping a sequence, creating a sequence with the same name creates a new version of the sequence. The
  new sequence does not resume generating numbers where the old sequence left off.
- Before dropping a sequence, verify that no tables or other database objects reference the sequence.
- If the dropped sequence was referenced in the `DEFAULT` clause of a table, then calling `GET_DDL()` for that
  table results in an error, rather than in the DDL that created the table.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop a sequence:

> Copy code
>
> ```
> DROP SEQUENCE IF EXISTS invoice_sequence_number;
> ```
