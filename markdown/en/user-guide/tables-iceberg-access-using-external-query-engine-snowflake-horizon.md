# Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog

Regional availability

- Available on Amazon S3, Google Cloud, or Microsoft Azure in all commercial regions.
- Available on FedRAMP (Moderate) deployments on AWS Commercial Gov (US) in the us-east-1 and us-west-2 regions.

Access Snowflake-managed Apache Iceberg™ tables by using an external query engine through
Snowflake Horizon Catalog. To ensure this interoperability with external engines, [Apache Polaris™](https://github.com/apache/polaris)
is integrated into Horizon Catalog. In addition, Horizon Catalog exposes the Apache Iceberg™ REST API (Horizon Iceberg REST Catalog API). This
API lets you access the tables by using external query engines.

You can use Horizon Catalog, which is available in all your existing Snowflake accounts, to read and write to Snowflake-managed Iceberg
tables with external query engines.

You can also access externally managed Iceberg tables in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database)
through the same Horizon IRC endpoint. For instructions, see
[Access externally managed Apache Iceberg™ tables in a catalog-linked database with an external engine through Snowflake Horizon Catalog](/user-guide/externally-managed-iceberg-tables-access-horizon-irc).

## Query Iceberg tables

By connecting an external query engine to Iceberg tables through Horizon Catalog, you can perform the following tasks:

- Use any external query engine that supports the open Iceberg REST protocol to query these tables, such as Apache Spark™.
- Query any existing and new Snowflake-managed Iceberg tables in a new or existing Snowflake account by using a single Horizon Catalog endpoint.
- Query the tables by using your existing users, roles, policies, and authentication in Snowflake.
- Use vended credentials.

For more information about Snowflake Horizon Catalog, see [Snowflake Horizon Catalog](/user-guide/snowflake-horizon).

## Write to Iceberg tables

You can read and write to Snowflake-managed Iceberg v2 and v3 tables from external engines through the Horizon Iceberg REST Catalog API.

To write to tables, follow the
[workflow for accessing Iceberg tables by using an external query engine](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-workflow).
When you configure access control, ensure that you
[configure write access to your tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-configure-write-access).

Then [write to Iceberg tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-write-to-iceberg-tables).

The following diagram shows external query engines reading and writing to Snowflake-managed Iceberg tables through Horizon Catalog and Snowflake reading and
writing to these tables:

![Diagram that shows external query engines reading and writing to Snowflake-managed Iceberg tables through Horizon Catalog and Snowflake reading and
writing to these tables. Both Read and Write are Generally Available.](/static/images/iceberg/tables-iceberg-query-using-external-query-engine-snowflake-horizon-diagram-ga.png)

## Billing

- The Horizon Iceberg REST Catalog API is available in all Snowflake editions.
- The API requests are billed as 0.5 credit per million calls and charged as Cloud Services.
- For cross-region data access, standard cross-region data egress charges as stated in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) are applicable.

Note

Billing for this feature is scheduled to begin in second half of 2026, subject to change.

## Supported external engines and catalogs

The following tables, although not exhaustive, show many external engines and catalogs that integrate with the Horizon Iceberg REST Catalog API.
This integration enables access to Snowflake managed Iceberg tables through external systems.

### Supported external engines

The following external query engines integrate with the Horizon Iceberg REST Catalog API:

| Product | Access Snowflake-managed Iceberg tables through Horizon Catalog |
| --- | --- |
| Apache Doris™ | ✔ |
| Apache Flink™ | ✔ |
| Apache Spark™ | ✔ |
| Dremio | ✔ |
| DuckDB | ✔ |
| PyIceberg | ✔ |
| StarRocks | ✔ |
| Trino | ✔ |

Expand

Show lessSee more

### Supported external catalogs

The following external catalogs integrate with the Horizon Iceberg REST Catalog API:

| Product | Access Snowflake-managed Iceberg tables through Horizon Catalog | Comment |
| --- | --- | --- |
| Apache Polaris™ | ✔ |  |
| AWS Glue | ✔ | For instructions on how to configure this integration, see [Access Snowflake Horizon Catalog data using catalog federation in the AWS Glue Data Catalog](https://aws.amazon.com/blogs/big-data/access-snowflake-horizon-catalog-data-using-catalog-federation-in-the-aws-glue-data-catalog/) in the AWS Big Data Blog. |
| Palantir Foundry | ✔ | For instructions on how to configure this integration, see [Iceberg tables (virtual tables only)](https://www.palantir.com/docs/foundry/available-connectors/snowflake#iceberg-tables-virtual-tables-only) in the Palantir documentation. |
| Databricks Unity Catalog | Not announced |  |
| Google BigLake Metastore | ✔ | For instructions on how to configure this integration, see [Configure a catalog integration for Google Cloud BigLake Metastore](/user-guide/tables-iceberg-configure-catalog-integration-rest-biglake). |
| Microsoft Fabric / Synapse | In development |  |

Expand

Show lessSee more

## Prerequisites

Retrieve the account identifier for your Snowflake account that contains the Iceberg tables that you want to access. For instructions,
see [Account identifiers](/user-guide/admin-account-identifier). You specify this identifier when you
[connect an external query engine to your Iceberg tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-query-engine).

Tip

To get your account identifier by using SQL, you can run the following command:

Copy code

```
SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME();
```

## (Optional) Private connectivity

For secure connectivity, consider configuring [Inbound](/user-guide/private-connectivity-inbound) and
[Outbound](/user-guide/private-connectivity-outbound) private connectivity for your Snowflake account while you access the
Horizon Catalog endpoint.

Note

Private connectivity is only supported for Snowflake-managed Iceberg tables stored on Amazon S3 or Azure Storage (ADLS).

## Workflow for accessing Iceberg tables by using an external query engine

To access Iceberg tables by using an external query engine, complete the following steps:

1. [Create Iceberg tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-create-tables)
2. [Configure access control](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-configure-access-control)
3. [Obtain an access token for authentication](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-generate-access-token)
4. [Verify access token permissions](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-verify-access-token-permissions)
5. [(Optional) Configure data protection policies](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-configure-access-policies)
6. [Connect an external query engine to Iceberg tables through Horizon Catalog](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-query-engine)
7. [Query Iceberg tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-query-iceberg-tables) or
   [write to Iceberg tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-write-to-iceberg-tables)

## Step 1: Create Iceberg tables

Important

If you already have Snowflake-managed Iceberg tables that you want to access, you can skip this step.

In this step, you create Snowflake-managed Iceberg tables that use Snowflake as the catalog, so you can access them with an external
query engine. For instructions, see the following topics:

- [Tutorial: Create your first Apache Iceberg™ table](/user-guide/tutorials/create-your-first-iceberg-table): A tutorial that shows how to create a database, create a Snowflake-managed Iceberg table, and load data into the table.
- [Create a Snowflake-managed Iceberg table](/user-guide/tables-iceberg-create#label-tables-iceberg-create-snowflake-catalog): Example code for creating a Snowflake-managed Iceberg table.

## Step 2: Configure access control

Important

If you already have roles that are configured with access to the Iceberg tables that you want to access, you can skip this step.

In this step, you configure access control for the Snowflake-managed Iceberg tables that you want to access with an external query engine.
For example, you can set up the following roles in Snowflake:

- data\_engineer role, which has access to all schemas and all Snowflake-managed Iceberg tables in a database.
- data\_analyst role, which has access to one schema in the database and only access to two Snowflake-managed Iceberg tables within that schema.

For more information, see the following sections:

- [Configure read access to your Iceberg tables](#label-tables-iceberg-query-horizon-configure-read-access)
- [Configure write access to your Iceberg tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-configure-write-access)

### Configure read access to your Iceberg tables

To query Iceberg tables, the role used to perform the operation must have the SELECT privilege on the Iceberg table and the USAGE
privilege on the parent database and schema. For an example of granting these privileges to a role, see
[Example: Set up a service account user](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-set-up-service-account-user).

Important

The role that has the OWNERSHIP privilege on an Iceberg table must maintain the USAGE privilege on the external volume associated with
the table. If the owner role doesn’t have USAGE on the external volume, any read or write table operation that asks for vended credentials
will fail.

#### Example: Set up a service account user

The following example sets up a service account user in Snowflake with read-only access to an Iceberg table:

- Creates a `data_engineer` role.
- Grants the `data_engineer` role USAGE and MONITOR privileges on the `iceberg_test_db` database and its `public` schema.
- Grants SELECT privileges on the `test_table` Iceberg table.
- Creates a service user named `horizon_rest_srv_account_user` and assigns the `data_engineer` role to that user.

Copy code

```
CREATE OR REPLACE ROLE data_engineer;

GRANT USAGE ON DATABASE iceberg_test_db TO ROLE data_engineer;
GRANT USAGE ON SCHEMA iceberg_test_db.public TO ROLE data_engineer;

GRANT SELECT ON TABLE iceberg_test_db.public.test_table TO ROLE data_engineer;

CREATE OR REPLACE USER horizon_rest_srv_account_user TYPE=SERVICE DEFAULT_ROLE=data_engineer;

GRANT ROLE data_engineer TO USER horizon_rest_srv_account_user;
```

#### (Optional) Apply future grants on Iceberg tables

To ensure access to any new Iceberg tables created in a schema, use the
[GRANT … ON FUTURE ICEBERG TABLES](/sql-reference/sql/grant-privilege#label-grant-privilege-schema-future-grants) syntax.

The following example grants the `data_engineer` role access to any Iceberg tables created under a schema named `my_schema`.

Copy code

```
GRANT SELECT ON FUTURE ICEBERG TABLES IN SCHEMA my_db.my_schema TO ROLE data_engineer;
```

For more information about access control in Snowflake, see the following topics:

- [Overview of Access Control](/user-guide/security-access-control-overview)
- [Configuring access control](/user-guide/security-access-control-configure)

### Configure write access to your Iceberg tables

The following table describes the privileges required for write operations on Iceberg tables:

| Operation | Necessary privileges |
| --- | --- |
| Data Manipulation Language (DML) operations | Important  A role used to execute the operation must have *all* of the following privileges:   - SELECT, UPDATE, TRUNCATE, INSERT, and DELETE privileges on the table - USAGE privilege for the parent schema where the table is nested under - USAGE privilege on the parent database or schema under which the table is nested |
| CREATE ICEBERG TABLE | A role used to execute the operation must have the following privileges:   - CREATE ICEBERG TABLE privilege on schema - USAGE privilege on the external volume |
| CREATE SCHEMA | A role used to execute the operation must have the CREATE SCHEMA privilege on the parent database. |
| Rename a table | A role used to execute the operation must have the OWNERSHIP privilege on the table.  Important  To move the table to a new schema, ensure that your role also has the CREATE ICEBERG TABLE privilege on the destination schema. |
| All other operations on a table | A role used to execute the operation must have the OWNERSHIP privilege on the table in addition to the privileges on the schema and database. For example, you must have these privileges to run the ALTER ICEBERG TABLE … ADD COLUMN or ALTER ICEBERG TABLE … DROP COLUMN operation. |

Expand

Show lessSee more

For more information about access control in Snowflake, see the following topics:

- [Overview of Access Control](/user-guide/security-access-control-overview)
- [Configuring access control](/user-guide/security-access-control-configure)

## Step 3: Obtain an access token for authentication

In this step, you obtain an access token, which you must have to authenticate to the Horizon Catalog endpoint for your Snowflake account. You
need to obtain an access token for each user — service or human — and role that is configured with access to Snowflake-managed Iceberg tables. For example, you need to
obtain one access token for a user with DATA\_ENGINEER role and another user with a DATA\_ANALYST role.

You specify this access token later when you
[connect an external query engine to Iceberg tables through Horizon Catalog](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-query-engine).

You can obtain an access token by using one of the following authentication options:

- [External OAuth](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-external-oauth)
- [Key-pair authentication](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-key-pair)
- [Programmatic access token (PAT)](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-pat)
- [Workload Identity Federation (WIF) / OIDC](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-wif)

### External OAuth

If you’re using External OAuth, generate an access token for your identity provider. For instructions, see [External OAuth overview](/user-guide/oauth-ext-overview).

Note

For External OAuth, alternatively, you can configure your connection to the engine with automatic token refresh instead of specifying
an access token.

### Key-pair authentication

If you use key-pair authentication, to obtain an access token, you sign a JSON web token (JWT) with your
private key.

The following steps cover how to generate an access token for key-pair authentication:

1. [Configure key-pair authentication](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-key-pair-configure)
2. [Grant a role to the user](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-key-pair-grant-role)
3. [Generate a JSON Web Token (JWT)](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-key-pair-generate-jwt)
4. [Generate an access token](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-key-pair-generate-access-token)

#### Step 1: Configure key-pair authentication

In this step, you perform the following tasks:

- Generate a private key
- Generate a public key
- Store the private and public keys securely
- Grant the privilege to assign a public key to a Snowflake user
- Assign the public key to a Snowflake user
- Verify the user’s public key fingerprint

For instructions, see [Configuring key-pair authentication](/user-guide/key-pair-auth#label-configuring-key-pair-authentication).

#### Step 2: Grant a role to the user

To grant to the key-pair authentication user the Snowflake role that has privileges to the tables you want to access, run the [GRANT ROLE](/sql-reference/sql/grant-role) command.
For example, to grant the ENGINEER role to the `my_service_user` user, run
the following command:

Copy code

```
GRANT ROLE ENGINEER to user my_service_user;
```

#### Step 3: Generate a JSON Web Token (JWT)

In this step, you use SnowSQL to generate a JSON Web Token (JWT) for key-pair authentication.

Note

- You must have [SnowSQL](https://www.snowflake.com/developers/downloads/snowsql/) installed on your machine.
- Alternatively, you can use Python, Snowflake CLI, Java, or Node.js to generate a JWT. For an example, see the following sections:
  - [Python example](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-python)
  - [Snowflake CLI example](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-snowcli)
  - [Java example](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-java)
  - [Node.js example](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-nodejs)

Use SnowSQL to generate a JWT:

Copy code

```
snowsql --private-key-path "<private_key_file>" \
  --generate-jwt \
  -h "<account_identifier>.snowflakecomputing.com" \
  -a "<account_locator>" \
  -u "<user_name>"
```

Where:

- `<private_key_file>` is the path to your private key file that corresponds to the public key assigned to your Snowflake user.
  For example: `/Users/jsmith/.ssh/rsa_key.p8`.
- `<account_identifier>` is the account identifier for your Snowflake account, in the format `<organization_name>-<account_name>`.
  To find the account identifier, see [Supported external engines and catalogs](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-before-you-begin).
  An example of an account identifier is `myorg-myaccount`.
- `<account_locator>` is the account locator for your Snowflake account.

  To find your account locator, see
  [Locate your Snowflake account information in Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-account-details) and view the *Account locator* in the **Account Details** dialog.
- `<user_name>` is the user name for a Snowflake user with the public key assigned to the user.

#### Step 4: Generate an access token

Important

To generate an access token, you must first [generate a JWT](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-key-pair-generate-jwt).
You must first generate a JWT because you use the JWT to
generate the access token.

Use a `curl` command to generate an access token:

Copy code

```
curl -i --fail -X POST "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog/v1/oauth/tokens" \
 --header 'Content-Type: application/x-www-form-urlencoded' \
 --data-urlencode 'grant_type=client_credentials' \
 --data-urlencode 'scope=session:role:<role>' \
 --data-urlencode 'client_secret=<JWT_token>'
```

Where:

- `<account_identifier>` is the account identifier for your Snowflake account, in the format `<organization_name>-<account_name>`.
  To find the account identifier, see [Supported external engines and catalogs](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-before-you-begin).
  An example of an account identifier is `myorg-myaccount`.
- `<role>` is the Snowflake role that is granted access to Iceberg tables, such as ENGINEER.
- `<JWT_token>` Is the JWT that you generated in the previous step.

### Programmatic access token (PAT)

If you use PATs, generate a PAT for authentication.

First, you generate a PAT, which you use to [connect an external query engine to Iceberg tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-query-engine).
Then, you generate an access token, which you only use to verify the permissions for your PAT.

#### Step 1: Generate a PAT

For instructions on how to configure and generate a PAT,
see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

The following example creates a programmatic access token (PAT) for the service account user that you created in the previous step by
using the [ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-add-programmatic-access-token) command:

Copy code

```
ALTER USER IF EXISTS HORIZON_REST_SRV_ACCOUNT_USER
ADD PAT HORIZON_REST_SRV_ACCOUNT_USER_PAT
  DAYS_TO_EXPIRY = 7
  ROLE_RESTRICTION = 'DATA_ENGINEER'
  COMMENT = 'HORIZON REST API PAT FOR SERVICE ACCOUNT';
```

#### Step 2: Generate an access token for your PAT

In this step, you generate an access token for your PAT.

Attention

You only specify the access token that you generate in this step when you
[verify the permissions](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-verify-access-token-permissions)
for your PAT. When you
[connect an external query engine to Iceberg tables](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-query-engine),
you must specify your PAT that you generated in the previous step, not the access token that you generate in this step.

Use a `curl` command to generate an access token for your PAT:

Copy code

```
curl -i --fail -X POST "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog/v1/oauth/tokens" \
 --header 'Content-Type: application/x-www-form-urlencoded' \
 --data-urlencode 'grant_type=client_credentials' \
 --data-urlencode 'scope=session:role:<role>' \
 --data-urlencode 'client_secret=<PAT_token>'
```

Where:

- `<account_identifier>` is the account identifier for your Snowflake account, in the format `<organization_name>-<account_name>`.
  To find the account identifier, see [Supported external engines and catalogs](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-before-you-begin).
  An example of an account identifier is `myorg-myaccount`.
- `<role>` is the Snowflake role that is granted to your PAT and has access to the Iceberg tables that you want to query or write to, such as ENGINEER.
- `<PAT_token>` is the value for the PAT token that you generated in the previous step.

### Workload Identity Federation (WIF) / OIDC

If you are running your external query engine in an environment that supports OpenID Connect (OIDC), you can use Workload Identity Federation
(WIF) for secretless authentication.

First, configure your Snowflake account to trust your external identity provider. You must create a Snowflake service user and
configure the `WORKLOAD_IDENTITY` property. For prerequisite instructions, see [Workload identity federation](/user-guide/workload-identity-federation).

Once your Snowflake service user is configured to accept OIDC tokens from your provider, your external query engine must fetch its
short-lived OIDC token dynamically at runtime.

When you connect your external query engine to Iceberg tables through Horizon Catalog, you must pass the fetched OIDC token as a
credential. The external catalog performs a token exchange with Snowflake to retrieve a valid access token bound to the scope you define.
You must also specify the workload identity provider using a custom header in your catalog configuration.

#### Example: Apache Spark™ configuration for WIF / OIDC

To authenticate using WIF / OIDC in Apache Spark™, supply the fetched OIDC token to the `.credential` property, define the `.scope`
property with your required Snowflake role, and add the `X-Snowflake-Workload-Identity-Provider` header to your Iceberg REST catalog
configuration.

Copy code

```
# ... [Other Spark Session Configurations] ...

# Pass the dynamically fetched OIDC token as the credential for token exchange
.config(f"spark.sql.catalog.{CATALOG_NAME}.credential", "<fetched_oidc_token>")

# Define the required Snowflake role scope
.config(f"spark.sql.catalog.{CATALOG_NAME}.scope", "session:role:<role>")

# Define the Workload Identity Provider header
.config(f"spark.sql.catalog.{CATALOG_NAME}.header.X-Snowflake-Workload-Identity-Provider", "OIDC")
```

Where:

- `<fetched_oidc_token>` is the short-lived OIDC token generated by your compute environment’s native identity provider.
- `<role>` is the Snowflake role that has access to the Iceberg tables you want to query or write to.

## Step 4: Verify access token permissions

In this step, you verify the permissions for the access token that you obtained in the previous step.

- [Verify access to the Horizon IRC endpoint](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-verify-access)
- [Retrieve the metadata for a table](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-load-table)

### Verify access to the Horizon IRC endpoint

Use a `curl` command to verify that you have permission to access your Horizon IRC endpoint:

Copy code

```
curl -i --fail -X GET "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog/v1/config?warehouse=<database_name>" \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json"
```

Where:

- `<account_identifier>` is the account identifier for your Snowflake account, in the format `<organization_name>-<account_name>`.
  To find the account identifier, see [Supported external engines and catalogs](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-before-you-begin).
  An example of an account identifier is `myorg-myaccount`.
- `<access_token>` is your access token that you generated. If you’re using a PAT, this value is the [access token you generated](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-pat-generate-access-token), not the
  *personal access token (PAT)* you generated.
- `<database_name>` is the name of the database that contains the Iceberg tables that you want to access.

  Important

  If your database was created without quotes around the name, you must specify the database name in *all capital letters*, even if it was created with lowercase letters.

Example return value:

```
{
  "defaults": {
    "default-base-location": ""
  },
  "overrides": {
    "prefix": "MY-DATABASE"
  }
}
```

### Retrieve the metadata for a table

You can also make a GET request to retrieve the metadata for a table. Snowflake uses the
[loadTable](https://github.com/apache/iceberg/blob/apache-iceberg-1.6.1/open-api/rest-catalog-open-api.yaml#L616)
operation to load table metadata from your REST catalog.

Copy code

```
curl -i --fail -X GET "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog/v1/<database_name>/namespaces/<namespace_name>/tables/<table_name>" \
 -H "Authorization: Bearer <access_token>" \
 -H "Content-Type: application/json"
```

Where:

- `<account_identifier>` is the account identifier for your Snowflake account, in the format `<organization_name>-<account_name>`.
  To find the account identifier, see [Supported external engines and catalogs](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-before-you-begin).
  An example of an account identifier is `myorg-myaccount`.
- `<database_name>` is the database of the table whose metadata you want to retrieve.
- `<namespace_name>` is the namespace of the table whose metadata you want to retrieve.
- `<table_name>` is the table whose metadata you want to retrieve.
- `<access_token>` is your access token that you generated. If you’re using a PAT, this value is the
  [access token you generated](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-pat-generate-access-token), not the
  *personal access token (PAT)* you generated.

Important

If your database, namespace, or table was created without quotes around the name, you must specify the database, namespaces, or table name in *all capital letters*, even if the object was created with lowercase
letters.

### Token auto-refresh for key-pair authentication

By default, the key-pair JWT has a 1-hour lifespan. To enable auto-refresh for sessions longer than 1 hour, you must first extend the
JWT lifespan for your account (contact Snowflake support to configure this). Once extended, you can configure the Iceberg REST catalog
client to automatically refresh the access token for the duration of the JWT’s validity.

When you use the `.credential` property (instead of `.token`) along with the `.oauth2-server-uri` property, the Apache Iceberg REST
catalog client uses the OAuth2 `client_credentials` flow to:

1. Exchange the JWT for an access token by calling the Snowflake Polaris token endpoint.
2. Parse the `expires_in` value from the token response to determine when the token expires.
3. Automatically request a new access token before the current one expires.

To enable automatic token refresh, replace the `.token` property in your Spark configuration with the `.credential` and
`.oauth2-server-uri` properties:

Copy code

```
# Token auto-refresh configuration (replaces .token)
.config(f"spark.sql.catalog.{CATALOG_NAME}.credential", JWT_TOKEN)
.config(f"spark.sql.catalog.{CATALOG_NAME}.oauth2-server-uri",
        f"https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog/v1/oauth/tokens")
```

Where `<your_JWT_token>` is the JWT generated using your private key (see [Step 3: Generate a JSON Web Token (JWT)](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-key-pair-generate-jwt)).

## (Optional) Step 5: Configure data protection policies

In this step, you configure data protection policies for Iceberg tables. If you don’t have tables that you need to
protect with Snowflake data policies, you can proceed to the next step.

Note

Tables protected by data protection policies can be accessed over the Horizon Iceberg REST API and by using Apache Spark™.

For instructions on how to configure data protection policies, see [Enforce data protection policies on Apache Iceberg™ tables from external query engines](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies).

## Step 6: Connect an external query engine to Iceberg tables through Horizon Catalog

In this step, you connect an external query engine to Iceberg tables through Horizon Catalog. With this connection, you can access the tables
by using the external query engine.

The external engines use the Apache Iceberg™ REST endpoint exposed by Snowflake. For your Snowflake account, this endpoint is
in the following format:

Copy code

```
https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog
```

The example code in this step shows how to set up a connection in Spark, and the example code is in PySpark. For more information,
see the following sections:

- [Connect by using External OAuth or key pair authentication](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-oauth-key-pair)
- [Connect by using a programmatic access token (PAT)](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-pat-token)

### Connect by using External OAuth or key pair authentication

Use one of the following configurations to connect:

- To access Iceberg tables that *don’t* have Snowflake data protection policies configured, [connect an external query engine without enforcing data policies](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-oauth-key-pair-no-access-policies).
- To access Iceberg tables that have Snowflake row access and masking policies configured, [connect an external query engine with data policies enforced](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-oauth-key-pair-access-policies).

#### Connect an external query engine without enforcing data policies

- To connect the external query engine to Iceberg tables by using External OAuth or key pair authentication. Use the following example code.

This code doesn’t enforce data protection policies:

Copy code

```
# Snowflake Horizon Catalog Configuration, change as per your environment

CATALOG_URI = "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog"
HORIZON_SESSION_ROLE = f"session:role:<role>"
CATALOG_NAME = "<database_name>" #provide in UPPER CASE

# Cloud Service Provider Region Configuration (where the Iceberg data is stored)
REGION = "eastus2"

# Paste the External Oauth Access token that you generated in Snowflake here
ACCESS_TOKEN = "<your_access_token>"

# Iceberg Version
ICEBERG_VERSION = "1.9.1"

def create_spark_session():
  """Create and configure Spark session for Snowflake Iceberg access."""
  spark = (
      SparkSession.builder
      .appName("SnowflakeIcebergReader")
      .master("local[*]")

# JAR Dependencies for Iceberg and Azure
      .config(
          "spark.jars.packages",
          f"org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:{ICEBERG_VERSION},"
          f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}"
          # for Azure storage, use the below package and comment above azure bundle
          # f"org.apache.iceberg:iceberg-azure-bundle:{ICEBERG_VERSION}"
      )

      # Iceberg SQL Extensions
      .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
      .config("spark.sql.defaultCatalog", CATALOG_NAME)

      # Horizon REST Catalog Configuration
      .config(f"spark.sql.catalog.{CATALOG_NAME}", "org.apache.iceberg.spark.SparkCatalog")
      .config(f"spark.sql.catalog.{CATALOG_NAME}.type", "rest")
      .config(f"spark.sql.catalog.{CATALOG_NAME}.uri", CATALOG_URI)
      .config(f"spark.sql.catalog.{CATALOG_NAME}.warehouse", CATALOG_NAME)
      .config(f"spark.sql.catalog.{CATALOG_NAME}.token", ACCESS_TOKEN)
      .config(f"spark.sql.catalog.{CATALOG_NAME}.scope", HORIZON_SESSION_ROLE)
      .config(f"spark.sql.catalog.{CATALOG_NAME}.client.region", REGION)

      # Required for vended credentials
      .config(f"spark.sql.catalog.{CATALOG_NAME}.header.X-Iceberg-Access-Delegation", "vended-credentials")
      .config("spark.sql.iceberg.vectorization.enabled", "false")
      .getOrCreate()
  )
  spark.sparkContext.setLogLevel("ERROR")
  return spark
```

Where:

- `<account_identifier>` is your Snowflake account identifier for the Snowflake account that contains the Iceberg tables that you
  want to access. To find this identifier, see [Supported external engines and catalogs](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-before-you-begin).
- `<your_access_token>` is your access token that you obtained. To obtain it, see [Step 3: Obtain an access token for authentication](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-generate-access-token).

  Note

  For External OAuth, alternatively, you can configure your connection to the engine with automatic token refresh instead of specifying
  an access token.
- `<database_name>` is the name of the database in your Snowflake account that contains Snowflake-managed Iceberg tables that you want to access.

  Note

  The `.warehouse` property in Spark expects your Snowflake *database* name, not your Snowflake warehouse name.
- `<role>` is the role in Snowflake that is configured with access to the Iceberg tables that you want to access. For example: DATA\_ENGINEER.

Important

By default, the code example is set up for Apache Iceberg™ tables stored on Amazon S3. If your Iceberg tables are stored on Azure Storage (ADLS),
perform the following steps:

> 1. Comment out the following line: `f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}"`
> 2. Uncomment the following line: `# f"org.apache.iceberg:iceberg-azure-bundle:{ICEBERG_VERSION}"`

#### Connect an external query engine with data policies enforced

- To connect with data protection policies enforced, see [Enforce data protection policies when querying Apache Iceberg™ tables from Apache Spark™](/user-guide/tables-iceberg-enforce-access-policies-spark-connector).

### Connect by using a programmatic access token (PAT)

Use one of the following configurations to connect:

- If you *don’t use* data protection policies with the Iceberg tables that you want to access, use the configuration [Connect an external query engine without enforcing data policies](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-pat-token-no-access-policies).
- If you *use* data protection policies with the Iceberg tables that you want to access, use the configuration [Connect an external query engine with data policies enforced](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-pat-token-access-policies).

#### Connect an external query engine without enforcing data policies

- To connect the external query engine to Iceberg tables by using a programmatic access token (PAT), use the following example code.

This code doesn’t enforce data protection policies:

Copy code

```
# Snowflake Horizon Catalog Configuration, change as per your environment

CATALOG_URI = "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog"
HORIZON_SESSION_ROLE = f"session:role:<role>"
CATALOG_NAME = "<database_name>" #provide in UPPER CASE

# Cloud Service Provider Region Configuration (where the Iceberg data is stored)
REGION = "eastus2"

# Paste the PAT you generated in Snowflake here
PAT_TOKEN = "<your_PAT_token>"

# Iceberg Version
ICEBERG_VERSION = "1.9.1"

def create_spark_session():
  """Create and configure Spark session for Snowflake Iceberg access."""
  spark = (
      SparkSession.builder
      .appName("SnowflakeIcebergReader")
      .master("local[*]")

# JAR Dependencies for Iceberg and Azure
      .config(
          "spark.jars.packages",
          f"org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:{ICEBERG_VERSION},"
          f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}"
          # for Azure storage, use the below package and comment above azure bundle
          # f"org.apache.iceberg:iceberg-azure-bundle:{ICEBERG_VERSION}"
      )

      # Iceberg SQL Extensions
      .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
      .config("spark.sql.defaultCatalog", CATALOG_NAME)

      # Horizon REST Catalog Configuration
      .config(f"spark.sql.catalog.{CATALOG_NAME}", "org.apache.iceberg.spark.SparkCatalog")
      .config(f"spark.sql.catalog.{CATALOG_NAME}.type", "rest")
      .config(f"spark.sql.catalog.{CATALOG_NAME}.uri", CATALOG_URI)
      .config(f"spark.sql.catalog.{CATALOG_NAME}.warehouse", CATALOG_NAME)
      .config(f"spark.sql.catalog.{CATALOG_NAME}.credential", PAT_TOKEN)
      .config(f"spark.sql.catalog.{CATALOG_NAME}.scope", HORIZON_SESSION_ROLE)
      .config(f"spark.sql.catalog.{CATALOG_NAME}.client.region", REGION)

      # Required for vended credentials
      .config(f"spark.sql.catalog.{CATALOG_NAME}.header.X-Iceberg-Access-Delegation", "vended-credentials")
      .config("spark.sql.iceberg.vectorization.enabled", "false")
      .getOrCreate()
  )
  spark.sparkContext.setLogLevel("ERROR")
  return spark
```

Where:

- `<account_identifier>` is your Snowflake account identifier for the Snowflake account that contains the Iceberg tables that you want
  to access. To find this identifier, see [Supported external engines and catalogs](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-before-you-begin).
- `<your_PAT_token>` is your PAT that you obtained. To obtain it, see [Step 3: Obtain an access token for authentication](#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-generate-access-token).
- `<role>` is the role in Snowflake that is configured with access to the Iceberg tables that you want to access. For example:
  DATA\_ENGINEER.
- `<database_name>` is the name of the database in your Snowflake account that contains Snowflake-managed Iceberg tables that you
  want to access.

  Note

  The `.warehouse` property in Spark expects your Snowflake *database* name, not your Snowflake warehouse name.

Important

By default, the code example is set up for Apache Iceberg™ tables stored on Amazon S3. If your Iceberg tables are stored on Azure Storage (ADLS),
perform the following steps:

> 1. Comment out the following line: `f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}"`
> 2. Uncomment the following line: `# f"org.apache.iceberg:iceberg-azure-bundle:{ICEBERG_VERSION}"`

#### Connect an external query engine with data policies enforced

- To connect with data protection policies enforced, see [Enforce data protection policies when querying Apache Iceberg™ tables from Apache Spark™](/user-guide/tables-iceberg-enforce-access-policies-spark-connector).

## Step 7: Access Iceberg tables

This section includes code examples for using Apache Spark™ to query and write to Iceberg tables.

### Query Iceberg tables

This section provides the following code examples for using Apache Spark™ to query Iceberg tables:

- Show namespaces
- Use namespaces
- Show tables
- Query a table

#### Show namespaces

Copy code

```
spark.sql("show namespaces").show()
```

#### Use namespace

Copy code

```
spark.sql("use namespace <your_schema_name_in_snowflake>")
```

#### Show tables

Copy code

```
spark.sql("show tables").show()
```

#### Query a table

Copy code

```
spark.sql("use namespace spark_demo")
spark.sql("select * from <your_table_name_in_snowflake>").show()
```

### Write to Iceberg tables

This section provides the following code examples for using Apache Spark™ to write to Iceberg tables:

- CREATE TABLE
- INSERT INTO <table>
- ALTER TABLE … ADD COLUMN
- UPDATE TABLE … WHERE
- DELETE TABLE … WHERE
- TRUNCATE TABLE
- RENAME TABLE
- DROP TABLE

#### CREATE TABLE

Copy code

```
spark.sql("CREATE TABLE MY_TABLE (COLUMN1 INT) USING ICEBERG").show();
```

#### INSERT INTO <table>

Copy code

```
spark.sql("INSERT INTO MY_TABLE VALUES (600)").show()
```

#### ALTER TABLE … ADD COLUMN

Copy code

```
spark.sql("ALTER TABLE MY_TABLE ADD COLUMN COLUMN2 INT").show()
```

#### UPDATE TABLE … WHERE

Copy code

```
spark.sql("UPDATE MY_TABLE SET COLUMN2 = 10 WHERE COLUMN1 = 100").show()
```

#### DELETE TABLE … WHERE

Copy code

```
spark.sql("DELETE FROM MY_TABLE WHERE COLUMN2 = 10").show()
```

#### TRUNCATE TABLE

Copy code

```
spark.sql("TRUNCATE TABLE MY_TABLE").show()
```

#### RENAME TABLE

Copy code

```
spark.sql("ALTER TABLE MY_TABLE RENAME TO MY_NEW_TABLE")
```

#### DROP TABLE

Copy code

```
spark.sql("DROP TABLE MY_TABLE")
```

## Considerations for accessing Iceberg tables with an external query engine

This section lists the considerations for accessing, querying, and writing to Iceberg tables with an external query engine.

Consider the following items when you access Iceberg tables with an external query engine:

- Iceberg

  - For tables in Snowflake:
    - Only Snowflake-managed Iceberg tables are supported.
- Listings:

  - Iceberg tables that you share through [auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment) aren’t
    accessible through the consumer account’s Horizon Iceberg REST Catalog API.
- Network and private connectivity:

  - Using network policies that are set at the user level isn’t supported with this feature.
  - For [Snowflake-managed network rules](/user-guide/network-rules#label-snowflake-managed-network-rules), egress IP addresses that are static aren’t supported.
  - Explicitly granting the Horizon Catalog endpoint access to your storage accounts isn’t supported. We recommend that you use private connectivity for
    secure connectivity from external engines to Horizon Catalog and from Horizon Catalog to your storage account.
- Clouds:

  - Commercial: This feature is only supported for Snowflake-managed Iceberg tables that are stored on Amazon S3, Google Cloud, or Microsoft Azure for
    all commercial cloud regions. S3-compatible non-AWS storage isn’t yet supported.
  - FedRAMP (Moderate): This feature is supported for Snowflake-managed Iceberg tables that are stored on FedRAMP (Moderate) deployments
    on AWS Commercial Gov (US) in the us-east-1 and us-west-2 regions.
  - For Iceberg tables stored on Amazon S3:

    - If you want to use SSE-KMS encryption, contact customer support or your account team for assistance with enabling access.
  - Reading and writing Iceberg v3 tables via the Horizon Iceberg REST Catalog API is supported for customer-managed and Snowflake-managed storage.
  - For Iceberg tables stored on Azure:

    - If you want to use Azure Virtual Network (VNet) for connectivity, contact customer support or your account team for assistance.

Consider the following items when you query (read) Iceberg tables with an external query engine:

- Iceberg

  - Querying the following tables isn’t supported:

    - Remote tables
    - Snowflake native tables
    - Externally managed Iceberg tables including Delta-based Iceberg tables and
      Snowflake-managed Iceberg tables that you loaded with data from Iceberg-compatible Parquet data files by using the COPY INTO table command
  - Reading Iceberg v2 and v3 tables is supported.
- Access control:

  - Tables protected by fine-grained data policies, such as masking and row access policies, can be accessed with external engines. For more
    information, see [Enforce data protection policies on Iceberg tables from external query engines](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies).
- Cloned and converted tables:

  - Reading and writing cloned or converted tables is not supported with vended credentials. To read these tables, use direct access to
    object storage.

Consider the following items when you write to Iceberg tables with an external query engine:

- Table operations:

  - You can’t specify a base location with your CREATE TABLE statement.

    When you create a Snowflake-managed table without specifying a base location, Snowflake constructs the following path for your table:
    `STORAGE_BASE_URL/database/schema/table_name.randomId/[data | metadata]/`
  - CREATE TABLE AS SELECT (CTAS) from an external engine is not supported.
  - Equality deletes aren’t supported.
  - Creating Iceberg tags and branches isn’t supported.
  - Writing to dynamic tables in Snowflake isn’t supported.
  - Writing to shared Iceberg tables isn’t supported.
  - Registering Iceberg tables isn’t supported.
- Maintenance operations:

  - You can’t roll back a table to a previous snapshot.
  - You can’t upgrade an Iceberg table from v2 to v3.
- Cloned and converted tables:

  - Writing to cloned or converted tables is not supported with vended credentials. To write to these tables, connect your external query
    engine directly to the object storage where your tables are stored.
  - You can’t write to an Iceberg table that was converted from externally managed to Snowflake managed.
- Streams:

  - On Iceberg v2 tables, deletes or updates that result in copy-on-write or merge-on-read operations can cause standard streams to represent
    an updated or relocated row as a DELETE record followed by an INSERT record for the same row.
