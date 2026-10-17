# Use default values with Apache Iceberg™ tables

Snowflake supports the default values feature for Apache Iceberg™ tables in accordance with the Iceberg v3 specification.
This feature lets you set default values for existing and new records without having to rewrite existing data files.
You can set the following default values for table columns:

- An initial default, which provides a default value for *existing* records when a field is added.
- A write default, which provides a default value for *new* records if the field with the default value isn’t specified during writes.

With this feature, you can evolve schemas while presenting values for historical data and provide a fallback value for future writes.
For more information, see [Default values](https://iceberg.apache.org/spec/#default-values) in the Apache Iceberg specification.

On Snowflake-managed v3 tables, you can also use [expression defaults](#label-tables-iceberg-expression-defaults), such as
`CURRENT_DATE()`, sequences, and identity columns, which Snowflake evaluates when a Snowflake write omits the column.

Important

To write default values to Iceberg metadata (`initial-default` and `write-default`), the table must conform to v3 of the
Apache Iceberg™ table specification. On Snowflake-managed v2 tables, and on v3 tables with `ALLOW_V3_EXPRESSION_DEFAULTS = TRUE`,
Snowflake applies column expression defaults to Snowflake writes only and doesn’t write them to Iceberg metadata.
For instructions on how to configure the Iceberg version for new tables, see [Configure the default Iceberg version](/user-guide/tables-iceberg-v3-specification-support#tables-iceberg-configuring-default-version).
To upgrade an existing table, see [Upgrade an Apache Iceberg™ table from version 2 to version 3](/user-guide/tables-iceberg-upgrade-version).

## Types of default values

How Snowflake stores a default in Iceberg metadata depends on whether Snowflake can evaluate it to a non-`NULL` constant when it
generates the table metadata:

| Default type | Examples | Snowflake behavior | Iceberg metadata |
| --- | --- | --- | --- |
| Literal constant | `DEFAULT 1` | Uses the constant when a write omits the column. | Contains the literal as the initial and write defaults. |
| Foldable expression | `PI()`, `1+1`, and `TO_DATE('2011-01-01')` | Retains the SQL expression as the column default and evaluates it for Snowflake writes. | Contains the evaluated constant as the initial and write defaults. |
| Snowflake-only default | `CURRENT_DATE()`, `CURRENT_USER()`, `RANDOM()`, identity columns (`AUTOINCREMENT`), and sequence references (`my_seq.NEXTVAL`) | Evaluates or generates the value when a Snowflake write omits the column. | Doesn’t contain an initial or write default. |

Expand

Show lessSee more

Literal constants are supported on both Snowflake-managed and externally managed v3 tables. Foldable expressions and
Snowflake-only defaults are supported only on Snowflake-managed v3 tables. Snowflake-only defaults also require the
[ALLOW\_V3\_EXPRESSION\_DEFAULTS](#label-tables-iceberg-expression-defaults-parameter) parameter.

## Use constant default values

You can specify a default value when you create or modify a table:

- To create a table with a default value for a column, use the DEFAULT keyword with your column definition. The value you specify
  is set as both the initial default and write default for the column. You can’t change the initial default for the column.
- To add a column with a default value to a table, use the DEFAULT keyword with the column definition in your ALTER ICEBERG TABLE command.
  The value you specify is set as both the initial default and write default for the column. You can’t change the initial default for the column.
- To change the write default for a column, use the WRITE DEFAULT keywords with the ALTER ICEBERG TABLE command.

### Example: Create a table with a default value

To create an Iceberg table with default values, use the
[CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command.

In the following example, you first set a default value for a column when you create a Snowflake-managed Iceberg table. Next, you insert a
record into the table without specifying a value for the column with the default value.

1. Create a `user_events` table, which includes an `event_version` column with a default value of `2`:

   Copy code

   ```
   CREATE ICEBERG TABLE user_events (
    event_id INT,
    user_id INT,
    event_type STRING,
    event_time TIMESTAMP,
    event_version INT DEFAULT 2
     )
     CATALOG = 'SNOWFLAKE'
     EXTERNAL_VOLUME = 'my_external_volume'
     BASE_LOCATION = 'database/schema/user_event'
     ICEBERG_VERSION = 3;
   ```

   Setting a default value in the table definition sets an initial default and a write default. Because the column has a write default,
   the value `2` will be used for new records if the `event_version` isn’t specified during writes.
2. Add a login event with `event_version` specified:

   Copy code

   ```
   INSERT INTO user_events VALUES
     (1, 101, 'login', '2025-11-01 10:00:00', 1);
   ```
3. Add a purchase event, but don’t specify an `event_version`:

   Copy code

   ```
   INSERT INTO user_events (event_id, user_id, event_type, event_time) VALUES
   (1, 101, 'purchase', '2025-11-01 10:01:00');
   ```

   As a result, Snowflake inputs the value for `event_version` into the table as `2`.
4. Query the table:

   Copy code

   ```
   SELECT * FROM user_events;
   ```

   Output:

   ```
   +-----------+----------+-------------+---------------------+----------------+
   | event_id  | user_id  | event_type  | event_time          | event_version  |
   +-----------+----------+-------------+---------------------+----------------+
   | 1         | 101      | login       | 2025-11-01 10:00:00 | 1              |
   | 1         | 101      | purchase    | 2025-11-01 10:01:00 | 2              |
   +-----------+----------+-------------+---------------------+----------------+
   ```

### Example: Add a column with a default value to an existing table

To add a new column with a default value to an Iceberg table, use the [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) command.

In the following example, you modify the `user_events` table by adding an `event_source` column, which has a default value of `'web'`:

Copy code

```
ALTER ICEBERG TABLE user_events ADD COLUMN event_source STRING DEFAULT 'web';
```

In addition to setting a write default, adding a column with a default value also sets an initial default for the column. As a
result, the value of the `event_source` column for existing records is `'web'`.

### Example: Change the write default for a column

The following example changes the write default for the `event_version` column of the `user_events` table to `3`:

Copy code

```
ALTER ICEBERG TABLE user_events ALTER COLUMN event_version SET WRITE DEFAULT 3;
```

You can’t change the write default on a table that has [ALLOW\_V3\_EXPRESSION\_DEFAULTS](#label-tables-iceberg-expression-defaults-parameter)
set to `TRUE`.

### Drop the write default

To drop the write default for a column, use the `DROP WRITE DEFAULT` keywords with the ALTER ICEBERG TABLE command.

The following example drops the default write value for the `event_version` column:

Copy code

```
ALTER ICEBERG TABLE user_events ALTER COLUMN event_version DROP WRITE DEFAULT;
```

## Use expression defaults with Snowflake-managed tables

On Snowflake-managed v3 tables, you can use SQL expressions, sequences, and identity columns as column defaults.
Snowflake evaluates these defaults when a Snowflake DML statement, such as INSERT or MERGE, omits the column.

Snowflake writes an expression default to Iceberg metadata only when it can evaluate the complete expression at compile time to
a non-`NULL` constant (a *foldable* expression). Snowflake retains the original SQL expression for foldable defaults. For example,
DESCRIBE ICEBERG TABLE and GET\_DDL show `DEFAULT PI()`, while the Iceberg `metadata.json` file contains the value `3.141592653589793`.

Snowflake doesn’t fold functions that are nondeterministic, generate data, depend on the current environment, or have side effects.
Those defaults, together with sequences and identity columns, are *Snowflake-only*. For conversion expressions such as `TO_DATE`,
use an unambiguous ISO-formatted literal because session parsing settings, including `DATE_INPUT_FORMAT`, can affect the evaluated value.

You can mix literal constant and expression defaults on the same table.

### When ALLOW\_V3\_EXPRESSION\_DEFAULTS is required

Snowflake-only defaults aren’t interoperable with external engines, so you must opt in by setting the
[ALLOW\_V3\_EXPRESSION\_DEFAULTS](/sql-reference/parameters#label-allow-v3-expression-defaults) parameter to `TRUE`.
Without it, statements that define a Snowflake-only default on a v3 table fail. Literal constants and foldable expressions
don’t require the parameter.

The parameter is required when you:

- Create a v3 table with a Snowflake-only default in the column list.
- Add a column with a Snowflake-only default by using `ALTER ICEBERG TABLE ... ADD COLUMN ... DEFAULT ...`.

You can set the parameter at the account, database, schema, or table level. The most specific setting wins, and new v3
tables inherit the setting from the containing schema, database, or account.

Note

You can’t use `ALTER ICEBERG TABLE ... ALTER COLUMN ... SET DEFAULT` to add or change a default on an existing v3 column.
To add an expression default, use `ADD COLUMN` with `DEFAULT`, or define the default when you create the table.

### Enable expression defaults

Set the parameter at the account, database, or schema level:

Copy code

```
ALTER ACCOUNT SET ALLOW_V3_EXPRESSION_DEFAULTS = TRUE;
ALTER DATABASE my_db SET ALLOW_V3_EXPRESSION_DEFAULTS = TRUE;
ALTER SCHEMA my_db.my_schema SET ALLOW_V3_EXPRESSION_DEFAULTS = TRUE;
```

Or set it on a table, either when you create the table or later:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE user_events (
  event_id INT,
  event_date DATE DEFAULT CURRENT_DATE(),
  created_by STRING DEFAULT CURRENT_USER(),
  event_version INT DEFAULT 1
)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'database/schema/user_events'
  ICEBERG_VERSION = 3
  ALLOW_V3_EXPRESSION_DEFAULTS = TRUE;
```

Copy code

```
ALTER ICEBERG TABLE user_events SET ALLOW_V3_EXPRESSION_DEFAULTS = TRUE;
```

To check the effective value and the level it’s set at, run SHOW PARAMETERS:

Copy code

```
SHOW PARAMETERS LIKE 'ALLOW_V3_EXPRESSION_DEFAULTS' IN TABLE user_events;
```

### Example: Insert rows with expression defaults

The following example creates a table that mixes all default types, and then inserts rows without specifying the defaulted columns:

Copy code

```
CREATE OR REPLACE SEQUENCE event_seq START = 100 INCREMENT = 1;

CREATE OR REPLACE ICEBERG TABLE user_events (
  event_id INT,
  event_date DATE DEFAULT CURRENT_DATE(),
  created_by STRING DEFAULT CURRENT_USER(),
  circle_ratio DOUBLE DEFAULT PI(),
  retry_count INT DEFAULT 1+1,
  seq_id INT DEFAULT event_seq.NEXTVAL,
  event_version INT DEFAULT 1
)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'database/schema/user_events'
  ICEBERG_VERSION = 3
  ALLOW_V3_EXPRESSION_DEFAULTS = TRUE;

INSERT INTO user_events (event_id) VALUES (1);
INSERT INTO user_events (event_id, event_date) VALUES (2, '2020-01-01');
```

The first row uses Snowflake-only defaults for `event_date`, `created_by`, and `seq_id`; foldable expression defaults for
`circle_ratio` and `retry_count`; and the literal constant `1` for `event_version`. The second row uses the explicit date you supplied.
In Iceberg metadata, `circle_ratio` has the value `3.141592653589793` and `retry_count` has the value `2` as their initial and write
defaults. The other expression columns have no Iceberg default.

Snowflake evaluates the same defaults for rows inserted by MERGE, and for rows inserted into a clone of the table. Cloned tables
preserve expression defaults.

### Example: Add a column with an expression default

The table must already have `ALLOW_V3_EXPRESSION_DEFAULTS = TRUE`, either set on the table or inherited from a higher level:

Copy code

```
ALTER ICEBERG TABLE user_events
  ADD COLUMN last_updated DATE DEFAULT CURRENT_DATE();
```

### Interoperability with external engines

Snowflake-only defaults aren’t written to Iceberg table metadata. External engines that access the table through
[Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon) don’t see these defaults:

- **Snowflake writes:** When you omit a column with a Snowflake-only default, Snowflake evaluates or generates the default.
- **External engine writes:** External engines don’t evaluate Snowflake-only defaults. For nullable columns, supply a value or write `NULL`.
  For `NOT NULL` columns, supply a value.
- **Constant and foldable defaults:** These columns have initial and write defaults in Iceberg metadata, so external engines can use them.

Snowflake INSERT and MERGE operations always evaluate the Snowflake defaults defined on the table, including after writes from
external engines.

Caution

External engines don’t see Snowflake-only defaults, so an external engine can set an Iceberg write default on a column that
already has a Snowflake-only default, and Snowflake Horizon Catalog currently accepts the change. Snowflake doesn’t use that write default:

- Snowflake writes that omit the column continue to evaluate the Snowflake-only default.
- The external write default isn’t added to the Snowflake column definition.
- The next time Snowflake writes to the table, the Iceberg metadata that Snowflake generates resets the column’s write default to
  none.

Until then, Snowflake and the external engine can each apply a different default to the same column. Don’t set write defaults
from external engines on columns that have Snowflake-only defaults; supply explicit values for those columns in external writes
instead. For more information, see [Considerations and limitations for default values](#label-tables-iceberg-default-values-limitations).

### Upgrading v2 tables that have expression defaults

When you [upgrade a Snowflake-managed v2 table to v3](/user-guide/tables-iceberg-upgrade-version) and the table has expression,
sequence, or identity column defaults, Snowflake automatically sets `ALLOW_V3_EXPRESSION_DEFAULTS = TRUE` on the table. The upgrade
preserves the original column defaults. Foldable defaults are also stored as Iceberg initial and write defaults; the other defaults
remain Snowflake-only.

## View the default values defined for a table

To view the default value for a table column in a Snowflake-managed or externally managed Iceberg table,
run the [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table) command, and then view the `DEFAULT` column and `WRITE DEFAULT` column in the output:

- The `DEFAULT` column maps to the `initial-default` value in the Apache Iceberg specification.
- The `WRITE DEFAULT` column maps to the `write-default` value in the Apache Iceberg specification.

These columns return in the output, regardless of whether the table is a v2 Iceberg table or a v3 Iceberg table.

The following example describes the columns for the `user_events` table. This table has an initial default and write default specified for
the `event_version` column:

Copy code

```
DESC ICEBERG TABLE user_events
  ->> SELECT
    "name",
    "kind",
    "default",
    "write default"
      FROM $1;
```

Output:

```
+-----------------+---------+---------+---------------+
| name            | kind    | default | write default |
+-----------------+---------+-------------------------+
| EVENT_ID        | COLUMN  |         |               |
| USER_ID         | COLUMN  |         |               |
| EVENT_TYPE      | COLUMN  |         |               |
| EVENT_TIME      | COLUMN  |         |               |
| EVENT_VERSION   | COLUMN  | 2       | 3             |
+-----------------+---------+---------+---------------+
```

Other ways to see defaults:

- **GET\_DDL:** `GET_DDL('ICEBERG_TABLE', '<table_name>')` includes the original expression in each column definition. It doesn’t include
  the `ALLOW_V3_EXPRESSION_DEFAULTS` table parameter. Before you recreate a table that has Snowflake-only defaults from the generated
  DDL, enable the parameter in the destination scope or add it to the statement.
- **INFORMATION\_SCHEMA.COLUMNS:** The `COLUMN_DEFAULT` column reports expression defaults for date functions, user functions, sequences,
  and constants. It returns `NULL` for `AUTOINCREMENT` identity columns.
- **Iceberg metadata.json:** Contains literals for constant defaults and foldable expression defaults only.

## Considerations and limitations for default values

### All Iceberg v3 tables

- You can’t later add or change an initial default for a column after you create it. Instead, drop the column and add it again by
  using ALTER ICEBERG TABLE … DROP COLUMN and ALTER ICEBERG TABLE … ADD COLUMN.
- The maximum size for a default value is 128 MB.
- For nanosecond-precision timestamp columns, such as TIMESTAMP\_NTZ(9) and TIMESTAMP\_LTZ(9), the default value must be between
  1677-09-21 and 2262-04-11.
- For DECIMAL columns, the default value must fit the column’s scale without rounding.
- Columns that use the `variant`, `geography`, or `geometry` data type can only have a `NULL` default, because these values can’t be
  represented as constants in the Iceberg specification.
- Default values can’t use the following data types, which are allowed in the Iceberg specification but aren’t supported in Snowflake:
  - `map`
  - `list`
  - `struct`

### Snowflake-managed Iceberg tables

- The `write-default` value is always initialized to the `initial-default` value.
- Snowflake-only defaults require `ALLOW_V3_EXPRESSION_DEFAULTS = TRUE` on the table or inherited from the account, database, or schema.
- Every `NOT NULL` column that you add to an existing table must specify a non-`NULL` default, even when the table is empty.
  You can use a literal constant, a foldable expression, a sequence, or an identity column. You can’t use a nondeterministic or
  environment-dependent expression such as `CURRENT_DATE()` as the default for a `NOT NULL` column that you add.
- You can’t change or drop the initial default of an existing v3 column by using ALTER COLUMN … SET DEFAULT or DROP DEFAULT.
- You can’t use ALTER ICEBERG TABLE … ALTER COLUMN … SET WRITE DEFAULT on any column of a table that has
  `ALLOW_V3_EXPRESSION_DEFAULTS = TRUE`, even if that column has a constant default.
- You can’t unset `ALLOW_V3_EXPRESSION_DEFAULTS` or set it to `FALSE` while the table has an expression, sequence, or identity default.
- CREATE ICEBERG TABLE … LIKE doesn’t support copying Snowflake-only defaults from the source table. To create a table that has
  Snowflake-only defaults, use an explicit column list, or use the output of GET\_DDL and set `ALLOW_V3_EXPRESSION_DEFAULTS = TRUE`.
  Literal constant and foldable expression defaults are copied as usual.

### Externally managed Iceberg tables

- Default values must be literal constants. Expression defaults, sequences, and identity columns aren’t supported on externally
  managed tables or on tables in a catalog-linked database.

For considerations and limitations that apply to all Iceberg v3 tables, see
[Iceberg v3 considerations and limitations](/user-guide/tables-iceberg-v3-specification-support#iceberg-v3-considerations-limitations).
