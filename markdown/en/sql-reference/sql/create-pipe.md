# CREATE PIPE

Creates a new pipe in the system for defining the [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement used by
[Snowpipe](/user-guide/data-load-snowpipe-intro) to load data from an ingestion queue, or by [Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview) to load data from a streaming source directly into tables.

This command supports the following variants:

- [CREATE OR ALTER PIPE](#label-create-or-alter-pipe-syntax): Creates a pipe if it doesn’t exist or alters an existing pipe.

See also:
:   [ALTER PIPE](/sql-reference/sql/alter-pipe), [DROP PIPE](/sql-reference/sql/drop-pipe), [SHOW PIPES](/sql-reference/sql/show-pipes), [DESCRIBE PIPE](/sql-reference/sql/desc-pipe)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] PIPE [ IF NOT EXISTS ] <name>
  [ AUTO_INGEST = [ TRUE | FALSE ] ]
  [ ERROR_INTEGRATION = <integration_name> ]
  [ AWS_SNS_TOPIC = '<string>' ]
  [ INTEGRATION = '<string>' ]
  [ COMMENT = '<string_literal>' ]
  AS <copy_statement>
```

## Variant syntax

### CREATE OR ALTER PIPE

Creates a new pipe if it doesn’t already exist, or transforms an existing pipe into the pipe defined in the statement.
A CREATE OR ALTER PIPE statement follows the syntax rules of a CREATE PIPE statement and has the same limitations as an
[ALTER PIPE](/sql-reference/sql/alter-pipe) statement.

The following modifications are supported when altering a pipe:

- Pausing or resuming the pipe using PIPE\_EXECUTION\_PAUSED.
- Adding, updating, or removing a COMMENT.

For more information, see [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER PIPE <name>
  [ AUTO_INGEST = [ TRUE | FALSE ] ]
  [ ERROR_INTEGRATION = <integration_name> ]
  [ AWS_SNS_TOPIC = '<string>' ]
  [ INTEGRATION = '<string>' ]
  [ PIPE_EXECUTION_PAUSED = TRUE | FALSE ]
  [ COMMENT = '<string_literal>' ]
  AS <copy_statement>
```

Note

You can use the `<copy_statement>` with two different types of data sources:

- A staged location: `COPY INTO mytable FROM @mystage ...`
- A streaming source: `COPY INTO mytable FROM (SELECT ... FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING')))`

## Required parameters

`name`
:   Identifier for the pipe; must be unique for the schema in which the pipe is created.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`copy_statement`
:   [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement used to load data from queued files into a Snowflake table. This statement serves
    as the text/definition for the pipe and is displayed in the [SHOW PIPES](/sql-reference/sql/show-pipes) output.

Note

We currently do not recommend using the following functions in the `copy_statement` for Snowpipe:

- CURRENT\_DATE
- CURRENT\_TIME
- CURRENT\_TIMESTAMP
- GETDATE
- LOCALTIME
- LOCALTIMESTAMP
- SYSDATE
- SYSTIMESTAMP

It is a known issue that the time values inserted using these functions can be a few hours earlier than the LOAD\_TIME values returned
by the [COPY\_HISTORY function](/sql-reference/functions/copy_history) or the
[COPY\_HISTORY view](/sql-reference/account-usage/copy_history).

It is recommended to query [METADATA$START\_SCAN\_TIME](/user-guide/querying-metadata) instead, which provides a more accurate representation of record loading.

## Optional parameters

`AUTO_INGEST = TRUE | FALSE`
:   Specifies whether to automatically load data files from the internal or external stage:

    > - `TRUE` enables automatic data loading.
    >
    >   Snowpipe supports loading from external stages (Amazon S3, Google Cloud Storage, or Microsoft Azure).
    > - `FALSE` disables automatic data loading. You must make calls to the Snowpipe REST API endpoints to load data files.
    >
    >   Snowpipe supports loading from internal stages (i.e. Snowflake named stages or table stages, but not user stages) or
    >   external stage (Amazon S3, Google Cloud Storage, or Microsoft Azure).

[Preview Feature](/release-notes/preview-features) — Open

For internal stages, using this parameter to automatically load data is only supported for Snowflake accounts hosted on AWS.

`ERROR_INTEGRATION = 'integration_name'`
:   Required only when configuring Snowpipe to send error notifications to a cloud messaging service.

    Specifies the name of the notification integration used to communicate with the messaging service. For more information, see
    [Snowpipe error notifications](/user-guide/data-load-snowpipe-errors).

`AWS_SNS_TOPIC = 'string'`
:   Required only when configuring AUTO\_INGEST for Amazon S3 external stages using SNS.

    Specifies the Amazon Resource Name (ARN) for the SNS topic for your S3 bucket. The CREATE PIPE statement subscribes the
    Amazon Simple Queue Service (SQS) queue to the specified SNS topic. The pipe copies files to the ingest queue triggered by event
    notifications via the SNS topic. For more information, see [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3).

`INTEGRATION = 'string'`
:   Required only when configuring AUTO\_INGEST for Google Cloud Storage or Microsoft Azure external stages.

    Specifies the existing notification integration used to access the storage queue. For more information, see:

    - [Automating Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs)
    - [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure)

    The integration name must be typed in all uppercase.

`COMMENT = 'string_literal'`
:   Specifies a comment for the pipe.

    Default: No value

## Pipes for Snowpipe Streaming with high-performance architecture

You can define a pipe for Snowpipe Streaming to load data directly from the Snowpipe Streaming API, without requiring a staged file location. This method is designed for low-latency, row-based ingestion.

The COPY INTO statement for a streaming pipe must use the DATA\_SOURCE table function in the FROM clause, with the `TYPE => 'STREAMING'` argument.

Note

- Pipes created for streaming don’t require an `AUTO_INGEST` parameter or a `FROM @stage` clause.
- The `copy_statement` within a streaming pipe’s definition is used to transform and load the data received from the API.
- Snowpipe Streaming also provides a [default pipe](/user-guide/snowpipe-streaming/snowpipe-streaming-pipe-object#label-ssv2-default-pipe) for each table, which is automatically created on demand. You only need to create a custom pipe if you require features like in-flight transformations or pre-clustering.

For examples, see [CREATE OR ALTER PIPE](#label-create-pipe-examples).

## Usage notes

- This SQL command requires the following minimum permissions:

  | Privilege | Object | Notes |
  | --- | --- | --- |
  | CREATE PIPE | Schema |  |
  | USAGE | Stage in the pipe definition | External stages only |
  | USAGE | Integration | Required for receiving Snowpipe error notifications |
  | READ | Stage in the pipe definition | Internal stages only |
  | SELECT, INSERT | Table in the pipe definition |  |
  | OWNERSHIP | Pipe | Required to execute a [CREATE OR ALTER PIPE](#label-create-or-alter-pipe-syntax) statement for an *existing* pipe. |
  | SQL operations on schema objects also require USAGE or any other privilege on the database and schema that contain the object. |  |  |

  Expand

  Show lessSee more
- All [COPY INTO <table>](/sql-reference/sql/copy-into-table) copy options are supported except for the following:

  - `FILES = ( 'file_name1' [ , 'file_name2', ... ] )`
  - `ON_ERROR = ABORT_STATEMENT`
  - `SIZE_LIMIT = num`
  - `PURGE = TRUE | FALSE` (i.e. automatic purging while loading)
  - `FORCE = TRUE | FALSE`

    Note that you can manually remove files from an internal (i.e. Snowflake) stage (after they’ve been loaded) using the
    [REMOVE](/sql-reference/sql/remove) command.
  - `RETURN_FAILED_ONLY = TRUE | FALSE`
  - `VALIDATION_MODE = RETURN_n_ROWS | RETURN_ERRORS | RETURN_ALL_ERRORS`
- The `PATTERN = 'regex_pattern'` copy option filters the set of files to load using a regular expression. Pattern matching
  behaves as follows depending on the AUTO\_INGEST parameter value:

  > - `AUTO_INGEST = TRUE`: The regular expression filters the list of files in the stage and optional path (i.e. cloud storage location)
  >   in the COPY INTO *<table>* statement.
  > - `AUTO_INGEST = FALSE`: The regular expression filters the list of files submitted in calls to the Snowpipe REST API
  >   `insertFiles` endpoint.
  >
  > Snowpipe trims any path segments in the stage definition from the storage location and applies the regular expression to any
  > remaining path segments and filenames. To view the stage definition, execute the [DESCRIBE STAGE](/sql-reference/sql/desc-stage) command for the
  > stage. The URL property consists of the bucket or container name and zero or more path segments. For example, if the FROM location in a COPY INTO *<table>* statement is `@s/path1/path2/` and the URL value for stage `@s` is `s3://mybucket/path1/`, then Snowpipe trims `s3://mybucket/path1/path2/` from the storage location in the FROM clause and applies the regular expression to the remaining filenames in the path.
  >
  > Important
  >
  > Snowflake recommends that you enable cloud event filtering for Snowpipe to reduce costs, event noise, and latency. Only use
  > the PATTERN option when your cloud provider’s event filtering feature is not sufficient. For more information about configuring
  > event filtering for each cloud provider, see the following pages:
  >
  > - **Amazon S3:** [Configuring event notifications using object key name filtering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html)
  > - **Microsoft Azure Event Grid:** [Understand event filtering for Event Grid subscriptions](https://docs.microsoft.com/en-us/azure/event-grid/event-filtering)
  > - **Google Cloud Pub/Sub:** [Filtering messages](https://cloud.google.com/pubsub/docs/filtering)
- Using a query as the source for the COPY statement for column reordering, column omission, and casts (i.e. transforming data during
  a load) is supported. For usage examples, see [Transform data during a load](/user-guide/data-load-transform). Note that only simple SELECT statements are
  supported. Filtering using a WHERE clause is not supported.
- Pipe definitions are not dynamic (i.e. a pipe is not automatically updated if the underlying stage or table changes, such as renaming
  or dropping the stage/table). Instead, you must create a new pipe and submit this pipe name in future Snowpipe REST API calls.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

Important

If you recreate a pipe (using the CREATE OR REPLACE PIPE syntax), see [Recreating pipes](/user-guide/data-load-snowpipe-manage#label-snowpipe-management-recreate-pipes) for related
considerations and best practices.

### CREATE OR ALTER PIPE

- All limitations of the [ALTER PIPE](/sql-reference/sql/alter-pipe) command apply.
- The pipe’s COPY INTO statement (`copy_statement`) can’t be changed for an existing pipe. If you need to change the pipe definition,
  drop the existing pipe and create a new one. See [Recreating pipes](/user-guide/data-load-snowpipe-manage#label-snowpipe-management-recreate-pipes) for related considerations.
- The AUTO\_INGEST, AWS\_SNS\_TOPIC, and INTEGRATION properties can’t be changed for an existing pipe.
- Setting or unsetting a tag is not supported.

## Examples

Create a pipe in the current schema that loads all the data from files staged in the `mystage` stage into `mytable`:

Copy code

```
CREATE PIPE mypipe
  AS
  COPY INTO mytable
  FROM @mystage
  FILE_FORMAT = (TYPE = 'JSON');
```

Same as the previous example, but with a data transformation. Only load data from the 4th and 5th columns in the staged files, in
reverse order:

Copy code

```
CREATE PIPE mypipe2
  AS
  COPY INTO mytable(C1, C2)
  FROM (SELECT $5, $4 FROM @mystage)
  FILE_FORMAT = (TYPE = 'JSON');
```

Create a pipe that loads all the data into columns in the target table that match corresponding columns represented in the data. Column names are case-insensitive.

In addition, load metadata from the METADATA$START\_SCAN\_TIME and METADATA$FILENAME [metadata columns](/user-guide/querying-metadata) to the columns named `c1` and `c2`.

Copy code

```
CREATE PIPE mypipe3
  AS
  (COPY INTO mytable
    FROM @mystage
    MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE
    INCLUDE_METADATA = (c1= METADATA$START_SCAN_TIME, c2=METADATA$FILENAME)
    FILE_FORMAT = (TYPE = 'JSON'));
```

Create a pipe in the current schema for automatic loading of data using event notifications received from a messaging service:

**Amazon S3**

Copy code

```
CREATE PIPE mypipe_s3
  AUTO_INGEST = TRUE
  AWS_SNS_TOPIC = 'arn:aws:sns:us-west-2:001234567890:s3_mybucket'
  AS
  COPY INTO snowpipe_db.public.mytable
  FROM @snowpipe_db.public.mystage
  FILE_FORMAT = (TYPE = 'JSON');
```

**Google Cloud Storage**

Copy code

```
CREATE PIPE mypipe_gcs
  AUTO_INGEST = TRUE
  INTEGRATION = 'MYINT'
  AS
  COPY INTO snowpipe_db.public.mytable
  FROM @snowpipe_db.public.mystage
  FILE_FORMAT = (TYPE = 'JSON');
```

**Microsoft Azure**

Copy code

```
CREATE PIPE mypipe_azure
  AUTO_INGEST = TRUE
  INTEGRATION = 'MYINT'
  AS
  COPY INTO snowpipe_db.public.mytable
  FROM @snowpipe_db.public.mystage
  FILE_FORMAT = (TYPE = 'JSON');
```

**Internal named stage**

[Preview Feature](/release-notes/preview-features) — Open

Preview support for this feature is only available to Snowflake accounts hosted on Amazon Web Services (AWS).

Create a pipe in the current schema that automatically loads all the data files on the internal named stage named `mystage`.

> Copy code
>
> ```
> CREATE PIPE mypipe_aws
>   AUTO_INGEST = TRUE
>   AS
>   COPY INTO snowpipe_db.public.mytable
>   FROM @snowpipe_db.public.mystage
>   FILE_FORMAT = (TYPE = 'JSON');
> ```

**Snowpipe Streaming with high-performance architecture**

Create a basic streaming pipe:

Copy code

```
CREATE OR REPLACE PIPE my_streaming_pipe
AS COPY INTO my_table
  FROM (SELECT $1, $1:c1, $1:ts FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING')));
```

Create a streaming pipe with in-flight transformations by specifying column expressions in the SELECT clause:

Copy code

```
CREATE OR REPLACE PIPE my_pipe_with_transforms
AS COPY INTO my_table (col1, col2, col3)
  FROM (
    SELECT
      $1:field1::STRING AS col1,
      $1:field2::NUMBER AS col2,
      CURRENT_TIMESTAMP() AS col3
    FROM TABLE (DATA_SOURCE(TYPE => 'STREAMING'))
  );
```

Create a streaming pipe with pre-clustering enabled for improved query performance. The target table must have clustering keys defined:

Copy code

```
CREATE OR REPLACE PIPE my_pipe_with_clustering
AS COPY INTO my_table
  FROM (SELECT $1, $1:c1, $1:ts FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING')))
  CLUSTER_AT_INGEST_TIME = TRUE;
```

**Apache Iceberg v3 support**

Note

For more information about other Iceberg v3 features that Snowflake supports, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).

The following example loads data from files for Iceberg v3 tables, for both Snowflake-managed and externally managed tables:

Copy code

```
CREATE PIPE mypipe
  AUTO_INGEST = TRUE
  INTEGRATION = 'MYINT'
  AS
  COPY INTO snowpipe_db.public.my_v3_iceberg_table
  FROM @snowpipe_db.public.mystage
  FILE_FORMAT = (TYPE = 'JSON');
```

### CREATE OR ALTER PIPE

Create a new pipe or pause an existing pipe:

Copy code

```
CREATE OR ALTER PIPE mypipe
  PIPE_EXECUTION_PAUSED = TRUE
  COMMENT = 'Loads data from mystage into mytable'
  AS
  COPY INTO mytable
  FROM @mystage
  FILE_FORMAT = (TYPE = 'JSON');
```
