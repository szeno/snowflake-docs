# Snowflake Postgres and self-hosted PostgreSQL

Use this guide for Snowflake Postgres and for PostgreSQL that you host yourself, on-premises or
on a cloud virtual machine. Both use the same Horizon Catalog PostgreSQL connector, and neither
requires AWS credentials or an IAM role.

## Before you start

To connect Snowflake Postgres or a self-hosted PostgreSQL instance to Horizon Catalog, you will
need…

- access to an administrative user on the instance. On Snowflake Postgres, that user is
  `snowflake_admin`.
- a PostgreSQL instance reachable from the internet on its port (default 5432), either directly
  or through an internet-facing load balancer or proxy that you control.

Network access

Horizon Catalog connects to your instance over the public internet, so the instance must be
reachable from the internet on the PostgreSQL port (default 5432), either directly or through an
internet-facing load balancer or proxy you control. Horizon Catalog doesn’t guarantee stable
egress IPs. The egress IPs it connects from can change at any time without notice. If you’d
rather allowlist specific CIDRs instead of allowing `0.0.0.0/0`, contact Snowflake support for
the egress IPs currently in use, and expect to update that allowlist when they change. For
details, see
[Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).

## 1. Create PostgreSQL user

Connect to the PostgreSQL database using an administrative user account and create a new user (service account) for the integration, by executing SQL query:

Copy code

```
CREATE USER snowflake_horizon WITH encrypted password 's313ctst8r'
```

Replace `s313ctst8r` with strong and secure password.

Then, it is necessary to grant permissions to selected databases and schemas. To do this, run the following query individually in the context of the selected database for each schema:

Copy code

```
GRANT USAGE ON SCHEMA <schema_name> TO snowflake_horizon;
ALTER DEFAULT PRIVILEGES GRANT USAGE ON SCHEMAS TO snowflake_horizon;
```

Replace `<schema_name>` with the expected schema name and repeat for each databases & schemas.

## 2. Create a new connection

1. In Snowflake, open **Catalog > Connections** and select **PostgreSQL** from the Metadata connections section.
2. Fill form in the required information:

   - **Source Type:** Select “PostgreSQL”
   - **Display Name:** This value is `PostgreSQL` by default, but you can override it if desired.
   - **Hostname**: The public hostname of your instance.
   - **Port**: The port used to connect. By default is `5432`, but you can adjust it if required.
   - **Username**: The PostgreSQL user name to connect. In our examples of SQL queries above, we use `snowflake_horizon`.
   - **Password**: The password of the PostgreSQL user.
   - **DB Name**: Any database we have access to that is used to initiate a first connection.
3. Select **Connect**.
4. For **Log type**, choose one of the following:

   - **Query statistics (pg\_stat\_statements)**: Reads statement statistics from the database.
     Use this for an instance that has the `pg_stat_statements` extension. See
     [Query statistics (pg\_stat\_statements)](/user-guide/snowflake-horizon/connectors/postgres/query-log-sources/pg-stat).
   - **None**: Metadata only. Lineage and popularity, except lineage from view definitions,
     will not be available.
5. Select **Connect** again.

## Connection security

Horizon Catalog uses a TLS-capable PostgreSQL client. If your PostgreSQL instance is configured
to accept TLS connections, the connection is encrypted automatically. However, if TLS is not
available on the server, the connection proceeds unencrypted.

You are responsible for enabling TLS on your database instance

Snowflake strongly recommends enforcing TLS 1.2 or higher on your PostgreSQL instance. Set the
following parameters in `postgresql.conf`:

| Parameter | Recommended value | Effect |
| --- | --- | --- |
| `ssl` | `on` | Enable TLS on the server. |
| `ssl_min_protocol_version` | `TLSv1.2` | Refuse TLS versions older than 1.2. |

Expand

Show lessSee more

You should also configure `pg_hba.conf` to require TLS for the Horizon Catalog service
account by using the `hostssl` connection type instead of `host`.

After applying these settings, Horizon Catalog connects over TLS without any changes on the
connector side.

For more details on the shared-responsibility model for Horizon Catalog connectors,
see [Security and data protection](/user-guide/snowflake-horizon/connectors/security).

## 3. Choose databases and schemas

After you fill in the information, you’ll be asked to select the databases you’d like to load into Horizon Catalog.

Note

Horizon Catalog will not read queries or metadata or generate lineage for databases, schemas, or tables that are not loaded. Please load all data for which you expect to see lineage.

Select the database, then select **Next**.

For each database you selected, you’ll be able to select the schemas.

Your metadata should start loading automatically. Please allow 24-48 hours to completely generate popularity and lineage.

When the sync is complete, you’ll be able to explore PostgreSQL in Horizon Catalog.
