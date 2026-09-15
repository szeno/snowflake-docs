# Connect to Snowflake Open Catalog with External OAuth

Feature — Generally Available

Not available in government regions.

This topic describes how to connect to Snowflake Open Catalog with External OAuth using a client application.

The example code in this topic shows how to connect using Apache Spark™, and the example code is in PySpark.

Note

If you’re using Snowflake to query Open Catalog-managed tables, you can create a catalog integration for Snowflake that uses External OAuth.
For more information, see [CREATE CATALOG INTEGRATION (Snowflake Open Catalog)](https://docs.snowflake.com/en/sql-reference/sql/create-catalog-integration-open-catalog)
in the Snowflake documentation.

## Prerequisites

Before you can connect to Open Catalog with External OAuth, you need to configure External OAuth in Open Catalog. For
instructions, see [Configure External OAuth in Snowflake Open Catalog](external-oauth-configure).

## Connect with Open Catalog by using automatic refresh token (Preferred method)

Use this method to connect by using an automatic refresh token so you don’t have to manually refresh the token.

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,<maven_coordinate>') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://<open_catalog_account_identifier>.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.warehouse','<catalog_name>') \
    .config('spark.sql.catalog.opencatalog.rest.auth.type','oauth2') \
    .config('spark.sql.catalog.opencatalog.oauth2-server-uri','<oauth2_server_uri>') \
    .config('spark.sql.catalog.opencatalog.credential','<oauth_client_id>:<oauth_client_secret>') \
    .config('spark.sql.catalog.opencatalog.scope','SESSION:ROLE:<custom_role>') \
    .config('spark.sql.catalog.opencatalog.audience','https://<open_catalog_account_identifier>.snowflakecomputing.com') \
    .getOrCreate()
```

### Parameters

| Parameter | Description |
| --- | --- |
| `<catalog_name>` | Specifies the name of the catalog to connect to.   **Important**: <catalog\_name> is case sensitive. |
| `<maven_coordinate>` | Specifies the Maven coordinate for your external cloud storage provider:  - **S3:** software.amazon.awssdk:bundle:2.20.160 - **Cloud Storage (from Google):** org.apache.iceberg:iceberg-gcp-bundle:1.5.2 - **Azure:** org.apache.iceberg:iceberg-azure-bundle:1.5.2  If you don’t see this parameter, the correct value is already specified in the code sample. |
| `<open_catalog_account_identifier>` | Specifies the account identifier for your Open Catalog account.   Depending on the region and cloud platform for the account, this identifier might be the account locator by itself (for example, `xy12345`) or include additional segments. For more information, see [Using an account locator as an identifier](https://docs.snowflake.com/en/user-guide/admin-account-identifier#using-an-account-locator-as-an-identifier). |
| `<oauth2_server_uri>` | Your OAuth2 server URI. |
| `<oauth_client_id>` | Your OAuth2 client ID. |
| `<oauth_client_secret>` | Your OAuth2 client secret. |
| `<custom_role>` | The name of the custom role in Open Catalog whose privileges you want to grant to the service principal. |

Expand

Show lessSee more

## Connect with Open Catalog by using an access token

If needed, you can connect with Open Catalog by using an access token. However, the access token will expire and you’ll need to manually
refresh it. Alternatively, you can [connect by using an automatic refresh token](#connect-with-open-catalog-by-using-automatic-refresh-token-preferred-method).

The following example code is for connecting with Open Catalog by using Spark.

### Parameters

| Parameter | Description |
| --- | --- |
| `<catalog_name>` | Specifies the name of the catalog to connect to.   **Important**: <catalog\_name> is case sensitive. |
| `<maven_coordinate>` | Specifies the Maven coordinate for your external cloud storage provider:  - **S3:** software.amazon.awssdk:bundle:2.20.160 - **Cloud Storage (from Google):** org.apache.iceberg:iceberg-gcp-bundle:1.5.2 - **Azure:** org.apache.iceberg:iceberg-azure-bundle:1.5.2  If you don’t see this parameter, the correct value is already specified in the code sample. |
| `<access_token>` | Specifies the access token for the client application to use.   Enter the [access token that you generated when you configured External OAuth in Open Catalog](external-oauth-configure#optional-step-9-generate-the-access-token). |
| `<open_catalog_account_identifier>` | Specifies the account identifier for your Open Catalog account.   Depending on the region and cloud platform for the account, this identifier might be the account locator by itself (for example, `xy12345`) or include additional segments. For more information, see [Using an account locator as an identifier](https://docs.snowflake.com/en/user-guide/admin-account-identifier#using-an-account-locator-as-an-identifier). |

Expand

Show lessSee more

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,<maven_coordinate>') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://<open_catalog_account_identifier>.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.token','<access_token>') \
    .config('spark.sql.catalog.opencatalog.warehouse','<catalog_name>') \
    .getOrCreate()
```

## Connect with a cross-region connection (Amazon S3 only)

The following example code is for connecting to Open Catalog when the following is true:

- Your Open Catalog account is hosted on Amazon S3.
- Your external storage provider is Amazon S3.
- Your Open Catalog account is hosted in an S3 region that is different from the S3 region where the storage bucket containing your Apache Iceberg™ tables is located.

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,software.amazon.awssdk:bundle:2.20.160') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://<open_catalog_account_identifier>.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.token','<access_token>') \
    .config('spark.sql.catalog.opencatalog.warehouse','<catalog_name>') \
    .config('spark.sql.catalog.opencatalog.client.region','<target_s3_region>') \
    .getOrCreate()
```

### Parameters

| Parameter | Description |
| --- | --- |
| `<catalog_name>` | Specifies the name of the catalog to connect to.   **Important**: <catalog\_name> is case sensitive. |
| `<access_token>` | Specifies the access token for the client application to use.   Enter the [access token that you generated when you configured External OAuth in Open Catalog](external-oauth-configure#optional-step-9-generate-the-access-token). |
| `<open_catalog_account_identifier>` | Specifies the account identifier for your Open Catalog account. Depending on the region and cloud platform for the account, this identifier might be the account locator by itself (for example, `xy12345`) or include additional segments. For more information, see [Using an account locator as an identifier](https://docs.snowflake.com/en/user-guide/admin-account-identifier#using-an-account-locator-as-an-identifier). |
| `<target_s3_region>` | Specifies the region code where the S3 bucket containing your Apache Iceberg tables is located. For the region codes, see [AWS service endpoints](https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_region) and refer to the Region column in the table. |

Expand

Show lessSee more

## Examples

This section contains examples of connecting to Open Catalog using Spark:

- [Example 1: Connect (S3)](#example-1-connect-s3)
- [Example 2: Connect (Cloud Storage from Google)](#example-2-connect-cloud-storage-from-google)
- [Example 3: Connect (Azure)](#example-3-connect-azure)

### Example 1: Connect (S3)

See:

- [Connect by using automatic refresh (S3)](#connect-by-using-automatic-refresh-s3)
- [Connect by using access token (S3)](#connect-by-using-access-token-s3)

#### Connect by using automatic refresh (S3)

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,software.amazon.awssdk:bundle:2.20.160') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://ab12345.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .config('spark.sql.catalog.opencatalog.rest.auth.type','oauth2') \
    .config('spark.sql.catalog.opencatalog.oauth2-server-uri','your-tenant.region.auth0.com') \
    .config('spark.sql.catalog.opencatalog.credential','11111111111111111111111111111111:222222222222222222222222222222222222222222222222222222222222222222') \
    .config('spark.sql.catalog.opencatalog.scope','SESSION:ROLE:DATA_ENG') \
    .config('spark.sql.catalog.opencatalog.audience','https://ab12345.snowflakecomputing.com') \
    .getOrCreate()
```

#### Connect by using access token (S3)

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,software.amazon.awssdk:bundle:2.20.160') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://ab12345.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.token','0000000000000000000000000001111111111111111111111111111111111111111111') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .getOrCreate()
```

### Example 2: Connect (Cloud Storage from Google)

See:

- [Connect by using automatic refresh (Cloud Storage from Google)](#connect-by-using-automatic-refresh-cloud-storage-from-google)
- [Connect by using access token (Cloud Storage from Google)](#connect-by-using-access-token-cloud-storage-from-google)

#### Connect by using automatic refresh (Cloud Storage from Google)

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,org.apache.iceberg:iceberg-gcp-bundle:1.5.2') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://ab12345.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .config('spark.sql.catalog.opencatalog.rest.auth.type','oauth2') \
    .config('spark.sql.catalog.opencatalog.oauth2-server-uri','your-tenant.region.auth0.com') \
    .config('spark.sql.catalog.opencatalog.credential','11111111111111111111111111111111:222222222222222222222222222222222222222222222222222222222222222222') \
    .config('spark.sql.catalog.opencatalog.scope','SESSION:ROLE:DATA_ENG') \
    .config('spark.sql.catalog.opencatalog.audience','https://ab12345.snowflakecomputing.com') \
    .getOrCreate()
```

#### Connect by using access token (Cloud Storage from Google)

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,org.apache.iceberg:iceberg-gcp-bundle:1.5.2') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://ab12345.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.token','0000000000000000000000000001111111111111111111111111111111111111111111') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .getOrCreate()
```

### Example 3: Connect (Azure)

See:

- [Connect by using automatic refresh (Azure)](#connect-by-using-automatic-refresh-azure)
- [Connect by using access token (Azure)](#connect-by-using-access-token-azure)

#### Connect by using automatic refresh (Azure)

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,org.apache.iceberg:iceberg-azure-bundle:1.5.2') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://ab12345.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .config('spark.sql.catalog.opencatalog.rest.auth.type','oauth2') \
    .config('spark.sql.catalog.opencatalog.oauth2-server-uri','your-tenant.region.auth0.com') \
    .config('spark.sql.catalog.opencatalog.credential','11111111111111111111111111111111:222222222222222222222222222222222222222222222222222222222222222222') \
    .config('spark.sql.catalog.opencatalog.scope','SESSION:ROLE:DATA_ENG') \
    .config('spark.sql.catalog.opencatalog.audience','https://ab12345.snowflakecomputing.com') \
    .getOrCreate()
```

#### Connect by using access token (Azure)

Copy code

```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('iceberg_lab') \
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.1,org.apache.iceberg:iceberg-azure-bundle:1.5.2') \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.defaultCatalog', 'opencatalog') \
    .config('spark.sql.catalog.opencatalog', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog.type', 'rest') \
    .config('spark.sql.catalog.opencatalog.uri','https://ab12345.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog.token','0000000000000000000000000001111111111111111111111111111111111111111111') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .getOrCreate()
```

## Verify the connection to Open Catalog

To verify that Spark is connected to Open Catalog, list the namespaces for the catalog. For more information,
see [List namespaces](spark-code-examples#list-namespaces).
