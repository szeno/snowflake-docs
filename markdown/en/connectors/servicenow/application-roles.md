# Role-based access control for connectors (ServiceNow)

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

The following sections describe application roles used in the connector application:

- ADMIN
- VIEWER
- DATA\_READER

These application roles are automatically assigned to the account level role responsible for installing the application on the account.
They can be reassigned to others to grant control and data access to connector data and to the connector itself.
See also [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role).

# ADMIN application role

You must use Snowflake Role ACCOUNTADMIN role paired with Application Role `ADMIN` to perform initial configuration of the connector, including the installation.

You can pair the `ADMIN` application role with any other Snowflake role after initial configuration to manage connector data synchronization.
The `ADMIN` application role grants access to all public views and procedures, which when paired with granted account level privileges can be used to:

- View Home Tab and ingestion statistics.
- View and manage data synchronization.
- View settings and connector configuration and manage alerts.

Attention

To manage connector alerts, grant either the ACCOUNTADMIN role or the CREATE INTEGRATION privilege to the role that the ADMIN application is assigned to.
To grant these rights, execute the following SQL code:
`GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE replace-with-your-role-name;`

## VIEWER application role

The `VIEWER` application role can be assigned to any role and is used to:

> - View the connector home tab and ingestion statistics.
> - View connector data synchronization.
> - View connector settings and configuration.

## DATA\_READER application role

Users who want to access the ingested data should use only the `DATA_READER` role.
The `DATA_READER` application role *must* be used to grant read privileges on replicated data.

This role is used to grant access to ingested data. To assign the `DATA_READER` role,
you can either use **Manage access** in Snowsight or execute the following SQL statement:

Copy code

```
GRANT APPLICATION ROLE DATA_READER to ROLE <replace-with-your-role-name>;
```

Do not attempt to access replicated data by changing ownership to the destination database;
instead grant the `DATA_READER` application role.

To view replicated data, a user must have the following privileges:

- `USAGE` on the destination database
- `USAGE` on the destination schema
- `SELECT` on the destination table

The connector grants `USAGE`/`SELECT` privileges to this role on all tables and views created by the application.

Attention

The `DATA_READER` application role is granted privileges only on objects created by the application.
If the destination database or destination schema already exists and is not owned by the connector application,
the connector won’t be able to grant proper privileges to the `DATA_READER` role on these objects.
In such situations, account level roles with the `DATA_READER` application role must be manually updated with a `USAGE` grant on these objects.
