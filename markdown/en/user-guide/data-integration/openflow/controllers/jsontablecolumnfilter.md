# JsonTableColumnFilter

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a table column filter based on a JSON configuration. The JSON configuration should be an array of objects, where each object represents a table and its column filter. The object should have the following properties: - schema: the schema name of the table - table: the table name - included: an array of column names to include - excluded: an array of column names to exclude - includedPattern: a regular expression pattern to include columns - excludedPattern: a regular expression pattern to exclude columns The schema and table must be provided for each object, and one or more of the *included*, *excluded*, *includedPattern*, or *excludedPattern* properties must be provided. If any column is included as both included and excluded, the column will be excluded. If only a single filter is provided, the JSON configuration may be a single JSON object, rather than an array.

## Tags

column, database, filter, snowflake, table

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Filter JSON | Filter JSON |  |  | JSON representation of the column filter |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
