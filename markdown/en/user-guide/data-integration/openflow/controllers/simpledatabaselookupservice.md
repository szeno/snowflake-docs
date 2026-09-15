# SimpleDatabaseLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A relational-database-based lookup service. When the lookup key is found in the database, the specified lookup value column is returned. Only one value will be returned for each lookup, duplicate database entries are ignored.

## Tags

cache, database, enrich, join, key, lookup, rdbms, reloadable, value

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Cache Expiration | Cache Expiration |  |  | Time interval to clear all cache entries. If the Cache Size is zero then this property is ignored. |
| Cache Size \* | dbrecord-lookup-cache-size | 0 |  | Specifies how many lookup values/records should be cached. The cache is shared for all tables and keeps a map of lookup values to records. Setting this property to zero means no caching will be done and the table will be queried for each lookup value in each record. If the lookup table changes often or the most recent data must be retrieved, do not use the cache. |
| Clear Cache on Enabled \* | dbrecord-lookup-clear-cache-on-enabled | true | - true - false | Whether to clear the cache when this service is enabled. If the Cache Size is zero then this property is ignored. Clearing the cache when the service is enabled ensures that the service will first go to the database to get the most recent data. |
| Database Connection Pooling Service \* | dbrecord-lookup-dbcp-service |  |  | The Controller Service that is used to obtain connection to database |
| Lookup Key Column \* | dbrecord-lookup-key-column |  |  | The column in the table that will serve as the lookup key. This is the column that will be matched against the property specified in the lookup processor. Note that this may be case-sensitive depending on the database. |
| Table Name \* | dbrecord-lookup-table-name |  |  | The name of the database table to be queried. Note that this may be case-sensitive depending on the database. |
| Lookup Value Column \* | lookup-value-column |  |  | The column whose value will be returned when the Lookup value is matched |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
