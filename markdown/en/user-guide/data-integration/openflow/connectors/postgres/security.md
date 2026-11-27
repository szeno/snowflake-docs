# Openflow Connector for PostgreSQL: Security

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

This page describes how to limit what the connector can read on the PostgreSQL server.

## Exclude columns from the PostgreSQL connector

To prevent column values from leaving the PostgreSQL server, use the configuration on this page. [Replicate a subset of columns in a table](/user-guide/data-integration/openflow/connectors/postgres/setup#label-postgres-connector-replication-subset-of-columns) filters columns after the connector has read the row.

Warning

PostgreSQL can’t stop this role from copying the data directory. Logical replication requires the `REPLICATION` attribute, and that attribute also allows a base backup. The connector opens a logical replication connection (`replication=database`). On that connection the server accepts a base-backup command and, with the default target, sends the files to the client. A `pg_hba.conf` entry that denies the `replication` pseudo-database doesn’t apply to this connection. No role attribute both allows logical replication and refuses a base backup.

A managed PostgreSQL service might refuse base backups on its own. Self-managed PostgreSQL doesn’t.

This role can copy the cluster. Sensitive values stay on the server only when they are absent from every database on that cluster, including existing WAL segments and backups. Dropping a column from a table that already contains the column leaves the values in existing files.

### Server version

Publication column lists require PostgreSQL 15 or later.

Restricting which output plugins a replication role can use requires PostgreSQL 15.19, 16.15, 17.11, or 18.6, or a newer minor release of that major version. You can apply that restriction only on a server where you can set `output_plugin_libraries`. Amazon RDS and Amazon Aurora don’t expose this parameter, so you can’t restrict the plugin list there.

### Role, grants, and publication

Replace the names, the password, and the column list in the following statements with your own. Every replica-identity column, including the primary key, must stay in the column list. The connector role can’t own the table.

Run the following steps on self-managed PostgreSQL, Amazon RDS, or Amazon Aurora:

1. Allow only the `pgoutput` output plugin, and reload the configuration. Amazon RDS and Amazon Aurora don’t expose `output_plugin_libraries`, so skip this step on those services:

   Copy code

   ```
   ALTER SYSTEM SET output_plugin_libraries = 'pgoutput';
   SELECT pg_reload_conf();
   ```
2. Create a login role for the connector:

   - On a server you manage, include the `REPLICATION` attribute. The role isn’t a superuser, and it can’t bypass row-level security, create databases, or create roles:

     Copy code

     ```
     CREATE ROLE openflow_user WITH
       LOGIN
       REPLICATION
       NOSUPERUSER
       NOBYPASSRLS
       NOCREATEDB
       NOCREATEROLE
       PASSWORD 'connector_password';
     ```
   - On Amazon RDS or Amazon Aurora, create the role without the `REPLICATION` attribute, and then grant `rds_replication`. Don’t grant `rds_superuser`. Column grants and the publication column list still apply, and the connector still uses `pgoutput`:

     Copy code

     ```
     CREATE ROLE openflow_user WITH LOGIN PASSWORD 'connector_password';
     GRANT rds_replication TO openflow_user;
     ```
3. Allow the role to use the schema:

   Copy code

   ```
   GRANT USAGE ON SCHEMA app TO openflow_user;
   ```
4. Remove every privilege the role has on the table:

   Copy code

   ```
   REVOKE ALL ON TABLE app.customers FROM openflow_user;
   ```
5. Remove table-level `SELECT` from `PUBLIC`, so members of `PUBLIC` don’t receive `SELECT` on every column:

   Copy code

   ```
   REVOKE SELECT ON TABLE app.customers FROM PUBLIC;
   ```
6. Grant `SELECT` on the columns to replicate:

   Copy code

   ```
   GRANT SELECT (id, name, updated_at) ON TABLE app.customers TO openflow_user;
   ```
7. Create a publication that lists those same columns:

   Copy code

   ```
   CREATE PUBLICATION openflow_pub
     FOR TABLE app.customers (id, name, updated_at);
   ```

Don’t grant `pg_read_all_data`, `pg_read_server_files`, or `pg_write_server_files`. Don’t make the connector role a member of the table owner.

Table-level `SELECT`, `GRANT SELECT ON ALL TABLES`, and `ALTER DEFAULT PRIVILEGES ... GRANT SELECT ON TABLES` cover every column, including columns added later. A column grant doesn’t extend to a new column. When a new column should be replicated, add it to the grant and to the publication.

Warning

This database must contain only the `openflow_pub` publication because publications have no privileges of their own, so any replication connection to the database can use any publication. `FOR ALL TABLES`, `FOR TABLES IN SCHEMA`, or a publication of this table with no column list publishes every column.

### Host-based authentication

This section applies to a server whose host-based authentication file you can edit. Amazon RDS and Amazon Aurora don’t give you access to `pg_hba.conf`.

Allow the connector role to connect to the application database. Don’t add a line whose database field is `replication`:

```
host  appdb  openflow_user  <connector-cidr>  scram-sha-256
```

This line allows `openflow_user` to connect to the `appdb` database from the connector’s network range and authenticates the connection with `scram-sha-256`.

### Check the configuration

Run the following queries, and replace the role, table, and publication names with the names you used:

1. Where you set `output_plugin_libraries`, confirm the value. On Amazon RDS and Amazon Aurora, skip this query:

   Copy code

   ```
   SELECT setting FROM pg_settings WHERE name = 'output_plugin_libraries';
   ```

   The setting must be `pgoutput`.
2. Confirm that the database contains only the connector publication, and that the publication doesn’t include every table:

   Copy code

   ```
   SELECT pubname, puballtables FROM pg_publication;
   ```

   The result must contain only `openflow_pub`, and `puballtables` must be false.
3. Confirm which columns the connector role can select:

   Copy code

   ```
   SELECT attname,
          has_column_privilege('openflow_user', 'app.customers', attname, 'SELECT') AS can_select
   FROM pg_attribute
   WHERE attrelid = 'app.customers'::regclass
     AND attnum > 0
     AND NOT attisdropped
   ORDER BY attnum;
   ```

   `can_select` must be false for every excluded column.

In the connector, set the source user to `openflow_user` and the publication name to `openflow_pub`.
