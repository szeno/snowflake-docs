# Connect to an open-sharing catalog

This topic is for external consumers: people or workloads outside Snowflake that read data that a provider shares through
[Open Data Sharing](/user-guide/open-data-sharing). You connect by using any engine or tool that supports the Apache Iceberg™ REST
Catalog (IRC) API. This topic uses Apache Spark™ as an example.

The connection works the same way as accessing Iceberg tables with an external engine through Snowflake Horizon Catalog. For more
background, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

## Before you begin

Get the following information from the data provider:

- The connection values for the listing: the catalog name (`catalog`), catalog URI (`catalog_uri`), OAuth scope (`scope`), and OAuth
  token URI (`oauth_token_uri`). The provider retrieves these values for you by calling
  [SYSTEM$GET\_LISTING\_URL\_FOR\_EXTERNAL\_CONSUMER](/sql-reference/functions/system_get_listing_url_for_external_consumer). The scope is
  always `session:role:external`.
- Your credentials, which depend on the authentication method the provider configured:
  - **Workload identity federation (WIF):** The identity provider type (`AWS`, `AZURE`, `GCP`, or `OIDC`) and the identity the provider
    registered for you, such as an AWS IAM role ARN, an Azure managed identity, a Google Cloud service account, or an OIDC issuer and
    subject. Your workload must run as that identity.
  - **Programmatic access token (PAT):** The PAT secret.

## How authentication works

Your client exchanges a credential for a short-lived access token at the catalog’s OAuth token endpoint, then uses that access token
for catalog requests. Most IRC clients, including Spark, perform this exchange for you when you set the `credential` and `scope`
properties.

The token request uses the following parameters:

| Parameter | Value |
| --- | --- |
| `grant_type` | `client_credentials` |
| `scope` | `session:role:external` |
| `client_secret` | With a PAT, the PAT secret. With WIF, the OpenID Connect (OIDC) token from your identity provider. |

Expand

Show lessSee more

With WIF, you must also send the `X-Snowflake-Workload-Identity-Provider` header. Set it to the `TYPE` of the workload identity that
the provider registered for you: `AWS`, `AZURE`, `GCP`, or `OIDC`. These are the same `TYPE` values that
[ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity) uses.

The following example requests an access token with a PAT:

Copy code

```
curl -i --fail -X POST "<oauth_token_uri>" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=client_credentials' \
  --data-urlencode 'scope=session:role:external' \
  --data-urlencode 'client_secret=<pat_secret>'
```

The following example requests an access token with WIF:

Copy code

```
curl -i --fail -X POST "<oauth_token_uri>" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --header 'X-Snowflake-Workload-Identity-Provider: <provider>' \
  --data-urlencode 'grant_type=client_credentials' \
  --data-urlencode 'scope=session:role:external' \
  --data-urlencode 'client_secret=<oidc_token>'
```

Where:

- `<oauth_token_uri>` is the OAuth token URI that the provider gave you.
- `<pat_secret>` is the PAT secret that the provider gave you.
- `<provider>` is the `TYPE` of your workload identity: `AWS`, `AZURE`, `GCP`, or `OIDC`. For more information about workload
  identity types, see [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity).
- `<oidc_token>` is the OIDC token that your workload obtains from its identity provider at runtime. For background on how workloads
  obtain tokens from each identity provider, see [Workload identity federation](/user-guide/workload-identity-federation).

## Connect with Apache Spark™

Choose the example that matches your authentication method. Both examples set the following:

- `spark.sql.iceberg.vectorization.enabled` to `false`, which is required to read Open Data Sharing tables.
- The Iceberg bundle for the cloud that hosts the listing. The examples use `iceberg-aws-bundle`. If the provider’s listing is served
  from a Microsoft Azure region, use `org.apache.iceberg:iceberg-azure-bundle` instead.

WIFPAT

Pass the OIDC token from your identity provider as the credential, and add the `X-Snowflake-Workload-Identity-Provider` header.
Because the token is short-lived, fetch it at runtime when you create the Spark session.

Copy code

```
from pyspark.sql import SparkSession

CATALOG_URI = "<catalog_uri>"
CATALOG_NAME = "<catalog_name>"
PROVIDER = "<provider>"  # AWS, AZURE, GCP, or OIDC
ICEBERG_VERSION = "1.9.1"

# Fetch the OIDC token from your identity provider at runtime
OIDC_TOKEN = "<oidc_token>"

spark = (
    SparkSession.builder
    .appName("OpenDataSharingWIF")
    .config(
        "spark.jars.packages",
        f"org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:{ICEBERG_VERSION},"
        # For listings served from Azure, use iceberg-azure-bundle instead
        f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}",
    )
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.iceberg.vectorization.enabled", "false")
    .config("spark.sql.defaultCatalog", CATALOG_NAME)
    .config(f"spark.sql.catalog.{CATALOG_NAME}", "org.apache.iceberg.spark.SparkCatalog")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.type", "rest")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.uri", CATALOG_URI)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.warehouse", CATALOG_NAME)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.credential", OIDC_TOKEN)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.scope", "session:role:external")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.header.X-Snowflake-Workload-Identity-Provider", PROVIDER)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.header.X-Iceberg-Access-Delegation", "vended-credentials")
    .getOrCreate()
)

spark.sql("SHOW NAMESPACES").show()
```

Pass the PAT secret as the credential.

Copy code

```
from pyspark.sql import SparkSession

CATALOG_URI = "<catalog_uri>"
CATALOG_NAME = "<catalog_name>"
PAT_SECRET = "<pat_secret>"
ICEBERG_VERSION = "1.9.1"

spark = (
    SparkSession.builder
    .appName("OpenDataSharingPAT")
    .config(
        "spark.jars.packages",
        f"org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:{ICEBERG_VERSION},"
        # For listings served from Azure, use iceberg-azure-bundle instead
        f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}",
    )
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.iceberg.vectorization.enabled", "false")
    .config("spark.sql.defaultCatalog", CATALOG_NAME)
    .config(f"spark.sql.catalog.{CATALOG_NAME}", "org.apache.iceberg.spark.SparkCatalog")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.type", "rest")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.uri", CATALOG_URI)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.warehouse", CATALOG_NAME)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.credential", PAT_SECRET)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.scope", "session:role:external")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.header.X-Iceberg-Access-Delegation", "vended-credentials")
    .getOrCreate()
)

spark.sql("SHOW NAMESPACES").show()
```

Where:

- `<catalog_uri>` and `<catalog_name>` are the catalog URI and catalog name that the provider gave you.
- `<provider>` is the `TYPE` of your workload identity: `AWS`, `AZURE`, `GCP`, or `OIDC`.
- `<oidc_token>` is the OIDC token that your workload obtains from its identity provider at runtime.
- `<pat_secret>` is the PAT secret that the provider gave you.

After you connect, query the shared tables:

Copy code

```
spark.sql("SHOW TABLES IN <schema_name>").show()
spark.sql("SELECT * FROM <schema_name>.<table_name> LIMIT 10").show()
```

Shared data is read-only. Write operations aren’t supported.
