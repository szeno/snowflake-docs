# DBCPConnectionPoolLookup

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a DBCPService that can be used to dynamically select another DBCPService. This service requires an attribute named ‘database.name’ to be passed in when asking for a connection, and will throw an exception if the attribute is missing. The value of ‘database.name’ will be used to select the DBCPService that has been registered with that name. This will allow multiple DBCPServices to be defined and registered, and then selected dynamically at runtime by tagging flow files with the appropriate ‘database.name’ attribute.

## Tags

connection, database, dbcp, jdbc, pooling, store

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
