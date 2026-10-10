# Set up the Snowpipe REST API

This topic describes how to set up the objects that your application needs to call the [Snowpipe REST API](/user-guide/data-load-snowpipe-rest-overview): a stage, a pipe, and a user with the required privileges. The user authenticates with key pair authentication or [workload identity federation](/user-guide/workload-identity-federation). This topic also describes how to install the optional Snowflake Ingest SDK for Java or Python.

Note

The instructions in this section assume you already have a target table in your Snowflake database where your data will be loaded.

## Step 1: Create a stage (if needed)

Snowpipe supports loading from the following stage types:

- Named internal (Snowflake) or external (Amazon S3, Google Cloud Storage, Microsoft Azure, or [S3-compatible storage](/user-guide/data-load-s3-compatible-storage)) stages
- Table stages

Snowpipe doesn’t load files from user stages or temporary stages.

Create a named stage using the [CREATE STAGE](/sql-reference/sql/create-stage) command, or you can choose to use an existing stage. You will stage your files temporarily before Snowpipe loads them into your target table.

To create the storage integration that an external stage on Amazon S3, Google Cloud Storage, or Microsoft Azure uses, see [Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration), [Configure an integration for Google Cloud Storage](/user-guide/data-load-gcs-config), or [Configure a storage integration for Microsoft Azure](/user-guide/data-load-azure-config#label-configuring-azure-storage-integration). An external stage for S3-compatible storage uses credentials instead of a storage integration; see [Work with Amazon S3-compatible storage](/user-guide/data-load-s3-compatible-storage). The following example creates an external stage named `orders_stage` for the `s3://mybucket/orders/` location:

Copy code

```
CREATE STAGE IF NOT EXISTS mydb.myschema.orders_stage
  URL = 's3://mybucket/orders/'
  STORAGE_INTEGRATION = my_storage_int;
```

## Step 2: Create a pipe

Create a new pipe that defines the `COPY INTO <table>` statement Snowpipe uses to load data from the ingest queue into tables. For more information, see [CREATE PIPE](/sql-reference/sql/create-pipe).

Note

Creating a pipe requires the `USAGE` privilege on the database and schema, the `CREATE PIPE` privilege on the schema, the `INSERT` and `SELECT` privileges on the target table, and either the `READ` privilege on an internal stage or the `USAGE` privilege on an external stage. If the pipe uses a named file format, you also need the `USAGE` privilege on the file format. If the pipe sends error notifications, you also need the `USAGE` privilege on its error integration. For more information, see the **Create a pipe** column in [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control).

For example, create a pipe in the `mydb.myschema` schema that loads the JSON files staged in the `orders_stage` stage into the `orders` table:

> Copy code
>
> ```
> CREATE PIPE IF NOT EXISTS mydb.myschema.orders_pipe
>   AS
>   COPY INTO mydb.myschema.orders
>     FROM @mydb.myschema.orders_stage
>     FILE_FORMAT = (TYPE = 'JSON')
>     MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
> ```

## Step 3: Configure security (per user)

For each user who calls the Snowpipe REST endpoints, set up [key pair authentication](#label-configuring-rsa-authentication-keys) or [workload identity federation](/user-guide/workload-identity-federation), and grant that user’s default role the privileges to call the endpoints. Snowpipe loads the files with the privileges of the role that owns the pipe, so the calling role doesn’t need privileges on the stage or the target table.

If you use key pair authentication and you plan to restrict calls to a single user, you only need to configure the key pair once. After that, you only need to grant the user’s default role the privileges on each pipe that the user calls, and the `USAGE` privilege on the database and schema that contain it.

Note

Snowflake recommends creating a separate user and role for calling the REST API. Create the user with this role as its default role.

### Authenticate the user

The usual authentication method is key pair authentication. Your application signs a JSON Web Token (JWT) with the private key of a Snowflake user. To set up key pair authentication, you must:

1. Generate a public-private key pair. The generated private key should be in a file, such as `rsa_key.p8`.
2. Assign the public key to the Snowflake user that calls the REST API. If you haven’t created the user yet, create it first, as shown in [the service user example](#label-snowpipe-rest-endpoints-access-control). After you assign the key to the user, run the [DESCRIBE USER](/sql-reference/sql/desc-user) command.
   In the output, the `RSA_PUBLIC_KEY_FP` property should be set to the fingerprint of the public key assigned to the user.

For instructions on how to generate the key pair and assign a key to a user, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

For language-specific examples of creating a fingerprint and generating a JWT, see the following sections:

- [Python](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-python)
- [Java](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-java)
- [Node.js](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-nodejs)

You can also authenticate with [workload identity federation](/user-guide/workload-identity-federation). Send the token in the `Authorization: Bearer WIF.<provider>.<token>` header. Snowflake recognizes the token type from the `WIF.` prefix, so you don’t need the `X-Snowflake-Authorization-Token-Type` header. To get a token, see [Using workload identity federation](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-wif).

### Grant access privileges

The role that calls the Snowpipe REST endpoints needs privileges to submit files and read load reports. It doesn’t need the privileges that the load itself uses, because Snowpipe loads files with the privileges of the role that owns the pipe, as described in [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). The calling role needs the following privileges:

| Object | Privilege | Notes |
| --- | --- | --- |
| Pipe | `OPERATE` | Required to call `insertFiles`. |
| Pipe | `MONITOR` | Required to call `insertReport` and `loadHistoryScan`. A role with `MONITOR EXECUTION` on the account can call those endpoints without `MONITOR` on the pipe. |
| Database and schema that contain the pipe | `USAGE` | Required to resolve the pipe. |

Expand

Show lessSee more

Use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command to grant these privileges to the role.

Note

Creating a role requires the `CREATE ROLE` privilege on the account, which the `USERADMIN` and `SECURITYADMIN` roles have by default. Granting privileges on the pipe, database, and schema requires the `OWNERSHIP` privilege on those objects or the global `MANAGE GRANTS` privilege, which the `SECURITYADMIN` role has by default. Creating the service user also requires the `CREATE USER` privilege on the account, which the `USERADMIN` and `SECURITYADMIN` roles have by default.

For example, create a role named `snowpipe1` that can call the REST API for a pipe named `orders_pipe`, and a service user that uses the role as its default role:

Copy code

```
-- Create a role for the Snowpipe privileges.
USE ROLE SECURITYADMIN;

CREATE OR REPLACE ROLE snowpipe1;

-- Grant the USAGE privilege on the database and schema that contain the pipe.
GRANT USAGE ON DATABASE mydb TO ROLE snowpipe1;
GRANT USAGE ON SCHEMA mydb.myschema TO ROLE snowpipe1;

-- Grant the privileges to submit files and to read load reports.
GRANT OPERATE, MONITOR ON PIPE mydb.myschema.orders_pipe TO ROLE snowpipe1;

-- Create a service user with the role as its default role. REST requests run with this role.
-- For key pair authentication, also set the user's RSA_PUBLIC_KEY property.
-- For workload identity federation, set the WORKLOAD_IDENTITY property instead.
CREATE USER IF NOT EXISTS snowpipe_loader_svc
  TYPE = SERVICE
  DEFAULT_ROLE = snowpipe1;

-- Grant the role to the user.
GRANT ROLE snowpipe1 TO USER snowpipe_loader_svc;
```

## Step 4: Stage data files

Copy data files to the internal or external stage you created for loading files using Snowpipe.

- Copy files to an external stage using the tools provided by the cloud storage service.
- Copy files to an internal stage using the [PUT](/sql-reference/sql/put) command.

**Next:** Submit the staged files to the REST API. For an example that uses curl, see [the curl example](/user-guide/data-load-snowpipe-rest-overview#label-snowpipe-rest-example). For examples that use the Snowflake Ingest SDK for Java or Python, [install the SDK](#label-snowpipe-rest-install-sdk), and then see [the SDK examples](/user-guide/data-load-snowpipe-rest-load).

## Install the Snowflake Ingest SDK for Java or Python (optional)

You can call the Snowpipe REST API with any HTTP client. Snowflake also provides the Snowflake Ingest SDKs for Java and Python, which build the requests and generate the JSON Web Token (JWT) for you.

Important

The binaries are provided as Client Software under the terms of your master service agreement (MSA) with Snowflake.

### Install the Java SDK

1. Download the Java SDK installer from the Maven Central Repository:

   [Sonatype](https://central.sonatype.com/search?q=g%3Anet.snowflake%20snowflake-ingest-sdk) (or <https://repo1.maven.org/maven2/net/snowflake/snowflake-ingest-sdk>)
2. Integrate the JAR file into an existing project.

Note

The developer notes are hosted with the source code on [GitHub](https://github.com/snowflakedb/snowflake-ingest-java).

### Install the Python SDK

Note that the Python SDK requires Python 3.6 or higher.

To install the SDK, run the following command:

> Copy code
>
> ```
> pip install snowflake-ingest
> ```

Alternatively, download the wheel file from [PyPI](https://pypi.org/project/snowflake-ingest/) and integrate it into an existing project.

Note

The developer notes are hosted with the source code on [GitHub](https://github.com/snowflakedb/snowflake-ingest-python).
