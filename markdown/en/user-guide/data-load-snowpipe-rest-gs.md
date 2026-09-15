# Data loading preparation using the Snowpipe REST API

This topic describes how to get started with Snowpipe when calling the REST API, including instructions for installing the required client SDK, creating a stage (if needed) and pipe, and the one-time security setup for each Snowpipe user.

Note

The instructions in this section assume you already have a target table in your Snowflake database where your data will be loaded.

## Client requirement (Java or Python SDK)

The Snowpipe service requires either the Java SDK or Python SDK. These SDKs are provided by Snowflake for your convenience.

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

To install the SDK, execute the following command:

> Copy code
>
> ```
> pip install snowflake-ingest
> ```

Alternatively, download the wheel file from [PyPI](https://pypi.org/project/snowflake-ingest/) and integrate it into an existing project.

Note

The developer notes are hosted with the source code on [GitHub](https://github.com/snowflakedb/snowflake-ingest-python).

## Step 1: Create a stage (if needed)

Snowpipe supports loading from the following stage types:

- Named internal (Snowflake) or external (Amazon S3, Google Cloud Storage, or Microsoft Azure) stages
- Table stages

Create a named stage using the [CREATE STAGE](/sql-reference/sql/create-stage) command, or you can choose to use an existing stage. You will stage your files temporarily before Snowpipe loads them into your target table.

## Step 2: Create a pipe

Create a new pipe in the system for defining the COPY INTO *<table>* statement used by Snowpipe to load data from an ingestion queue into tables. For information, see [CREATE PIPE](/sql-reference/sql/create-pipe).

Note

Creating a pipe requires the CREATE PIPE access control privilege, as well as the USAGE privilege on the database, schema and stage.

For example, create a pipe in the `mydb.myschema` schema that loads all the data from files staged in the `mystage` stage into the `mytable` table:

> Copy code
>
> ```
> create pipe mydb.myschema.mypipe if not exists as copy into mydb.myschema.mytable from @mydb.myschema.mystage;
> ```

## Step 3: Configure security (per user)

For each user who will execute continuous data loads using Snowpipe, generate a public-private key pair for making calls to the Snowpipe REST endpoints. In addition, grant sufficient privileges on the objects for
the data load (i.e. the target database, schema, and table), the stage object, and the pipe.

If you plan to restrict Snowpipe data loads to a single user, you only need to configure key pair authentication for the user once. After that, you only need to grant access control privileges on the database objects used for each data load.

Note

To follow the general principle of least privilege, we recommend creating a separate user and role to use for ingesting files using a pipe. The user should be created with this role as its default role.

### Use key pair authentication & key rotation

The Snowpipe REST endpoints require key pair authentication with JSON Web Token (JWT). JWTs are signed using a public/private key pair with
RSA encryption.

As part of this process, you must:

1. Generate a public-private key pair. The generated private key should be in a file (e.g. named `rsa_key.p8`).
2. Assign the public key to your Snowflake user. After you assign the key to the user, run the [DESCRIBE USER](/sql-reference/sql/desc-user) command.
   In the output, the `RSA_PUBLIC_KEY_FP` property should be set to the fingerprint of the public key assigned to the user.

For instructions on how to generate the key pair and assign a key to a user, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

For language-specific examples of creating a fingerprint and generating a JWT token, see the following sections:

> - [Python](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-python)
> - [Java](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-java)
> - [Node.js](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair-nodejs)

### Grant access privileges

Calling the Snowpipe REST endpoints requires a role with the following minimum privileges:

| Object | Privilege | Notes |
| --- | --- | --- |
| Named pipe | OPERATE (`insertFiles` endpoint), MONITOR (`insertReport`, `loadHistoryScan` endpoints) |  |
| Named stage | USAGE (external stage) , READ (internal stage) |  |
| Named file format | USAGE | Optional; only needed if either the stage (see [Step 1: Create a Stage (If Needed)](#step-1-create-a-stage-if-needed)) or the pipe (see [Step 2: Create a Pipe](#step-2-create-a-pipe)) references a named file format. |
| Target database | USAGE |  |
| Target schema | USAGE |  |
| Target table | INSERT , SELECT |  |

Expand

Show lessSee more

Use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command to grant these privileges to the role.

Note

Only security administrators (i.e. users with the SECURITYADMIN role) or higher, or another role with both the CREATE ROLE privilege on the account and the global MANAGE GRANTS privilege, can create roles and grant privileges.

For example, create a role named `snowpipe1` that can load data via a pipe named `mypipe`. The pipe references an external stage:

Copy code

```
 -- Create a role for the Snowpipe privileges.
use role securityadmin;

create or replace role snowpipe1;

-- Grant the USAGE privilege on the database and schema that contain the pipe object.
grant usage on database mydb to role snowpipe1;
grant usage on schema mydb.myschema to role snowpipe1;

-- Grant the INSERT and SELECT privileges on the target table.
grant insert, select on mydb.myschema.mytable to role snowpipe1;

-- Grant the USAGE privilege on the external stage.
grant usage on stage mydb.myschema.mystage to role snowpipe1;

-- Grant the OPERATE and MONITOR privileges on the pipe object.
grant operate, monitor on pipe mydb.myschema.mypipe to role snowpipe1;

-- Grant the role to a user
grant role snowpipe1 to user jsmith;

-- Set the role as the default role for the user
alter user jsmith set default_role = snowpipe1;
```

## Step 4: Stage data files

Copy data files to the internal or external stage you created for loading files using Snowpipe.

- Copy files to an external stage using the tools provided by the cloud storage service.
- Copy files to an internal stage using the [PUT](/sql-reference/sql/put) command.

  Note

  If your Snowflake account is hosted on Amazon Web Services, we recommend always using the PUT … OVERWRITE = TRUE syntax.

  Amazon S3 provides read-after-write consistency for new objects created in a bucket. However, if a HEAD or GET request for an object is made before it is created, then S3 provides *eventual consistency* for the object. This means that an immediate request for a new object after it is created could return a `file not found` exception. Setting the OVERWRITE = TRUE parameter avoids the initiation of a HEAD request prior to the creation of the object in the S3 bucket.

  For more information about the S3 consistency model, see the [S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/Introduction.html#ConsistencyModel).

**Next:** Learn how to call the public REST endpoints to load data and retrieve load history reports, in [Overview of the Snowpipe REST endpoints to load data](/user-guide/data-load-snowpipe-rest-overview).
