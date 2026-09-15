# DESCRIBE TABLE

Describes either the columns in a table or the set of stage properties for the table (current values and default values).

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP TABLE](/sql-reference/sql/drop-table) , [ALTER TABLE](/sql-reference/sql/alter-table) , [CREATE TABLE](/sql-reference/sql/create-table) , [SHOW TABLES](/sql-reference/sql/show-tables)

    [DESCRIBE VIEW](/sql-reference/sql/desc-view)

## Syntax

Copy code

```
{ DESCRIBE | DESC } TABLE <name> [ TYPE =  { COLUMNS | STAGE } ]
```

## Parameters

`name`
:   Specifies the identifier for the table to describe. If the identifier contains spaces or special characters, the entire string must
    be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`TYPE = COLUMNS | STAGE`
:   Specifies whether to display the columns for the table or the set of stage properties for the table (current values and default values).

    Default: `TYPE = COLUMNS`

## Usage notes

- This command does not show the object parameters for a table. Instead, use [SHOW PARAMETERS IN TABLE](/sql-reference/sql/show-parameters).
- DESCRIBE TABLE and [DESCRIBE VIEW](/sql-reference/sql/desc-view) are interchangeable. Both commands return details for the specified table or view; however,
  `TYPE = STAGE` does not apply for views because views do not have stage properties.
- If schema evolution is enabled on the table, the output contains a `schema_evolution_record` column. This column was introduced with the [2023\_08 Bundle (Generally Enabled)](/release-notes/bcr-bundles/2023_08_bundle). For more information, see [Enable automatic table schema evolution](/user-guide/data-load-schema-evolution).
- The output includes a `policy name` column to indicate the [masking policy](/user-guide/security-column-intro) set directly on the
  column. If the column is protected by a [tag-based masking policy](/user-guide/tag-based-masking-policies), Snowflake returns
  `NULL`.

  If a masking policy is not set directly on the column or if the Snowflake account is not Enterprise Edition or higher, Snowflake returns
  `NULL`.
- The output includes a `privacy domain` column to indicate the [privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains)
  set on the column.

  If a privacy domain is not set on the column or if the Snowflake account is not Enterprise Edition or higher, Snowflake returns
  `NULL`.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Output

When `TYPE = COLUMNS`, the command output provides the following properties and metadata:

| Column | Description |
| --- | --- |
| `name` | Name of the column in the table. |
| `type` | Data type of the column in the table. If [collation](/sql-reference/collation) has been specified for the column, the collation specification is included. |
| `kind` | The kind of column: `COLUMN` for regular columns or `VIRTUAL` for virtual columns defined by an expression. |
| `null?` | Whether the column accepts NULL values (`Y` or `N`). |
| `default` | The default value for the column, if any (otherwise `NULL`). |
| `primary key` | Whether the column is the primary key (or part of a multi-column primary key; `Y` or `N`). |
| `unique key` | Whether the column has a UNIQUE constraint (`Y` or `N`). |
| `check` | Reserved for future use. |
| `expression` | The SQL expression that defines a virtual column. NULL for non-virtual columns. |
| `comment` | The comment set for the column, if any (otherwise `NULL`). |
| `policy name` | The [masking policy](/sql-reference/sql/create-masking-policy) set for the column, if any (otherwise `NULL`). |
| `privacy domain` | The [privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains) set for the column, if any (otherwise `NULL`). |
| `schema_evolution_record` | Records information about the latest triggered Schema Evolution for a given table column. This column contains the following subfields:   - EvolutionType: The type of the triggered schema evolution (ADD\_COLUMN or DROP\_NOT\_NULL). - EvolutionMode: The triggering ingestion mechanism (COPY, SNOWPIPE, or SNOWPIPE\_STREAMING). - FileName: The file name that triggered the evolution (NULL for SNOWPIPE\_STREAMING). - TriggeringTime: The approximate time when the column was evolved. - QueryId or PipeId: A unique identifier of the triggering query or pipe (QUERY ID for COPY, PIPE ID for SNOWPIPE, or NULL for SNOWPIPE\_STREAMING). - Pipe name: Fully qualified pipe name that triggered schema evolution (SNOWPIPE\_STREAMING only). - Channel name: Channel that triggered schema evolution (SNOWPIPE\_STREAMING only). - offsetTokenUpperBound: An offset at or before which schema evolution was triggered (SNOWPIPE\_STREAMING only). |

Expand

Show lessSee more

When `TYPE = STAGE`, the command output provides the current and default values for the table’s stage properties. See
[Example: Describe stage properties](#label-desc-table-stage-output).

## Examples

The following examples show how to describe tables.

### Example: Describe a table that has constraints and other column attributes

Create a table with five columns, two with constraints. Give one column a DEFAULT value and a
comment.

Copy code

```
CREATE OR REPLACE TABLE desc_example(
  c1 INT PRIMARY KEY,
  c2 INT,
  c3 INT UNIQUE,
  c4 VARCHAR(30) DEFAULT 'Not applicable' COMMENT 'This column is rarely populated',
  c5 VARCHAR(100));
```

Describe the columns in the table:

Copy code

```
DESCRIBE TABLE desc_example;
```

```
+------+--------------+--------+-------+------------------+-------------+------------+-------+------------+---------------------------------+-------------+----------------+-------------------------+
| name | type         | kind   | null? | default          | primary key | unique key | check | expression | comment                         | policy name | privacy domain | schema evolution record |
|------+--------------+--------+-------+------------------+-------------+------------+-------+------------+---------------------------------+-------------+----------------+-------------------------|
| C1   | NUMBER(38,0) | COLUMN | N     | NULL             | Y           | N          | NULL  | NULL       | NULL                            | NULL        | NULL           | NULL                    |
| C2   | NUMBER(38,0) | COLUMN | Y     | NULL             | N           | N          | NULL  | NULL       | NULL                            | NULL        | NULL           | NULL                    |
| C3   | NUMBER(38,0) | COLUMN | Y     | NULL             | N           | Y          | NULL  | NULL       | NULL                            | NULL        | NULL           | NULL                    |
| C4   | VARCHAR(30)  | COLUMN | Y     | 'Not applicable' | N           | N          | NULL  | NULL       | This column is rarely populated | NULL        | NULL           | NULL                    |
| C5   | VARCHAR(100) | COLUMN | Y     | NULL             | N           | N          | NULL  | NULL       | NULL                            | NULL        | NULL           | NULL                    |
+------+--------------+--------+-------+------------------+-------------+------------+-------+------------+---------------------------------+-------------+----------------+-------------------------+
```

### Example: Describe a table that has a masking policy on a column

Create a [normal masking policy](/sql-reference/sql/create-masking-policy#label-create-masking-policy-normal), then recreate the `desc_example` table with the masking policy set on one column. (To run this example, create the `email_mask` masking policy first.)

Copy code

```
CREATE OR REPLACE TABLE desc_example(
  c1 INT PRIMARY KEY,
  c2 INT,
  c3 INT UNIQUE,
  c4 VARCHAR(30) DEFAULT 'Not applicable' COMMENT 'This column is rarely populated',
  c5 VARCHAR(100) WITH MASKING POLICY email_mask);
```

```
+------+--------------+--------+-------+------------------+-------------+------------+-------+------------+---------------------------------+---------------------------------+----------------+-------------------------+
| name | type         | kind   | null? | default          | primary key | unique key | check | expression | comment                         | policy name                     | privacy domain | schema evolution record |
|------+--------------+--------+-------+------------------+-------------+------------+-------+------------+---------------------------------+---------------------------------+----------------|-------------------------|
| C1   | NUMBER(38,0) | COLUMN | N     | NULL             | Y           | N          | NULL  | NULL       | NULL                            | NULL                            | NULL           | NULL                    |
| C2   | NUMBER(38,0) | COLUMN | Y     | NULL             | N           | N          | NULL  | NULL       | NULL                            | NULL                            | NULL           | NULL                    |
| C3   | NUMBER(38,0) | COLUMN | Y     | NULL             | N           | Y          | NULL  | NULL       | NULL                            | NULL                            | NULL           | NULL                    |
| C4   | VARCHAR(30)  | COLUMN | Y     | 'Not applicable' | N           | N          | NULL  | NULL       | This column is rarely populated | NULL                            | NULL           | NULL                    |
| C5   | VARCHAR(100) | COLUMN | Y     | NULL             | N           | N          | NULL  | NULL       | NULL                            | HT_SENSORS.HT_SCHEMA.EMAIL_MASK | NULL           | NULL                    |
+------+--------------+--------+-------+------------------+-------------+------------+-------+------------+---------------------------------+---------------------------------+----------------+-------------------------+
```

### Example: Describe stage properties

Describe the current stage properties for the same table (only the first five rows are shown here):

Copy code

```
DESCRIBE TABLE desc_example TYPE = STAGE;
```

```
+--------------------+--------------------------------+---------------+-----------------+------------------+
| parent_property    | property                       | property_type | property_value  | property_default |
|--------------------+--------------------------------+---------------+-----------------+------------------|
| STAGE_FILE_FORMAT  | TYPE                           | String        | CSV             | CSV              |
| STAGE_FILE_FORMAT  | RECORD_DELIMITER               | String        | \n              | \n               |
| STAGE_FILE_FORMAT  | FIELD_DELIMITER                | String        | ,               | ,                |
| STAGE_FILE_FORMAT  | FILE_EXTENSION                 | String        |                 |                  |
| STAGE_FILE_FORMAT  | SKIP_HEADER                    | Integer       | 0               | 0                |
...
```
