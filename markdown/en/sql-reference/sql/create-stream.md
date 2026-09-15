# CREATE STREAM

Creates a new stream in the current/specified schema or replaces an existing [stream](/user-guide/streams-intro). A stream records data
manipulation language (DML) changes made to a table, directory table, dynamic table, external table, or the underlying tables in a view (including
secure views). The object for which changes are recorded is called the *source object*.

In addition, this command supports the following variants:

- [CREATE STREAM … CLONE](#label-create-stream-clone-syntax): Creates a clone of an existing stream.
- [CREATE OR ALTER STREAM](#label-create-or-alter-stream-syntax): Creates a stream if it doesn’t exist or alters an existing stream.

See also:
:   [ALTER STREAM](/sql-reference/sql/alter-stream), [DROP STREAM](/sql-reference/sql/drop-stream), [SHOW STREAMS](/sql-reference/sql/show-streams), [DESCRIBE STREAM](/sql-reference/sql/desc-stream)

## Syntax

The command syntax differs depending on the object on which the stream is created:

Copy code

```
-- table
CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
  <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COPY GRANTS ]
  ON TABLE <table_name>
  [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> | STREAM => '<name>' } ) ]
  [ APPEND_ONLY = TRUE | FALSE ]
  [ SHOW_INITIAL_ROWS = TRUE | FALSE ]
  [ COMMENT = '<string_literal>' ]

-- Event table
CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
  <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COPY GRANTS ]
  ON EVENT TABLE <table_name>
  [ COMMENT = '<string_literal>' ]

-- External table
CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
  <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COPY GRANTS ]
  ON EXTERNAL TABLE <external_table_name>
  [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> | STREAM => '<name>' } ) ]
  [ INSERT_ONLY = TRUE ]
  [ COMMENT = '<string_literal>' ]

-- Directory table
CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
  <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COPY GRANTS ]
  ON STAGE <stage_name>
  [ COMMENT = '<string_literal>' ]

-- Dynamic table
CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
  <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COPY GRANTS ]
  ON DYNAMIC TABLE <table_name>
  [ COMMENT = '<string_literal>' ]

-- View
CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
  <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COPY GRANTS ]
  ON VIEW <view_name>
  [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> | STREAM => '<name>' } ) ]
  [ APPEND_ONLY = TRUE | FALSE ]
  [ SHOW_INITIAL_ROWS = TRUE | FALSE ]
  [ COMMENT = '<string_literal>' ]
```

## Variant syntax

### CREATE STREAM … CLONE

Creates a new stream with the same definition as the source stream. The clone inherits the current *offset* (i.e. the current
transactional [table version](/user-guide/streams-intro#label-streams-table-versioning)) from the source stream.

> Copy code
>
> ```
> CREATE [ OR REPLACE ] STREAM <name> CLONE <source_stream>
>   [ COPY GRANTS ]
>   [ ... ]
> ```

For more information about cloning, see [CREATE <object> … CLONE](/sql-reference/sql/create-clone).

### CREATE OR ALTER STREAM

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a new stream if it doesn’t already exist, or transforms an existing stream into the stream defined in the statement.
A CREATE OR ALTER STREAM statement follows the syntax rules of a CREATE STREAM statement and has the same limitations as an
[ALTER STREAM](/sql-reference/sql/alter-stream) statement.

The following modifications are supported when altering a stream:

- Adding, updating, or removing a COMMENT.

For more information, see [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

The syntax differs depending on the object on which the stream is created. The following example shows a stream on a table:

Copy code

```
-- Table stream
CREATE OR ALTER STREAM <name>
  ON TABLE <table_name>
  [ APPEND_ONLY = TRUE | FALSE ]
  [ SHOW_INITIAL_ROWS = TRUE | FALSE ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the stream; must be unique for the schema in which the stream is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`table_name`
:   String that specifies the identifier (i.e. name) for the table whose changes are tracked by the stream (i.e. the source table).

    Access control:
    :   To query a stream, a role must have the SELECT privilege on the underlying table.

`external_table_name`
:   String that specifies the identifier (i.e. name) for the external table whose changes are tracked by the stream (i.e. the source
    external table).

    Access control:
    :   To query a stream, a role must have the SELECT privilege on the underlying external table.

`stage_name`
:   String that specifies the identifier (i.e. name) for the stage whose directory table changes are tracked by the stream (i.e. the
    source directory table).

    Access control:
    :   To query a stream, a role must have the USAGE (external stage) or READ (internal stage) privilege on the underlying
        stage.

`view_name`
:   String that specifies the identifier (i.e. name) for the source view. The stream tracks DML changes to the underlying tables in
    the view.

    For more information about streams on views, see [Streams on views](/user-guide/streams-intro#label-streams-views).

    Access control:
    :   To query a stream, a role must have the SELECT privilege on the view.

## Optional parameters

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`COPY GRANTS`
:   Specifies to retain the access permissions from the original stream when a new stream is created using any of the following
    CREATE STREAM variants:

    > - CREATE OR REPLACE STREAM
    > - CREATE STREAM … CLONE

    The parameter copies all permissions, except OWNERSHIP, from the existing stream to the new stream. By default, the role
    that executes the CREATE STREAM command owns the new stream.

    Note

    - If the CREATE STREAM statement references more than one stream (e.g. `create or replace stream t1 clone t2;`), the
      `COPY GRANTS` clause gives precedence to the stream being replaced.
    - The [SHOW GRANTS](/sql-reference/sql/show-grants) output for the replacement stream lists the grantee for the copied privileges as the
      role that executed the CREATE STREAM statement, with the current timestamp when the statement was executed.
    - The operation to copy grants occurs atomically in the CREATE STREAM command (i.e. within the same transaction).

    Note

    This parameter is not supported currently.

`{ AT ( { TIMESTAMP => timestamp | OFFSET => time_difference | STATEMENT => id | STREAM => 'name' } ) | BEFORE ( { TIMESTAMP => timestamp | OFFSET => time_difference | STATEMENT => id } ) }`
:   Creates a stream at a specific time/point in the past (using [Time Travel](/user-guide/data-time-travel)). The
    [AT | BEFORE](/sql-reference/constructs/at-before) clause determines the point in the past from which historical data is requested:

    > - The `AT` keyword specifies that the request is inclusive of any changes made by a statement or transaction with a timestamp
    >   equal to the specified parameter.
    >
    >   The `STREAM => '<name>'` value is special. When provided, the CREATE STREAM statement creates the new stream at the same
    >   offset as the specified stream. You can also provide this value when recreating an existing stream (using the `OR REPLACE`
    >   keywords) to retain the current offset of the stream after it is recreated. `'<name>'` is the identifier (i.e. name) for
    >   the existing stream whose offset is copied to the new or recreated stream.
    >
    >   The new or recreated stream advances the offset, as usual, when the stream is used in a DML transaction.
    > - The `BEFORE` keyword specifies that the request refers to a point immediately preceding the specified parameter.
    >
    > Note
    >
    > If no change tracking data is available on the source object at the point in the past specified in the AT | BEFORE clause, the
    > CREATE STREAM statement fails. No stream can be created at a time in the past before change tracking was recorded.

`APPEND_ONLY = TRUE | FALSE`
:   Only supported for streams on standard tables or streams on views that query standard tables.

    Specifies whether this is an append-only stream. Append-only streams track row inserts only. Update and delete operations (including
    table truncates) are not recorded. For example, if 10 rows are inserted into a table and then 5 of those rows are deleted before the
    offset for an append-only stream is advanced, the stream records 10 rows.

    This type of stream improves query performance over standard streams and is very useful for extract, load, transform (ELT) and similar
    scenarios that depend exclusively on row inserts.

    A standard stream joins the deleted and inserted rows in the change set to determine which rows were deleted and which were updated.
    An append-only stream returns the appended rows only and therefore can be much more performant than a standard stream. For example,
    the source table can be truncated immediately after the rows in an append-only stream are consumed, and the record deletions do not
    contribute to the overhead the next time the stream is queried or consumed.

    Default:
    :   `FALSE`

`INSERT_ONLY = TRUE | FALSE`
:   Required for streams on external tables and externally managed Iceberg tables. Not supported by streams on other objects.

    Specifies whether this is an insert-only stream. Insert-only streams track row inserts only; they do not record delete operations
    that remove rows from an inserted set (i.e. no-ops). For example, in-between any two offsets, if `File1` is removed from the
    cloud storage location referenced by the external table, and `File2` is added, the stream returns records for the rows in
    `File2` only, regardless of whether `File1` was added before or within the requested change interval. Unlike
    when tracking change data capture (CDC) data for standard tables, access to the historical records for files in cloud storage is
    not governed by or guaranteed to Snowflake.

    Overwritten or appended files are essentially handled as new files: The old version of the file is removed from cloud storage, but the
    insert-only stream does not record the delete operation. The new version of the file is added to cloud storage, and the insert-only
    stream records the rows as inserts. The stream does not record the diff of the old and new file versions. Note that appends may not
    trigger an automatic refresh of the external table metadata, such as when using
    [Azure AppendBlobs](/user-guide/tables-external-azure).

    Default:
    :   `FALSE`

`SHOW_INITIAL_ROWS = TRUE | FALSE`
:   Specifies the records to return the first time the stream is consumed.

    `TRUE`
    :   The stream returns only the rows that existed in the source object at the moment when the stream was created. The
        METADATA$ISUPDATE column shows a FALSE value in these rows. Subsequently, the stream returns any DML changes to the source object
        since the most recent offset; that is, the normal stream behavior.

        This parameter enables initializing any downstream process with the contents of the source object for the stream.

    `FALSE`

    > The stream returns any DML changes to the source object since the most recent offset.

    Default:
    :   `FALSE`

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the stream.

    Default: No value

## Output

The output for a stream includes the same columns as the source object along with the following additional columns:

- METADATA$ACTION: Specifies the action (INSERT or DELETE).
- METADATA$ISUPDATE: Specifies whether the action recorded (INSERT or DELETE) is part of an UPDATE applied to the rows in the source table
  or view.

  Note that streams record the differences between two offsets. If a row is added and then updated in the current offset, the delta change
  is a new row. The METADATA$ISUPDATE row records a FALSE value.
- METADATA$ROW\_ID: Specifies the unique and immutable ID for the row, which can be used to track changes to specific rows over time.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

Streams on standard tables:

> | Object | Privilege | Notes |
> | --- | --- | --- |
> | Schema | CREATE STREAM |  |
> | Table | SELECT | If change tracking has not been enabled on the source table (using [ALTER TABLE … SET CHANGE\_TRACKING = TRUE](/sql-reference/sql/alter-table)), then only the table owner (i.e. the role that has the OWNERSHIP privilege on the table) can create the initial stream on the table. Creating the initial stream automatically enables change tracking on the table. |
>
> Expand
>
> Show lessSee more
>
> Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

Streams on views:

> | Object | Privilege | Notes |
> | --- | --- | --- |
> | Schema | CREATE STREAM |  |
> | View | SELECT | If change tracking has not been enabled on the source view and its underlying tables, then only a role that has the OWNERSHIP privilege on the view and its underlying tables can create the initial stream on the view. Creating the initial stream automatically enables change tracking on the view and its underlying tables. For instructions on enabling change tracking on a view and its underlying tables, refer to [Enabling change tracking on views and underlying tables](/user-guide/streams-manage#label-enabling-change-tracking-views). Note that enabling change tracking locks the underlying tables while change tracking is being enabled. Locks on the underlying objects may cause latency in DDL/DML operations with these objects. For more information, refer to [Resource locking](/sql-reference/transactions#label-txn-locking). |
>
> Expand
>
> Show lessSee more
>
> Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

Streams on directory tables:

> | Object | Privilege | Notes |
> | --- | --- | --- |
> | Schema | CREATE STREAM |  |
> | Stage | USAGE (external stage) or READ (internal stage) |  |
>
> Expand
>
> Show lessSee more
>
> Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

Streams on external tables:

> | Object | Privilege | Notes |
> | --- | --- | --- |
> | Schema | CREATE STREAM |  |
> | External table | SELECT |  |
>
> Expand
>
> Show lessSee more
>
> Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Stream | Required to execute a [CREATE OR ALTER STREAM](#label-create-or-alter-stream-syntax) statement for an *existing* stream. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A stream can be queried multiple times to update multiple objects in the same transaction and it will return the same data.
- The stream position (i.e. *offset*) is advanced when the stream is used in a DML statement. The position is updated at the end of the
  transaction to the beginning timestamp of the transaction. The stream describes change records starting from the current position of the
  stream and ending at the current transactional timestamp.

  To ensure multiple statements access the same change records in the stream, surround them with an explicit transaction statement
  ([BEGIN](/sql-reference/sql/begin) .. [COMMIT](/sql-reference/sql/commit)). An explicit transaction locks the stream, so that DML updates to
  the source object are not reported to the stream until the transaction is committed.
- Streams have no Fail-safe period or Time Travel retention period. The metadata in these objects cannot be recovered if a stream is dropped.
- Streams on shared tables:
  - The retention period for a source table is not extended automatically to prevent any streams on the table from becoming stale.
- Standard streams cannot retrieve change data for geospatial data. We recommend creating append-only streams on objects that contain
  geospatial data.
- Streams on views:
  - Creating the first stream on a view using the view owner role (i.e. the role with the OWNERSHIP privilege on the view) enables change
    tracking on the view. If the same role also owns the underlying tables, change tracking is also enabled on the tables. If the role was
    not granted the OWNERSHIP privilege on both the view and its underlying tables, then change tracking must be enabled manually on the
    applicable objects. For instructions, see [Enabling change tracking on views and underlying tables](/user-guide/streams-manage#label-enabling-change-tracking-views).
  - Depending on the number of joins in a view, a single change in the underlying tables could result in a large number of changes in the
    stream output.
  - Any stream on a given view breaks if the source view or underlying tables are dropped or recreated (using CREATE OR REPLACE VIEW).
  - Any streams on a secure view adhere to the secure view constraints.

    If the owner of a non-secure view (i.e. the role with the OWNERSHIP privilege on the view) changes it to a secure view (using ALTER
    VIEW … SET SECURE), any stream on the view automatically enforces secure view constraints.

    In addition, the retention period for the underlying tables is not extended automatically to prevent any streams on the secure
    view from becoming stale.
  - Streams based on views where the view uses non-deterministic functions can return non-deterministic results.

    For example, the results of [context functions](/sql-reference/functions-context) such as [CURRENT\_DATE](/sql-reference/functions/current_date),
    and [CURRENT\_USER](/sql-reference/functions/current_user) are non-deterministic. The results of [data generation functions](/sql-reference/functions-data-generation)
    such as [RANDOM](/sql-reference/functions/random) are also non-deterministic.
    If a view contains a non-deterministic function, then any stream on that view will not be a constant snapshot of the
    function’s output. Instead, the value in the stream may change when queried.

    We recommend that you ensure that the non-determinism in the results of a view does not
    affect the correctness of the stream query results.

    For an example, see [Stream on a view that calls a non-deterministic SQL function](/user-guide/streams-examples#label-example-stream-view-non-deterministic-function).
- Streams on directory tables: The METADATA$ROW\_ID column values in the stream output are empty.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

### CREATE OR ALTER STREAM

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

- All limitations of the [ALTER STREAM](/sql-reference/sql/alter-stream) command apply.
- The source object (table, view, external table, stage, or dynamic table), APPEND\_ONLY setting, and INSERT\_ONLY setting can’t be changed
  for an existing stream. If you need to change any of these properties, drop the existing stream and create a new one.
- COPY GRANTS is not supported.
- Setting or unsetting a tag is not supported.

## Examples

### Creating a table stream

Create a stream on the `mytable` table:

Copy code

```
CREATE STREAM mystream ON TABLE mytable;
```

### Using Time Travel with the source table

Create a stream on the `mytable` table as it existed before the date and time in the specified timestamp:

Copy code

```
CREATE STREAM mystream ON TABLE mytable BEFORE (TIMESTAMP => TO_TIMESTAMP(40*365*86400));
```

Create a stream on the `mytable` table as it existed exactly at the date and time of the specified timestamp:

Copy code

```
CREATE STREAM mystream ON TABLE mytable AT (TIMESTAMP => TO_TIMESTAMP_TZ('02/02/2019 01:02:03', 'mm/dd/yyyy hh24:mi:ss'));
```

Create a stream on the `mytable` table as it existed 5 minutes ago:

Copy code

```
CREATE STREAM mystream ON TABLE mytable AT(OFFSET => -60*5);
```

Create a stream on the `mytable` table with the same offset as existing stream `oldstream` on the same source table:

Copy code

```
CREATE STREAM mystream ON TABLE mytable AT(STREAM => 'oldstream');
```

Recreate the existing `mystream` stream but retain its current offset:

Copy code

```
CREATE OR REPLACE STREAM mystream ON TABLE mytable AT(STREAM => 'mystream');
```

Create a stream on the `mytable` table including transactions up to, but not including any changes made by the specified transaction:

Copy code

```
CREATE STREAM mystream ON TABLE mytable BEFORE(STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726');
```

### Creating a stream on a single-table view

Create a stream on the `myview` view:

Copy code

```
CREATE STREAM mystream ON VIEW myview;
```

For additional examples, see [Stream examples](/user-guide/streams-examples).

### Creating an insert-only stream on an external table

Create an external table stream and query the change data capture records in the stream, which track the records added to the external
table metadata:

Copy code

```
-- Create an external table that points to the MY_EXT_STAGE stage.
-- The external table is partitioned by the date (in YYYY/MM/DD format) in the file path.
CREATE EXTERNAL TABLE my_ext_table (
  date_part date as to_date(substr(metadata$filename, 1, 10), 'YYYY/MM/DD'),
  ts timestamp AS (value:time::timestamp),
  user_id varchar AS (value:userId::varchar),
  color varchar AS (value:color::varchar)
) PARTITION BY (date_part)
  LOCATION=@my_ext_stage
  AUTO_REFRESH = false
  FILE_FORMAT=(TYPE=JSON);

-- Create a stream on the external table
CREATE STREAM my_ext_table_stream ON EXTERNAL TABLE my_ext_table INSERT_ONLY = TRUE;

-- Execute SHOW streams
-- The MODE column indicates that the new stream is an INSERT_ONLY stream
SHOW STREAMS;
+-------------------------------+------------------------+---------------+-------------+--------------+-----------+------------------------------------+-------+-------+-------------+
| created_on                    | name                   | database_name | schema_name | owner        | comment   | table_name                         | type  | stale | mode        |
|-------------------------------+------------------------+---------------+-------------+--------------+-----------+------------------------------------+-------+-------+-------------|
| 2020-08-02 05:13:20.174 -0800 | MY_EXT_TABLE_STREAM    | MYDB          | PUBLIC      | MYROLE       |           | MYDB.PUBLIC.EXTTABLE_S3_PART       | DELTA | false | INSERT_ONLY |
+-------------------------------+------------------------+---------------+-------------+--------------+-----------+------------------------------------+-------+-------+-------------+

-- Add a file named '2020/08/05/1408/log-08051409.json' to the stage using the appropriate tool for the cloud storage service.

-- Manually refresh the external table metadata.
ALTER EXTERNAL TABLE my_ext_table REFRESH;

-- Query the external table stream.
-- The stream indicates that the rows in the added JSON file were recorded in the external table metadata.
SELECT * FROM my_ext_table_stream;
+----------------------------------------+------------+-------------------------+---------+-------+-----------------+-------------------+-----------------+---------------------------------------------+
| VALUE                                  | DATE_PART  | TS                      | USER_ID | COLOR | METADATA$ACTION | METADATA$ISUPDATE | METADATA$ROW_ID | METADATA$FILENAME                           |
|----------------------------------------+------------+-------------------------+---------+-------+-----------------+-------------------+-----------------+---------------------------------------------|
| {                                      | 2020-08-05 | 2020-08-05 15:57:01.000 | user25  | green | INSERT          | False             |                 | test/logs/2020/08/05/1408/log-08051409.json |
|   "color": "green",                    |            |                         |         |       |                 |                   |                 |                                             |
|   "time": "2020-08-05 15:57:01-07:00", |            |                         |         |       |                 |                   |                 |                                             |
|   "userId": "user25"                   |            |                         |         |       |                 |                   |                 |                                             |
| }                                      |            |                         |         |       |                 |                   |                 |                                             |
| {                                      | 2020-08-05 | 2020-08-05 15:58:02.000 | user56  | brown | INSERT          | False             |                 | test/logs/2020/08/05/1408/log-08051409.json |
|   "color": "brown",                    |            |                         |         |       |                 |                   |                 |                                             |
|   "time": "2020-08-05 15:58:02-07:00", |            |                         |         |       |                 |                   |                 |                                             |
|   "userId": "user56"                   |            |                         |         |       |                 |                   |                 |                                             |
| }                                      |            |                         |         |       |                 |                   |                 |                                             |
+----------------------------------------+------------+-------------------------+---------+-------+-----------------+-------------------+-----------------+---------------------------------------------+
```

### Creating a standard stream on a directory table

Create a stream on the directory table for a stage named `mystage`:

Copy code

```
CREATE STREAM dirtable_mystage_s ON STAGE mystage;
```

Manually refresh the directory table metadata to populate the stream:

Copy code

```
ALTER STAGE mystage REFRESH;
```

Query the stream after one or more files were added to the stage after the most recent offset for the stream:

Copy code

```
SELECT * FROM dirtable_mystage_s;

+-------------------+--------+-------------------------------+----------------------------------+----------------------------------+-------------------------------------------------------------------------------------------+-----------------+-------------------+-----------------+
| RELATIVE_PATH     | SIZE   | LAST_MODIFIED                 | MD5                              | ETAG                             | FILE_URL                                                                                  | METADATA$ACTION | METADATA$ISUPDATE | METADATA$ROW_ID |
|-------------------+--------+-------------------------------+----------------------------------+----------------------------------+-------------------------------------------------------------------------------------------+-----------------+-------------------+-----------------|
| file1.csv.gz      |   1048 | 2021-05-14 06:09:08.000 -0700 | c98f600c492c39bef249e2fcc7a4b6fe | c98f600c492c39bef249e2fcc7a4b6fe | https://myaccount.snowflakecomputing.com/api/files/MYDB/MYSCHEMA/MYSTAGE/file1%2ecsv%2egz | INSERT          | False             |                 |
| file2.csv.gz      |   3495 | 2021-05-14 06:09:09.000 -0700 | 7f1a4f98ef4c7c42a2974504d11b0e20 | 7f1a4f98ef4c7c42a2974504d11b0e20 | https://myaccount.snowflakecomputing.com/api/files/MYDB/MYSCHEMA/MYSTAGE/file2%2ecsv%2egz | INSERT          | False             |                 |
+-------------------+--------+-------------------------------+----------------------------------+----------------------------------+-------------------------------------------------------------------------------------------+-----------------+-------------------+-----------------+
```

### CREATE OR ALTER STREAM

Create a new stream or update the comment for an existing stream on a table:

Copy code

```
CREATE OR ALTER STREAM mystream
  ON TABLE mytable
  COMMENT = 'Tracks DML changes on mytable';
```
