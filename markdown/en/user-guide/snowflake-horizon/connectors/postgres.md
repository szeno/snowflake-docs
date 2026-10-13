# PostgreSQL

## Supported deployments

- [AWS RDS PostgreSQL](/user-guide/snowflake-horizon/connectors/postgres/aws-rds)
- [AWS Aurora PostgreSQL](/user-guide/snowflake-horizon/connectors/postgres/aws-aurora)
- [Snowflake Postgres and self-hosted PostgreSQL](/user-guide/snowflake-horizon/connectors/postgres/on-prem)

## Additional information

### Sync new data assets

After first connection, if you create a new PostgreSQL schema in your database, you need to re-grant permissions.

To sync your new assets into Horizon Catalog, follow these steps:

1. GRANT access to the new Schema:

   Copy code

   ```
   GRANT USAGE ON SCHEMA <schema_name> TO snowflake_horizon;
   ALTER DEFAULT PRIVILEGES GRANT USAGE ON SCHEMAS TO snowflake_horizon;
   ```
2. In Snowflake, open **Catalog > Connections**, find your data source, and click **Configure**.
3. Click **Refresh**.
4. Click Next, and make sure your new Schema is selected.
   [![Schema selection in data source configuration](/static/images/user-guide/snowflake-horizon/connectors/postgres-schema-selection.png)](/static/images/user-guide/snowflake-horizon/connectors/postgres-schema-selection.png)

   [![Confirm schema selection](/static/images/user-guide/snowflake-horizon/connectors/postgres-schema-confirm.png)](/static/images/user-guide/snowflake-horizon/connectors/postgres-schema-confirm.png)
