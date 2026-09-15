# Enforce data protection policies when querying Apache Iceberg™ tables from Apache Spark™

This topic describes how to enforce data protection policies set on Apache Iceberg™ tables when accessed over Apache Spark™ through Snowflake
Horizon Catalog. To enforce data protection policies, you install the Snowflake Connector for Spark, *Spark connector*. For more information
about the Spark connector, see [Snowflake Connector for Spark](/user-guide/spark-connector).

The Spark connector supports querying tables that are protected by Snowflake policies by routing the query through Snowflake, which ensures efficient
use of compute and consistent enforcement. The Spark connector also supports performing write operations on tables that are protected by Snowflake policies by
routing the write through Snowflake.

Note

The Spark connector also supports directly querying Apache Iceberg tables without fine-grained data protection policies by using Spark
session compute through Snowflake Horizon Catalog.

## Workflow to enforce data protection policies when querying Iceberg tables from Spark

To enforce data protection policies when querying Iceberg tables from Spark, complete the following steps:

1. [Configure data protection policies](#label-enforce-access-policies-spark-configure-policies).
2. [Connect Spark with Snowflake Spark Connector to Iceberg tables](#label-connect-spark-enforce-access-policies-spark-connect-spark), which includes downloading the Snowflake Connector for Spark
   and connecting Spark to Iceberg tables through Snowflake Horizon Catalog.
3. [Query Iceberg tables](#label-connect-spark-enforce-access-policies-spark-query-tables).

## Supported data protection policies

The following data protection policies are supported:

- [Masking policies](/user-guide/security-column-intro)
- [Tag-based masking policies](/user-guide/tag-based-masking-policies)
- [Row access policies](/user-guide/security-row-intro)

Queries on tables that are protected with any other data policy result in an error.

## Prerequisites

- Spark 3.5.3 or higher is required to use this feature.
- Retrieve the following information:

  - The username of the Snowflake user who will query the tables
  - The name of the Snowflake database that contains the tables that you want to query
  - The name of the virtual warehouse in Snowflake to use for policy evaluation
- Retrieve the account identifier for your Snowflake account that contains the Iceberg tables that you want to query. For instructions,
  see [Account identifiers](/user-guide/admin-account-identifier). You specify this identifier when you
  [connect Spark to Iceberg tables with data access policies enforced](#label-connect-spark-enforce-access-policies-spark-connect-spark).

  Tip

  To get your account identifier by using SQL, run the following command:

  Copy code

  ```
  SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME();
  ```

## Step 1: Configure data protection policies

Important

If you already set data protection policies on the Iceberg tables that you want to query, proceed to the next step.

In this step, you configure data protection policies.

- To configure data protection policies, set data access policies on the Iceberg tables that you want to query:
  - To assign masking policies, see [Understanding Dynamic Data Masking](/user-guide/security-column-ddm-intro).
  - To assign tag-based masking policies, see [Tag-based masking policies](/user-guide/tag-based-masking-policies).
  - To assign row access policies, see [Understanding row access policies](/user-guide/security-row-intro).

## Step 2: Connect Spark with Snowflake Connector for Spark to Iceberg tables

In this step, you connect Spark to Iceberg tables through Horizon Catalog. With this
connection, you can query the tables by using Spark with the data protection policies enforced on the tables.

To Connect Spark with the Snowflake Connector for Spark (Spark connector) to Iceberg tables, you first download the Spark connector, and
then you connect Spark to Iceberg tables.

### Download the Snowflake Connector for Spark

To download 3.1.6 or a later version of the Snowflake Connector for Spark, follow the instructions in [Installing and Configuring the Spark Connector](/user-guide/spark-connector-install).

### Connect Spark to Iceberg tables

In this step, you connect Spark to Iceberg tables through Horizon Catalog. This connection includes configurations for you to use
the Snowflake Connector for Spark with Horizon catalog to query the tables that are protected by Snowflake data protection policies.

Note

If you’re using External OAuth or key-pair authentication, see
[Connect Spark to Iceberg tables by using External OAuth or key pair authentication](#label-connect-spark-enforce-access-policies-spark-external-oauth-key-pair-auth).

- To connect Spark to Iceberg tables by using a programmatic access token (PAT), use the following example PySpark code:

  Copy code

  ```
  from pyspark.sql import SparkSession

  # Snowflake Horizon Catalog Configuration, change as per your environment

  CATALOG_URI = "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog"
  ROLE = "<role>"
  HORIZON_SESSION_ROLE = f"session:role:{ROLE}"
  CATALOG_NAME = "<database_name>" #provide in UPPER CASE
  SF_URL= "<account_identifier>.snowflakecomputing.com"
  SF_USER = "<user_name>" #provide in UPPER CASE
  SF_PASSWORD = "<user_password>"
  SF_SCHEMA = "<schema_name>" #provide in UPPER CASE
  SF_WAREHOUSE = "<warehouse_name>" #provide in UPPER CASE

  # Cloud Service Provider Region Configuration (where the Iceberg data is stored)
  REGION = "<region_name>"

  # Paste the External Oauth Access token that you generated in Snowflake here
  ACCESS_TOKEN = "<your_access_token>"

  # Paste the PAT you generated in Snowflake here
  PAT_TOKEN = "<your_PAT_token>"

  # Iceberg Version
  ICEBERG_VERSION = "1.9.1"

  #Snowflake Connector for Spark
  DRIVER_VERSION = "3.24.0" # (or above)
  SNOWFLAKE_CONNECTOR_VERSION = "3.1.6"

  try:
   spark.stop()
  except:
   pass

    spark = (
     SparkSession.builder

     .master("local[*]")
  .config("spark.ui.port", "0")
     .config("spark.driver.bindAddress", "127.0.0.1")
     .config("spark.driver.host", "127.0.0.1")
     .config("spark.driver.port", "0")
     .config("spark.blockManager.port", "0")

  # JAR Dependencies for Iceberg, Azure and Snowflake Connector for Spark
     .config(
   "spark.jars.packages",
   f"org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:{ICEBERG_VERSION},"
   f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION},"

  # for Azure storage, use the below package and comment above azure bundle
         # f"org.apache.iceberg:iceberg-azure-bundle:{ICEBERG_VERSION}"
  # for Snowflake Connector for Spark
   f"net.snowflake:snowflake-jdbc:{DRIVER_VERSION},"
   f"net.snowflake:spark-snowflake_2.12:{SNOWFLAKE_CONNECTOR_VERSION}"

  )
     # Iceberg SQL Extensions
     .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
     .config("spark.sql.defaultCatalog", "horizoncatalog")
  .config("spark.sql.catalog.horizoncatalog", "org.apache.spark.sql.snowflake.catalog.SnowflakeFallbackCatalog")

    #Horizon REST Catalog Configuration
  .config(f"spark.sql.catalog.horizoncatalog.catalog-impl", "org.apache.iceberg.spark.SparkCatalog")
     .config(f"spark.sql.catalog.horizoncatalog.type", "rest")
     .config(f"spark.sql.catalog.horizoncatalog.uri", CATALOG_URI)
     .config(f"spark.sql.catalog.horizoncatalog.warehouse", CATALOG_NAME)
     .config(f"spark.sql.catalog.horizoncatalog.scope", HORIZON_SESSION_ROLE)
     .config(f"spark.sql.catalog.horizoncatalog.client.region", REGION)
     .config(f"spark.sql.catalog.horizoncatalog.credential", PAT_TOKEN)
  # for External Oauth use below and comment above configuration .token
  #.config(f"spark.sql.catalog.horizoncatalog.token", ACCESS_TOKEN)

  .config("spark.sql.catalog.horizoncatalog.io-impl","org.apache.iceberg.aws.s3.S3FileIO")
  # Enforcing policies using Snowflake Connector for Spark
  .config("spark.snowflake.sfURL", SF_URL)
  .config("spark.snowflake.sfUser", SF_USER)
  .config("spark.snowflake.sfPassword", SF_PASSWORD)
  # for External Oauth uncomment below and comment above configurations for user and password
  #.config("spark.snowflake.sfAuthenticator","oauth")
  #.config("spark.snowflake.sfToken",ACCESS_TOKEN)
  .config("spark.snowflake.sfDatabase", CATALOG_NAME)
  .config("spark.snowflake.sfSchema",SF_SCHEMA) # Optional
  .config("spark.snowflake.sfRole",ROLE)
  .config("spark.snowflake.sfWarehouse",SF_WAREHOUSE)

    # Required for vended credentials
   .config(f"spark.sql.catalog.horizoncatalog.header.X-Iceberg-Access-Delegation", "vended-credentials")
     .config("spark.sql.iceberg.vectorization.enabled", "false")
     .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
  ```

  Where:

  - `<account_identifier>` is your Snowflake account identifier for the Snowflake account that contains the Iceberg tables that you want
    to query. To find this identifier, see [Account identifiers](/user-guide/admin-account-identifier).
  - `<your_access_token>` is your access token that you obtained. To obtain an access token, see
    [Obtain access token for authentication](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-generate-access-token).

    Note

    For External OAuth, alternatively, you can configure your connection to the engine with automatic token refresh instead of specifying
    an access token.
  - `<database_name>` is the name of the database in your Snowflake account that contains Snowflake-managed Iceberg tables that you want to query.

    Note

    The following properties in Spark expect your Snowflake *database* name, not your Snowflake warehouse name:

    - `.warehouse`
    - `.sfDatabase`
  - `<role>` is the role in Snowflake that is configured with access to the Iceberg tables that you want to query. For example: DATA\_ENGINEER.
  - `<user_name>` is the user name that is used to access tables in Snowflake.
  - `<user_password>` is the password for the user accessing the tables.

    Note

    This password can be the programmatic access token (PAT)
    that you obtained for authentication, if applicable.
  - `<schema_name>` is the schema in Snowflake where the tables are stored. This is optional.
  - `<warehouse_name>` is the Snowflake warehouse (compute instance) name that you want to be used for evaluating policies.

  Important

  By default, the code example is set up for Apache Iceberg™ tables stored on Amazon S3. If your Iceberg tables are stored on Azure Storage (ADLS),
  perform the following steps:

  > 1. Comment out the following line: `f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}"`
  > 2. Uncomment the following line: `# f"org.apache.iceberg:iceberg-azure-bundle:{ICEBERG_VERSION}"`

#### Connect Spark to Iceberg tables by using External OAuth or key pair authentication

The previous code example shows the configuration for connecting by using a programmatic access token (PAT).

To connect
Spark to Iceberg tables by using External OAuth or key pair authentication, follow these steps to alter the previous code example:

1. For `<your_access_token>`, specify your access token for External OAuth or key-pair authentication.

   To obtain an access token, see [Step 3: Obtain an access token for authentication](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-generate-access-token).
2. Comment out the following line: `.config(f"spark.sql.catalog.{CATALOG_NAME}.credential", PAT_TOKEN)`
3. Uncomment the following line: `#.config(f"spark.sql.catalog.{CATALOG_NAME}.token", ACCESS_TOKEN)`

## Step 3: Query Iceberg tables by using Spark

Use Spark to read Iceberg tables that are protected by Snowflake data protection policies. Spark can automatically route queries of tables that
are protected by Snowflake policies through Snowflake to ensure consistent enforcement.

### Query a table

Copy code

```
spark.sql("SHOW NAMESPACES").show(truncate=False)
spark.sql("USE horizoncatalog.<schema_name>")
spark.sql("SHOW TABLES").show(truncate=False)
spark.sql("Select * from <your_table_name_in_snowflake>").show(truncate=False)
```

## Monitor a query for policy evaluation

To monitor query activity in Snowflake for queries that are routed from Spark to Snowflake for policy evaluation,
you can monitor query activity in your Snowflake account.

- To monitor query history in Snowflake, follow the instructions in [Monitor query activity with Query History](/user-guide/ui-snowsight-activity).

## Considerations for configuring data protection policies

Consider the following items when you configure data protection policies:

- Enforcing data protection policies on Iceberg tables that you query by using Spark is only supported when the following data protection policies
  are set on the tables:

  - Masking policies
  - Tag-based masking policies
  - Row access policies

  Queries on tables that are protected by all other policies will result in an error.
