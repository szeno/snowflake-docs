Categories:
:   [Query syntax](/sql-reference/constructs)

# CHANGES

The CHANGES clause enables querying the change tracking metadata for a table or view within a specified interval of time
without having to create a stream with an explicit transactional offset. Multiple queries can retrieve the change tracking
metadata between different transactional start and endpoints.

Note

Change tracking must be enabled on the source table or the source view and its underlying tables. For details, see the usage notes
(in this topic).

In a query, the CHANGES clause is specified in the [FROM](/sql-reference/constructs/from) clause.

The optional END keyword specifies the end of the change interval. The results are inclusive of the end marker.

## Syntax

Copy code

```
SELECT ...
FROM ...
   CHANGES ( INFORMATION => { DEFAULT | APPEND_ONLY } )
   AT ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> | STREAM => '<name>' } ) | BEFORE ( STATEMENT => <id> )
   [ END( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
[ ... ]
```

## Parameters

`INFORMATION => { DEFAULT | APPEND_ONLY }`
:   Specifies the type of change tracking data to return based on the metadata recorded in each:

    `DEFAULT`
    :   Returns all DML changes to the source object, including inserts, updates, and deletes (including table truncates). This type of change
        tracking compares inserted and deleted rows in the change set to provide the row level delta. As a net effect, for example, a row that
        is inserted and then deleted between two transactional points of time in a table is removed in the delta (i.e. is not returned in the
        query results).

    `APPEND_ONLY`
    :   Returns appended rows only; therefore no join is performed. As a result, querying append-only changes can be much more performant than querying standard (default) changes for extract, load, transform (ELT) and similar scenarios that depend exclusively on row inserts.

`TIMESTAMP => timestamp`
:   Specifies an exact date and time to use for Time Travel. Note that the value must be explicitly cast to a TIMESTAMP.

`OFFSET => time_difference`
:   Specifies the difference in seconds from the current time to use for Time Travel, in the form `-N` where `N` can be an integer or arithmetic expression (e.g. `-120` is 120 seconds, `-30*60`
    is 1800 seconds or 30 minutes).

`STATEMENT => id`
:   Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types:

    - DML (e.g. INSERT, UPDATE, DELETE)
    - TCL (BEGIN, COMMIT transaction)
    - SELECT

`STREAM => 'name'`
:   Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in
    the stream is used as the `AT` point in time for returning change data for the source object.

## Usage notes

- The CHANGES clause is not supported when querying for changes (which are resolved using change-tracking metadata) for
  [directory tables](/user-guide/data-load-dirtables) or [external tables](/user-guide/tables-external-intro).
- Currently, at least one of the following must be true before change tracking metadata is recorded for a table:

  - Change tracking is enabled on the table or view for the interval queried by CHANGES.
  - A stream is created for the table.

  Change tracking can be enabled explicitly by using the [ALTER TABLE](/sql-reference/sql/alter-table) command or implicitly when a stream or table is created.

  Copy code

  ```
  ALTER TABLE mytable SET CHANGE_TRACKING = TRUE;
  ```

  Both options add hidden columns to the table which store change tracking metadata. The columns consume a small amount of storage.

  To query the change data for a view, change tracking must be enabled on the source view and its underlying tables. For instructions, see
  [Enabling change tracking on views and underlying tables](/user-guide/streams-manage#label-enabling-change-tracking-views). Additionally, the view is subject to the same limitations as streams on views. For more information, see [Streams on views](/user-guide/streams-intro#label-streams-views).
- The [AT | BEFORE](/sql-reference/constructs/at-before) clause is required and sets the current offset for the change tracking metadata.
- The optional END clause sets the end timestamp for the change interval. If no END value is specified, the current timestamp is used as the end of the change interval.

  Note that the END clause is valid only when combined with the CHANGES clause to query change tracking metadata (i.e. this clause cannot be combined with AT|BEFORE when using Time Travel to query historic data for other objects).
- The value for TIMESTAMP or OFFSET must be a constant expression.
- The smallest time resolution for TIMESTAMP is milliseconds.
- If requested data is beyond the Time Travel retention period (default is 1 day), the statement fails.

  In addition, if the requested data is within the Time Travel retention period but no historical data is available (e.g. if the retention period was extended), the statement fails.
- The CHANGES clause computes the changes on the specified interval, without maintaining a durable [offset store](/user-guide/streams-intro#label-streams-introduction-offset). For more information, see [CHANGES clause: Read-only alternative to streams](/user-guide/streams-intro#label-streams-changes-clause).

## Examples

The following example queries the standard (delta) and append-only change tracking metadata for a table. No END() value is provided, so the current timestamp is used as the endpoint in the transactional interval of time:

Copy code

```
 CREATE OR REPLACE TABLE t1 (
   id number(8) NOT NULL,
   c1 varchar(255) default NULL
 );

-- Enable change tracking on the table.
 ALTER TABLE t1 SET CHANGE_TRACKING = TRUE;

 -- Initialize a session variable for the current timestamp.
 SET ts1 = (SELECT CURRENT_TIMESTAMP());

 INSERT INTO t1 (id,c1)
 VALUES
 (1,'red'),
 (2,'blue'),
 (3,'green');

 DELETE FROM t1 WHERE id = 1;

 UPDATE t1 SET c1 = 'purple' WHERE id = 2;

 -- Query the change tracking metadata in the table during the interval from $ts1 to the current time.
 -- Return the full delta of the changes.
 SELECT *
 FROM t1
   CHANGES(INFORMATION => DEFAULT)
   AT(TIMESTAMP => $ts1);

 +----+--------+-----------------+-------------------+------------------------------------------+
 | ID | C1     | METADATA$ACTION | METADATA$ISUPDATE | METADATA$ROW_ID                          |
 |----+--------+-----------------+-------------------+------------------------------------------|
 |  2 | purple | INSERT          | False             | 1614e92e93f86af6348f15af01a85c4229b42907 |
 |  3 | green  | INSERT          | False             | 86df000054a4d1dc64d5d74a44c3131c4c046a1f |
 +----+--------+-----------------+-------------------+------------------------------------------+

 -- Query the change tracking metadata in the table during the interval from $ts1 to the current time.
 -- Return the append-only changes.
 SELECT *
 FROM t1
   CHANGES(INFORMATION => APPEND_ONLY)
   AT(TIMESTAMP => $ts1);

 +----+-------+-----------------+-------------------+------------------------------------------+
 | ID | C1    | METADATA$ACTION | METADATA$ISUPDATE | METADATA$ROW_ID                          |
 |----+-------+-----------------+-------------------+------------------------------------------|
 |  1 | red   | INSERT          | False             | 6a964a652fa82974f3f20b4f49685de54eeb4093 |
 |  2 | blue  | INSERT          | False             | 1614e92e93f86af6348f15af01a85c4229b42907 |
 |  3 | green | INSERT          | False             | 86df000054a4d1dc64d5d74a44c3131c4c046a1f |
 +----+-------+-----------------+-------------------+------------------------------------------+
```

The following example consumes the append-only changes for a table from a transactional point of time before the rows were deleted from the table:

Copy code

```
CREATE OR REPLACE TABLE t1 (
  id number(8) NOT NULL,
  c1 varchar(255) default NULL
);

-- Enable change tracking on the table.
ALTER TABLE t1 SET CHANGE_TRACKING = TRUE;

-- Initialize a session 'start timestamp' variable for the current timestamp.
SET ts1 = (SELECT CURRENT_TIMESTAMP());

INSERT INTO t1 (id,c1)
VALUES
(1,'red'),
(2,'blue'),
(3,'green');

-- Initialize a session 'end timestamp' variable for the current timestamp.
SET ts2 = (SELECT CURRENT_TIMESTAMP());

DELETE FROM t1 WHERE id = 3;
SET last_query_id = (SELECT LAST_QUERY_ID());

-- Create a table populated by the change data between the start and end timestamps.
CREATE OR REPLACE TABLE t2 (
  c1 varchar(255) default NULL
  )
AS SELECT C1
  FROM t1
  CHANGES(INFORMATION => APPEND_ONLY)
  AT(TIMESTAMP => $ts1)
  END(TIMESTAMP => $ts2);

SELECT * FROM t2;

+-------+
| C1    |
|-------|
| red   |
| blue  |
| green |
+-------+

-- Create a table populated by the change data between the start timestamp and end statement.
-- This example demonstrates that END is inclusive of the statement passed in.
CREATE OR REPLACE TABLE t3 (
  c1 varchar(255) default NULL
  )
AS SELECT C1
  FROM t1
  CHANGES(INFORMATION => DEFAULT)
  AT(TIMESTAMP => $ts1)
  END(STATEMENT => $last_query_id);

+-------+
| C1    |
|-------|
| red   |
| blue  |
+-------+
```

The following example is similar to the previous example. This example uses the current
offset for a stream on the source table as the start point in time for populating the new table
with change data from the source table. Because a stream is created on the source object,
you do not need to explicitly enable change tracking on the object:

Copy code

```
CREATE OR REPLACE TABLE t1 (
  id number(8) NOT NULL,
  c1 varchar(255) default NULL
);

-- Create a stream on the table.
CREATE OR REPLACE STREAM s1 ON TABLE t1;

INSERT INTO t1 (id,c1)
VALUES
(1,'red'),
(2,'blue'),
(3,'green');

-- Initialize a session 'end timestamp' variable for the current timestamp.
SET ts2 = (SELECT CURRENT_TIMESTAMP());

DELETE FROM t1;

-- Create a table populated by the change data between the current
-- s1 offset and the end timestamp.
CREATE OR REPLACE TABLE t2 (
  c1 varchar(255) default NULL
  )
AS SELECT C1
  FROM t1
  CHANGES(INFORMATION => APPEND_ONLY)
  AT(STREAM => 's1')
  END(TIMESTAMP => $ts2);

SELECT * FROM t2;

+-------+
| C1    |
|-------|
| red   |
| blue  |
| green |
+-------+
```
