# Application roles in the Snowflake Connector for PostgreSQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

The following sections describe application roles available in the connector application:

> - ADMIN
> - AGENT
> - VIEWER
> - DATA\_READER

All the application roles are automatically assigned to the account level role responsible for installing the application on the account.
They can be then reassigned for easier control over the connector application access.
For more information, see [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role).

# ADMIN application role

The `ADMIN` application role can be used to view connector configuration and state.
It also lets you execute procedures contained in the application.

## AGENT application role

The `AGENT` application role is used by the agent in order to be able to perform replication process. Should not be used manually.

## VIEWER application role

The `VIEWER` application role provides access to view basic configuration of the connector.

## DATA\_READER application role

The `DATA_READER` application role can be used to give read privileges on replicated data without access to the connector application itself.

In order to view replicated data, a user needs to have following privileges:

> - `USAGE` grant on destination database
> - `USAGE` grant on destination schema
> - `SELECT` grant on destination table

The connector grants `USAGE` / `SELECT` privileges to this role on all destination databases, schemas and tables created by the application.

Attention

Be aware, that the `DATA_READER` application role is provided with privileges only on objects created by the application.
If the destination database or destination schema already exists and is not owned by the connector application,
the connector won’t be able to grant proper privileges to the `DATA_READER` role on these objects.
In such case, account level roles with the `DATA_READER` application role need to be manually supplemented with the `USAGE` grant on these objects.
