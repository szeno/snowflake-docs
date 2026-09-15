# Continuous data pipeline examples

This topic provides practical examples of use cases for data pipelines.

## Prerequisites

The role used to execute the SQL statements in these examples requires the following access control privileges:

`EXECUTE TASK`
:   Global EXECUTE TASK privilege to run tasks

`USAGE`
:   USAGE privilege on the database and schema in which the SQL statements are executed, as well as on the warehouse that runs any tasks in these examples.

`CREATE object`
:   Various `CREATE object` privileges on the schema in which the SQL statements are executed, to create objects such as tables, streams, and tasks.

For more information about access control in Snowflake, see [Overview of Access Control](/user-guide/security-access-control-overview).

## Transform loaded JSON data on a schedule

The following example loads raw JSON data into a single landing table named `raw`. Two tasks query table streams created on the `raw` table and insert subsets of rows into multiple tables. Because each task consumes the change data capture records in a table stream, multiple streams are required.

Copy code

```
-- Create a landing table to store raw JSON data.
-- Snowpipe could load data into this table.
create or replace table raw (var variant);

-- Create a stream to capture inserts to the landing table.
-- A task will consume a set of columns from this stream.
create or replace stream rawstream1 on table raw;

-- Create a second stream to capture inserts to the landing table.
-- A second task will consume another set of columns from this stream.
create or replace stream rawstream2 on table raw;

-- Create a table that stores the names of office visitors identified in the raw data.
create or replace table names (id int, first_name string, last_name string);

-- Create a table that stores the visitation dates of office visitors identified in the raw data.
create or replace table visits (id int, dt date);

-- Create a task that inserts new name records from the rawstream1 stream into the names table
-- every minute when the stream contains records.
-- Replace the 'mywh' warehouse with a warehouse that your role has USAGE privilege on.
create or replace task raw_to_names
warehouse = mywh
schedule = '1 minute'
when
system$stream_has_data('rawstream1')
as
merge into names n
  using (select var:id id, var:fname fname, var:lname lname from rawstream1) r1 on n.id = to_number(r1.id)
  when matched then update set n.first_name = r1.fname, n.last_name = r1.lname
  when not matched then insert (id, first_name, last_name) values (r1.id, r1.fname, r1.lname)
;

-- Create another task that merges visitation records from the rawstream2 stream into the visits table
-- every minute when the stream contains records.
-- Records with new IDs are inserted into the visits table;
-- Records with IDs that exist in the visits table update the DT column in the table.
-- Replace the 'mywh' warehouse with a warehouse that your role has USAGE privilege on.
create or replace task raw_to_visits
warehouse = mywh
schedule = '1 minute'
when
system$stream_has_data('rawstream2')
as
merge into visits v
  using (select var:id id, var:visit_dt visit_dt from rawstream2) r2 on v.id = to_number(r2.id)
  when matched then update set v.dt = r2.visit_dt
  when not matched then insert (id, dt) values (r2.id, r2.visit_dt)
;

-- Resume both tasks.
alter task raw_to_names resume;
alter task raw_to_visits resume;

-- Insert a set of records into the landing table.
insert into raw
  select parse_json(column1)
  from values
  ('{"id": "123","fname": "Jane","lname": "Smith","visit_dt": "2019-09-17"}'),
  ('{"id": "456","fname": "Peter","lname": "Williams","visit_dt": "2019-09-17"}');

-- Query the change data capture record in the table streams
select * from rawstream1;
select * from rawstream2;

-- Wait for the tasks to run.
-- A tiny buffer is added to the wait time
-- because absolute precision in task scheduling is not guaranteed.
call system$wait(70);

-- Query the table streams again.
-- Records should be consumed and no longer visible in streams.

-- Verify the records were inserted into the target tables.
select * from names;
select * from visits;

-- Insert another set of records into the landing table.
-- The records include both new and existing IDs in the target tables.
insert into raw
  select parse_json(column1)
  from values
  ('{"id": "456","fname": "Peter","lname": "Williams","visit_dt": "2019-09-25"}'),
  ('{"id": "789","fname": "Ana","lname": "Glass","visit_dt": "2019-09-25"}');

-- Wait for the tasks to run.
call system$wait(70);

-- Records should be consumed and no longer visible in streams.
select * from rawstream1;
select * from rawstream2;

-- Verify the records were inserted into the target tables.
select * from names;
select * from visits;
```

## Unload data on a schedule

The following example unloads the change data capture records in a stream into an internal (i.e. Snowflake) stage.

Copy code

```
-- Use the landing table from the previous example.
-- Alternatively, create a landing table.
-- Snowpipe could load data into this table.
create or replace table raw (id int, type string);

-- Create a stream on the table.  We will use this stream to feed the unload command.
create or replace stream rawstream on table raw;

-- Create a task that executes the COPY statement every minute.
-- The COPY statement reads from the stream and loads into the table stage for the landing table.
-- Replace the 'mywh' warehouse with a warehouse that your role has USAGE privilege on.
create or replace task unloadtask
warehouse = mywh
schedule = '1 minute'
when
  system$stream_has_data('RAWSTREAM')
as
copy into @%raw/rawstream from rawstream overwrite=true;
;

-- Resume the task.
alter task unloadtask resume;

-- Insert raw data into the landing table.
insert into raw values (3,'processed');

-- Query the change data capture record in the table stream
select * from rawstream;

-- Wait for the tasks to run.
-- A tiny buffer is added to the wait time
-- because absolute precision in task scheduling is not guaranteed.
call system$wait(70);

-- Records should be consumed and no longer visible in the stream.
select * from rawstream;

-- Verify the COPY statement unloaded a data file into the table stage.
ls @%raw;
```

## Refresh external table metadata on a schedule

The following example refreshes the metadata for an external table named `mydb.myschema.exttable` (using [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) … REFRESH) on a schedule.

Note

When an external table is created, the AUTO\_REFRESH parameter is set to `TRUE` by default. We recommend that you accept this default value for external tables that reference data files in either Amazon S3 or Microsoft Azure stages. However, the automatic refresh option is not available currently for external tables that reference Google Cloud Storage stages. For these external tables, manually refreshing the metadata on a schedule can be useful.

Copy code

```
-- Create a task that executes an ALTER EXTERNAL TABLE ... REFRESH statement every 5 minutes.
-- Replace the 'mywh' warehouse with a warehouse that your role has USAGE privilege on.
CREATE TASK exttable_refresh_task
WAREHOUSE=mywh
SCHEDULE='5 minutes'
  AS
ALTER EXTERNAL TABLE mydb.myschema.exttable REFRESH;
```
