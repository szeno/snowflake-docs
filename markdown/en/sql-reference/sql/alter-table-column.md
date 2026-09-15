# ALTER TABLE … ALTER COLUMN

This topic describes how to modify one or more column properties for a table using an `ALTER COLUMN` clause in a
[ALTER TABLE](/sql-reference/sql/alter-table) statement.

The following table describes the supported/unsupported actions for modifying column properties:

| Action | Supported | Unsupported | Notes |
| --- | --- | --- | --- |
| **Default Values** |  |  |  |
| Drop the default for a column (i.e. `DROP DEFAULT`). | ✔ |  | Not allowed if the column and default were defined by an ALTER TABLE command. For details, see the [Usage Notes](#label-alter-table-column-usage-notes) below. |
| Change the default sequence for a column (i.e. `SET DEFAULT seq_name.NEXTVAL`). | ✔ |  | Use only for columns that have a sequence already. |
| Change the default for a column, unless the default is a sequence. |  | ✔ |  |
| Add a default for a column. |  | ✔ |  |
| **Nullability** |  |  |  |
| Change the nullability of a column (i.e. `SET NOT NULL` or `DROP NOT NULL`). | ✔ |  |  |
| **Data Types** |  |  |  |
| Change a column [data type](/sql-reference-data-types) to a synonymous type (for example, `STRING` to `VARCHAR`). | ✔ |  |  |
| Change a column [data type](/sql-reference-data-types) to a different type (for example, `STRING` to `NUMBER`). |  | ✔ |  |
| Increase the length of a [text string column](/sql-reference/data-types-text#label-character-datatypes) (for example, `VARCHAR(50)` to `VARCHAR(100)`). | ✔ |  |  |
| Decrease the length of a [text string column](/sql-reference/data-types-text#label-character-datatypes) (for example, `VARCHAR(50)` to `VARCHAR(25)`). |  | ✔ |  |
| Increase the length of a [binary string column](/sql-reference/data-types-text#label-binary-datatypes) (for example, `BINARY(50)` to `BINARY(100)`). |  | ✔ |  |
| Decrease the length of a [binary string column](/sql-reference/data-types-text#label-binary-datatypes) (for example, `BINARY(50)` to `BINARY(25)`). |  | ✔ |  |
| Increase the precision of a [number column](/sql-reference/data-types-numeric#label-data-type-number) (for example, `NUMBER(10,2)` to `NUMBER(20,2)`). | ✔ |  |  |
| Decrease the precision of a [number column](/sql-reference/data-types-numeric#label-data-type-number) (for example, `NUMBER(20,2)` to `NUMBER(10,2)`). | ✔ |  | Only allowed if the new precision is sufficient to hold all values currently in the column. In addition, decreasing the precision can impact Time Travel (see [Usage Notes](#usage-notes) for details). |
| Change the scale of a [number column](/sql-reference/data-types-numeric#label-data-type-number) (for example, `NUMBER(10,2)` to `NUMBER(10,4)`). |  | ✔ |  |
| **Comments** |  |  |  |
| Set or unset the comment for a column. | ✔ |  |  |
| **Masking Policy** |  |  |  |
| Set or unset a [masking policy](/user-guide/security-column-intro) on a column. | ✔ |  |  |
| **Projection Policy** |  |  |  |
| Set or unset a [projection policy](/user-guide/projection-policies) on a column. | ✔ |  |  |
| **Object Tagging** |  |  |  |
| Set or unset a [tag](/user-guide/object-tagging/introduction) on a column | ✔ |  | A column can support up to 20 tags, and the maximum number of characters for a tag string value is 256. |

Expand

Show lessSee more

See also:
:   [ALTER TABLE](/sql-reference/sql/alter-table) , [CREATE TABLE](/sql-reference/sql/create-table) , [DROP TABLE](/sql-reference/sql/drop-table) , [SHOW TABLES](/sql-reference/sql/show-tables) , [DESCRIBE TABLE](/sql-reference/sql/desc-table)

## Syntax

Copy code

```
ALTER TABLE <name> { ALTER | MODIFY } [ ( ]
                                              [ COLUMN ] <col1_name> DROP DEFAULT
                                            , [ COLUMN ] <col1_name> SET DEFAULT <seq_name>.NEXTVAL
                                            , [ COLUMN ] <col1_name> { [ SET ] NOT NULL | DROP NOT NULL }
                                            , [ COLUMN ] <col1_name> [ [ SET DATA ] TYPE ] <type>
                                            , [ COLUMN ] <col1_name> COMMENT '<string>'
                                            , [ COLUMN ] <col1_name> UNSET COMMENT
                                          [ , [ COLUMN ] <col2_name> ... ]
                                          [ , ... ]
                                      [ ) ]

ALTER TABLE <name> { ALTER | MODIFY } [ COLUMN ] dataGovnPolicyTagAction
```

## Usage notes

- A single ALTER TABLE statement can be used to modify multiple columns in a table. Each change is specified as a clause consisting of the column
  and column property to modify, separated by commas:

  - Use either the `ALTER` or `MODIFY` keyword to initiate the list of clauses (i.e. columns/properties to modify) in the statement.
  - Parentheses can be used for grouping the clauses, but are not required.
  - The `COLUMN` keyword can be specified in each clause, but is not required.
  - The clauses can be specified in any order.
- When setting a column to `NOT NULL`, if the column contains NULL values, an error is returned and no changes are applied to the column.
- Columns that use semi-structured data types (ARRAY, OBJECT, and VARIANT) cannot be set to `NOT NULL`, except when the table is empty. Setting these columns to `NOT NULL` when the table contains rows is not supported and results in an error.
- To change the default sequence for a column, the column must already have a default sequence. You cannot use the command
  `ALTER TABLE ... SET DEFAULT <seq_name>` to add a sequence to a column that does not already have a sequence.
- If you alter a table to add a column with a `DEFAULT` value, then you cannot drop the default value for that column.
  For example, in the following sequence of statements, the last `ALTER TABLE ... ALTER COLUMN` statement causes an error:

  Copy code

  ```
  CREATE TABLE t(x INT);
  INSERT INTO t VALUES (1), (2), (3);
  ALTER TABLE t ADD COLUMN y INT DEFAULT 100;
  INSERT INTO t(x) VALUES (4), (5), (6);

  ALTER TABLE t ALTER COLUMN y DROP DEFAULT;
  ```

  This restriction prevents inconsistency between values in rows inserted before the column was added and
  rows inserted after the column was added. If the default were dropped, then the column would contain:

  - A NULL value for rows inserted before the column was added.
  - The default value for rows inserted after the column was added.

  Dropping the default column value from any clone of the table is also prohibited.
- When setting the `TYPE` for a column, the specified type (i.e. `type`) must be
  [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) or a [text data type](/sql-reference/data-types-text) (VARCHAR,
  STRING, TEXT, etc.).

  - For the NUMBER data type, `TYPE` can be used to:

    - Increase the precision of the specified number column.
    - Decrease the precision of the specified number column if the new precision is sufficient to hold
      all data values currently in the column.
  - For text data types, `TYPE` can be used only to increase the length of the column.
- If the precision of a column is decreased below the maximum precision of any column data retained in Time Travel, you cannot restore the
  table without first increasing the precision.
- For [interactive tables](/user-guide/interactive), currently the only clauses that you can
  use with the ALTER TABLE MODIFY COLUMN command are COMMENT and UNSET COMMENT.

- For masking policies:
  - The `USING` clause and the `FORCE` keyword are both optional; neither are required to set a masking policy on a column. The
    `USING` clause and the `FORCE` keyword can be used separately or together. For details, see:

    - [Apply a conditional masking policy on a column](/user-guide/security-column-intro#label-security-column-intro-apply-cond-cols)
    - [Replace a masking policy on a column](/user-guide/security-column-intro#label-security-column-intro-replace-policy)
  - A single masking policy that uses conditional columns can be applied to multiple tables provided that the column structure of the table
    matches the columns specified in the policy.
  - When modifying one or more table columns with a masking policy or the table itself with a row access policy, use the
    [POLICY\_CONTEXT](/sql-reference/functions/policy_context) function to simulate a query on the column(s) protected by a masking policy and the
    table protected by a row access policy.

- Regarding metadata (for example, the `COMMENT` field):

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Example setup:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE t1 (
>    c1 NUMBER NOT NULL,
>    c2 NUMBER DEFAULT 3,
>    c3 NUMBER DEFAULT seq1.nextval,
>    c4 VARCHAR(20) DEFAULT 'abcde',
>    c5 STRING);
>
> DESC TABLE t1;
>
> +------+-------------------+--------+-------+-------------------------+-------------+------------+-------+------------+---------+
> | name | type              | kind   | null? | default                 | primary key | unique key | check | expression | comment |
> |------+-------------------+--------+-------+-------------------------+-------------+------------+-------+------------+---------|
> | C1   | NUMBER(38,0)      | COLUMN | N     | NULL                    | N           | N          | NULL  | NULL       | NULL    |
> | C2   | NUMBER(38,0)      | COLUMN | Y     | 3                       | N           | N          | NULL  | NULL       | NULL    |
> | C3   | NUMBER(38,0)      | COLUMN | Y     | DB1.PUBLIC.SEQ1.NEXTVAL | N           | N          | NULL  | NULL       | NULL    |
> | C4   | VARCHAR(20)       | COLUMN | Y     | 'abcde'                 | N           | N          | NULL  | NULL       | NULL    |
> | C5   | VARCHAR(16777216) | COLUMN | Y     | NULL                    | N           | N          | NULL  | NULL       | NULL    |
> +------+-------------------+--------+-------+-------------------------+-------------+------------+-------+------------+---------+
> ```

Make the following changes to `t1`:

> - Change NOT NULL column `c1` to NULL.
> - Drop the default for column `c2` and change the default sequence for column `c3`.
> - Increase the length of column `c4` and drop the default for the column.
> - Add a comment for column `c5`.
>
> Copy code
>
> ```
> ALTER TABLE t1 ALTER COLUMN c1 DROP NOT NULL;
>
> ALTER TABLE t1 MODIFY c2 DROP DEFAULT, c3 SET DEFAULT seq5.nextval ;
>
> ALTER TABLE t1 ALTER c4 SET DATA TYPE VARCHAR(50), COLUMN c4 DROP DEFAULT;
>
> ALTER TABLE t1 ALTER c5 COMMENT '50 character column';
>
> DESC TABLE t1;
>
> +------+-------------------+--------+-------+-------------------------+-------------+------------+-------+------------+---------------------+
> | name | type              | kind   | null? | default                 | primary key | unique key | check | expression | comment             |
> |------+-------------------+--------+-------+-------------------------+-------------+------------+-------+------------+---------------------|
> | C1   | NUMBER(38,0)      | COLUMN | Y     | NULL                    | N           | N          | NULL  | NULL       | NULL                |
> | C2   | NUMBER(38,0)      | COLUMN | Y     | NULL                    | N           | N          | NULL  | NULL       | NULL                |
> | C3   | NUMBER(38,0)      | COLUMN | Y     | DB1.PUBLIC.SEQ5.NEXTVAL | N           | N          | NULL  | NULL       | NULL                |
> | C4   | VARCHAR(50)       | COLUMN | Y     | NULL                    | N           | N          | NULL  | NULL       | NULL                |
> | C5   | VARCHAR(16777216) | COLUMN | Y     | NULL                    | N           | N          | NULL  | NULL       | 50 character column |
> +------+-------------------+--------+-------+-------------------------+-------------+------------+-------+------------+---------------------+
> ```

Same as previous example, but with the following changes to illustrate the versatility/flexibility of the command:

> - All actions executed in a single `ALTER COLUMN` clause.
> - The order of the columns within the clause is different.
> - `SET DATA TYPE` shortened to simply `TYPE`.
>
> Copy code
>
> ```
> ALTER TABLE t1 ALTER (
>    c1 DROP NOT NULL,
>    c5 COMMENT '50 character column',
>    c4 TYPE VARCHAR(50),
>    c2 DROP DEFAULT,
>    COLUMN c4 DROP DEFAULT,
>    COLUMN c3 SET DEFAULT seq5.nextval
>   );
> ```
>
> This example produces the same results.

Apply a Column-level Security masking policy to a table column:

> Copy code
>
> ```
> -- single column
>
> ALTER TABLE empl_info MODIFY COLUMN empl_id SET MASKING POLICY mask_empl_id;
>
> -- multiple columns
>
> ALTER TABLE empl_info MODIFY
>     COLUMN empl_id SET MASKING POLICY mask_empl_id
>   , COLUMN empl_dob SET MASKING POLICY mask_empl_dob
> ;
> ```

Unset a Column-level Security masking policy from a table column:

> Copy code
>
> ```
> -- single column
>
> ALTER TABLE empl_info modify column empl_id unset masking policy;
>
> -- multiple columns
>
> ALTER TABLE empl_info MODIFY
>     COLUMN empl_id UNSET MASKING POLICY
>   , COLUMN empl_dob UNSET MASKING POLICY
> ;
> ```
