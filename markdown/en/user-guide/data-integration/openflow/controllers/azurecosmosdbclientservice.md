# AzureCosmosDBClientService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a controller service that configures a connection to Cosmos DB (Core SQL API) and provides access to that connection to other Cosmos DB-related components.

## Tags

azure, cosmos, document, service

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Cosmos DB Access Key | Cosmos DB Access Key |  |  | Cosmos DB Access Key from Azure Portal (Settings->Keys). Choose a read-write key to enable database or container creation at run time |
| Cosmos DB Consistency Level | Cosmos DB Consistency Level | SESSION | - STRONG - BOUNDED\_STALENESS - SESSION - CONSISTENT\_PREFIX - EVENTUAL | Choose from five consistency levels on the consistency spectrum. Refer to Cosmos DB documentation for their differences |
| Cosmos DB URI | Cosmos DB URI |  |  | Cosmos DB URI, typically in the form of https://{databaseaccount}.documents.azure.com:443/ Note this host URL is for Cosmos DB with Core SQL API from Azure Portal (Overview->URI) |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
