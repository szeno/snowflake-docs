# Configuring replication for the Snowflake Connector for MySQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for MySQL.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/about) and
includes better performance, customizability, and enhanced deployment options.

The process of configuring replication for the Snowflake Connector for MySQL the following steps:

- [Adding a data source](#adding-a-data-source)

And optionally:

- [Add a source table for replication](#add-a-source-table-for-replication)
- [Remove a table from replication](#remove-a-table-from-replication)

## Adding a data source

A data source is a representation of a single MySQL server.
The Snowflake Connector for MySQL can replicate data from multiple data sources.
Before you start replication, you need to add at least one data source.

The Snowflake Connector for MySQL replicates data from each data source to a distinct destination
database in Snowflake. The same destination database cannot be used by multiple data sources.

To add a data source, run the following command:

> Copy code
>
> ```
> CALL PUBLIC.ADD_DATA_SOURCE('<data_source_name>', '<dest_db>');
> ```
>
> Where:
>
> > `data_source_name`
> > :   Specifies the unique name of the data source. The name should correspond to the name of a datasource defined in the agent configuration. Please ensure that the chosen name complies with the following requirements:
> >
> >     - The name contains only uppercase letters (A-Z), and decimal digits (0-9).
> >     - The name cannot be longer than 50 characters.
> >
> > `dest_db`
> > :   Specifies the name of the destination database in Snowflake. If the database does not exist, the procedure automatically creates it.
> >     Otherwise, the connector uses an existing database. In that case, you must grant privileges on the database to the connector before adding a data source.
>
> Note
>
> Once added, a data source cannot be renamed or dropped.

### (Optional) Granting privileges on the destination database

To use an existing database as a destination database, the Snowflake Connector for MySQL requires the [CREATE SCHEMA](/sql-reference/sql/create-schema) permission on that database. The connector is the owner of the schemas and tables containing ingested MySQL data.

To grant the [CREATE SCHEMA](/sql-reference/sql/create-schema) permission, run the following command:

> Copy code
>
> ```
> GRANT CREATE SCHEMA ON DATABASE <dest_db> TO APPLICATION <app_db_name>;
> ```
>
> Where:
>
> > `dest_db`
> > :   Specifies the name of the destination database for the data from a data source.
> >
> > `app_db_name`
> > :   Specifies the name of the connector database.

## Adding other data sources

You can add new data sources at any time. To add a new data source while the agent is already running, do the following:

1. [Add a data source](#label-mysql-connector-add-data-source).
2. Ensure the agent is stopped.
3. [Configure the agent connection to the new data source](/connectors/mysql6/install-agent#label-mysql-connector-prepare-agent-config-6).
4. [Run the Docker container of the agent](/connectors/mysql6/install-agent#label-mysql-connector-run-the-docker-container-6).

## Add a source table for replication

To add source tables for replication, run the following command:

> Copy code
>
> ```
> CALL PUBLIC.ADD_TABLES('<data_source_name>', '<schema_name>', <table_names_array>);
> ```
>
> Where:
>
> > `data_source_name`
> > :   Specifies the name of the data source that contains the source table.
> >
> > `schema_name`
> > :   Specifies the name of the schema of the source table.
> >
> > `table_names_array`
> > :   Specifies the array of table names:
> >
> >     `ARRAY_CONSTRUCT('table_name', 'other_table_name', ...)`

Adding a source table has the following effects:

- `schema_name` and `table_name` are used as the schema name and table name respectively for replicating source data from the source database.

Note

In one procedure call you can add many tables from the same datasource and schema.

Note

**Schema and table names must match**

You must use the exact table name and schema name, including case, as defined in the source database. The names you
provide are used verbatim to generate the SELECT query in the source database. MySQL server names can be
case-sensitive and using a different case could result in a “table does not exist” exception.

**Recently removed tables**

If tables were recently removed ([Remove a table from replication](#label-mysql-connector-remove-source-table)), it might not be possible to add them back at this point in configuration.
If an error with a message `Tables are not ready to be re-added` appears, wait several minutes before trying again.

## Add a source table with column filters

To add a source table with filtered columns, run the following command:

> Copy code
>
> ```
> CALL PUBLIC.ADD_TABLE_WITH_COLUMNS('<data_source_name>', '<schema_name>', '<table_name>', <included_columns_array>, <excluded_columns_array>);
> ```
>
> Where:
>
> > `data_source_name`
> > :   Specifies the name of the data source that contains the source table.
> >
> > `schema_name`
> > :   Specifies the name of the schema of the source table.
> >
> > `table_name`
> > :   Specifies the name of the source table.
> >
> > `included_columns`
> > :   Specifies the array of column names that should be replicated:
> >
> >     `ARRAY_CONSTRUCT('column_name', 'other_column_name', ...)`
> >
> > `excluded_columns`
> > :   Specifies the array of column names that should be ignored:
> >
> >     `ARRAY_CONSTRUCT('column_name', 'other_column_name', ...)`

Attention

Column names passed to the procedure must be case-sensitive, exactly as they are represented in source database.

Following rules apply to the above procedure:

- Filtering occurs before the data is ingested to Snowflake - only data from the chosen columns is streamed to Snowflake in both snapshot and incremental loads.
- `included_columns` and `excluded_columns` are just masks. This way the connector will not throw an error if specified column does not exist. Mask for the non-existent column will simply get ignored.
- You shouldn’t provide both `included_columns` and `excluded_columns`. If you want to list `included_columns`, you should leave the `excluded_columns` empty, and vice versa.
- If both arrays are not empty and there aren’t any conflicting columns, `included_columns` takes precedence over `excluded_columns`.
- If a column appears in both `included_columns` and `excluded_columns`, the procedure throws an error.
- If both `included_columns` and `excluded_columns` are empty arrays, all available columns will be ingested.
- Regardless of configuration, primary key columns always get replicated.

For example, let’s assume we have a source table with given columns: A, B, C, D, where A is a primary key column, then:

| Included columns | Excluded columns | Expected result |
| --- | --- | --- |
| [] | [] | [A, B, C, D] |
| [A, B] | [] | [A, B] |
| [B] | [] | [A, B] |
| [] | [C, D] | [A, B] |
| [] | [A, B] | [A, C, D] |
| [A, B, Z] | [] | [A, B] |
| [A] | [A] | Error |

Expand

Show lessSee more

## Remove a table from replication

To remove a **single source table** from replication, run the following command:

Copy code

```
CALL PUBLIC.REMOVE_TABLE('<data_source_name>', '<schema_name>', '<table_name>');
```

Where:

> `data_source_name`
> :   Specifies the name of the data source that contains the source table.
>
> `schema_name`
> :   Specifies the name of the schema of the source table.
>
> `table_name`
> :   Specifies the name of the source table.

To remove **multiple source tables** from the same data source and schema with one procedure call, run the following command:

Copy code

```
CALL PUBLIC.REMOVE_TABLES('<data_source_name>', '<schema_name>', '<table_names_array>');
```

Where:

> `data_source_name`
> :   Specifies the name of the data source that contains the source table.
>
> `schema_name`
> :   Specifies the name of the schema of the source table.
>
> `table_names_array`
> :   Specifies the array of table names:
>
>     `ARRAY_CONSTRUCT('table_name', 'other_table_name', ...)`

Note

The process of removing a table from replication takes a few minutes. Once complete, the table will disappear from the `PUBLIC.REPLICATION_STATE` view in the connector (see [Monitor](monitor)). Only then can it be enabled for replication again.

At this point the destination table is still **owned by the connector application**. If you wish to drop or otherwise modify the destination table, you need to first transfer its ownership to a role in your account. Execute the following query as `ACCOUNTADMIN`:

Copy code

```
GRANT OWNERSHIP ON TABLE <destination_database_name>.<schema_name>.<table_name>
  TO ROLE <role_name>
  REVOKE CURRENT GRANTS;
```

Note

If you’re removing a table from replication fix its `FAILED` state, you will also need to rename or drop the destination table manually before enabling its replication again.

## Configuring scheduled replication

The connector can replicate data in two modes: continuous or scheduled. The default is a continuous mode.

Continuous mode replicates data as fast as possible. It requires running an operational warehouse 24/7, which might generate unnecessary costs, even without an ongoing replication.

Scheduled mode replicates data according to a configured schedule. It aims to reduce replication costs when there is no need to replicate data continuously, or the data volume is small (causing the connector to be in idle state most of the time).

Scheduled mode introduces the concept of replication completion. The snapshot replication begins when the `SELECT columns FROM TABLE` query execution starts, and it ends when data gets replicated into the destination table.
The incremental replication begins from the previously stored change data capture (CDC) pointer, but it does not have an ending, as the data is ingested continuously.
Therefore, the connector replicates data from previously stored CDC pointer until the latest CDC pointer (determined at the start of the replication). This way, the connector provides the completion of replication in a scheduled mode.

Scheduled mode reduces replication costs by suspending the operational warehouse. The warehouse can be suspended if the replication of each source table is completed. The warehouse remains suspended until the next run of the replication, according to the schedule.

Note

Only one replication can run at a given time. If a replication is still running when the next scheduled run time occurs, then that scheduled time is skipped.

To enable scheduled mode, run the following command:

> Copy code
>
> ```
> CALL PUBLIC.ENABLE_SCHEDULED_REPLICATION('<data_source_name>', '<schedule>');
> ```
>
> Where:
>
> > `data_source_name`
> > :   Specifies the name of the data source.
> >
> > `schedule`
> > :   Specifies the schedule or frequency at which the connector runs the replication of the data source. The minimum allowed
> >     frequency is 15 minutes. For details on specifying the schedule or frequency, see
> >     [SCHEDULE parameter](/sql-reference/sql/create-task#label-create-task-schedule).

Schedule examples:

- `60 MINUTE`
  :   Schedules replication to every 60 minutes.
- `USING CRON 0 2 * * * UTC`
  :   Schedules replication to 2 a.m. UTC daily.

To disable scheduled mode, run the following command:

> Copy code
>
> ```
> CALL PUBLIC.DISABLE_SCHEDULED_REPLICATION('<data_source_name>');
> ```
>
> Where:
>
> > `data_source_name`
> > :   Specifies the name of the data source.

To check current schedule, see [Viewing data sources](/connectors/mysql6/monitor#label-mysql-connector-monitoring-data-sources-6).

Note

The operational warehouse handles replications from all data sources. The warehouse can only be suspended if the replication of each source table from every data source is completed. In other words, scheduled mode must be enabled for all data sources to ensure the auto-suspension works properly.

## Next steps

After completing these procedures, follow the steps in [Viewing MySQL data in Snowflake](/connectors/mysql6/view-data)
