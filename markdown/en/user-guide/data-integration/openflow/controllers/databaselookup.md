# DatabaseLookup

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A Lookup Service that allows for enrichment with a database using a user-specified SQL statement. The SQL statement may reference any value from the FlowFile’s Record that is provided by the calling Processor.

## Tags

database, enrich, join, lookup, openflow, rdbms, record, sql

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Connection Pooling Service \* | Connection Pooling Service |  |  | The Connection Pooling Service that is used to obtain a connection to the database |
| Max Array Size \* | Max Array Size | 1000 |  | The maximum number of records to include in the array. This is a mechanism to ensure that the returned results due not cause memory issues. If the result set contains more records than this value, the lookup will fail. If the desire is instead to limit the number of rows returned, a LIMIT clause should be added to the SQL. |
| Multiple Result Field Name \* | Multiple Result Field Name | results |  | If multiple results are returned, they will be combined into an array. This property dictates the name of the field in the returned record. |
| Multiple Result Strategy \* | Multiple Result Strategy | Fail | - Use Array - Use First Only - Fail | Specifies how to handle the situation where the lookup results in multiple records. |
| SQL \* | SQL |  |  | The SQL statement to execute against the database in order to lookup the value. The statement may reference any attributes or values from the incoming Record that are provided by the calling Processor via Expression Language. The processor is will extract any Expression Language expressions and replace them with parameterized values so that the SQL can be safely executed, avoiding SQL Injection attacks. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
