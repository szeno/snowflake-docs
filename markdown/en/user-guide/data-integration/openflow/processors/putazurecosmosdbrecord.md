# PutAzureCosmosDBRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

This processor is a record-aware processor for inserting data into Cosmos DB with Core SQL API. It uses a configured record reader and schema to read an incoming record set from the body of a Flowfile and then inserts those records into a configured Cosmos DB Container.

## Tags

azure, cosmos, insert, put, record

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Cosmos DB Access Key | Cosmos DB Access Key from Azure Portal (Settings->Keys). Choose a read-write key to enable database or container creation at run time |
| Cosmos DB Conflict Handling Strategy | Choose whether to ignore or upsert when conflict error occurs during insertion |
| Cosmos DB Connection Service | If configured, the controller service used to obtain the connection string and access key |
| Cosmos DB Consistency Level | Choose from five consistency levels on the consistency spectrum. Refer to Cosmos DB documentation for their differences |
| Cosmos DB Container ID | The unique identifier for the container |
| Cosmos DB Name | The database name or id. This is used as the namespace for document collections or containers |
| Cosmos DB Partition Key | The partition key used to distribute data among servers |
| Cosmos DB URI | Cosmos DB URI, typically in the form of https://{databaseaccount}.documents.azure.com:443/ Note this host URL is for Cosmos DB with Core SQL API from Azure Portal (Overview->URI) |
| Insert Batch Size | The number of records to group together for one single insert operation against Cosmos DB |
| Record Reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | All FlowFiles that cannot be written to Cosmos DB are routed to this relationship |
| success | All FlowFiles that are written to Cosmos DB are routed to this relationship |

Expand

Show lessSee more
