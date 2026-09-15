# Register a service connection

Feature — Generally Available

Not available in government regions.

This topic covers how to register your service connection credentials with Snowflake or your third-party service (for example, Apache Spark™).
The Snowflake Open Catalog administrator registers a service connection.

The example code in this topic shows how to register a service connection in Spark, and the example code is in PySpark.

## Prerequisites

Before you can register a service connection, you need to configure a service connection. For instructions, see [Configure a service connection](configure-service-connection).

## Register a service connection

The following example code is for registering a single service connection.

**Note**

> You can also register multiple service connections; see [Example 2: Register two service connections](#example-2-register-two-service-connections-s3).

### Parameters

| Parameter | Description |
| --- | --- |
| <catalog\_name> | Specifies the name of the catalog to connect to. <br /><br />**Important**:<br /><catalog\_name> is case sensitive. |
| <maven\_coordinate> | Specifies the Maven coordinate for your external cloud storage provider:<ul><li>**S3:** software.amazon.awssdk:bundle:2.20.160</li><li>**Cloud Storage (from Google):** org.apache.iceberg:iceberg-gcp-bundle:1.5.2</li><li>**Azure:** org.apache.iceberg:iceberg-azure-bundle:1.5.2</li></ul> If you don’t see this parameter, the correct value is already specified in the code sample. |
| <client\_id> | Specifies the client ID for the service principal to use. <br /><br />Enter the **Client ID** that you copied when you configured a new service connection. |
| <client\_secret> | Specifies the client secret for the service principal to use. <br /><br />Enter the **Secret** that you copied when you configured a new service connection. |
| <open\_catalog\_account\_identifier> | Specifies the account identifier for your Open Catalog account. <br /><br />Depending on the region and cloud platform for the account, this identifier might be the account locator by itself (for example, xy12345) or include additional segments. For more information, see [Using an account locator as an identifier](https://docs.snowflake.com/en/user-guide/admin-account-identifier#using-an-account-locator-as-an-identifier). |
| <principal\_role\_name> | Specifies the principal role that is granted to the service principal.<br /><br />To view this principal role, in Open Catalog, select the **Connections** page, select your service connection, and in the **Principal Details** dialog, refer to **Principal Roles.** |

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
    .config('spark.sql.catalog.opencatalog.credential','<client_id>:<client_secret>') \
    .config('spark.sql.catalog.opencatalog.warehouse','<catalog_name>') \
    .config('spark.sql.catalog.opencatalog.scope','PRINCIPAL_ROLE:<principal_role_name>') \
    .getOrCreate()
```

## Register a cross-region service connection (Amazon S3 only)

The following example code is for registering a service connection when the following is true:

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
    .config('spark.sql.catalog.opencatalog.credential','<client_id>:<client_secret>') \
    .config('spark.sql.catalog.opencatalog.warehouse','<catalog_name>') \
    .config('spark.sql.catalog.opencatalog.client.region','<target_s3_region>') \
    .config('spark.sql.catalog.opencatalog.scope','PRINCIPAL_ROLE:<principal_role_name>') \
    .getOrCreate()
```

### Parameters

| Parameter | Description |
| --- | --- |
| `<catalog_name>` | Specifies the name of the catalog to connect to.   **Important**: <catalog\_name> is case sensitive. |
| `<client_id>` | Specifies the client ID for the service principal to use. |
| `<client_secret>` | Specifies the client secret for the service principal to use. |
| `<open_catalog_account_identifier>` | Specifies the account identifier for your Open Catalog account. Depending on the region and cloud platform for the account, this identifier might be the account locator by itself (for example, `xy12345`) or include additional segments. For more information, see [Using an account locator as an identifier](https://docs.snowflake.com/en/user-guide/admin-account-identifier#using-an-account-locator-as-an-identifier). |
| `<target_s3_region>` | Specifies the region code where the S3 bucket containing your Apache Iceberg tables is located. For the region codes, see [AWS service endpoints](https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_region) and refer to the Region column in the table. |
| `<principal_role_name>` | Specifies the principal role that is granted to the service principal. |

Expand

Show lessSee more

## Examples

This section contains examples of registering a service connection in Spark.

- [Example 1: Register a single service connection (S3)](#example-1-register-a-single-service-connection-s3)
- [Example 2: Register two service connections (S3)](#example-2-register-two-service-connections-s3)
- [Example 3: Register a single service connection (Cloud Storage from Google)](#example-3-register-a-single-service-connection-cloud-storage-from-google)
- [Example 4: Register a single service connection (Azure)](#example-4-register-a-single-service-connection-azure)

### Example 1: Register a single service connection (S3)

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
    .config('spark.sql.catalog.opencatalog.credential','000000000000000000000000000=:1111111111111111111111111111111111111111111=') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .config('spark.sql.catalog.opencatalog.scope','PRINCIPAL_ROLE:data_engineer') \
    .getOrCreate()
```

### Example 2: Register two service connections (S3)

**Important**

> When registering multiple service connections, you must change the `opencatalog` instances in the code for the first connection to
> unique text in the code for each subsequent connection. For example, in the following code, the `opencatalog` instances for the first connection
> are changed to `opencatalog1` for the second connection:

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
    .config('spark.sql.catalog.opencatalog.credential','000000000000000000000000000=:1111111111111111111111111111111111111111111=') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .config('spark.sql.catalog.opencatalog.scope','PRINCIPAL_ROLE:data_scientist') \
    .config('spark.sql.catalog.opencatalog1', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.opencatalog1.type', 'rest') \
    .config('spark.sql.catalog.opencatalog1.uri','https://ab12345.snowflakecomputing.com/polaris/api/catalog') \
    .config('spark.sql.catalog.opencatalog1.header.X-Iceberg-Access-Delegation','vended-credentials') \
    .config('spark.sql.catalog.opencatalog1.credential','222222222222222222222222222=:3333333333333333333333333333333333333333333=') \
    .config('spark.sql.catalog.opencatalog1.warehouse','Catalog2') \
    .config('spark.sql.catalog.opencatalog1.scope','PRINCIPAL_ROLE:data_scientist') \
    .getOrCreate()
```

### Example 3: Register a single service connection (Cloud Storage from Google)

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
    .config('spark.sql.catalog.opencatalog.credential','000000000000000000000000000=:1111111111111111111111111111111111111111111=') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .config('spark.sql.catalog.opencatalog.scope','PRINCIPAL_ROLE:data_engineer') \
    .getOrCreate()
```

### Example 4: Register a single service connection (Azure)

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
    .config('spark.sql.catalog.opencatalog.credential','000000000000000000000000000=:1111111111111111111111111111111111111111111=') \
    .config('spark.sql.catalog.opencatalog.warehouse','Catalog1') \
    .config('spark.sql.catalog.opencatalog.scope','PRINCIPAL_ROLE:data_engineer') \
    .getOrCreate()
```

## Verify the connection to Open Catalog

To verify that Spark is connected to Open Catalog, list the namespaces for the catalog. For more information,
see [List namespaces](spark-code-examples#list-namespaces).
