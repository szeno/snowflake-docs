# Snowflake Connector for PostgreSQL installation and configuration tasks

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

Working with the Snowflake Connector for PostgreSQL includes the following common task areas:

- [Installing and configuring the connector](#installing-and-configuring-the-connector)
- [Reviewing data](#reviewing-data)

It’s important to carefully review each of the installation and configuration steps,
before enabling data replication.

## Installing and configuring the connector

Perform the following tasks to install and configure the Snowflake Connector for PostgreSQL.

After all prerequisites are satisfied you can install and configure your Snowflake Connector for PostgreSQL using either SQL or Snowsight.

| Task | Description | Area Involved |
| --- | --- | --- |
| [Prerequisites for Snowflake Connector for PostgreSQL datasources](/connectors/postgres6/prereqs-datasource) | The configuration of the source database instance to enable data replication. | Source Database Administrator |
| [Setting up the Snowflake Connector for PostgreSQL using Snowsight](/connectors/postgres6/install-snowsight) | Installation of the Connector using Snowsight. | Snowflake Administrator |
| [Set up connectivity](/connectors/postgres6/install-agent#label-setup-connectivity-postgres6) | The configuration of the network access to Snowflake. A sub-task of [Setting up the Snowflake Connector for PostgreSQL Agent container](/connectors/postgres6/install-agent). | Network Administrator |
| [Setting up the Snowflake Connector for PostgreSQL Agent container](/connectors/postgres6/install-agent) | Installation and configuring the Snowflake Connector for PostgreSQL agent. | Developer and Operations |
| [Setting up Email Notifications for the PostgreSQL connector](/connectors/postgres6/email-notifications) | The configuration of email notifications for the connector. | Snowflake Administrator |
| [Configuring replication for the Snowflake Connector for PostgreSQL](/connectors/postgres6/configure-replication) | Configure connector replication | Developer and Operations |

Expand

Show lessSee more

## Reviewing data

Review the following to examine Snowflake Connector for PostgreSQL data

| Task | Description |
| --- | --- |
| [Viewing PostgreSQL data in Snowflake](/connectors/postgres6/view-data) | Viewing data ingested using the connector. |

Expand

Show lessSee more
