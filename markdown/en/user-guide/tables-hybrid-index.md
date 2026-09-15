# Index hybrid tables

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This topic explains how to index [hybrid tables](/user-guide/tables-hybrid).

## Types of indexes

Hybrid tables support two types of indexes:

- Indexes that are created automatically when you declare constraints for hybrid table columns.

  - Indexes for PRIMARY KEY constraints
  - Indexes for FOREIGN KEY constraints
  - Indexes for UNIQUE constraints
- User-defined indexes, known as *secondary indexes*, that you can define on other columns as needed.
  A single index can cover one or more columns. You can use CREATE HYBRID TABLE or CREATE INDEX to
  define secondary indexes.

  When you create secondary indexes, you can “include” columns that are not part of the index key but are
  associated and stored with the index itself. See [INCLUDE columns](#label-indexes-with-include-columns).

  Attention

  To add a secondary index, you must use a role that is granted the SELECT
  privilege on the hybrid table. If you have access to a view of the
  data in the hybrid table, but not the table itself, you can’t add a secondary index.

## Add secondary indexes

All hybrid tables require a unique primary key. The data in a hybrid table is ordered by this primary key.
You can create additional secondary indexes on non-primary key attributes to accelerate lookups on those
attributes. Indexes might be able to reduce the number of records that are scanned when
a query predicate uses one of the following conditions:

- `=`, `>`, `>=`, `<`, `<=` ([comparison operators](/sql-reference/operators-comparison))
- [[ NOT ] IN](/sql-reference/functions/in) conditions
- [[ NOT ] BETWEEN](/sql-reference/functions/between) conditions
- [STARTSWITH](/sql-reference/functions/startswith) conditions
- prefix patterns (`LIKE '<prefix>%'`)

Note that `ILIKE` patterns don’t qualify for index use and require a full table scan.

If you have common, repeated queries with predicates on a specific attribute or a composite group of attributes,
consider adding an index to that attribute or group of attributes to improve performance. Be aware of the
following considerations when you use indexes:

- Increase in storage consumption when storing additional copies of the subset of data in the index.
- Additional overhead on DMLs because indexes are maintained synchronously.

You can add secondary indexes to a hybrid table when you create it, or you can add them later by using the
CREATE INDEX command. For example, the following CREATE HYBRID TABLE statement creates two indexes automatically (on the
PRIMARY KEY and UNIQUE columns, `col1` and `col2`) and one user-defined secondary index (on `col3`):

Copy code

```
CREATE OR REPLACE HYBRID TABLE target_hybrid_table (
    col1 VARCHAR(32) PRIMARY KEY,
    col2 NUMBER(38,0) UNIQUE,
    col3 NUMBER(38,0),
    INDEX index_col3 (col3)
    )
  AS SELECT col1, col2, col3 FROM source_table;
```

Alternatively, you can create a secondary index for an existing hybrid table by using the
[CREATE INDEX](/sql-reference/sql/create-index) command. Use this command to add an index to a hybrid table
that is actively being used for a workload and is serving queries, or has foreign keys. The CREATE INDEX
command builds indexes concurrently without locking the table during the operation.

When you use [ALTER TABLE](/sql-reference/sql/alter-table) to add a UNIQUE or FOREIGN KEY constraint to an
existing hybrid table, Snowflake builds the underlying index the same way, so the table stays
available while the build runs. Because that build also validates the rows that are already in the
table, it can fail when existing data violates the new constraint. For more information, see
[Add and drop constraints on an existing hybrid table](/sql-reference/sql/create-hybrid-table#label-hybrid-table-online-constraints).

Tip

Check the index build status with the [SHOW INDEXES](/sql-reference/sql/show-indexes) command. Only one
index build at a time is supported.

However, if your hybrid table application is in development or test mode, and some downtime for the
table is not an issue, it is more efficient to recreate the hybrid table and create the indexes by
running an optimized bulk load. This method is more efficient than online index building with the CREATE INDEX
command.

Optimized bulk loading is supported for CTAS, COPY, and all variants of INSERT except INSERT ALL.
The same rules apply as in [Loading data](/user-guide/tables-hybrid-create#label-create-loading-data): when a hybrid table is empty, all of these
methods use optimized bulk loading; when a hybrid table already contains data, optimized bulk loading
is automatically used for COPY and for all variants of INSERT except INSERT ALL, depending on the size
and number of rows being loaded.

You can’t define a FOREIGN KEY constraint in a CTAS statement. The second table created in this
example, `fk_hybrid_table`, would have to be bulk-loaded with COPY or INSERT INTO … SELECT.
Alternatively, you can use CTAS to create and load the table without the foreign key, then add the
foreign key afterward with [ALTER TABLE](/sql-reference/sql/alter-table). See
[Add and drop constraints on an existing hybrid table](/sql-reference/sql/create-hybrid-table#label-hybrid-table-online-constraints).

Copy code

```
CREATE OR REPLACE HYBRID TABLE ref_hybrid_table (
    col1 VARCHAR(32) PRIMARY KEY,
    col2 NUMBER(38,0) UNIQUE
);

CREATE OR REPLACE HYBRID TABLE fk_hybrid_table (
    col1 VARCHAR(32) PRIMARY KEY,
    col2 NUMBER(38,0),
    col3 NUMBER(38,0),
    FOREIGN KEY (col2) REFERENCES ref_hybrid_table(col2),
    INDEX index_col3 (col3)
);
```

### INCLUDE columns

Although they are not part of the secondary index key, INCLUDE columns are stored with the index records. Because of this
association between the actual indexed columns and the data in the included columns, certain queries can avoid table scans and
benefit from less costly scans that use the index. However, using included columns in indexes might cause an
increase in storage consumption because additional columns are stored with the indexed columns.

For example, consider the following table and index. The index in this case could be declared in either the CREATE TABLE
statement or the CREATE INDEX statement.

Copy code

```
CREATE OR REPLACE HYBRID TABLE sensor_data_device1 (
  device_id VARCHAR(10),
  timestamp TIMESTAMP PRIMARY KEY,
  temperature DECIMAL(6,4),
  vibration DECIMAL(6,4),
  motor_rpm INT
  );

CREATE INDEX sec_sensor_idx
  ON sensor_data_device1(temperature)
    INCLUDE (vibration, motor_rpm);
```

Because this secondary index covers one column directly (`temperature`) and two columns indirectly
(`vibration, motor_rpm`), the index can be used to optimize certain queries that constrain `temperature` and select
data from the included columns.

To test this behavior, first generate some rows for the table:

Copy code

```
INSERT INTO sensor_data_device1 (device_id, timestamp, temperature, vibration, motor_rpm)
  SELECT 'DEVICE1', timestamp,
    UNIFORM(25.1111, 40.2222, RANDOM()), -- Temperature range in °C
    UNIFORM(0.2985, 0.3412, RANDOM()), -- Vibration range in mm/s
    UNIFORM(1400, 1495, RANDOM()) -- Motor RPM range
  FROM (
    SELECT DATEADD(SECOND, SEQ4(), '2024-03-01') AS timestamp
      FROM TABLE(GENERATOR(ROWCOUNT => 2678400)) -- seconds in 31 days
  );
```

Now run the following query:

Copy code

```
SELECT temperature, vibration, motor_rpm
  FROM sensor_data_device1
  WHERE temperature = 25.6;
```

This query makes use of the secondary index named `sec_sensor_idx`. You can verify this behavior
by running the EXPLAIN command on the query or by reviewing the query profile in Snowsight.
You will see an index scan on the secondary index and no “probe scan” on the hybrid table itself.

The following queries, using other supported WHERE clause conditions, would also benefit from the
same secondary index:

Copy code

```
SELECT temperature, vibration, motor_rpm
  FROM sensor_data_device1
  WHERE temperature IN (25.6, 31.2, 35.8);

SELECT temperature, vibration, motor_rpm
  FROM sensor_data_device1
  WHERE temperature BETWEEN 25.0 AND 26.0;
```

Now modify the first query by adding the `device_id` column to the select list. This column isn’t covered by
the `sec_sensor_idx` index.

Copy code

```
SELECT device_id, temperature, vibration, motor_rpm
  FROM sensor_data_device1
  WHERE temperature = 25.6;
```

This query can’t depend on the secondary index entirely; a probe scan of the hybrid table is needed
to return the correct `device_id` values.
