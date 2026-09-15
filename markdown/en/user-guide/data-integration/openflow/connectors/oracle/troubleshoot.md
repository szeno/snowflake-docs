# Troubleshooting the Openflow Connector for Oracle

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Note

The Openflow Connector for Oracle is also subject to additional terms of service beyond the standard
connector terms of service. For more information, see the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

This topic describes how to troubleshoot common issues with the
Openflow Connector for Oracle.

## A table was added to replication but doesn’t appear in Snowflake

The table’s fully qualified name (FQN) might be incorrectly specified in the connector
configuration.

**Solution**

- Check the format of the FQN in `Oracle Ingestion Parameters`. It should be
  `<database_name>.<schema_name>.<table_name>` (note the database prefix).
- Check the database name in `Oracle Source Parameters` » `Oracle Connection URL`.
  While FQNs support specifying the name of the database, currently data must reside in
  the same database instance as the one used for this connection.
- Verify that you have provided the full database name including the domain name in the
  connector configuration. For example, use `MYDB.EXAMPLE.COM` instead of just `MYDB`.

  To find the correct database name, run the following query on your Oracle database:

  Copy code

  ```
  SELECT property_value
    FROM database_properties
    WHERE property_name = 'GLOBAL_DB_NAME';
  ```

  In general, `property_value` is the same as the service name of the database.
  However, the returned database name might include an appended domain name (for
  example, for service name `FOO`, the query might return `FOO.EXAMPLE.COM`). In
  that case, use the full name with the domain (double-quoted, because it contains dots).

## A table fails because the connector can’t find a replication key

The connector reports that a table can’t be replicated because no primary key, unique
constraint, or unique index qualifies as a replication key. The connector evaluates
candidates as described in [How the connector chooses a replication key](/user-guide/data-integration/openflow/connectors/oracle/about#label-oracle-replication-key-selection).

**Solution**

1. Confirm the table has no primary key:

   Copy code

   ```
   SELECT constraint_name, status
   FROM all_constraints
   WHERE owner = 'YOUR_SCHEMA'
     AND table_name = 'YOUR_TABLE'
     AND constraint_type = 'P';
   ```
2. Find unique constraints that the connector skipped, and check why they didn’t
   qualify (`STATUS != ENABLED`, `DEFERRED != IMMEDIATE`, or any column nullable):

   Copy code

   ```
   SELECT c.constraint_name,
       c.status,
       c.deferred,
       acc.column_name,
       atc.nullable
   FROM all_constraints c
   JOIN all_cons_columns acc
     ON acc.owner = c.owner
    AND acc.constraint_name = c.constraint_name
   JOIN all_tab_cols atc
     ON atc.owner = acc.owner
    AND atc.table_name = acc.table_name
    AND atc.column_name = acc.column_name
   WHERE c.owner = 'YOUR_SCHEMA'
     AND c.table_name = 'YOUR_TABLE'
     AND c.constraint_type = 'U';
   ```
3. Find unique indexes that the connector skipped, and check why they didn’t qualify
   (`STATUS = UNUSABLE`, `INDEX_TYPE != NORMAL`, the index backs a constraint, or
   any column is nullable):

   Copy code

   ```
   SELECT i.index_name,
       i.uniqueness,
       i.status,
       i.index_type,
       ic.column_name,
       atc.nullable
   FROM all_indexes i
   JOIN all_ind_columns ic
     ON i.owner = ic.index_owner
    AND i.index_name = ic.index_name
   JOIN all_tab_cols atc
     ON atc.owner = ic.table_owner
    AND atc.table_name = ic.table_name
    AND atc.column_name = ic.column_name
   WHERE ic.table_owner = 'YOUR_SCHEMA'
     AND ic.table_name = 'YOUR_TABLE'
     AND i.uniqueness = 'UNIQUE';
   ```

Resolve the issue by one of the following:

- Add a primary key, or modify an existing constraint or index so it qualifies (enable
  it, change `DEFERRABLE INITIALLY DEFERRED` to `DEFERRABLE INITIALLY IMMEDIATE`,
  rebuild an unusable index, or add `NOT NULL` to the relevant columns).
- Specify a logical key for the table. For more information, see
  [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-logical-key).

After you make the change, restart replication for the affected table: see
[Restart table replication](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-of-oracle-restart-table-replication).

## The CDC processor doesn’t start after editing Table Key Configuration JSON

The **Read Oracle CDC Stream** processor stays invalid or fails to start after you
configure or update the **Table Key Configuration JSON** value on a
`MultiDatabaseJsonTableKeyConfigService` controller service. The controller service
itself fails to enable because the JSON value is malformed, which keeps the CDC
processor invalid because it depends on the service.

**Solution**

1. Open the controller service properties and review the validation message on the
   **Table Key Configuration JSON** field.
2. Correct the JSON. For the expected format, see
   [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-logical-key).
3. Enable the controller service. Once it’s enabled, start the CDC processor.

## A logical-key column was dropped or renamed on the source

A table that uses a user-declared logical key is marked `FAILED` after a column listed
in `logicalKey` is dropped or renamed on the source. The connector can’t continue
replicating the table because the configured key columns no longer match the live
schema.

**Solution**

1. Update the **Table Key Configuration JSON** value on the
   `MultiDatabaseJsonTableKeyConfigService` controller service so that `logicalKey`
   uses the current column names. Disable and re-enable the service for the change to
   take effect.
2. Restart replication for the affected table: see
   [Restart table replication](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-of-oracle-restart-table-replication).

## A logical-key configuration references a column that doesn’t exist

A table stays in the `NEW` state and the connector log shows a message such as
“`Logical key column '<column>' does not exist in table schema`”. The
**Table Key Configuration JSON** value lists a column name that the connector can’t
find on the source table.

**Solution**

1. Confirm the column exists and check its name in `ALL_TAB_COLS`:

   Copy code

   ```
   SELECT column_name
   FROM all_tab_cols
   WHERE owner = 'YOUR_SCHEMA'
     AND table_name = 'YOUR_TABLE'
     AND user_generated = 'YES';
   ```
2. Correct the column name in the **Table Key Configuration JSON** value. Disable and
   re-enable the controller service for the change to take effect.

You don’t need to remove and re-add the table: the connector retries schema
initialization on the next poll, and replication resumes from `NEW`.

## A logical-key column contains duplicate values in the source

A column declared in the **Table Key Configuration JSON** as part of the logical key
doesn’t actually contain unique values in the source table. The connector doesn’t
validate data-level uniqueness of logical-key values, so this condition doesn’t produce
an error.

**Impact**

The connector’s MERGE operation deduplicates rows by logical-key value using a
last-write-wins strategy. When multiple source rows share the same logical-key value:

- During the snapshot, only one row per key value reaches the destination. The other
  rows are silently dropped.
- During incremental replication, change events for different source rows that share a
  key value overwrite each other in the destination.

This results in silent data loss with no error in the connector log.

**Solution**

1. Verify whether the logical-key columns contain duplicates:

   Copy code

   ```
   SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT <logical_key_columns>) AS distinct_keys
   FROM <schema>.<table>;
   ```

   If `total_rows` differs from `distinct_keys`, the columns aren’t suitable as a
   logical key.
2. Correct the key configuration (choose columns that are unique, or add a primary key
   to the table) and run a full reload for the affected table to reconcile the
   destination.

Note

To avoid this issue, verify uniqueness before declaring a logical key. On large
tables, consider running the verification query during a low-traffic window or
sampling with a `WHERE` clause.

## No changes in incremental load

The incremental load isn’t capturing or applying changes from the source database.

**Solution**

Run the verification for the **Read Oracle CDC Stream** processor:

1. In your Openflow runtime, double-click the **Oracle** flow.
2. Double-click the process group named **Incremental Load**.
3. Find the **Read Oracle CDC Stream** processor.

   1. If it is running, right-click and select **Stop**. The processor must be stopped
      before you can verify its configuration.
4. Right-click **Read Oracle CDC Stream** again, then select **Configure**.
5. Select the **Properties** tab.
6. Select the **Verification** checkmark icon in the upper-right corner.
7. In the popup window that appears, select **Verify** in the lower-right corner.

   The results of the verification procedure appear below. The procedure validates
   database connectivity and checks the status of the components required for incremental
   load to work.

If any of the verification steps fail, view the error message, fix the issue, and run the
verification again. The following sections describe specific issues and solutions.

## The connector stops reading changes after a network interruption with no errors

The **Read Oracle CDC Stream** processor stops producing data but reports no errors. The
processor appears to be running, yet no new changes are ingested, and it recovers only
after the runtime is restarted.

This occurs only when the connection to the Oracle database is dropped silently and no
read timeout is configured: for example, a firewall or load balancer that drops an idle
connection without notifying either side. The connector keeps waiting to read from a
connection that is no longer alive, with no error to trigger a reconnect. Interruptions
that close the connection cleanly surface an error and the connector recovers on its own.

**Solution**

Configure read timeouts on both connection URLs in `Oracle Source Parameters`. The
following examples use a 5-minute timeout:

- `Oracle Connection URL` (thin driver): add the `oracle.jdbc.ReadTimeout` property
  (in milliseconds) to the URL query string. You can use either URL form:
  - Easy Connect: `jdbc:oracle:thin:@//<host>:<port>/DB?oracle.jdbc.ReadTimeout=300000`
  - TNS connect descriptor: `jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=...)(CONNECT_DATA=...))?oracle.jdbc.ReadTimeout=300000`
- `XStream Out Server URL` (OCI driver): add the `RECV_TIMEOUT` parameter (in seconds)
  inside the TNS connect descriptor. The OCI driver honors `RECV_TIMEOUT` only in the
  TNS connect descriptor form, not in the short Easy Connect form:
  - TNS connect descriptor: `jdbc:oracle:oci:@(DESCRIPTION=(RECV_TIMEOUT=300)(ADDRESS=...)(CONNECT_DATA=...))`

With these timeouts set, a dropped connection surfaces an error instead of hanging, and
the connector reconnects automatically. The error depends on which connection times out:
`ORA-12609: TNS: Receive timeout occurred` for the `XStream Out Server URL` (OCI driver),
or `ORA-18730: Socket read timed out` for the `Oracle Connection URL` (thin driver).

## Capture Status not ENABLED

The capture process status is `DISABLED` or `ABORTED`. A `DISABLED` status means the
capture process was stopped manually (with `DBMS_XSTREAM_ADM.STOP_OUTBOUND`) or the
database was restarted. An `ABORTED` status means the capture encountered an error,
usually because redo logs needed for the capture process have been deleted.
You can confirm this by checking the System Change Number (SCN) position or querying
the capture status.

**Solution**

Start the outbound server:

Copy code

```
BEGIN
   DBMS_XSTREAM_ADM.START_OUTBOUND('XOUT1');
END;
/
```

## UNKNOWN status of LogMiner session

The LogMiner status is `UNKNOWN`, which means that archived logs that LogMiner depended
on were deleted. You can confirm this by querying `V$ARCHIVED_LOG` and checking for rows
where the DELETED column has the value `YES`.

**Solution**

Recreate the XStream outbound server. For more information, see [Problems occur with the XStream outbound server](#label-recreate-xstream-outbound-server).

## WAITING FOR REDO status of XStream capture

The XStream capture status shows
`WAITING FOR REDO: FILE NA, THREAD 1, SEQUENCE 47, SCN 0x0000000000190ac4`.
This means LogMiner is waiting for an archived log file that isn’t available because it
was deleted. You can confirm this by querying `V$ARCHIVED_LOG` and checking for rows
where the DELETED column has the value `YES`.

**Solution**

Recreate the XStream outbound server. For more information, see [Problems occur with the XStream outbound server](#label-recreate-xstream-outbound-server).

## XStream capture rules are incorrect

XStream isn’t configured to capture changes from the expected schemas or tables.

**Solution**

Verify the capture rules by running the following query:

Copy code

```
SELECT STREAMS_NAME, SCHEMA_NAME, OBJECT_NAME, RULE_TYPE
FROM DBA_XSTREAM_RULES
WHERE STREAMS_NAME = 'XOUT1';
```

You can also query the capture status and error message directly:

Copy code

```
SELECT CLIENT_NAME, STATUS, ERROR_MESSAGE FROM ALL_CAPTURE;
```

This query returns:

- `CLIENT_NAME`: The name of the XStream client (outbound server).
- `STATUS`: The current status of the capture process (for example, `ENABLED`,
  `DISABLED`, `ABORTED`).
- `ERROR_MESSAGE`: Any error message associated with the capture process.

## Error ORA-21560: argument last\_position is null, invalid, or out of range

The connector attempted to connect to an SCN position for which redo logs are no longer
available.

**Solution**

Confirm the issue by running the following query. The SCN for
`Last SCN processed by XStream` must be higher than the lowest SCN for which redo logs
exist.

Copy code

```
SELECT min(FIRST_CHANGE#) as SCN,
       'Lowest SCN for which redo logs still exist' AS DESCRIPTION
FROM V$ARCHIVED_LOG
WHERE DELETED = 'NO'
UNION ALL
SELECT PROCESSED_LOW_SCN,
       'Last SCN processed by XStream'
FROM DBA_XSTREAM_OUTBOUND_PROGRESS
WHERE SERVER_NAME = 'XOUT1'
ORDER BY SCN;
```

To recover from this error, recreate the XStream outbound server. For more information,
see [Problems occur with the XStream outbound server](#label-recreate-xstream-outbound-server).

## Error ORA-26701: Streams process XOUT1 does not exist

The XStream outbound server can’t be found on the database instance.

**Solution**

Verify the following:

- The database name in `Oracle Source Parameters` » `XStream Out Server URL` points
  to the database instance with the XStream outbound server, not a different PDB.
- XStream has been created on this instance and has the same name.

## Insufficient privileges error in an Oracle RAC environment

The connector reports an insufficient privileges error even though the Oracle user has the required permissions. In an Oracle RAC environment, this can happen when the connection is routed to a node that doesn’t host the XStream outbound server.

To confirm, first check which RAC instance the connector is connected to. You can run this query directly from the Openflow UI by adding a temporary **ExecuteSQL** processor that uses the same JDBC connection as the connector, then comparing the result with the same query run on the Oracle server. This `SYS_CONTEXT` check only tells you which node the connector landed on; the `V$` vs `GV$` check further down confirms which node XStream actually runs on:

Copy code

```
SELECT SYS_CONTEXT('USERENV', 'INSTANCE_NAME') AS instance_name,
       SYS_CONTEXT('USERENV', 'INSTANCE')      AS instance_number,
       SYS_CONTEXT('USERENV', 'SERVER_HOST')   AS host_name,
       SYS_CONTEXT('USERENV', 'SERVICE_NAME')  AS service_name
FROM DUAL;
```

If the values differ between the two, the connector is connecting to a different node than expected.

Alternatively, run the following queries directly on the Oracle node that the runtime is connected to. Query the local view, which returns a row only on the node hosting the XStream capture process:

Copy code

```
SELECT STATE FROM V$XSTREAM_CAPTURE
WHERE CAPTURE_NAME = (SELECT CAPTURE_NAME FROM DBA_CAPTURE WHERE CLIENT_NAME = 'XOUT1');
```

Query the global view, which spans all RAC nodes:

Copy code

```
SELECT STATE, INST_ID FROM GV$XSTREAM_CAPTURE
WHERE CAPTURE_NAME = (SELECT CAPTURE_NAME FROM DBA_CAPTURE WHERE CLIENT_NAME = 'XOUT1');
```

If `GV$XSTREAM_CAPTURE` returns a row but `V$XSTREAM_CAPTURE` returns nothing, the XStream outbound server is running on a different RAC node than the one the connector is connected to.

Note

Querying `GV$` views requires `SELECT ANY DICTIONARY` or an explicit grant on the view. If the query returns a privileges error, ask your DBA to grant the privilege or run the query as a DBA.

**Solution**

Use Oracle Connection Manager (CMAN) as a proxy between the connector and the Oracle RAC cluster. CMAN routes connections to the correct RAC node transparently and supports failover. Update both `Oracle Connection URL` and `XStream Out Server URL` in `Oracle Source Parameters` to point to your CMAN host and port.

## Error ORA-16224: Database Guard is enabled

Connecting to or reading from the XStream outbound server fails with:

Copy code

```
oracle.streams.StreamsException: ORA-16224: Database Guard is enabled
```

This error occurs on a logical standby when Database Guard is set to `ALL`
(the default). With that setting, the XStream client can’t read the outbound
server.

**Solution**

On the logical standby, set Database Guard to `STANDBY`:

Copy code

```
ALTER DATABASE GUARD STANDBY;
```

For more information, see
[Logical standby requirements](/user-guide/data-integration/openflow/connectors/oracle/setup-oracledb#label-oracle-logical-standby-requirements).

## Error ORA-01722: invalid number when creating the outbound server

Executing `DBMS_XSTREAM_ADM.CREATE_OUTBOUND` fails with:

Copy code

```
ORA-01722: invalid number
ORA-06512: at "SYS.DBMS_LOGREP_UTIL", line 582
ORA-06512: at "SYS.DBMS_LOGREP_UTIL", line 636
ORA-06512: at "SYS.DBMS_XSTREAM_ADM_UTL", line 440
ORA-06512: at "SYS.DBMS_XSTREAM_UTL_IVK", line 2094
ORA-06512: at "SYS.DBMS_XSTREAM_UTL_IVK", line 2302
ORA-06512: at "SYS.DBMS_XSTREAM_ADM", line 44
ORA-06512: at line 8
```

This error is misleading. The outbound server already exists.

**Solution**

No action is needed. Use the existing outbound server.

## Problems occur with the XStream outbound server

Multiple issues, such as deleted redo logs or corrupted LogMiner state, can be resolved
by recreating the XStream outbound server.

**Solution**

1. Drop the existing outbound server:

   Copy code

   ```
   BEGIN
   DBMS_XSTREAM_ADM.DROP_OUTBOUND('XOUT1');
   END;
   /
   ```
2. Create the outbound server again. For more information, see
   [Create XStream Outbound Server](/user-guide/data-integration/openflow/connectors/oracle/setup-oracledb#label-create-xstream-outbound-server).
