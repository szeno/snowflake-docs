# SnowflakeSignJWTService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides OAuth2 access token using a JWT signed with a secret stored in Snowflake. The JWT is signed using the SYSTEM$SIGN\_JWT\_USING\_SECRET function, which requires a valid Snowflake connection.

## Tags

jwt, preview, snowflake

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Audience \* | Audience |  |  | The audience claim (aud) for the JWT. |
| Connection Pooling Service \* | Connection Pooling Service |  |  | The Connection Pooling Service that is used to obtain a connection to the database |
| JWT Expiration Time \* | JWT Expiration Time | 5 minutes |  | Expiration time used to set the corresponding claim of the JWT. |
| Snowflake Secret Name \* | Snowflake Secret Name |  |  | Name of the JWT Key Pair secret in Snowflake that will be used to sign the JWT. |
| Subject \* | Subject |  |  | The subject claim (sub) for the JWT. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
