# Using CoCo CLI with other data platforms

CoCo CLI supports plugins that extend its capabilities to external data platforms. Each platform plugin adds
domain-specific skills that you can use through natural language prompts.

## Prerequisites

- [CoCo CLI](/user-guide/cortex-code/cortex-code-cli) installed and authenticated to Snowflake.

## AWS Glue

CoCo includes built-in skills for both preparing AWS-side Iceberg infrastructure and creating a Snowflake
catalog integration with AWS Glue Data Catalog. You can use these skills end-to-end: from raw data in S3 to
queryable Iceberg tables in Snowflake, or independently if your data is already registered in Glue.

Note

These are built-in capabilities. No plugin needs to be enabled: the skills are available in every CoCo
session.

### Preparing data in AWS Glue

Use this skill to prepare the AWS side of an Iceberg pipeline: verify credentials, discover S3 data, create a Glue
database and crawler, validate schemas, and convert parquet or CSV data to Iceberg format using Athena. At the end of
this workflow, CoCo can hand off directly to the Snowflake catalog integration skill.

#### Capabilities

| Capability | Description | Example Prompt |
| --- | --- | --- |
| AWS authentication | Verify AWS CLI credentials, identify the caller identity, and list accessible S3 buckets | “Check my AWS credentials and show me my S3 buckets” |
| S3 data discovery | Inventory source files in S3, identify formats, and validate directory structure for Athena compatibility | “What data files are in my S3 bucket and are they structured for Athena?” |
| Glue database & crawler setup | Create or reuse a Glue database and IAM crawler role, detect Lake Formation mode, run the crawler | “Set up a Glue database and crawler for my S3 data” |
| Lake Formation grants | Detect LF mode and grant the crawler role the minimum required permissions on the database and S3 location | “My Glue crawler is failing with a Lake Formation permission error — help me fix it” |
| Schema discovery & validation | List discovered tables, compare column types, fix duplicate partition columns from Snowflake-exported parquet | “Validate the schemas for the tables my crawler discovered” |
| Parquet-to-Iceberg conversion | Convert parquet, CSV, or JSON tables to Iceberg format using Athena CTAS or Glue Spark | “Convert my parquet tables to Iceberg using Athena” |
| Iceberg table registration | Register existing Iceberg tables in Glue Data Catalog with correct `StorageDescriptor` and metadata location | “Register my existing Iceberg tables in Glue” |
| Crawler cleanup | Delete the crawler after schema discovery to avoid accidental re-crawls and ongoing cost | “Delete the Glue crawler now that schema discovery is done” |

Expand

Show lessSee more

#### AWS side prerequisites

- AWS CLI installed and configured. If it is not installed, CoCo provides installation instructions.
- An AWS profile with sufficient permissions to create Glue databases, crawlers, and IAM roles, and to run Athena
  queries. See the minimum operator policy below.
- Athena engine version 3 (Trino-based) workgroup if you are converting data to Iceberg format. CoCo checks
  the workgroup version and prompts you to upgrade if needed.

The following IAM policy covers the minimum permissions needed to run this skill:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "GlueSetup",
      "Effect": "Allow",
      "Action": [
        "glue:CreateDatabase", "glue:GetDatabase", "glue:GetDatabases",
        "glue:CreateCrawler", "glue:StartCrawler", "glue:GetCrawler",
        "glue:DeleteCrawler",
        "glue:GetTable", "glue:GetTables", "glue:UpdateTable"
      ],
      "Resource": "*"
    },
    {
      "Sid": "IAMRoleCreation",
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole", "iam:AttachRolePolicy", "iam:PutRolePolicy",
        "iam:GetRole", "iam:ListAttachedRolePolicies", "iam:PassRole"
      ],
      "Resource": "arn:aws:iam::<account-id>:role/<crawler-role-name>"
    },
    {
      "Sid": "S3Access",
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets", "s3:GetBucketLocation",
        "s3:ListBucket", "s3:GetObject",
        "s3:PutObject", "s3:DeleteObject", "s3:CreateBucket"
      ],
      "Resource": [
        "arn:aws:s3:::<source-bucket>",
        "arn:aws:s3:::<source-bucket>/*",
        "arn:aws:s3:::<athena-results-bucket>",
        "arn:aws:s3:::<athena-results-bucket>/*"
      ]
    },
    {
      "Sid": "AthenaExecution",
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution", "athena:GetQueryExecution",
        "athena:GetWorkGroup", "athena:ListWorkGroups"
      ],
      "Resource": "*"
    },
    {
      "Sid": "LakeFormation",
      "Effect": "Allow",
      "Action": [
        "lakeformation:GetDataLakeSettings",
        "lakeformation:GrantPermissions",
        "lakeformation:ListResources"
      ],
      "Resource": "*"
    }
  ]
}
```

If you already have a crawler IAM role, omit the `IAMRoleCreation` block. If Lake Formation is not enabled in
your account, omit the `LakeFormation` block.

#### Getting started

Start a CoCo session. CoCo asks for your AWS CLI profile and region before running any commands.

If your data is already in Iceberg format in S3 and you want to register it in Glue:

```
Register my Iceberg tables in AWS Glue Data Catalog
```

If your data is in parquet, CSV, or JSON and needs converting:

```
Set up a Glue database and convert my parquet data to Iceberg using Athena
```

To run individual phases:

```
Check my AWS credentials and list my S3 buckets
```

```
Create a Glue crawler for s3://my-bucket/data/ and run it
```

```
Validate the schemas for the tables my Glue crawler discovered
```

```
Convert my Glue external tables to Iceberg using Athena CTAS
```

At the end of AWS setup, CoCo asks whether you want to continue with Snowflake catalog integration.
If yes, it passes all collected variables (account ID, region, Glue database name, IAM role ARN, table names)
directly to the catalog integration skill.

#### Troubleshooting

AWS credentials expired
:   **Symptom:** Commands fail with `ExpiredTokenException` or `ExpiredToken`.

    **Solution:** Run `aws sso login --profile <profile>` to refresh your session, or run
    `aws configure --profile <profile>` to reconfigure credentials.

Lake Formation permission error on crawler
:   **Symptom:** The Glue crawler fails with
    `Insufficient Lake Formation permission(s): Required Describe on <database>`.

    **Solution:** Lake Formation is active in your account. The crawler IAM role needs explicit LF grants on the Glue
    database. Use the prompt `My Glue crawler is failing with a Lake Formation permission error` and CoCo
    detects whether LF is in restrictive or IAM compatibility mode and generates the correct `grant-permissions`
    commands.

Tables not discovered correctly after crawling Iceberg data
:   **Symptom:** The crawler creates entries for metadata files (`metadata/`, `*.avro`) instead of the actual
    Iceberg tables, or table names don’t match expectations.

    **Solution:** The standard S3 Glue crawler does not natively recognize Iceberg format. Use the prompt
    `Register my existing Iceberg tables in Glue` to bypass the crawler and register tables directly with the
    correct `table_type = ICEBERG` parameter and metadata location.

Athena CTAS fails with `HIVE_BAD_DATA`
:   **Symptom:** Parquet-to-Iceberg conversion fails with a type mismatch error.

    **Solution:** The source table has column types that Athena can’t implicitly cast. CoCo re-generates the
    CTAS statement with explicit `CAST()` expressions for the affected columns. You can also ask
    `Switch to Glue Spark for the conversion` to use the `add_files` approach instead of Athena.

Athena backtick syntax error
:   **Symptom:** CTAS or SELECT queries fail with `SYNTAX_ERROR: backquoted identifiers are not supported`.

    **Solution:** Athena’s Trino engine (v3) uses double quotes for identifiers, not backticks. CoCo
    automatically uses the correct quoting in generated SQL.

Duplicate partition column error
:   **Symptom:** Athena queries on a partitioned table fail with a duplicate column error after crawling.

    **Solution:** This occurs when Snowflake-exported parquet files include the partition column both inside the
    file and in the Hive directory path (`column=value/`). Use the prompt
    `Fix duplicate partition columns in my Glue table` and CoCo runs `aws glue update-table` to remove
    the duplicate from `StorageDescriptor.Columns`.

### Snowflake catalog integration

Use this skill to create a Snowflake catalog integration for AWS Glue Data Catalog, configure access delegation,
and query Iceberg tables registered in Glue directly from Snowflake using the Iceberg REST Catalog (IRC) protocol.

#### Capabilities

| Capability | Description | Example Prompt |
| --- | --- | --- |
| Catalog integration setup | Create a Snowflake catalog integration for AWS Glue Data Catalog using public connectivity or AWS PrivateLink | “Set up a catalog integration for my AWS Glue Data Catalog” |
| Access delegation | Configure catalog-vended credentials (Lake Formation) or external volume credentials for S3 data access | “Help me choose between vended credentials and external volume for Glue access” |
| IAM trust policy | Retrieve the Snowflake IAM user ARN and external ID, then configure the AWS trust policy | “What trust policy do I need to add to my IAM role for Snowflake?” |
| PrivateLink connectivity | Provision an outbound PrivateLink endpoint and create the catalog integration for private connectivity | “Set up a private Glue catalog integration using PrivateLink” |
| Verification | Test the catalog integration by listing namespaces and tables from Glue Data Catalog | “Verify my Glue catalog integration and list available tables” |
| Troubleshooting | Diagnose and fix connection errors, IAM permission issues, Lake Formation access failures, and PrivateLink problems | “My Glue catalog integration is returning a 403 error — help me fix it” |

Expand

Show lessSee more

#### Snowflake prerequisites

**Snowflake**:

- `ACCOUNTADMIN` role, or explicit grants for `CREATE INTEGRATION` and `CREATE EXTERNAL VOLUME` on the account.
- Business Critical Edition or higher if you are using PrivateLink connectivity.

**AWS**:

- An AWS account with Glue Data Catalog configured and Iceberg tables registered.
- An IAM role that Snowflake can assume to access Glue and S3.
- Lake Formation enabled and configured if you are using catalog-vended credentials (recommended).

#### Getting started

Start a CoCo session and use natural language to trigger the skill:

```
Set up a catalog integration for my AWS Glue Data Catalog
```

CoCo walks you through the setup one step at a time, collecting your AWS account ID, region, IAM role ARN,
access delegation mode, and connectivity type before generating the SQL.

To verify an existing integration:

```
Verify my Glue catalog integration
```

To troubleshoot a failing integration:

```
My Glue catalog integration returns an error — help me diagnose it
```

#### Authentication

The Glue catalog integration uses AWS SigV4 authentication. Snowflake assumes an IAM role in your AWS account to
interact with Glue and S3.

During setup, CoCo generates the `CREATE CATALOG INTEGRATION` SQL with the role ARN you provide, then
retrieves the Snowflake IAM user ARN and external ID. You add those values to your IAM role’s trust policy to
authorize the connection.

#### Troubleshooting

Trust relationship not configured
:   **Symptom:** Verification returns an `Access denied` or `InvalidClientTokenId` error.

    **Solution:** Run `DESC CATALOG INTEGRATION <name>` to retrieve the Snowflake IAM user ARN and external ID, then
    add them to your IAM role’s trust policy in the AWS console.

External ID mismatch
:   **Symptom:** Verification fails with an authentication error even though the trust policy exists.

    **Solution:** Re-run `DESC CATALOG INTEGRATION <name>` to get the current external ID and update the trust policy
    condition to match exactly.

Lake Formation access denied
:   **Symptom:** Tables are visible but queries return a `403 Forbidden` or Lake Formation permission error.

    **Solution:** Grant the IAM role `SELECT` permission on the Glue database and tables in the Lake Formation console.

PrivateLink endpoint not available
:   **Symptom:** `CREATE CATALOG INTEGRATION` with `CATALOG_API_TYPE = AWS_PRIVATE_GLUE` fails with a connectivity
    error.

    **Solution:** Run `SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT('com.amazonaws.<region>.glue', 'glue.&lt;region&gt;.amazonaws.com')` to provision the endpoint, wait for it to become available, then retry.

Cross-region PrivateLink not supported
:   **Symptom:** PrivateLink provisioning fails when your Snowflake account and Glue Data Catalog are in different
    regions.

    > **Solution:** Use public connectivity, or ensure your Snowflake account and Glue Data Catalog are in the same AWS
    > region. AWS does not support cross-region PrivateLink for the Glue service.

## Databricks

CoCo provides a built-in Databricks plugin with skills for managing workspaces, browsing Unity Catalog,
building ETL pipelines, deploying bundles, diagnosing performance, optimizing costs, and more.

### Capabilities

| Capability | Description | Example Prompt |
| --- | --- | --- |
| CLI Setup & Auth | Install the Databricks CLI and authenticate to your workspace using OAuth or a personal access token | “Help me install the Databricks CLI and authenticate to my workspace” |
| Unity Catalog | Browse catalogs, schemas, tables, and volumes in your Databricks workspace | “List all catalogs in my Databricks workspace” |
| Cluster & Job Management | List clusters, inspect job runs, view failures, and manage compute resources | “Show me recent job runs that failed” |
| PySpark ETL Pipelines | Build medallion-architecture ETL pipelines with PySpark notebooks that read and write to Delta tables | “Build a medallion ETL pipeline that reads and writes silver/gold tables” |
| dbt on Databricks | Create dbt projects with staging and marts layers, configured for Databricks and deployed with bundles | “Create a dbt project with staging and marts layers deployed via DAB” |
| Automation Bundles (DAB) | Initialize and deploy Databricks Asset Bundles with scheduled jobs, pipelines, and configuration | “Initialize a Databricks bundle project with a scheduled job that runs daily” |
| Local Testing | Generate pytest unit tests for PySpark notebooks with mocked dbutils and SparkSession | “Generate pytest unit tests for my PySpark notebook that mock dbutils and SparkSession” |
| Spark Performance | Diagnose slow Spark jobs, identify spill, skew, and shuffle bottlenecks, and recommend fixes | “My Spark job is slow and spilling to disk – help me diagnose and fix it” |
| Cost Optimization | Audit Databricks compute spend, identify waste, and recommend right-sizing and policy changes | “Audit my Databricks compute costs and recommend optimizations” |
| Notebook Refactoring | Refactor monolithic notebooks into modular Python packages with thin orchestrator notebooks | “Refactor my large notebook into modular Python packages with thin orchestrator notebooks” |
| Databricks SQL | Create and manage materialized views, use AI functions, and work with SQL warehouses | “Help me create a materialized view and use AI functions in Databricks SQL” |

Expand

Show lessSee more

### Databricks prerequisites

- A Databricks workspace with API access enabled.
- Workspace admin or sufficient permissions for the operations you want to perform.
- The Databricks CLI is installed automatically on first use if not already present.

### Enabling the Databricks plugin

Enable the plugin and start a new CoCo session:

Copy code

```
cortex plugin enable databricks
cortex
```

After enabling, Databricks skills are available in all future sessions until you disable the plugin.

To disable the plugin:

Copy code

```
cortex plugin disable databricks
```

### Getting started

After enabling the plugin, start a CoCo session and set up your connection:

```
Help me install the Databricks CLI and authenticate to my workspace
```

Once connected, explore your environment:

```
List all catalogs in my Databricks workspace
```

```
List my Databricks clusters
```

```
Show me recent job runs that failed
```

Then try more advanced workflows:

```
Build a medallion ETL pipeline that reads and writes silver/gold tables
```

```
Create a dbt project with staging and marts layers deployed via DAB
```

```
Initialize a Databricks bundle project with a scheduled job that runs daily
```

```
Generate pytest unit tests for my PySpark notebook that mock dbutils and SparkSession
```

```
My Spark job is slow and spilling to disk -- help me diagnose and fix it
```

```
Audit my Databricks compute costs and recommend optimizations
```

```
Refactor my large notebook into modular Python packages with thin orchestrator notebooks
```

```
Help me create a materialized view and use AI functions in Databricks SQL
```

### Authentication

The Databricks plugin uses the Databricks CLI’s authentication. You can authenticate using OAuth (recommended) or a
personal access token.

OAuth (recommended)
:   Run the following command and follow the browser prompts:

    Copy code

    ```
    databricks auth login --host https://your-workspace.cloud.databricks.com
    ```

    This creates a reusable OAuth token stored locally. CoCo uses it automatically.

Personal access token
:   Set the following environment variables before starting CoCo:

    Copy code

    ```
    export DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
    export DATABRICKS_TOKEN=your-personal-access-token
    ```

### Troubleshooting

Plugin not found
:   **Symptom:** `cortex plugin enable databricks` reports that the plugin doesn’t exist.

    **Solution:** Update CoCo CLI to the latest version. The Databricks plugin ships with CoCo starting
    from version 1.0.75.

Authentication failures
:   **Symptom:** Operations return 401 or 403 errors.

    **Solution:** Try the following steps:

    - Run `databricks auth login` again to refresh your OAuth token.
    - Verify that your personal access token hasn’t expired.
    - Check that your user has the required workspace permissions for the operation.

Workspace connectivity
:   **Symptom:** Operations time out or fail to connect.

    **Solution:** Verify the workspace URL is correct and reachable from your machine. If you’re behind a VPN or
    firewall, make sure that outbound HTTPS traffic to your Databricks workspace is allowed.
