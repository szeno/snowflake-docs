# Snowflake Postgres

## About Snowflake Postgres

Snowflake Postgres lets you create, manage, and use Postgres instances directly from Snowflake. Each instance runs a Postgres
database server on a dedicated virtual machine managed by Snowflake. You connect directly to your instances using any Postgres
client. Snowflake Postgres brings the reliable and trusted transactional database capabilities of Postgres to the Snowflake data
platform.

## About Postgres

PostgreSQL (also referred to as Postgres) is a mature, open-source relational database management system that has been actively
developed for more than 30 years. As a general-purpose transactional database, Postgres is designed for operational applications that
require highly-concurrent read/write operations, and low-latency data processing. Postgres offers a wide array of data types, including
JSONB, and sophisticated indexing capabilities. Postgres is increasingly becoming the database of choice for a wide range of use cases,
and is supported by an ecosystem of community-sponsored developer tools and extensions that offer enhanced capabilities. With
its proven reliability and performance, and active developer community, Postgres is a great addition to the Snowflake AI Data Cloud
platform that supports an expanded set of customer workloads.

## Architecture

Postgres is a mature, battle-tested database known for its reliability and performance, but it follows a more traditional architectural
model than the rest of the Snowflake platform. To bring Postgres into Snowflake, we designed an approach that preserves its operational
strengths while integrating it with Snowflake’s security, management, and connectivity capabilities.

Snowflake Postgres provisions a dedicated Postgres instance with attached disks to deliver best-in-class transactional performance. Each
Postgres instance runs in a fully isolated private network and supports private connectivity via firewall rules or Private Link. Snowflake
Postgres also offers built-in connection pooling via PgBouncer to support high-concurrency application workloads.

Snowflake Postgres is fully compatible with existing Postgres tooling and workloads, enabling you to lift-and-shift applications to
Snowflake with no code changes, and use everything that works with your Postgres instances today, including ORMs and all supported SQL
clients.

## Regional availability

Snowflake Postgres is available for the Amazon Web Services (AWS) and Microsoft Azure cloud service
providers (CSPs). Google Cloud Platform (GCP) isn’t currently supported.

Snowflake Postgres is available in the following [regions](/user-guide/intro-regions).

| Cloud region | Cloud region ID |
| --- | --- |
| **Amazon Web Services (AWS)** |  |
| US East (N. Virginia) | us-east-1 |
| US East (Ohio) | us-east-2 |
| US West (Oregon) | us-west-2 |
| Canada (Central) | ca-central-1 |
| South America (Sao Paulo) | sa-east-1 |
| EU (Ireland) | eu-west-1 |
| Europe (London) | eu-west-2 |
| EU (Paris) | eu-west-3 |
| EU (Frankfurt) | eu-central-1 |
| EU (Zurich) | eu-central-2 |
| EU (Stockholm) | eu-north-1 |
| Africa (Cape Town) | af-south-1 |
| Asia Pacific (Mumbai) | ap-south-1 |
| Asia Pacific (Singapore) | ap-southeast-1 |
| Asia Pacific (Jakarta) | ap-southeast-3 |
| Asia Pacific (Sydney) | ap-southeast-2 |
| Asia Pacific (Tokyo) | ap-northeast-1 |
| Asia Pacific (Seoul) | ap-northeast-2 |
| Asia Pacific (Osaka) | ap-northeast-3 |
| **Microsoft Azure** |  |
| East US 2 (Virginia) | eastus2 |
| Central US (Iowa) | centralus |
| South Central US (Texas) | southcentralus |
| West US 2 (Washington) | westus2 |
| Canada Central (Toronto) | canadacentral |
| North Europe (Ireland) | northeurope |
| UK South (London) | uksouth |
| West Europe (Netherlands) | westeurope |
| Switzerland North (Zurich) | switzerlandnorth |
| Sweden Central | swedencentral |
| Southeast Asia (Singapore) | southeastasia |
| Japan East (Tokyo) | japaneast |
| Australia East (Sydney) | australiaeast |
| Korea Central (Seoul) | koreacentral |
| Central India (Pune) | centralindia |
| UAE North (Dubai) | uaenorth |

Expand

Show lessSee more

## Postgres versions

Postgres major versions 16-18 are currently available. When you choose a major version for your new instance, Snowflake Postgres automatically uses the latest available minor version. The latest available minor versions for each major version are 16.13, 17.9,
and 18.3.

For details on upgrading the Postgres version of your existing Snowflake Postgres instances see [Snowflake Postgres version upgrades](/user-guide/snowflake-postgres/postgres-upgrades).

## When to use Postgres

Choose Postgres when you need a high-throughput, high-concurrency operational database, you have a use case that can benefit from
specific Postgres capabilities, or have an existing Postgres application.

## Customer Configurable Security Controls

Customers are responsible for managing the following controls to ensure a level of security appropriate to the particular content of their Postgres instances:

- Securing, keeping confidential, and rotating Postgres instance credentials, including passwords and connection strings.
- Maintaining appropriate password uniqueness, length, complexity, and expiration.
- Using [Snowflake Token Authentication for Snowflake Postgres](/user-guide/snowflake-postgres/postgres-token-auth) passwords for interactive user connections.
- Using restrictive [networking policies and rules](/user-guide/snowflake-postgres/postgres-network).
- Configuring [SSL certificate verification](/user-guide/snowflake-postgres/postgres-ssl-certs) for your client connections to Snowflake Postgres instances.
- Configuring user and role-based access controls, including scope and duration of user access.
