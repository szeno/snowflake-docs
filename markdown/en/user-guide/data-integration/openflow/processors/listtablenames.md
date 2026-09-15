# ListTableNames 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-database-cdc-processors-nar

## Description

Fetches all source table names and matches them with one of the possible configurations: - regexp expression e.g. “(?i)customer.(orders|payments)” - it matches names in case insensitive way. It would match both “CUSTOMER.ORDERS” and “customer.orders” source table names. - comma separated list of source table names. e.g. “customer.orders, customer.payments”. It matches source table names in case sensitive way i.e. “customer.orders” source table will be forwarded to MATCH relationship but “customer. ORDERS” won ‘t match. Matched source tables that cannot be replicated will be routed to FAILURE relationship, each table in a separate FlowFile, with a reason in attributes. Configuration is passed as a FlowFile attribute. Source table name is represented as <schema\_name>.<table\_name> so both inputs should take that into consideration. Matched source table names are forwarded to MATCHED relationship. Processor generates a single FlowFile with matching tables. Disclaimers - Postgresql lets you define database object names in case sensitive or case insensitive way. When user creates a table using following query’CREATE TABLE ORDERS(id int not null) ‘then internally Postgresql stores it using lower case letters i.e. orders. To enforce case sensitivity user has to wrap the table name with double quotes i.e.’CREATE TABLE “ORDERS”(id int not null)’. This is important aspect when configuring table that we would like to replicate.

## Tags

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Pool | The Controller Service that is used to obtain a connection to the database. |
| Included Comma Separated Source Table Names | The list of comma separated list of tables to replicate. A single table should be formatted as <schema\_name>.<table\_name> e.g. customer.orders, customer.payments. This is combined with the regular expression to include any matching table. |
| Included Source Table Pattern | Regular Expression for specifying table names to replicate e.g. customer.(orders|payments). This is combined with the comma-separated list to include any matching table. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile attribute cannot be read or is incorrect, it will be routed to this Relationship. |
| matched | Successfully created FlowFile, with a list of matching tables found in the source database. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| source.schema.name | Name of the schema of the table from which an event originated |
| source.table.name | Name of the table from which an event originated |
| source.entry | The original entry that was attempted to parse when processing table names |
| reason | Reason why table cannot be replicated |
| source.database.version.major | The major version of the source database. |
| mime.type | The MIME type of the FlowFile content. |

Expand

Show lessSee more
