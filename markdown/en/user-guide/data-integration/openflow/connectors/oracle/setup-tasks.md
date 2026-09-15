# Set up tasks for the Openflow Connector for Oracle

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Note

The Openflow Connector for Oracle is also subject to additional terms of service beyond the standard
connector terms of service. For more information, see the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

This topic describes the overall tasks required to set up, configure, and run the Openflow Connector for Oracle.

## Prerequisites

Before you set up the Openflow Connector for Oracle, verify that the following prerequisites are met:

1. Ensure that you have reviewed [About Openflow Connector for Oracle](/user-guide/data-integration/openflow/connectors/oracle/about).
2. Ensure that you have set up an Openflow deployment:
   - [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc)
   - [Set up Openflow - Snowflake Deployment](/user-guide/data-integration/openflow/setup-openflow-spcs)

## Tasks

Perform the following tasks to set up, configure, and run the Openflow Connector for Oracle.

| Order | Task | Description | Persona |
| --- | --- | --- | --- |
| 1 | Review [Prerequisites](#label-oracle-of-connector-prerequisites) | Review and confirm all required prerequisites. | **Snowflake account administrator** |
| 2 | [Enable the connector](/user-guide/data-integration/openflow/connectors/oracle/manage-commercial-terms#label-oracle-enable-service) | Accept the Oracle XStream terms to make the connector visible in the list of available connectors. | **Organization administrator (ORGADMIN)** |
| 3 | [Configure the Oracle database](/user-guide/data-integration/openflow/connectors/oracle/setup-oracledb) | Configure the Oracle database for Openflow Connector for Oracle including replication settings and credentials. | **Oracle database administrator** |
| 4 | [Set up Snowflake](/user-guide/data-integration/openflow/connectors/oracle/setup-snowflake) | Grant the execute-as role access to a destination database and warehouse for the Openflow Connector for Oracle. BYOC deployments using key-pair authentication also need a service user. | **Snowflake account administrator** |
| 5 | [Configure the connector](/user-guide/data-integration/openflow/connectors/oracle/setup-connector) | Install, configure, and run the Openflow Connector for Oracle connector. | **Snowflake account administrator** |
| 6 | [Set up licensing](/user-guide/data-integration/openflow/connectors/oracle/manage-commercial-terms#label-oracle-license-setup) | Configure your licensing model after the connector detects your source database inventory. | **Organization administrator (ORGADMIN)** |

Expand

Show lessSee more

## Next steps

- [Monitor the flow](/user-guide/data-integration/openflow/monitor).
- [Maintenance](/user-guide/data-integration/openflow/connectors/oracle/maintenance) for reinstalling the connector or changing the XStream position.
