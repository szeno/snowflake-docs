# SnowflakeConnectionService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides pooled database connections to Snowflake services

## Tags

connection, database, jdbc, openflow, snowflake

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Account \* | Account |  |  | Snowflake Account Identifier with Organization Name and Account Name formatted as [organization-name]-[account-name] |
| Authentication Strategy \* | Authentication Strategy | PASSWORD | - Password - Key Pair - Snowflake Session Token | Strategy for authenticating Snowflake connections |
| Connection Strategy \* | Connection Strategy | STANDARD | - Standard - Private Connectivity | Strategy for connecting to Snowflake services |
| Connection Timeout \* | Connection Timeout | 30 seconds |  | Maximum amount of time to wait for a connection from a reusable pool |
| Database Name | Database Name |  |  | Default Snowflake Database for connections |
| Idle Timeout \* | Idle Timeout | 10 minutes |  | Maximum amount of time for a connection to remain idle in a reusable pool |
| Maximum Connections \* | Maximum Connections | 10 |  | Maximum number of connections created and managed in a reusable pool |
| Maximum Lifetime \* | Maximum Lifetime | 30 minutes |  | Maximum lifetime for each connection in a reusable pool |
| Password \* | Password |  |  | Snowflake Password for authenticating connections |
| Private Key Service \* | Private Key Service |  |  | RSA Private Key Service for authenticating connections |
| Role | Role |  |  | Default Snowflake Role for connections |
| Schema | Schema |  |  | Default Snowflake Schema for connections |
| User \* | User |  |  | Snowflake User for authenticating connections |
| Warehouse | Warehouse |  |  | Default Snowflake Warehouse for connections |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
