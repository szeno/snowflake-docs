# About Salesforce Data Cloud and Snowflake

Snowflake and Salesforce have partnered to offer customers a seamless zero-copy integration between Salesforce Data Cloud and Snowflake. The integration enables customers to access semantically rich Salesforce data products directly from their existing Snowflake accounts, without ETL pipelines, data replication, or moving data out of Salesforce.

Leveraging zero-copy data access, data and AI teams can work with real-time Salesforce customer, engagement, and business data in Snowflake, building analytics, machine learning models, and AI applications grounded in the full context of their mission-critical Salesforce data.

## How it works

Salesforce Data Cloud shares data products with your Snowflake account through a Zerocopy Connector. The connector establishes a secure, authenticated channel between Salesforce Data Cloud and your Snowflake account. Once connected, Salesforce data products appear in Snowflake as catalog-linked databases, which are native Snowflake database objects that expose the shared data for querying without copying it.

Data stays in Salesforce. Snowflake queries it on demand. There is no ETL and no duplication.

## Integration for existing Snowflake customers

The Salesforce Data Cloud Zero-Copy integration is designed for existing Snowflake customers who want to bring Salesforce data products into their Snowflake account. You use your existing Snowflake account to set up the integration.

As a Snowflake account administrator, you create a Zerocopy Connector in your account and retrieve an Enrollment ID. You then provide that Enrollment ID to your Salesforce administrator, who creates a Data Share Target in Salesforce Data Cloud to authorize the connection. Once connected, Salesforce administrators can share data products from the Salesforce Data Cloud catalog with your connector, and you can immediately query them in Snowflake.

## Prerequisites

Before starting, ensure:

- You have an existing Snowflake account (Standard, Enterprise, or Business Critical edition).
- Your Snowflake account is in a supported region. For details, see [Supported Cloud Regions](/user-guide/intro-regions).
- Your Salesforce administrator has access to Salesforce Data Cloud and can provision a connector and share data products.

## Set up the integration

Perform the following tasks in order to set up, configure, and run the Salesforce Data Cloud Zero-Copy integration.

| Order | Task | Description | Persona |
| --- | --- | --- | --- |
| 1 | [Set up the Salesforce Data Cloud Zerocopy Connector](/user-guide/data-integration/zero-copy/salesforce/setup) | Create the Zerocopy Connector in Snowflake and retrieve the Enrollment ID to provide to your Salesforce administrator. | Snowflake account administrator |
| 2 | [Set up Salesforce Data Cloud for Zero-Copy](/user-guide/data-integration/zero-copy/salesforce/setup-salesforce) | Create a Data Share Target in Salesforce Data Cloud using the Enrollment ID to authorize the connection, then link existing or new Data Shares to the Data Share Target. | Salesforce administrator |
| 3 | [Salesforce Data Cloud Zerocopy Connector: Security and privileges](/user-guide/data-integration/zero-copy/salesforce/security) | Review security requirements and privileges required for Snowflake management of the Zerocopy Connector. | Snowflake account administrator |
| 4 | [Explore data products from Salesforce Data Cloud](/user-guide/data-integration/zero-copy/salesforce/explore-data-products) | Explore data products shared from Salesforce Data Cloud to Snowflake, create catalog-linked databases, and query the data. | Snowflake account administrator and data engineer |

Expand

Show lessSee more
