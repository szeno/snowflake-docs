# CREATE *<object>* … CLONE

Creates a copy of an existing object in the system. This command is primarily used for creating
[zero-copy clones](/user-guide/tables-storage-considerations#label-cloning-tables) of databases, schemas, and tables.
You can also use this command to create clones of other schema objects, including
external stages, file formats, sequences, and database roles.

The command is a variation of the object-specific [CREATE <object>](/sql-reference/sql/create) commands with the addition of the `CLONE` keyword.

## Clone objects using Time Travel

For databases, schemas, and non-temporary tables, `CLONE` supports an additional `AT | BEFORE` clause for cloning using
[Time Travel](/user-guide/data-time-travel).

For databases and schemas:

- `CLONE` supports the IGNORE TABLES WITH INSUFFICIENT DATA RETENTION parameter to skip any
  tables that have been purged from Time Travel (for example,
  [transient tables with a one day data retention period](/sql-reference/sql/create-clone#label-clone-database-with-transient-tables-example)).
- `CLONE` supports the IGNORE HYBRID TABLES parameter to skip hybrid tables, if required.

Note

For information about cloning databases that contain hybrid tables, see [Clone databases that contain hybrid tables](/user-guide/tables-hybrid-clone).

## Syntax

### Databases, schemas

Copy code

```
CREATE [ OR REPLACE ] { DATABASE | SCHEMA } [ IF NOT EXISTS ] <object_name>
  CLONE <source_object_name>
    [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
    [ IGNORE TABLES WITH INSUFFICIENT DATA RETENTION ]
    [ IGNORE HYBRID TABLES ]
    [ INCLUDE INTERNAL STAGES ]
  ...
```

### Tables

Copy code

```
CREATE [ OR REPLACE ] TABLE [ IF NOT EXISTS ] <object_name>
  CLONE <source_object_name>
    [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
  ...
```

### Dynamic tables

Copy code

```
CREATE [ OR REPLACE ] DYNAMIC TABLE <name>
  CLONE <source_dynamic_table>
    [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
  [
    TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
    WAREHOUSE = <warehouse_name>
  ]
```

### Event tables

Copy code

```
CREATE [ OR REPLACE ] EVENT TABLE <name>
  CLONE <source_event_table>
    [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
```

### Apache Iceberg™ tables

Copy code

```
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <name>
  CLONE <source_iceberg_table>
    [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
    [ COPY GRANTS ]
    ...
```

### Database roles

Copy code

```
CREATE [ OR REPLACE ] DATABASE ROLE [ IF NOT EXISTS ] <database_role_name>
  CLONE <source_database_role_name>
```

### Other schema objects

Copy code

```
CREATE [ OR REPLACE ] { ALERT | FILE FORMAT | SEQUENCE | STAGE | STREAM | TASK }
  [ IF NOT EXISTS ] <object_name>
  CLONE <source_object_name>
  ...
```

## Time Travel parameters

`{ AT | BEFORE } ( { TIMESTAMP => timestamp | OFFSET => time_difference | STATEMENT => id } )`
:   The [AT | BEFORE](/sql-reference/constructs/at-before) clause accepts one of the following parameters:

    `TIMESTAMP => timestamp`
    :   Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP,
        TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, or TIMESTAMP\_TZ data type.

        If no explicit cast is specified, the timestamp in the AT clause is treated as a timestamp with the UTC time zone (equivalent to
        TIMESTAMP\_NTZ). Using the TIMESTAMP data type for an explicit cast may also result in the value being treated as a TIMESTAMP\_NTZ
        value. For details, see [Date & time data types](/sql-reference/data-types-datetime).

    `OFFSET => time_difference`
    :   Specifies the difference in seconds from the current time to use for Time Travel, in the form `-N` where `N`
        can be an integer or arithmetic expression (e.g. `-120` is 120 seconds, `-30*60` is 1800 seconds or 30 minutes).

    `STATEMENT => id`
    :   Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the
        following types:

        - DML (e.g. INSERT, UPDATE, DELETE)
        - TCL (BEGIN, COMMIT transaction)
        - SELECT

        The query ID must reference a query that has been executed within the last 14 days. If the query ID references a query over 14 days old,
        the following error is returned:

        ```
        Error: statement <query_id> not found
        ```

        To work around this limitation, use the timestamp for the referenced query.

`IGNORE TABLES WITH INSUFFICIENT DATA RETENTION`

> Ignore tables that no longer have historical data available in Time Travel to clone. If the time in the past specified in the
> AT | BEFORE clause is beyond the data retention period for any child table in a database or schema, skip the cloning operation
> for the child table. For more information, see
> [Child Objects and Data Retention Time](/user-guide/object-clone#label-child-objects-and-data-retention-time).

## Hybrid tables parameters

`IGNORE HYBRID TABLES`
:   Ignore hybrid tables when cloning a database or schema. The cloned database or schema includes other objects but skips hybrid tables.
    For more information, see [Clone databases that contain hybrid tables](/user-guide/tables-hybrid-clone).

## Internal stage parameters

`INCLUDE INTERNAL STAGES`
:   Include named internal stages when cloning a database or schema.

    For more information, see the [usage notes](/sql-reference/sql/create-clone#label-create-clone-internal-stages-notes).

## Access control requirements

To create a clone, your current role must have the following privilege(s) on the source object:

> Databases:
> :   USAGE on the database.
>
> Database roles:
> :   OWNERSHIP on the database role and the CREATE DATABASE ROLE privilege on the target database.
>
> Schemas:
> :   If you specify the WITH MANAGED ACCESS clause, the required privileges depend on whether the source schema is a
>     managed or unmanaged schema. For details, see [CREATE SCHEMA privileges](/sql-reference/sql/create-schema#label-create-schema-ac).
>
> Tables:
> :   SELECT
>
> Alerts, Pipes, Streams, Tasks:
> :   OWNERSHIP
>
> Other objects:
> :   USAGE
>
> In addition, to clone a schema or an object within a schema, your current role must have required privileges on the container object(s)
> for both the source and the clone.
>
> For information about privilege inheritance for cloned objects, see [Cloning considerations](/user-guide/object-clone).

## General usage notes

- A clone is writable and is independent of its source. Changes made to the source or clone aren’t reflected in the other object.
- Parameters that are explicitly set on a source database, schema, or table are retained in any clones created from the source container or
  child objects.
- For database roles:

  - A database role is cloned when you run the CREATE DATABASE … CLONE command to clone a database. However, if you clone other database
    objects, such as a schema or table, database roles in the database are not cloned with the schema or table.
  - If the database role is already cloned to the target database, the command fails. If this occurs, drop the database role from the
    target database and try the CLONE command again.
- For databases and schemas, cloning is recursive:

  - Cloning a database clones all the schemas and other objects in the database.
  - Cloning a schema clones all the contained objects in the schema.
  - Cloning includes only the objects on which the role that creates the clone has [appropriate privileges](#label-create-clone-access-control-reqs).

  However, the following object types are not cloned:

  - External tables
  - Hybrid tables can be cloned for databases but not for schemas.
  - User tasks in a database or schema are not cloned when using CREATE SCHEMA … TIMESTAMP. In the following example, tasks in the source schema (S1) are not cloned to the schema with a timestamp (S2) but are cloned to the schema without a timestamp (S3).

    Copy code

    ```
    CREATE SCHEMA S1;
    USE SCHEMA S1;
    CREATE TASK T1 AS SELECT 1;
    CREATE SCHEMA S2 CLONE S1 AT(TIMESTAMP => '2025-04-01 12:00:00');
      -- T1 is not cloned into S2
    CREATE SCHEMA S3 CLONE S1;
      -- T1 is cloned into S3
    ```
- For databases, schemas, and tables, a clone does not contribute to the overall data storage for the object until operations are
  performed on the clone that modify existing data or add new data, such as:

  - Adding, deleting, or modifying rows in a cloned table.
  - Creating a new, populated table in a cloned schema.
- Cloning a table replicates the structure, data, and certain other properties (for example, `STAGE FILE FORMAT`) of the source table.

  However:

  - A cloned table does not include the load history of the source table. One consequence of this is that data files that
    were loaded into a source table can be loaded again into its clones.
  - Although a cloned table replicates the source table’s clustering keys, the new table starts with Automatic Clustering
    suspended – even if Automatic Clustering is not suspended for the source table.
  - [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) aren’t automatically applied to cloned tables.
    If the source table has a storage lifecycle policy
    attached, you must manually attach the policy to the clone by using the [ALTER TABLE](/sql-reference/sql/alter-table) command.
- The COPY GRANTS parameter affects a new table clone as follows:

  - If the COPY GRANTS parameter is used, then the new object inherits any explicit access privileges granted on the original table but does
    not inherit any future grants defined for the object type in the schema.
  - If the COPY GRANTS parameter is not used, then the new object clone does not inherit any explicit access privileges granted on
    the original table but does inherit any future grants defined for the object type in the schema (using the
    [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) … ON FUTURE syntax).

  Note

  If the statement is replacing an existing table of the same name, then the grants are copied from the table
  being replaced. If there is no existing table of that name, then the grants are copied from the source table
  being cloned.
- For [Apache Iceberg™ tables](/user-guide/tables-iceberg), cloning is currently supported for Snowflake-managed tables only. For more information, see
  [Cloning and Apache Iceberg™ tables](/user-guide/object-clone#label-cloning-and-iceberg-tables).

- For named internal stages:

  - Cloning is supported only at the database or schema level.
  - For stages with a directory table enabled, Snowflake uses the directory table as the source of truth for files on the stage.
    We recommend refreshing the directory table before cloning.

    The cloned stage contains copies of any undeleted files registered in the source directory table at the time of cloning.
    If a file has been updated, but the directory table isn’t refreshed, the updated file isn’t copied.
    After cloning, the source
    stage and the clone aren’t linked. Changes to files on the source stage don’t affect the files on the cloned stage (and the other way around).
  - For stages without a directory table enabled, Snowflake creates empty clones (doesn’t make copies of files on the source stage).
  - Snowflake makes clones of internal stages in their current state, regardless of whether your CREATE CLONE statement uses
    Time Travel (AT | BEFORE). If you specify a point in time before a stage was created, the stage won’t be cloned.
  - Cloning for internal stages relies on the [COPY FILES](/sql-reference/sql/copy-files) service, which incurs compute and file transfer charges.
    To monitor credit usage and bytes copied, you can query the [COPY\_FILES\_HISTORY view](/sql-reference/account-usage/copy_files_history) view.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Additional rules that apply to cloning objects

Metadata:
:   An object clone inherits the name and structure of the source object current at the time the CREATE *<object>* CLONE
    statement is executed or at a specified time/point in the past using [Time Travel](/user-guide/data-time-travel). An object clone
    inherits any other metadata, such as comments or table clustering keys, that is current in the source object at the time the statement
    is executed, regardless of whether Time Travel is used.

Child objects:
:   A database or schema clone includes all child objects active at the time the statement is executed or at the specified time/point
    in the past. A snapshot of the table data represents the state of the source data when the statement is executed or at the specified time/point
    in the past. Child objects inherit the name and structure of the source child objects at the time the statement is executed.

    Not cloned:
    :   Cloning a database or schema does not clone external tables in the database or schema.

        Hybrid tables can be cloned for databases but not for schemas.

    Pipes:
    :   A database or schema clone includes only pipe objects that reference external (Amazon S3, Google Cloud Storage, or Microsoft Azure)
        stages; internal (Snowflake) pipes are not cloned.

        The default state of a pipe clone is as follows:

        - When `AUTO_INGEST = FALSE`, a cloned pipe is paused by default.
        - When `AUTO_INGEST = TRUE`, a cloned pipe is set to the `STOPPED_CLONED` state. In this state, pipes do not accumulate event
          notifications as a result of newly staged files. When a pipe is explicitly resumed, it only processes data files triggered as a
          result of new event notifications.

        A pipe clone in either state can be resumed by executing an [ALTER PIPE](/sql-reference/sql/alter-pipe) … SET PIPE\_EXECUTION\_PAUSED = false statement.

    Tags:
    :   Cloning a database or schema affects [tags](/user-guide/object-tagging/introduction) in that database or schema as follows:

        - Tag associations in the source object (e.g. table) are maintained in the cloned objects.
        - For a database or a schema:

          When a database or schema is cloned, tags that reside in that schema or database are also cloned.

          If a table or view exists in the source schema/database and has references to tags in the same schema or database, the cloned table or view is mapped to the corresponding cloned tag (in the target schema/database) instead of the tag in the source schema or database.

    Java UDF:
    :   A Java UDF can be cloned when the database or schema containing the Java UDF is cloned. To be cloned, the Java UDF must meet certain
        conditions. For more information, see [Limitations on cloning](/developer-guide/udf/java/udf-java-limitations#label-limitations-on-cloning-java-udfs).

    Data metric functions:
    :   Cloning does not result in DMF assignments on the target object. If you clone a database or schema that contains DMFs, the DMFs are
        cloned to the target database or schema.

Table data:
:   When cloning a database, schema, or table, a snapshot of the data in each table is taken and made available to the clone. The snapshot
    represents the state of the source data either at the time the statement is executed or at the specified time/point in the past (using
    [Time Travel](/user-guide/data-time-travel)).

Object references:
:   Objects such as views, streams, and tasks include object references in their definition. For example:

    - A view contains a stored query that includes table references.
    - A stream points to a source table.
    - A task or alert calls a stored procedure or executes a SQL statement that references other objects.

    When one of these objects is cloned, either in a cloned database or schema or as an individual object, for those object types that support
    cloning, the clone inherits references to other objects from the definition of the source object. For example, a clone of a view inherits
    the stored query from the source view, including the table references in the query.

    Pay close attention to whether any object names in the definition of a source object are fully or partially qualified. A fully-qualified
    name includes the database and schema names. Any clone of the source object includes these parts in its own definition.

    For example:

    Copy code

    ```
    -- Create a schema to serve as the source for a cloned schema.
    CREATE SCHEMA source;

    -- Create a table.
    CREATE TABLE mytable (col1 string, col2 string);

    -- Create a view that references the table with a fully-qualified name.
    CREATE VIEW myview AS SELECT col1 FROM source.mytable;

    -- Retrieve the DDL for the source schema.
    SELECT GET_DDL ('schema', 'source', true);
    ```

    ```
    +--------------------------------------------------------------------------+
    | GET_DDL('SCHEMA', 'SOURCE', TRUE)                                        |
    |--------------------------------------------------------------------------|
    | create or replace schema MPETERS_DB.SOURCE;                              |
    |                                                                          |
    | create or replace TABLE MPETERS_DB.SOURCE.MYTABLE (                      |
    |   COL1 VARCHAR(16777216),                                                |
    |   COL2 VARCHAR(16777216)                                                 |
    | );                                                                       |
    |                                                                          |
    | create view MPETERS_DB.SOURCE.MYVIEW as select col1 from SOURCE.MYTABLE; |
    |                                                                          |
    +--------------------------------------------------------------------------+
    ```

    Copy code

    ```
    -- Clone the source schema.
    CREATE SCHEMA source_clone CLONE source;

    -- Retrieve the DDL for the clone of the source schema.
    -- The clone of the view references the source table with the same fully-qualified name
    -- as in the view in the source schema.
    SELECT GET_DDL ('schema', 'source_clone', true);
    ```

    ```
    +--------------------------------------------------------------------------------+
    | GET_DDL('SCHEMA', 'SOURCE_CLONE', TRUE)                                        |
    |--------------------------------------------------------------------------------|
    | create or replace schema MPETERS_DB.SOURCE_CLONE;                              |
    |                                                                                |
    | create or replace TABLE MPETERS_DB.SOURCE_CLONE.MYTABLE (                      |
    |   COL1 VARCHAR(16777216),                                                      |
    |   COL2 VARCHAR(16777216)                                                       |
    | );                                                                             |
    |                                                                                |
    | create view MPETERS_DB.SOURCE_CLONE.MYVIEW as select col1 from SOURCE.MYTABLE; |
    |                                                                                |
    +--------------------------------------------------------------------------------+
    ```

    If you intend to point a view to tables with the same names in *other* databases or schemas, we suggest creating a new view rather
    than cloning an existing view. This guidance also pertains to other objects that reference objects in their definition.

Note

- Certain limitations apply to cloning operations. For example, DDL statements that affect the source object during a cloning operation
  can alter the outcome or cause errors.
- Cloning is not instantaneous, particularly for large objects (databases, schemas, tables), and does not lock the object being cloned.
  As such, a clone does not reflect any DML statements applied to table data, if applicable, while the cloning operation is still running.

For more information about this and other use cases that might affect your cloning operations, see [Cloning considerations](/user-guide/object-clone).

## Notes for cloning with Time Travel

- The [AT | BEFORE](/sql-reference/constructs/at-before) clause clones a database, schema, or table as of a specified time in the past or based on
  a specified SQL statement:

  - The `AT` keyword specifies that the request is inclusive of any changes made by a statement or transaction with timestamp equal
    to the specified parameter.
  - The `BEFORE` keyword specifies that the request refers to a point immediately preceding the specified parameter.
- Cloning using `STATEMENT` is equivalent to using `TIMESTAMP` with a value equal to the recorded execution time of the SQL
  statement (or its enclosing transaction), as identified by the specified statement ID.
- An error is returned if:

  - The object being cloned did not exist at the point in the past specified in the [AT | BEFORE](/sql-reference/constructs/at-before) clause.
  - The historical data required to clone the object or any of its child objects (for example, tables in cloned schemas or database) has been
    purged.

    As a workaround for child objects that have been purged from Time Travel, use the
    [IGNORE TABLES WITH INSUFFICIENT DATA RETENTION](/sql-reference/sql/create-clone#label-ignore-tables-with-insufficient-data-retention) parameter of the
    CREATE <object> … CLONE command. For more information, see [Child objects and data retention time](/user-guide/object-clone#label-child-objects-and-data-retention-time).
- If any child object in a cloned database or schema did not exist at the point in the past specified in the
  [AT | BEFORE](/sql-reference/constructs/at-before) clause, the child object is not cloned.

If you don’t specify a point in time, the clone defaults to the state of the object as of now
(the [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) value).

For more information, see [Understanding & using Time Travel](/user-guide/data-time-travel).

### Troubleshoot cloning objects using Time Travel

The following scenarios can help you troubleshoot issues that can occur when cloning an object using Time Travel.

|  |  |
| --- | --- |
| Error | ``` 000707 (02000): Time travel data is not available for <object_type> <object_name>. The requested time is either beyond the allowed time travel period or before the object creation time. ``` |

Expand

Show lessSee more

This error can be returned for the following reasons:

|  |  |
| --- | --- |
| Cause | The time in the past specified by the AT | BEFORE clause is beyond the data retention period for the object. |
| Solution | Verify the data retention period for the object using the appropriate [SHOW <objects>](/sql-reference/sql/show) command and the `retention_time` column. Update the CREATE *<object>* … CLONE statement to use a time in the past that is within the data retention period for the object. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Cause | The cloning operation for a database or schema fails if the historical data for any child object has moved out of Time Travel. |
| Solution | To skip child tables that no longer have historical data available in Time Travel, execute the cloning statement using the [IGNORE TABLES WITH INSUFFICIENT DATA RETENTION](/sql-reference/sql/create-clone#label-ignore-tables-with-insufficient-data-retention) parameter to skip these tables. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Cause | In some cases, this is caused by using a string where a timestamp is expected. |
| Solution | Cast the string to a timestamp.  Copy code  ``` ... AT(TIMESTAMP => '2023-12-31 12:00:00')               -- fails ... AT(TIMESTAMP => '2023-12-31 12:00:00'::TIMESTAMP)    -- succeeds ``` |

Expand

Show lessSee more

## Examples

Clone a database and all objects within the database at its current state:

Copy code

```
CREATE DATABASE mytestdb_clone CLONE mytestdb;
```

Clone a schema and all objects within the schema at its current state:

Copy code

```
CREATE SCHEMA mytestschema_clone CLONE testschema;
```

Clone a table at its current state:

Copy code

```
CREATE TABLE orders_clone CLONE orders;
```

Clone a schema as it existed before the date and time in the specified timestamp:

Copy code

```
CREATE SCHEMA mytestschema_clone_restore CLONE testschema
  BEFORE (TIMESTAMP => TO_TIMESTAMP(40*365*86400));
```

Clone a table as it existed exactly at the date and time of the specified timestamp:

Copy code

```
CREATE TABLE orders_clone_restore CLONE orders
  AT (TIMESTAMP => TO_TIMESTAMP_TZ('04/05/2013 01:02:03', 'mm/dd/yyyy hh24:mi:ss'));
```

Clone a table as it existed immediately before the execution of the specified statement. Replace the query ID for the STATEMENT
parameter in the example and execute the following CREATE TABLE statement:

Copy code

```
CREATE TABLE orders_clone_restore CLONE orders BEFORE (STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726');
```

Clone a database and all its objects as they existed four days ago and skip any tables that have a data retention period of
less than four days:

Copy code

```
CREATE DATABASE restored_db CLONE my_db
  AT (TIMESTAMP => DATEADD(days, -4, current_timestamp)::timestamp_tz)
  IGNORE TABLES WITH INSUFFICIENT DATA RETENTION;
```

Clone a schema that contains a mixture of standard tables and hybrid tables:

Copy code

```
CREATE OR REPLACE SCHEMA clone_ht_schema CLONE ht_schema
  IGNORE HYBRID TABLES;
```

The new schema will only contain the standard tables from the original schema. If IGNORE HYBRID TABLES is not specified
in this example, the command fails with an error because schemas that contain hybrid tables can’t be cloned.
