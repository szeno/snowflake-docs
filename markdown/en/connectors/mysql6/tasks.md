# Snowflake Connector for MySQL installation and configuration tasks

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for MySQL.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/about) and
includes better performance, customizability, and enhanced deployment options.

Working with the Snowflake Connector for MySQL involves several key tasks:

- [Installation and configuration of the connector](#installation-and-configuration-of-the-connector)
- [Configuring data replication and examining the ingested data](#configuring-data-replication-and-examining-the-ingested-data)

It’s important to carefully review each of the installation and configuration steps, before enabling data replication.

## Installation and configuration of the connector

These steps are designed to guide you through the initial setup of the Connector. The installation process involves various stages and contributions from different departments.

| Task | Description | Area Involved |
| --- | --- | --- |
| [Prerequisites for Snowflake Connector for MySQL datasources](/connectors/mysql6/prereqs-datasource) | The configuration of the source database instance to enable data replication. | Source Database Administrator |
| [Setting up the Snowflake Connector for MySQL using Snowsight](/connectors/mysql6/install-snowsight) | Installation of the Connector using Snowsight. | Snowflake Administrator |
| [Set up connectivity](/connectors/mysql6/install-agent#label-setup-connectivity-mysql6) | The configuration of the network access to Snowflake. A sub-task of [Setting up the Snowflake Connector for MySQL Agent container](/connectors/mysql6/install-agent). | Network Administrator |
| [Setting up the Snowflake Connector for MySQL Agent container](/connectors/mysql6/install-agent) | Installation and configuring the Snowflake Connector for MySQL agent. | Developer and Operations |
| [Setting up Email Notifications for the MySQL connector](/connectors/mysql6/email-notifications) | The configuration of email notifications for the connector. | Snowflake Administrator |
| [Configuring replication for the Snowflake Connector for MySQL](/connectors/mysql6/configure-replication) | Configure connector replication | Developer and Operations |

Expand

Show lessSee more

## Configuring data replication and examining the ingested data

This installation step enables you to configure the data source and activate table replication.

| Task | Description |
| --- | --- |
| [Configuring replication for the Snowflake Connector for MySQL](/connectors/mysql6/configure-replication) | Configure connector replication |
| [Viewing MySQL data in Snowflake](/connectors/mysql6/view-data) | Viewing data ingested using the connector. |

Expand

Show lessSee more
