# CREATE | ALTER TABLE … CONSTRAINT

This topic describes how to create constraints by specifying a CONSTRAINT clause in a
[CREATE TABLE](/sql-reference/sql/create-table), [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table),
or [ALTER TABLE](/sql-reference/sql/alter-table) statement:

- An inline constraint is specified as part of the individual column definition.
- An out-of-line constraint is specified as an independent clause:
  - When creating a table, the clause is part of the column definitions for the table.
  - When altering a table, the clause is specified as an explicit `ADD` action for the table.

For more information, see [Constraints](/sql-reference/constraints).

If you are creating or altering [hybrid tables](/user-guide/tables-hybrid), the syntax for defining constraints is the same; however, the rules and requirements are different.

## Syntax for inline constraints

Copy code

```
CREATE TABLE <name> (
  <col1_name> <col1_type>  [ NOT NULL ] { inlineUniquePK | inlineFK | inlineCH }
  [ , <col2_name> <col2_type> [ NOT NULL ] { inlineUniquePK | inlineFK | inlineCH } ]
  [ , ... ]
)

ALTER TABLE <name> ADD COLUMN
  <col_name> <col_type> [ NOT NULL ] { inlineUniquePK | inlineFK | inlineCH }
```

Where:

> Copy code
>
> ```
> inlineUniquePK ::=
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE | PRIMARY KEY }
>   [ [ NOT ] ENFORCED ]
>   [ [ NOT ] DEFERRABLE ]
>   [ INITIALLY { DEFERRED | IMMEDIATE } ]
>   [ { ENABLE | DISABLE } ]
>   [ { VALIDATE | NOVALIDATE } ]
>   [ { RELY | NORELY } ]
> ```
>
> Copy code
>
> ```
> inlineFK ::=
>   [ CONSTRAINT <constraint_name> ]
>   [ FOREIGN KEY ]
>   REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
>   [ MATCH { FULL | SIMPLE | PARTIAL } ]
>   [ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
>        [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
>   [ [ NOT ] ENFORCED ]
>   [ [ NOT ] DEFERRABLE ]
>   [ INITIALLY { DEFERRED | IMMEDIATE } ]
>   [ { ENABLE | DISABLE } ]
>   [ { VALIDATE | NOVALIDATE } ]
>   [ { RELY | NORELY } ]
> ```
>
> Copy code
>
> ```
> inlineCH ::=
>   [ CONSTRAINT <constraint_name> ] CHECK ( <expr> )
>   [ ENABLE { VALIDATE | NOVALIDATE } ]
> ```

## Syntax for out-of-line constraints

Copy code

```
CREATE TABLE <name> ... (
  <col1_name> <col1_type>
  [ , <col2_name> <col2_type> , ... ]
  [ , { outoflineUniquePK | outoflineFK | outoflineCH } ]
  [ , { outoflineUniquePK | outoflineFK | outoflineCH } ]
  [ , ... ]
)

ALTER TABLE <name> ... ADD { outoflineUniquePK | outoflineFK | outoflineCH }
```

Where:

> Copy code
>
> ```
> outoflineUniquePK ::=
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE | PRIMARY KEY } ( <col_name> [ , <col_name> , ... ] )
>   [ [ NOT ] ENFORCED ]
>   [ [ NOT ] DEFERRABLE ]
>   [ INITIALLY { DEFERRED | IMMEDIATE } ]
>   [ { ENABLE | DISABLE } ]
>   [ { VALIDATE | NOVALIDATE } ]
>   [ { RELY | NORELY } ]
>   [ COMMENT '<string_literal>' ]
> ```
>
> Copy code
>
> ```
> outoflineFK ::=
>   [ CONSTRAINT <constraint_name> ]
>   FOREIGN KEY ( <col_name> [ , <col_name> , ... ] )
>   REFERENCES <ref_table_name> [ ( <ref_col_name> [ , <ref_col_name> , ... ] ) ]
>   [ MATCH { FULL | SIMPLE | PARTIAL } ]
>   [ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
>        [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
>   [ [ NOT ] ENFORCED ]
>   [ [ NOT ] DEFERRABLE ]
>   [ INITIALLY { DEFERRED | IMMEDIATE } ]
>   [ { ENABLE | DISABLE } ]
>   [ { VALIDATE | NOVALIDATE } ]
>   [ { RELY | NORELY } ]
>   [ COMMENT '<string_literal>' ]
> ```
>
> Copy code
>
> ```
> outoflineCH ::=
>   [ CONSTRAINT <constraint_name> ] CHECK ( <expr> )
>   [ ENABLE { VALIDATE | NOVALIDATE } ]
> ```

## Constraint properties

For compatibility with other databases, and for use with hybrid tables, Snowflake provides constraint properties.
The properties that can be specified for a constraint depend on the type:

- Some properties apply to all keys (unique, primary, and foreign).
- Other properties apply only to foreign keys.

Important

For standard Snowflake tables, these properties are provided to facilitate migrating from other databases. They are not
enforced or maintained by Snowflake. This means that the defaults can be changed for these properties, but changing the
defaults results in Snowflake not creating the constraint.

An exception is the RELY property. If you have ensured that the data in your standard tables complies with UNIQUE, PRIMARY
KEY, and FOREIGN KEY constraints, you can set the RELY property for those constraints. See also
[Setting the RELY Constraint Property to Eliminate Unnecessary Joins](/user-guide/join-elimination#label-join-elimination-setting-rely).

If you are creating or altering [hybrid tables](/user-guide/tables-hybrid), the rules and requirements are different.
See [Overview of constraints](/sql-reference/constraints-overview).

Most of the supported constraint properties are ANSI SQL standard properties; however, the following properties are Snowflake extensions:

- ENABLE | DISABLE
- VALIDATE | NOVALIDATE
- RELY | NORELY

You can also define a comment within an out-of-line constraint definition; see [Comments on constraints](#label-comments-on-constraints).

### Properties (for all constraints)

The following properties apply to all constraints (the order of the properties is interchangeable):

Copy code

```
[ NOT ] ENFORCED
[ NOT ] DEFERRABLE
INITIALLY { DEFERRED | IMMEDIATE }
{ ENABLE | DISABLE }
{ VALIDATE | NOVALIDATE }
{ RELY | NORELY }
```

`{ ENFORCED | NOT ENFORCED }`
:   Specifies whether the constraint is enforced in a transaction. For standard tables, NOT NULL and CHECK are the
    only types of constraints that are enforced by Snowflake, regardless of this property.

    For hybrid tables, you can’t set the NOT ENFORCED property on PRIMARY KEY, FOREIGN KEY, and UNIQUE constraints.
    Setting this property results in an “invalid constraint property” error.

    See also [Referential Integrity Constraints](/user-guide/table-considerations#label-table-considerations-referential-integrity-constraints).

    Default: NOT ENFORCED

`{ DEFERRABLE | NOT DEFERRABLE }`
:   Specifies whether, in subsequent transactions, the constraint check can be deferred until the end of the transaction.

    Default: NOT DEFERRABLE

`INITIALLY { DEFERRED | IMMEDIATE }`
:   For DEFERRABLE constraints, specifies whether the check for the constraints can be deferred, starting from the next transaction.

    Default: INITIALLY DEFERRED

`{ ENABLE | DISABLE }`
:   Specifies whether the constraint is enabled or disabled. These properties are provided for compatibility with Oracle.

    Default: DISABLE

`{ VALIDATE | NOVALIDATE }`
:   Specifies whether to validate existing data on the table when a constraint is created. Applies only when either
    `{ ENFORCED | NOT ENFORCED }` or `{ ENABLE | DISABLE }` is specified.

    Default for PRIMARY KEY and FOREIGN KEY constraints: NOVALIDATE

    Default for CHECK constraints: VALIDATE

    For [hybrid tables](/user-guide/tables-hybrid), adding a UNIQUE or FOREIGN KEY constraint with ALTER TABLE always
    validates the rows that are already in the table, regardless of this property. See
    [Add and drop constraints on an existing hybrid table](/sql-reference/sql/create-hybrid-table#label-hybrid-table-online-constraints).

`{ RELY | NORELY }`
:   Specifies whether a constraint in NOVALIDATE mode is taken into account during query rewrite.

    If you have ensured that the data in the table complies with the constraints, you can change this property
    to RELY to indicate that the query optimizer should expect such data integrity. For standard tables, it is your responsibility to
    enforce RELY constraints; otherwise, you might risk unintended behavior and unexpected results.

    If the RELY property is set for a constraint and a violation of referential integrity occurs, DML and CTAS statements might insert
    incorrect data.

    Setting the RELY property might improve query
    performance (for example, by [eliminating unnecessary joins](/user-guide/join-elimination)).

    For related PRIMARY KEY and FOREIGN KEY constraints, set this property on both constraints. For example:

    Copy code

    ```
    ALTER TABLE table_with_primary_key ALTER CONSTRAINT a_primary_key_constraint RELY;
    ALTER TABLE table_with_foreign_key ALTER CONSTRAINT a_foreign_key_constraint RELY;
    ```

    Default: NORELY

### Properties (for FOREIGN KEY constraints only)

The following constraint properties apply only to foreign keys (the order of the properties is interchangeable):

Copy code

```
MATCH { FULL | SIMPLE | PARTIAL }
ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
   [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
```

`MATCH { FULL | PARTIAL | SIMPLE }`
:   Specifies whether the FOREIGN KEY constraint is satisfied with regard to NULL values in one or more of the columns.

    Default: MATCH FULL

`UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION }`
:   Specifies the action performed when the primary or unique key for the foreign key is updated.

    Default: UPDATE NO ACTION

`DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION }`
:   Specifies the action performed when the primary or unique key for the foreign key is deleted.

    Default: DELETE NO ACTION

### Properties (for CHECK constraints only)

The following constraint properties apply only to CHECK constraints:

Copy code

```
CHECK ( <expr> )
```

`CHECK ( expr )`
:   An expression that defines the condition to enforce.

    The expression can contain any of the following items:

    - Table columns defined in the table on which the CHECK constraint operates.
    - Constant values.
    - [Scalar functions](/sql-reference/functions) that don’t rely on the environment or execution context.

    The expression can’t contain any of the following items:

    - User-defined functions (UDFs).
    - Aggregate functions, window functions, table functions, or subqueries.
    - System-defined functions that change database state, such as the SYSTEM$CANCEL\_ALL\_QUERIES function.
    - Non-deterministic system-defined functions, such as the RANDOM function.
    - System-defined functions that rely on the environment or execution context, such as the CURRENT\_DATE
      function or the CURRENT\_ROLE function.

    For more information, see [CHECK constraints](/sql-reference/constraints-overview#label-constraints-check).

### Non-default values for ENABLE and VALIDATE properties

For syntax compatibility with other databases, Snowflake supports specifying non-default values for constraint properties.

However, for PRIMARY KEY, UNIQUE, and FOREIGN KEY constraints, if you specify ENABLE or VALIDATE (the non-default values
for these properties) when creating a new constraint, *the constraint isn’t created*. This doesn’t apply to RELY. Specifying
RELY does result in the creation of the new constraint.

For CHECK constraints, ENABLE is the default and is required. If you specify DISABLE, then *the CHECK constraint isn’t created*.
Both NOVALIDATE and VALIDATE are supported for new tables. VALIDATE isn’t supported on existing tables.

Snowflake provides a session parameter, [UNSUPPORTED\_DDL\_ACTION](/sql-reference/parameters#label-unsupported-ddl-action), which determines whether specifying non-default
values during constraint creation generates an error.

## Comments on constraints

Similar to other database objects and constructs, Snowflake supports comments on constraints:

- Out-of-line constraints support the COMMENT clause within the constraint definition.

  Copy code

  ```
  CREATE OR REPLACE TABLE uni (c1 INT, c2 int, CONSTRAINT uni1 UNIQUE(C1) COMMENT 'Unique column');
  ```
- A COMMENT clause within the column definition can be used to comment on the column itself or its constraint:

  Copy code

  ```
  CREATE OR REPLACE TABLE uni (c1 INT UNIQUE COMMENT 'Unique column', c2 int);
  ```

Note the following limitations:

- You can’t set comments on constraints by using the [COMMENT](/sql-reference/sql/comment) command.
- The [DESCRIBE TABLE](/sql-reference/sql/desc-table) command shows comments defined on columns, but not comments defined on constraints.
  To see comments on constraints, select from the [TABLE\_CONSTRAINTS view](/sql-reference/info-schema/table_constraints) or the
  [REFERENTIAL\_CONSTRAINTS view](/sql-reference/info-schema/referential_constraints).
- The COMMENT clause within column and constraint definitions does’t support the equals sign (`=`). Do not specify:

  Copy code

  ```
  COMMENT = 'My comment'
  ```

  Use the syntax shown in the previous examples:

  Copy code

  ```
  COMMENT 'My comment'
  ```

## Usage notes

- NOT NULL specifies that the column doesn’t allow NULL values:

  - For standard Snowflake tables, NOT NULL and CHECK are the only types of constraints that are enforced. See [Referential Integrity Constraints](/user-guide/table-considerations#label-table-considerations-referential-integrity-constraints).
  - It can be specified only as an inline constraint within the column definition.
  - The default is to allow NULL values in columns.
- Multi-column constraints (composite unique or primary keys) can only be defined out-of-line.
- When defining foreign keys, either inline or out-of-line, column name(s) for the referenced table do not need to be specified if the
  signature (name and data type) of the foreign key column(s) and the referenced table’s primary key column(s) exactly match.
- `NOT NULL` and `CHECK` constraints can’t be set on [virtual columns](/sql-reference/virtual-columns).

- If you create a foreign key, the columns in the REFERENCES clause must be listed in the same order as they were
  listed for the primary key. For example:

  Copy code

  ```
  CREATE TABLE parent ... CONSTRAINT primary_key_1 PRIMARY KEY (c_1, c_2) ...
  CREATE TABLE child  ... CONSTRAINT foreign_key_1 FOREIGN KEY (...) REFERENCES parent (c_1, c_2) ...
  ```

  In both cases, the order of the columns is `c_1, c_2`. If the order of the columns in the foreign key had been different
  (for example, `c_2, c_1`), the attempt to create the foreign key would have failed.

## Access control requirements

For creating PRIMARY KEY or UNIQUE constraints:

- When altering an existing table to add the constraint, you must use a role that has the OWNERSHIP privilege on the table.
- When creating a new table, you must use a role that has the CREATE TABLE privilege on the schema where the table will be created.

For creating FOREIGN KEY constraints:

- You must use a role that has the OWNERSHIP privilege on the foreign key table.
- You must use a role that has the REFERENCES privilege on the unique or primary key table.

The REFERENCES privilege can be granted to and revoked from roles using the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) and
[REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege) commands:

> Copy code
>
> ```
> GRANT REFERENCES ON TABLE <pk_table_name> TO ROLE <role_name>
>
> REVOKE REFERENCES ON TABLE <pk_table_name> FROM ROLE <role_name>
> ```

## Examples of constraints with standard tables

For examples of constraints with hybrid tables, see [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table).

The example below shows how to create a simple NOT NULL constraint while creating a table, and another NOT NULL
constraint while altering a table:

Create a table and create a constraint at the same time:

Copy code

```
CREATE TABLE table1 (col1 INTEGER NOT NULL);
```

Alter the table to add a column with a constraint:

Copy code

```
ALTER TABLE table1 ADD COLUMN col2 VARCHAR NOT NULL;
```

The following example specifies that the intent of the column is to hold unique values, but makes clear that the
constraint is not actually enforced. This example also demonstrates how to specify a name for the constraint
(“uniq\_col3” in this case.)

Copy code

```
ALTER TABLE table1
  ADD COLUMN col3 VARCHAR NOT NULL CONSTRAINT uniq_col3 UNIQUE NOT ENFORCED;
```

The following creates a parent table with a PRIMARY KEY constraint and another table with a FOREIGN KEY constraint
that points to the same columns as the first table’s PRIMARY KEY constraint.

Copy code

```
CREATE TABLE table2 (
  col1 INTEGER NOT NULL,
  col2 INTEGER NOT NULL,
  CONSTRAINT pkey_1 PRIMARY KEY (col1, col2) NOT ENFORCED
);
CREATE TABLE table3 (
  col_a INTEGER NOT NULL,
  col_b INTEGER NOT NULL,
  CONSTRAINT fkey_1 FOREIGN KEY (col_a, col_b) REFERENCES table2 (col1, col2) NOT ENFORCED
);
```

The following example specifies an inline CHECK constraint in a CREATE TABLE statement:

Copy code

```
CREATE TABLE test_check_constraint_orders (
  order_id INT,
  quantity INT CHECK (quantity > 0),
  price NUMBER(10, 2));
```

This CHECK constraint fails for the following DML operations because the
quantity is a negative value or zero:

Copy code

```
INSERT INTO test_check_constraint_orders (order_id, quantity, price)
  VALUES (101, -5, 25.35);
```

Copy code

```
UPDATE test_CHECK_constraint_orders
  SET quantity = 0
  WHERE order_id = 101;
```

The following example specifies an out-of-line CHECK constraint on multiple columns:

Copy code

```
CREATE TABLE test_check_constraint_max_orders (
  order_id INT,
  quantity INT,
  price NUMBER(10, 2),
  max_price NUMBER(10, 2),
  CONSTRAINT chk_price_max CHECK (price < max_price));
```

The CHECK constraint ensures that price doesn’t exceed the maximum price.

The following example specifies an inline CHECK constraint in a CTAS statement:

Copy code

```
CREATE TABLE high_value_products (
  product_id INT,
  product_name VARCHAR(100),
  list_price NUMBER(10, 2),
  CONSTRAINT high_price CHECK (list_price > 100)
  )
  AS SELECT product_id,
            product_name,
            list_price
  FROM products
  WHERE list_price > 100;
```

The CHECK constraint ensures that the new `high_value_products` table only contains items that
are considered to be high-priced.
