# About Workday Data Cloud and Snowflake

Feature — Generally Available

This integration is generally available to accounts in all AWS, Azure, and GCP commercial regions. It is not available in VPS deployments, government regions, or the People’s Republic of China.

For details, see [Supported regions](#supported-regions).

Snowflake and Workday have partnered to offer a zero-copy integration between Workday Data Cloud and Snowflake. The integration lets you query Workday Data Cloud tables directly from your existing Snowflake account, without ETL pipelines, data replication, or moving data out of Workday.

## How it works

You create a Zerocopy Connector that authenticates to your Workday tenant using an API client that your Workday administrator registers for integrations. When the connector reaches `CONNECTED` state, you mount the Workday Data Cloud catalog as a catalog-linked database, which is a native Snowflake database object that exposes the Workday tables for querying without copying them.

Each Workday namespace becomes a schema in the catalog-linked database, and each Workday table becomes a table.

Data stays in Workday and Snowflake reads it in place, so there is no ETL and no duplication. Snowflake contacts Workday each time you run a `SELECT` against a mounted table, so every query returns fresh data rather than a cached copy. For the connector’s metadata refresh and catalog discovery intervals, see [Refresh intervals](/user-guide/data-integration/zero-copy/workday-data-cloud/setup#label-workday-refresh-intervals).

Catalog-linked databases are read-only, and Workday remains the system of record.

## Integration for existing Snowflake customers

The Workday Data Cloud zero-copy integration is designed for existing Snowflake customers who want to bring Workday data into their Snowflake account. You use your existing Snowflake account to set up the integration.

As a Snowflake account administrator, you create a Zerocopy Connector in your account and connect it with the credentials that your Workday administrator supplies. The connector authenticates outbound to your Workday tenant. After the connector is connected, you can mount the catalog and immediately query Workday tables in Snowflake.

## Supported regions

On the Snowflake side, the integration is available to accounts in all AWS, Azure, and GCP commercial regions. For the full list, see [Supported cloud regions](/user-guide/intro-regions).

The integration is not available in the following Snowflake deployments:

- [Virtual Private Snowflake (VPS)](/user-guide/intro-editions)
- [Government regions](/user-guide/intro-regions#label-us-gov-regions)
- The People’s Republic of China

On the Workday side, Snowflake supports Workday Data Cloud on AWS only. Your Snowflake account doesn’t have to be on AWS or in the same region. The integration supports cross-cloud and cross-region connections.

## Prerequisites

Before starting, ensure:

- You have an existing Snowflake account, and the account is enabled for the Workday connector. If the `CREATE ZEROCOPY CONNECTOR` command isn’t recognized, contact your Snowflake account team.
- Your Snowflake account is in a supported region and deployment. For details, see [Supported regions](#label-workday-supported-regions).
- Your Workday administrator has access to Workday Data Cloud and can register an API client for integrations. The API client supplies the tenant, host, and credential values that the connector needs. For the full list, see [Set up the Workday Data Cloud Zerocopy Connector](/user-guide/data-integration/zero-copy/workday-data-cloud/setup).

## Set up the integration

Perform the following tasks in order to set up, configure, and run the Workday Data Cloud zero-copy integration.

| Order | Task | Description | Persona |
| --- | --- | --- | --- |
| 1 | [Set up the Workday Data Cloud Zerocopy Connector](/user-guide/data-integration/zero-copy/workday-data-cloud/setup) | Create the Zerocopy Connector in Snowflake and connect it to your Workday tenant using the values supplied by your Workday administrator. | Snowflake account administrator |
| 2 | [Security and privileges](/user-guide/data-integration/zero-copy/workday-data-cloud/security) | Review the privileges required to create and manage the Zerocopy Connector, how Snowflake protects the Workday credentials, and the connector states. | Snowflake account administrator |
| 3 | [Explore and query Workday Data Cloud data](/user-guide/data-integration/zero-copy/workday-data-cloud/explore-data) | Mount the Workday Data Cloud catalog as a catalog-linked database, then discover and query the Workday tables. | Snowflake account administrator and data engineer |

Expand

Show lessSee more

Note

Workday Data Cloud zero-copy is a different integration from Workday Live Data Query for Snowflake, which queries Workday from a Snowflake Notebook using a Python connector. For that integration, see [About Workday Live Data Query for Snowflake](/user-guide/data-integration/zero-copy/about-workday-ldq).
