# CREATE HYBRID TABLE

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

Creates a new hybrid table in the current/specified schema or replaces an existing table. A table can have multiple columns,
with each column definition consisting of a name, data type, and optionally whether the column:

- Requires a NOT NULL value.
- Has a default value or is an identity column.
- Has any inline constraints.

Note

When you create a hybrid table, you must define a PRIMARY KEY constraint on one or more columns.

You can also use the following CREATE TABLE variants to create hybrid tables:

- [CREATE HYBRID TABLE … AS SELECT (CTAS)](#label-create-hybrid-table-as) (creates a populated table; also referred to as CTAS)
- [CREATE HYBRID TABLE … LIKE](#label-create-hybrid-table-like) (creates an empty copy of an existing hybrid table)

For the full CREATE TABLE syntax used for standard Snowflake tables, see [CREATE TABLE](/sql-reference/sql/create-table).

Tip

Before creating and using hybrid tables, you should become familiar with some
[unsupported features and limitations](/user-guide/tables-hybrid-limitations).

See also:
:   [CREATE INDEX](/sql-reference/sql/create-index) [DROP INDEX](/sql-reference/sql/drop-index), [SHOW INDEXES](/sql-reference/sql/show-indexes), [ALTER TABLE](/sql-reference/sql/alter-table) , [DROP TABLE](/sql-reference/sql/drop-table) , [SHOW TABLES](/sql-reference/sql/show-tables)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] HYBRID TABLE [ IF NOT EXISTS ] <table_name>
  ( <col_name> <col_type>
    [
      {
        DEFAULT <expr>
        | { AUTOINCREMENT | IDENTITY }
          [
            {
              ( <start_num> , <step_num> )
              | START <num> INCREMENT <num>
            }
          ]
          [ { ORDER | NOORDER } ]
      }
    ]
    [ NOT NULL ]
    [ inlineConstraint ]
    [ COLLATE '<collation_specification>' ]
    [ COMMENT '<string_literal>' ]
    [ , <col_name> <col_type> [ ... ] ]
    [ , outoflineConstraint ]
    [ , outoflineIndex ]
    [ , ... ]
  )
  [ COMMENT = '<string_literal>' ]
```

Where:

> Copy code
>
> ```
> inlineConstraint ::=
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE
>     | PRIMARY KEY
>     | { [ FOREIGN KEY ] REFERENCES <ref_table_name> [ ( <ref_col_name> ) ] }
>     | CHECK ( <expr> )
>   }
>   [ <constraint_properties> ]
>
> outoflineConstraint ::=
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE [ ( <col_name> [ , <col_name> , ... ] ) ]
>     | PRIMARY KEY [ ( <col_name> [ , <col_name> , ... ] ) ]
>     | [ FOREIGN KEY ] [ ( <col_name> [ , <col_name> , ... ] ) ]
>       REFERENCES <ref_table_name> [ ( <ref_col_name> [ , <ref_col_name> , ... ] ) ]
>     | CHECK ( <expr> )
>   }
>   [ <constraint_properties> ]
>   [ COMMENT '<string_literal>' ]
>
> outoflineIndex ::=
>   INDEX <index_name> ( <col_name> [ , <col_name> , ... ] )
>     [ INCLUDE ( <col_name> [ , <col_name> , ... ] ) ]
> ```
>
> For inline and out-of-line constraint details, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint).

## Required parameters

`name`
:   Specifies the identifier (i.e. name) for the table; must be unique for the schema in which the table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`col_name`
:   Specifies the column identifier (i.e. name). All the requirements for table identifiers also apply to column identifiers.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax) and [Reserved & limited keywords](/sql-reference/reserved-keywords).

    Note

    In addition to the standard reserved keywords, the following keywords cannot be used as column identifiers because they are reserved for ANSI-standard context functions:

    - `CURRENT_DATE`
    - `CURRENT_ROLE`
    - `CURRENT_TIME`
    - `CURRENT_TIMESTAMP`
    - `CURRENT_USER`

    For the list of reserved keywords, see [Reserved & limited keywords](/sql-reference/reserved-keywords).

`col_type`
:   Specifies the data type for the column.

    For details about the data types that can be specified for table columns, see [SQL data types reference](/sql-reference-data-types).

`PRIMARY KEY ( col_name [ , col_name , ... ] )`
:   Specifies the required primary key constraint for the table, either within a column definition (inline) or separately (out-of-line).
    See also [Constraints for hybrid tables](#label-hybrid-table-notes-on-constraints).

    For complete syntax details, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint). For general information about constraints, see
    [Constraints](/sql-reference/constraints).

## Optional parameters

`DEFAULT ...` or `AUTOINCREMENT ...`
:   Specifies whether a default value is automatically inserted in the column if a value is not explicitly specified via an INSERT or
    CREATE HYBRID TABLE AS SELECT statement:

    > `DEFAULT expr`
    > :   Column default value is defined by the specified expression which can be any of the following:
    >
    >     - Constant value.
    >     - Simple expression.
    >     - Sequence reference (`seq_name.NEXTVAL`).
    >
    >     A simple expression is an expression that returns a scalar value; however, the expression cannot contain
    >     references to:
    >
    >     - Subqueries.
    >     - Aggregates.
    >     - Window functions.
    >     - External functions.
    >
    > `{ AUTOINCREMENT | IDENTITY }` `[ { ( start_num , step_num ) | START num INCREMENT num } ]` `[ { ORDER | NOORDER } ]`
    > :   When `AUTOINCREMENT` is used, the default value for the column starts with a specified number and each successive
    >     value is automatically generated. Values generated by an `AUTOINCREMENT` column are guaranteed to be unique. The
    >     difference between any pair of the generated values is guaranteed to be a multiple of the increment amount.
    >
    >     The optional `ORDER` and `NOORDER` parameters specify whether or not the generated values provide ordering
    >     guarantees as specified in [Sequence Semantics](/user-guide/querying-sequences#label-sequence-semantics). `NOORDER` is the default option for `AUTOINCREMENT`
    >     columns on hybrid tables. `NOORDER` typically provides significantly better performance for point writes.
    >
    >     These parameters can only be used for columns with numeric data types (NUMBER, INT, FLOAT, etc.)
    >
    >     `AUTOINCREMENT` and `IDENTITY` are synonymous. If either is specified for a column, Snowflake utilizes a
    >     sequence to generate the values for the column. For more information about sequences, see
    >     [Using Sequences](/user-guide/querying-sequences).
    >
    >     The default value for both start and step/increment is `1`.

    Default: No value (the column has no default value)

    Note

    - `DEFAULT` and `AUTOINCREMENT` are mutually exclusive; only one can be specified for a column.
    - For performance-sensitive workloads, `NOORDER` is the recommended option for `AUTOINCREMENT` columns.

`CONSTRAINT ...`
:   Defines an inline or out-of-line constraint for the specified column(s) in the table. UNIQUE, FOREIGN KEY, and CHECK
    constraints are optional for hybrid table columns. See also [Constraints for hybrid tables](#label-hybrid-table-notes-on-constraints) and
    [CHECK constraints](#label-hybrid-table-check-constraints).

    For complete syntax details, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint). For general information about constraints, see
    [Constraints](/sql-reference/constraints).

`COLLATE 'collation_specification'`
:   Specifies the collation to use for column operations such as string comparisons. This parameter applies only to
    [text columns](/sql-reference/data-types-text#label-character-datatypes) that are not indexed. For more information,
    see [Collations on hybrid table columns](#label-hybrid-table-collations-disable) and [Collation specifications](/sql-reference/collation#label-collation-specification).

`INDEX index_name ( col_name [ , col_name , ... ]`
:   Specifies a secondary index on one or more columns in the table. (When you define constraints on hybrid table columns,
    indexes are automatically created on those columns.)

    Indexes cannot be defined on the following columns:

    - [Semi-structured columns](/sql-reference/data-types-semistructured) (VARIANT, OBJECT, ARRAY)
      because of space constraints associated with the underlying storage engines for the key of each record.
    - [Geospatial columns](/sql-reference/data-types-geospatial) (GEOGRAPHY, GEOMETRY) or
      [VECTOR columns](/sql-reference/data-types-vector).
    - [TIMESTAMP\_TZ](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations) columns (or [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp)
      columns that resolve to TIMESTAMP\_TZ). TIMESTAMP\_NTZ columns are supported.

    Indexes can be defined when the table is created, or with the CREATE INDEX command. For more information about creating indexes for
    hybrid tables, see [Index hybrid tables](/user-guide/tables-hybrid-index) and [CREATE INDEX](/sql-reference/sql/create-index).

`INCLUDE ( col_name [ , col_name , ... ] )`
:   Specifies one or more included columns for a secondary index. Using included columns with a secondary index is
    particularly useful when queries frequently contain a set of columns in the SELECT list but not in
    the list of WHERE predicates. See [INCLUDE columns](/user-guide/tables-hybrid-index#label-indexes-with-include-columns).

    INCLUDE columns cannot be semi-structured columns (VARIANT, OBJECT, ARRAY) or geospatial columns (GEOGRAPHY, GEOMETRY).

`COMMENT = 'string_literal'`
:   Specifies a comment at the column, constraint, or table level. For details, see [Comments on constraints](/sql-reference/sql/create-table-constraint#label-comments-on-constraints).

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE HYBRID TABLE | Schema | None. |
| SELECT | Table, external table, view | Required on queried tables and/or views only when cloning a table or executing CTAS statements. |
| APPLY | Masking policy, row access policy, tag | Required only when applying a masking policy, row access policy, object tags, or any combination of these [governance](/guides-overview-govern) features when creating tables. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Usage notes

- To recreate or replace a hybrid table, call the [GET\_DDL](/sql-reference/functions/get_ddl) function to see the definition of the
  hybrid table before running a CREATE OR REPLACE HYBRID TABLE command.
- You cannot create hybrid tables that are [temporary or transient](/user-guide/tables-temp-transient). In turn, you cannot
  create hybrid tables within transient schemas or databases.
- A schema cannot contain tables and/or views with the same name. When creating a table:

  - If a view with the same name already exists in the schema, an error is returned and the table is not created.
  - If a table with the same name already exists in the schema, an error is returned and the table is not created, unless the
    optional `OR REPLACE` keyword is included in the command.

  Important

  Using `OR REPLACE` is the equivalent of using [DROP TABLE](/sql-reference/sql/drop-table) on the existing table and then
  creating a new table with the same name.

  Note that the drop and create actions occur in a single atomic operation. This means that any queries concurrent with the
  CREATE OR REPLACE TABLE operation use either the old or new table version.

  Recreating or swapping a table drops its change data.
- The `OR REPLACE` and `IF NOT EXISTS` clauses are mutually exclusive. They can’t both be used in the same statement.
- For information about cloning hybrid tables, see [Clone databases that contain hybrid tables](/user-guide/tables-hybrid-clone).
- Similar to [reserved keywords](/sql-reference/reserved-keywords), ANSI-reserved function names
  ([CURRENT\_DATE](/sql-reference/functions/current_date), [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp), etc.) cannot be used as
  column names.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Constraints for hybrid tables

The following rules apply to constraints that are defined on hybrid tables.

- A hybrid table must be created with a PRIMARY KEY constraint.

  Multi-column (or composite) primary keys are supported. To define a multi-column primary key, use the
  syntax shown in the following example, where the constraint is defined “out of line” and refers to
  multiple columns that were previously defined for the table:

  Copy code

  ```
  CREATE OR REPLACE HYBRID TABLE ht2pk (
    col1 INTEGER NOT NULL,
    col2 INTEGER NOT NULL,
    col3 VARCHAR,
    CONSTRAINT pkey_1 PRIMARY KEY (col1, col2)
    );
  ```
- PRIMARY KEY, UNIQUE, FOREIGN KEY, and CHECK constraints are all enforced on hybrid tables. Setting the NOT ENFORCED
  property on a PRIMARY KEY, UNIQUE, or FOREIGN KEY constraint returns an error. A CHECK constraint accepts
  NOT ENFORCED without returning an error, but Snowflake then creates no constraint at all rather than an unenforced
  one, so don’t use NOT ENFORCED to define an advisory CHECK constraint.
- PRIMARY KEY, UNIQUE, and FOREIGN KEY constraints build their own underlying indexes. The creation of indexes results in
  additional data being stored. Secondary (or covering) indexes can also be defined explicitly when the table is created,
  using the `outoflineIndex` syntax.
- Constraints are enforced at the row level, not at the statement or transaction level (that is, deferred constraints).
- PRIMARY KEY and CHECK constraints can be defined only when the table is created. You can add and drop UNIQUE and
  FOREIGN KEY constraints on an existing hybrid table by using [ALTER TABLE](/sql-reference/sql/alter-table). For more
  information, see [Add and drop constraints on an existing hybrid table](#label-hybrid-table-online-constraints).
- CHECK constraints are enforced on every write. You can rename or drop a CHECK constraint on an existing hybrid
  table, but you can’t add one. For more information, see [CHECK constraints](#label-hybrid-table-check-constraints).
- You cannot alter a column to be UNIQUE. To add a UNIQUE constraint to an existing hybrid table, use the out-of-line
  ALTER TABLE … ADD CONSTRAINT syntax.

The following rules apply specifically to FOREIGN KEY constraints:

- A foreign key in a hybrid table that references a primary key cannot be NULL. If you attempt to
  load a NULL value into a column that has a FOREIGN KEY constraint, the load operation fails with a constraint error.
  See [Create two hybrid tables with a primary-key/foreign-key relationship](#label-hybrid-table-pk-fk-example).
- FOREIGN KEY constraints are supported only among hybrid tables that belong to the same database.
- The referenced table from a FOREIGN KEY constraint cannot be truncated as long as the FOREIGN KEY relationship exists.
- FOREIGN KEY constraints do not support partial matching.
- FOREIGN KEY constraints do not support deferrable behavior.
- FOREIGN KEY constraints only support [RESTRICT and NO ACTION properties](/sql-reference/sql/create-table-constraint#label-properties-fk-constraints-only)
  for DELETE and UPDATE operations.

### CHECK constraints

A CHECK constraint enforces a SQL expression as a condition on the values that can be inserted into or updated in one
or more columns. Hybrid tables enforce CHECK constraints on every write, the same way standard tables do. For general
information about the constraint and its expression rules, see [CHECK constraints](/sql-reference/constraints-overview#label-constraints-check).

The following rules are specific to hybrid tables:

- You can define a CHECK constraint only when you create the table. Every form of CREATE HYBRID TABLE supports the
  constraint, including [CREATE HYBRID TABLE … AS SELECT (CTAS)](#label-create-hybrid-table-as) and [CREATE HYBRID TABLE … LIKE](#label-create-hybrid-table-like). Adding a CHECK
  constraint to an existing hybrid table with ALTER TABLE … ADD CONSTRAINT isn’t supported.
- You can rename or drop an existing CHECK constraint with
  [ALTER TABLE … RENAME CONSTRAINT or ALTER TABLE … DROP CONSTRAINT](/sql-reference/sql/alter-table). Because you
  can’t add a CHECK constraint to an existing hybrid table, dropping one is permanent. To restore the constraint, you
  must re-create the table.
- ALTER TABLE … ALTER CONSTRAINT isn’t supported for a CHECK constraint on a hybrid table, so you can’t change the
  constraint to VALIDATE or NOVALIDATE after you create the table.
- You can’t use [COPY INTO <table>](/sql-reference/sql/copy-into-table) to load a hybrid table that has a CHECK constraint. The
  operation fails. Load the table with [INSERT](/sql-reference/sql/insert) or CREATE HYBRID TABLE … AS SELECT instead.

As with standard tables, an inline CHECK constraint can reference only the column it’s defined on. Define the
constraint out of line to enforce a condition that spans multiple columns.

The following example defines an inline CHECK constraint on a single column and a named out-of-line CHECK constraint
that spans two columns:

Copy code

```
CREATE OR REPLACE HYBRID TABLE orders (
  order_id INTEGER PRIMARY KEY,
  quantity INTEGER CHECK (quantity > 0),
  list_price NUMBER(10,2),
  sale_price NUMBER(10,2),
  CONSTRAINT check_sale_price CHECK (sale_price <= list_price)
  );
```

An INSERT, UPDATE, or MERGE statement that violates either constraint fails, and the row isn’t written:

Copy code

```
INSERT INTO orders VALUES (1, 5, 100.00, 150.00);
```

Because `sale_price` is greater than `list_price`, the statement violates the out-of-line constraint and returns an
error that identifies the constraint by name:

```
Operation on table ORDERS failed because CHECK constraint CHECK_SALE_PRICE,
which requires that sale_price <= list_price, was violated
```

If you don’t name a constraint, Snowflake generates a name for it, and the error message reports that generated name
instead. Naming your CHECK constraints makes these errors easier to interpret.

### Add and drop constraints on an existing hybrid table

You can add and drop UNIQUE and FOREIGN KEY constraints on a hybrid table that’s already in use without taking the
table offline. Snowflake builds the index that backs the constraint in the background, and the table stays available for
SELECT and DML statements while the build runs. This behavior matches the online index builds that
[CREATE INDEX](/sql-reference/sql/create-index) performs.

The following example adds a foreign key to a `player` table that was created without one. For a version of these tables
that declares the foreign key when the table is created, see [Create two hybrid tables with a primary-key/foreign-key relationship](#label-hybrid-table-pk-fk-example).

Copy code

```
ALTER TABLE player ADD CONSTRAINT fk_player_team
  FOREIGN KEY (team_id) REFERENCES team(team_id);
```

#### Track the index build

The ALTER TABLE statement returns as soon as Snowflake accepts the change. Because the build runs in the background, a
successful statement doesn’t mean the constraint is fully built. Use [SHOW INDEXES](/sql-reference/sql/show-indexes) to track the
build:

Copy code

```
SHOW INDEXES IN TABLE player;
```

The `status` column reports `BUILD IN PROGRESS` while the index is being built and `ACTIVE` when the constraint is
fully in place.

Snowflake builds one index at a time for a given hybrid table. If you submit a second ADD CONSTRAINT statement while a
build is still running, the second statement fails with an error that tells you to wait for the current build to finish
or to cancel that build.

#### When existing data violates the constraint

Adding a constraint validates the rows that are already in the table. If any of them violate the new constraint, the
ALTER TABLE statement still succeeds because validation happens during the background build. SHOW INDEXES reports
`BUILD VALIDATION FAILURE` in the `status` column, and the `status_info` column explains that the existing data violates
the constraint.

A constraint left in this state still enforces every new write. Statements that would violate it fail, valid statements
succeed, and TRUNCATE TABLE on a referenced table fails. Only the rows that were already in the table when you added the
constraint remain unvalidated.

SHOW INDEXES is the only command that reports this state. The constraint-oriented metadata doesn’t: SHOW IMPORTED KEYS,
[SHOW PRIMARY KEYS](/sql-reference/sql/show-primary-keys), the [TABLE\_CONSTRAINTS view](/sql-reference/info-schema/table_constraints) view, and
[GET\_DDL](/sql-reference/functions/get_ddl) all list the constraint exactly as they would if it had validated. Check
SHOW INDEXES before you rely on a constraint that you added to a table that already contained rows.

To recover, drop the constraint, correct the offending rows, and add the constraint again:

Copy code

```
ALTER TABLE player DROP CONSTRAINT fk_player_team;

DELETE FROM player
  WHERE team_id NOT IN (SELECT team_id FROM team);

ALTER TABLE player ADD CONSTRAINT fk_player_team
  FOREIGN KEY (team_id) REFERENCES team(team_id);
```

## Collations on hybrid table columns

Collations are not supported on PRIMARY KEY columns and other indexed columns in hybrid tables. However, if you do not intend to
index a column, and the column has a [character data type](/sql-reference/data-types-text#label-character-datatypes), you can specify a COLLATE clause for
that column.

For example:

Copy code

```
CREATE OR REPLACE HYBRID TABLE ht1 (c1 INT PRIMARY KEY, c2 VARCHAR(10) COLLATE 'de');

DESCRIBE TABLE ht1;
```

```
+------+--------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type                     | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+--------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| C1   | NUMBER(38,0)             | COLUMN | N     | NULL    | Y           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| C2   | VARCHAR(10) COLLATE 'de' | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+--------------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

In some cases, you might need to disable collation for hybrid table columns by using the `DEFAULT_DDL_COLLATION = ''` syntax,
which applies to all columns in the table. You might need to do this when a default collation is set at the account level or for all columns
in all tables in a schema or database.

For example:

Copy code

```
ALTER SCHEMA ht SET DEFAULT_DDL_COLLATION = 'de';

CREATE OR REPLACE HYBRID TABLE ht2 (c1 INT PRIMARY KEY, c2 VARCHAR(10),
  INDEX idx_c2 (c2));
```

```
391464 (0A000): SQL compilation error: Collations are not supported on primary keys or indexed columns.
```

Copy code

```
CREATE OR REPLACE HYBRID TABLE ht2 (c1 INT PRIMARY KEY, c2 VARCHAR(10),
  INDEX idx_c2 (c2))
  DEFAULT_DDL_COLLATION = '';
```

```
+---------------------------------+
| status                          |
|---------------------------------|
| Table HT2 successfully created. |
+---------------------------------+
```

Table `ht2` is defined without a collation setting on the indexed column `c2`, despite the fact that
the DEFAULT\_DDL\_COLLATION parameter is set to `'de'` at the schema level.

For general information about collations, see [Collation control](/sql-reference/collation#label-collation-control).

## CREATE HYBRID TABLE … AS SELECT (CTAS)

Creates a new hybrid table that contains the results of a query:

> Copy code
>
> ```
> CREATE [ OR REPLACE ] HYBRID TABLE <table_name> [ ( <col_name> [ <col_type> ] , <col_name> [ <col_type> ] , ... ) ]
>   [ ... ]
>   AS <query>
> ```
>
> Note
>
> When you use a CTAS statement to create a hybrid table, you must define the table schema explicitly. You must specify the
> following table properties in the syntax before the definition of the query:
>
> - Column definitions
> - A PRIMARY KEY constraint
> - Other constraints, as needed (UNIQUE, NOT NULL, FOREIGN KEY, CHECK)
> - Secondary indexes (and any INCLUDE columns)
>
> The schema of the new hybrid table can’t be inferred from a SELECT statement.

The number of column names specified must match the number of [SELECT](/sql-reference/sql/select) list items in the query.

To create the table with rows in a specific order, use an ORDER BY clause at the end of the query.

For information about loading hybrid tables, see [Loading data](/user-guide/tables-hybrid-create#label-create-loading-data).

## CREATE HYBRID TABLE … LIKE

Creates a new hybrid table with the same column definitions as an existing hybrid table, but without copying data from the
existing table.

Column names, types, defaults, constraints, and indexes are copied to the new table:

> Copy code
>
> ```
> CREATE [ OR REPLACE ] HYBRID TABLE <table_name> LIKE <source_hybrid_table>
>   [ ... ]
> ```
>
> Note
>
> CREATE HYBRID TABLE … LIKE only supports another hybrid table as the source table type.
>
> CREATE HYBRID TABLE … LIKE for a table with an auto-increment sequence accessed through a data share is
> not supported.

## Examples

Create a hybrid table in the current database with `customer_id` as the primary key, a unique constraint on `email`,
and a secondary index on `full_name`:

Copy code

```
CREATE HYBRID TABLE mytable (
  customer_id INT AUTOINCREMENT PRIMARY KEY,
  full_name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  extended_customer_info VARIANT,
  INDEX index_full_name (full_name)
);
```

```
+-------------------------------------+
| status                              |
|-------------------------------------|
| Table MYTABLE successfully created. |
+-------------------------------------+
```

Insert a row into this table:

Copy code

```
INSERT INTO mytable (customer_id, full_name, email, extended_customer_info)
  SELECT 100, 'Jane Doe', 'jdoe@example.com',
    parse_json('{"address": "1234 Main St", "city": "San Francisco", "state": "CA", "zip":"94110"}');
```

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       1 |
+-------------------------+
```

The primary key must be unique. For example, if you try to insert the same primary key from the previous example a second time,
the command fails with the following error:

```
200001 (22000): Primary key already exists
```

The email address must also follow the inline UNIQUE constraint. For example, if you attempt to insert two records with the
same email address, the statement fails with the following error:

```
Duplicate key value violates unique constraint "SYS_INDEX_MYTABLE_UNIQUE_EMAIL"
```

View table properties and metadata. Note the value of the `is_hybrid` column:

Copy code

```
SHOW TABLES LIKE 'mytable';
```

```
+-------------------------------+---------+---------------+-------------+-------+-----------+---------+------------+------+-------+--------+----------------+----------------------+-----------------+---------------------+------------------------------+---------------------------+-------------+
| created_on                    | name    | database_name | schema_name | kind  | is_hybrid | comment | cluster_by | rows | bytes | owner  | retention_time | automatic_clustering | change_tracking | search_optimization | search_optimization_progress | search_optimization_bytes | is_external |
|-------------------------------+---------+---------------+-------------+-------+-----------+---------+------------+------+-------+--------+----------------+----------------------+-----------------+---------------------+------------------------------+---------------------------+-------------|
| 2022-02-23 23:53:19.707 +0000 | MYTABLE | MYDB          | PUBLIC      | TABLE | Y         |         |            | NULL |  NULL | MYROLE | 10             | OFF                  | OFF             | OFF                 |                         NULL |                      NULL | N           |
+-------------------------------+---------+---------------+-------------+-------+-----------+---------+------------+------+-------+--------+----------------+----------------------+-----------------+---------------------+------------------------------+---------------------------+-------------+
```

View details for all hybrid tables:

Copy code

```
SHOW HYBRID TABLES;
```

```
+-------------------------------+---------------------------+---------------+-------------+--------------+--------------+------+-------+---------+
| created_on                    | name                      | database_name | schema_name | owner        | datastore_id | rows | bytes | comment |
|-------------------------------+---------------------------+---------------+-------------+--------------+--------------+------+-------+---------|
| 2022-02-24 02:07:31.877 +0000 | MYTABLE                   | DEMO_DB       | PUBLIC      | ACCOUNTADMIN |         2002 | NULL |  NULL |         |
+-------------------------------+---------------------------+---------------+-------------+--------------+--------------+------+-------+---------+
```

Display information about the columns in the table:

Copy code

```
DESCRIBE TABLE mytable;
```

```
+-------------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
| name              | type         | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
|-------------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
| CUSTOMER_ID       | NUMBER(38,0) | COLUMN | N     | NULL    | Y           | N          | NULL  | NULL       | NULL    | NULL        |
| FULL_NAME         | VARCHAR(256) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
| APPLICATION_STATE | VARIANT      | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
+-------------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
```

Select data from the table:

Copy code

```
SELECT customer_id, full_name, email, extended_customer_info
  FROM mytable
  WHERE extended_customer_info['state'] = 'CA';
```

```
+-------------+-----------+------------------+------------------------------+
| CUSTOMER_ID | FULL_NAME | EMAIL            | EXTENDED_CUSTOMER_INFO       |
|-------------+-----------+------------------+------------------------------|
|         100 | Jane Doe  | jdoe@example.com | {                            |
|             |           |                  |   "address": "1234 Main St", |
|             |           |                  |   "city": "San Francisco",   |
|             |           |                  |   "state": "CA",             |
|             |           |                  |   "zip": "94110"             |
|             |           |                  | }                            |
+-------------+-----------+------------------+------------------------------+
```

### Create two hybrid tables with a primary-key/foreign-key relationship

This example shows the creation of two hybrid tables that reference each other. The first table, `team`, has a
PRIMARY KEY constraint on its `team_id` column. The second table, `player`, has a FOREIGN KEY constraint on
its `team_id` column, which references the `team_id` column in the `team` table.

Copy code

```
CREATE OR REPLACE HYBRID TABLE team
  (team_id INT PRIMARY KEY,
  team_name VARCHAR(40),
  stadium VARCHAR(40));

CREATE OR REPLACE HYBRID TABLE player
  (player_id INT PRIMARY KEY,
  first_name VARCHAR(40),
  last_name VARCHAR(40),
  team_id INT,
  FOREIGN KEY (team_id) REFERENCES team(team_id));
```

You can verify that referential integrity is enforced by inserting some rows into both tables. You can also
confirm that NULL values are not allowed in columns defined as foreign keys.

The first insert into the `player` table succeeds as expected. The second insert fails because `3`
does not exist as an ID in the `team` table. The third insert fails because NULL is not allowed as a foreign key.

Copy code

```
INSERT INTO team VALUES (1, 'Bayern Munich', 'Allianz Arena');
INSERT INTO player VALUES (100, 'Harry', 'Kane', 1);
INSERT INTO player VALUES (301, 'Gareth', 'Bale', 3);
```

```
200009 (22000): Foreign key constraint "SYS_INDEX_PLAYER_FOREIGN_KEY_TEAM_ID_TEAM_TEAM_ID" was violated.
```

Copy code

```
INSERT INTO player VALUES (200, 'Tommy', 'Atkins', NULL);
```

```
200009 (22000): Foreign key constraint "SYS_INDEX_PLAYER_FOREIGN_KEY_TEAM_ID_TEAM_TEAM_ID" was violated.
```

Copy code

```
SELECT * FROM team t, player p WHERE t.team_id=p.team_id;
```

```
+---------+---------------+---------------+-----------+------------+-----------+---------+
| TEAM_ID | TEAM_NAME     | STADIUM       | PLAYER_ID | FIRST_NAME | LAST_NAME | TEAM_ID |
|---------+---------------+---------------+-----------+------------+-----------+---------|
|       1 | Bayern Munich | Allianz Arena |       100 | Harry      | Kane      |       1 |
+---------+---------------+---------------+-----------+------------+-----------+---------+
```

A possible workaround for the rejection of NULL in this case is to insert a “dummy” row into the
`team` table with a team ID of `0`. Then you can insert rows into the `player` table that use a
matching placeholder value of `0` instead of NULL. For example:

Copy code

```
INSERT INTO team VALUES (0, 'Unknown', 'Unknown');
INSERT INTO player VALUES (200, 'Tommy', 'Atkins', 0);

SELECT * FROM team t, player p WHERE t.team_id=p.team_id;
```

```
+---------+---------------+---------------+-----------+------------+-----------+---------+
| TEAM_ID | TEAM_NAME     | STADIUM       | PLAYER_ID | FIRST_NAME | LAST_NAME | TEAM_ID |
|---------+---------------+---------------+-----------+------------+-----------+---------|
|       1 | Bayern Munich | Allianz Arena |       100 | Harry      | Kane      |       1 |
|       0 | Unknown       | Unknown       |       200 | Tommy      | Atkins    |       0 |
+---------+---------------+---------------+-----------+------------+-----------+---------+
```

### Create a hybrid table with a comment on the primary key column

Create a hybrid table that includes a comment within the column definition for the primary key.

Copy code

```
CREATE OR REPLACE HYBRID TABLE ht1pk
  (COL1 NUMBER(38,0) NOT NULL COMMENT 'Primary key',
  COL2 NUMBER(38,0) NOT NULL,
  COL3 VARCHAR(16777216),
  CONSTRAINT PKEY_1 PRIMARY KEY (COL1));

DESCRIBE TABLE ht1pk;
```

```
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+-------------+-------------+----------------+
| name | type              | kind   | null? | default | primary key | unique key | check | expression | comment     | policy name | privacy domain |
|------+-------------------+--------+-------+---------+-------------+------------+-------+------------+-------------+-------------+----------------|
| COL1 | NUMBER(38,0)      | COLUMN | N     | NULL    | Y           | N          | NULL  | NULL       | Primary key | NULL        | NULL           |
| COL2 | NUMBER(38,0)      | COLUMN | N     | NULL    | N           | N          | NULL  | NULL       | NULL        | NULL        | NULL           |
| COL3 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL        | NULL        | NULL           |
+------+-------------------+--------+-------+---------+-------------+------------+-------+------------+-------------+-------------+----------------+
```

Note that if you put this comment in the CONSTRAINT clause, the comment will not be visible in the DESCRIBE TABLE output. You can query
the [TABLE\_CONSTRAINTS view](/sql-reference/info-schema/table_constraints) to see complete information about constraints.
