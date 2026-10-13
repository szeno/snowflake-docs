# IBM Db2

## Overview

Horizon Catalog ingests Db2 metadata through a direct database connection that uses a dedicated
service account with read access to the Db2 system catalog. On each crawl, the connector collects
schemas, tables, views, columns, primary keys, foreign keys, and indexes.

The Db2 connector collects metadata and view lineage only. It doesn’t read a Db2 query log, so a
Db2 data source doesn’t include the following:

- Popularity, which Horizon Catalog derives from query log records.
- Table lineage derived from queries.
- Column lineage.

Horizon Catalog builds view lineage from the view definitions it reads in the system catalog, so
lineage between a view and the tables that the view reads is available.

## Prerequisites

To connect Db2 to Horizon Catalog, you need the following:

- A Db2 for Linux, UNIX, and Windows (Db2 LUW) database that Horizon Catalog can reach over the
  public internet. This guide doesn’t cover Db2 for z/OS or Db2 for i.
- Administrative access to the Db2 instance, so that you can create a service account and run
  `GRANT` statements.
- A Db2 endpoint that accepts non-TLS connections.

Warning

The connector has no Db2 TLS settings, so it can’t connect to an SSL-only port. Connect on the
non-TLS service port (`SVCENAME`, or the RDS endpoint port). Traffic on that port is unencrypted.

Complete the following steps to connect Db2 to Horizon Catalog:

1. [Create a Db2 service account](#1-create-a-db2-service-account).
2. [Grant access to the system catalog](#2-grant-access-to-the-system-catalog).
3. [Ensure network connectivity](#3-ensure-network-connectivity).
4. [Create the Db2 connection](#4-create-the-db2-connection).

## 1. Create a Db2 service account

Snowflake recommends a dedicated service account for Horizon Catalog that reads metadata only.

For self-managed Db2 with the default `SERVER` authentication type, create an operating-system user
on the database server. If the instance uses another authentication facility, create the account
there instead. For information about authentication types, see
[Authentication methods for your server](https://www.ibm.com/docs/en/db2/11.5.x?topic=details-authentication-methods-servers)
in the IBM documentation.

For Amazon RDS for Db2, connect to the `rdsadmin` database as the master user, then call
`rdsadmin.add_user`. Replace the placeholders with the service account credentials:

Copy code

```
CALL rdsadmin.add_user('<username>', '<password>', NULL);
```

For details, see [Stored procedures for granting and revoking privileges for RDS for Db2](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/db2-sp-granting-revoking-privileges.html)
in the AWS documentation.

Note the username and password. Then connect to the database you enter as **Source Database**
and grant catalog privileges in [Step 2](#2-grant-access-to-the-system-catalog).

## 2. Grant access to the system catalog

Horizon Catalog reads metadata from the Db2 catalog views. Connect as an administrative user to the
database you enter as **Source Database**, and grant the service account the following
privileges, replacing `<username>` with the service account you created in
[Step 1](#1-create-a-db2-service-account):

Copy code

```
GRANT CONNECT ON DATABASE TO USER <username>;
GRANT USAGE ON WORKLOAD SYSDEFAULTUSERWORKLOAD TO USER <username>;
GRANT SELECT ON TABLE SYSCAT.SCHEMATA TO USER <username>;
GRANT SELECT ON TABLE SYSCAT.TABLES TO USER <username>;
GRANT SELECT ON TABLE SYSCAT.COLUMNS TO USER <username>;
GRANT SELECT ON TABLE SYSCAT.VIEWS TO USER <username>;
GRANT SELECT ON TABLE SYSCAT.INDEXES TO USER <username>;
GRANT SELECT ON TABLE SYSCAT.TABCONST TO USER <username>;
GRANT SELECT ON TABLE SYSCAT.KEYCOLUSE TO USER <username>;
GRANT SELECT ON TABLE SYSIBM.SQLFOREIGNKEYS TO USER <username>;
```

Amazon RDS for Db2 creates instances in `RESTRICTIVE` mode. After the earlier grants, also grant the
`ROLE_NULLID_PACKAGES` role so the CLI driver can run the `NULLID` packages used on the
connection:

Copy code

```
GRANT ROLE ROLE_NULLID_PACKAGES TO USER <username>;
```

For details, see [Granting and revoking privileges for RDS for Db2](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/db2-granting-revoking-privileges.html)
in the AWS documentation.

The following table describes what Horizon Catalog reads from each view:

| Catalog view | What Horizon Catalog reads |
| --- | --- |
| `SYSCAT.SCHEMATA` | The schemas that are available to crawl. |
| `SYSCAT.TABLES` | Table names, table types, and table comments. |
| `SYSCAT.COLUMNS` | Column names, data types, nullability, comments, and primary keys. |
| `SYSCAT.VIEWS` | View names and view definitions, which produce view lineage. |
| `SYSCAT.INDEXES` | Secondary indexes. |
| `SYSCAT.TABCONST` | Unique-constraint metadata used during table reflection. |
| `SYSCAT.KEYCOLUSE` | Constraint-column metadata used during table reflection. |
| `SYSIBM.SQLFOREIGNKEYS` | Foreign key relationships between tables. |

Expand

Show lessSee more

Note

The foreign key view is in the `SYSIBM` schema. Every other view that the connector reads is in
`SYSCAT`.

The service account needs no privileges on your own tables and views. Horizon Catalog reads
metadata from the catalog views and doesn’t read table contents from Db2. The `GRANT` list matches
the views the connector queries; it isn’t proven as a complete least-privilege set on a restricted
user.

## 3. Ensure network connectivity

Horizon Catalog connects to your Db2 instance over the public internet, so the instance must
accept inbound TCP connections on its Db2 service port. For self-managed Db2, use the instance’s
`SVCENAME` value, often `50000`. Don’t use `SSL_SVCENAME`. For Amazon RDS for Db2, use the
endpoint port from **Connectivity & security**. Don’t use the instance’s SSL port. Either make the
instance publicly reachable, or put it behind an internet-facing load balancer or proxy that you
control and that forwards to the Db2 port.

The **Hostname** value must be a DNS name, not an IP address. Use a domain name such as
`db2.example.com`. Horizon Catalog rejects a value that isn’t a domain name before it checks
reachability. The name must
resolve to a publicly routable address. Horizon Catalog also rejects a hostname that resolves to a
private address range, such as an address inside your own virtual private cloud.

About egress IPs

Horizon Catalog doesn’t guarantee stable egress IPs. The egress IPs it connects from can change
at any time without notice. If you prefer to allowlist specific CIDRs instead of allowing
`0.0.0.0/0`, contact Snowflake support for the egress IPs currently in use, and expect to update
that allowlist when they change. For details, see
[Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).

## 4. Create the Db2 connection

In Snowflake, open **Catalog > Connections** and select **IBM Db2** from the Metadata connections
section. Fill in the following fields, then select **Next**:

| Field | Value |
| --- | --- |
| **Display Name** | A name for this data source in Horizon Catalog. The default is `IBM Db2`. |
| **Hostname** | The DNS hostname of the Db2 instance, without a protocol prefix, port number, or IP address. |
| **Port** | The Db2 service port. For self-managed Db2, use `SVCENAME`. For Amazon RDS for Db2, use the endpoint port. The wizard default is `50000`. |
| **Username** | The service account from [Step 1](#1-create-a-db2-service-account). |
| **Password** | The password for the service account. |
| **Source Database** | The Db2 database to crawl. Each data source crawls a single database. |
| **Snowflake Database** | The Snowflake database where the connector stores its metadata. The default is `CONNECTORS`. |
| **Snowflake Schema** | The Snowflake schema where the connector stores its metadata. The default is `METADATA`. |

Expand

Show lessSee more

The next wizard step is named **Select databases**; the description mentions databases and schemas,
but **Source Database** already scoped the data source to one database. Choose the schemas you want
Horizon Catalog to crawl, then select **Done**. Horizon Catalog collects no metadata for a schema
that you don’t select, so select everything you expect to see in the catalog. You can change the
selection later in the data source settings.

Initial metadata typically appears within a few minutes.

## Connection security

Horizon Catalog connects to Db2 over unencrypted TCP/IP and authenticates with the username and
password from [Step 1](#1-create-a-db2-service-account). Horizon Catalog stores the password in a
Snowflake-managed encrypted storage layer. The endpoint requirement is described in
[Prerequisites](#prerequisites).

The grants in [Step 2](#2-grant-access-to-the-system-catalog) cover the system catalog only, so
Horizon Catalog reads schema, table, view, and column definitions over this connection and never
reads the contents of your tables.

For more details on the shared-responsibility model for Horizon Catalog connectors, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).

## Troubleshooting

The following table describes the errors you’re most likely to see when you create the connection:

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| `Invalid host provided. Host should be a valid domain name without protocol or port` | The **Hostname** value is an IP address, includes a protocol or port, or isn’t a domain name. | Step 3. |
| `Invalid host name or address. Check that the host is reachable from outside Snowflake and not an internal/private IP.` | The hostname resolves to a private or otherwise blocked address. | Step 3. |
| `Unable to connect to Db2`, with `SQLCODE=-1336` or `SQLCODE=-30081` | The hostname or port is wrong, the instance isn’t reachable, or the endpoint requires TLS. | Step 3. |
| `Unable to authenticate to Db2`, with `SQLCODE=-30082` | The username or password is wrong, or the account is disabled. | Step 1. |
| `Unable to access to Db2 database`, with `SQLCODE=-30061` | The **Source Database** value doesn’t match a database in the instance. | Step 4. |
| The connection succeeds, but schemas or tables are missing | The schema isn’t selected, or the service account is missing a grant. | Steps 2 and 4. |

Expand

Show lessSee more
