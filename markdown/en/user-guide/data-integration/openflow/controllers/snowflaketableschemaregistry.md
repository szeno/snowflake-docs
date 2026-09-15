# SnowflakeTableSchemaRegistry

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Uses Snowflake tables as the source of schema — utilises Snowpipe Streaming REST API. Requires a fully qualified table name as the schema name.

## Tags

openflow, registry, schema, snowflake

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Account \* | Account |  |  | Snowflake Account Identifier with Organization Name and Account Name formatted as [organization-name]-[account-name] |
| Private Key Service \* | Private Key Service |  |  | RSA Private Key Service for authenticating connections |
| User \* | User |  |  | Snowflake User for authenticating connections |
| Web Client Service Provider \* | Web Client Service Provider |  |  | Web Client Service Provider to make connections |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
