# ALTER SEQUENCE

Modifies the properties for an existing sequence.

See also:
:   [CREATE SEQUENCE](/sql-reference/sql/create-sequence) , [DROP SEQUENCE](/sql-reference/sql/drop-sequence) , [SHOW SEQUENCES](/sql-reference/sql/show-sequences) , [DESCRIBE SEQUENCE](/sql-reference/sql/desc-sequence)

## Syntax

Copy code

```
ALTER SEQUENCE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER SEQUENCE [ IF EXISTS ] <name> [ SET ] [ INCREMENT [ BY ] [ = ] <sequence_interval> ]

ALTER SEQUENCE [ IF EXISTS ] <name> SET
  [ { ORDER | NOORDER } ]
  [ COMMENT = '<string_literal>' ]

ALTER SEQUENCE [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the sequence to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the sequence; must be unique for the schema.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET...`
:   Specifies the properties to set for the sequence:

    `[ INCREMENT [ BY ] sequence_interval ]`
    :   Specifies the step interval of the sequence:

        - For positive sequence interval `n`, the next `n-1` values are reserved by each sequence call.
        - For negative sequence interval `-n`, the next `n-1` lower values are reserved by each sequence call.

        Supported values are any non-zero value that can be represented by a 64-bit two’s complement integer.

    `{ ORDER | NOORDER }`
    :   Specifies whether or not the values are generated for the sequence in
        [increasing order](/user-guide/querying-sequences#label-querying-sequences-increasing-values).

        - ORDER specifies that the values generated for a sequence or auto-incremented column are in increasing order (or, if the interval
          is a negative value, in decreasing order).

          For example, if a sequence or auto-incremented column has `START 1 INCREMENT 2`, the generated values might be
          `1`, `3`, `5`, `7`, `9`, etc.
        - NOORDER specifies that the values are not guaranteed to be in increasing order.

          For example, if a sequence has `START 1 INCREMENT 2`, the generated values might be `1`, `3`, `101`, `5`, `103`, etc.

          NOORDER can improve performance when multiple INSERT operations are performed concurrently (for example, when multiple
          clients are executing multiple INSERT statements).

        Note

        If a sequence is set to NOORDER, you cannot change the sequence to ORDER.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the sequence.

`UNSET ...`
:   Specifies the properties to unset for the sequence, which resets them to the defaults.

    Currently, the only property you can unset is COMMENT, which removes the comment, if one exists, for the sequence.

## Usage notes

- The first/initial value for a sequence cannot be changed after the sequence is created.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename sequence `myseq` to `newseq`:

Copy code

```
ALTER SEQUENCE myseq RENAME TO newseq;
```

More examples are available in [Using Sequences](/user-guide/querying-sequences).
