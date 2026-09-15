# ListDatabaseTables 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Generates a set of flow files, each containing attributes corresponding to metadata about a table from a database connection. Once metadata about a table has been fetched, it will not be fetched again until the Refresh Interval (if set) has elapsed, or until state has been manually cleared.

## Tags

database, jdbc, list, sql, table

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| list-db-include-count | Whether to include the table’s row count as a flow file attribute. This affects performance as a database query will be generated for each table in the retrieved list. |
| list-db-refresh-interval | The amount of time to elapse before resetting the processor state, thereby causing all current tables to be listed. During this interval, the processor may continue to run, but tables that have already been listed will not be re-listed. However new/added tables will be listed as the processor runs. A value of zero means the state will never be automatically reset, the user must Clear State manually. |
| list-db-tables-catalog | The name of a catalog from which to list database tables. The name must match the catalog name as it is stored in the database. If the property is not set, the catalog name will not be used to narrow the search for tables. If the property is set to an empty string, tables without a catalog will be listed. |
| list-db-tables-db-connection | The Controller Service that is used to obtain connection to database |
| list-db-tables-name-pattern | A pattern for matching tables in the database. Within a pattern, “%” means match any substring of 0 or more characters, and “\_” means match any one character. The pattern must match the table name as it is stored in the database. If the property is not set, all tables will be retrieved. |
| list-db-tables-schema-pattern | A pattern for matching schemas in the database. Within a pattern, “%” means match any substring of 0 or more characters, and “\_” means match any one character. The pattern must match the schema name as it is stored in the database. If the property is not set, the schema name will not be used to narrow the search for tables. If the property is set to an empty string, tables without a schema will be listed. |
| list-db-tables-types | A comma-separated list of table types to include. For example, some databases support TABLE and VIEW types. If the property is not set, tables of all types will be returned. |
| record-writer | Specifies the Record Writer to use for creating the listing. If not specified, one FlowFile will be created for each entity that is listed. If the Record Writer is specified, all entities will be written to a single FlowFile instead of adding attributes to individual FlowFiles. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | After performing a listing of tables, the timestamp of the query is stored. This allows the Processor to not re-list tables the next time that the Processor is run. Specifying the refresh interval in the processor properties will indicate that when the processor detects the interval has elapsed, the state will be reset and tables will be re-listed as a result. This processor is meant to be run on the primary node only. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles that are received are routed to success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| db.table.name | Contains the name of a database table from the connection |
| db.table.catalog | Contains the name of the catalog to which the table belongs (may be null) |
| db.table.schema | Contains the name of the schema to which the table belongs (may be null) |
| db.table.fullname | Contains the fully-qualified table name (possibly including catalog, schema, etc.) |
| db.table.type | Contains the type of the database table from the connection. Typical types are “TABLE”, “VIEW”, “SYSTEM TABLE”, “GLOBAL TEMPORARY”, “LOCAL TEMPORARY”, “ALIAS”, “SYNONYM” |
| db.table.remarks | Contains the name of a database table from the connection |
| db.table.count | Contains the number of rows in the table |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Perform a full load of a database, retrieving all rows from all tables, or a specific set of tables. |
| --- |

Expand

Show lessSee more
