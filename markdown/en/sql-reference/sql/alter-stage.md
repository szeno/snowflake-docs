# ALTER STAGE

Modifies the properties for an existing named internal or external stage.

See also:
:   [CREATE STAGE](/sql-reference/sql/create-stage) , [DROP STAGE](/sql-reference/sql/drop-stage) , [SHOW STAGES](/sql-reference/sql/show-stages) , [DESCRIBE STAGE](/sql-reference/sql/desc-stage)

## Syntax

Copy code

```
ALTER STAGE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER STAGE [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER STAGE <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER STAGE [ IF EXISTS ] <name> UNSET DCM PROJECT

-- Internal stage
ALTER STAGE [ IF EXISTS ] <name> SET
  [ FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML | CUSTOM } [ formatTypeOptions ] } ) ]
  { [ COMMENT = '<string_literal>' ] }

-- External stage
ALTER STAGE [ IF EXISTS ] <name> SET {
    [ externalStageParams ]
    [ FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML | CUSTOM } [ formatTypeOptions ] } ) ]
    [ COMMENT = '<string_literal>' ]
    }
```

Where:

> Copy code
>
> ```
> externalStageParams (for Amazon S3) ::=
>   URL = '<protocol>://<bucket>[/<path>/]'
>   [ AWS_ACCESS_POINT_ARN = '<string>' ]
>   [ { STORAGE_INTEGRATION = <integration_name> } | { CREDENTIALS = ( {  { AWS_KEY_ID = '<string>' AWS_SECRET_KEY = '<string>' [ AWS_TOKEN = '<string>' ] } | AWS_ROLE = '<string>'  } ) } ]
>   [ ENCRYPTION = ( [ TYPE = 'AWS_CSE' ] MASTER_KEY = '<string>'
>                    | TYPE = 'AWS_SSE_S3'
>                    | TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = '<string>' ]
>                    | TYPE = 'NONE' ) ]
>   [ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
> ```
>
> Copy code
>
> ```
> externalStageParams (for Google Cloud Storage) ::=
>   [ URL = 'gcs://<bucket>[/<path>/]' ]
>   [ STORAGE_INTEGRATION = <integration_name> } ]
>   [ ENCRYPTION = (   TYPE = 'GCS_SSE_KMS' [ KMS_KEY_ID = '<string>' ]
>                    | TYPE = 'NONE' ) ]
> ```
>
> Copy code
>
> ```
> externalStageParams (for Microsoft Azure) ::=
>   [ URL = 'azure://<account>.blob.core.windows.net/<container>[/<path>/]' ]
>   [ { STORAGE_INTEGRATION = <integration_name> } | { CREDENTIALS = ( [ AZURE_SAS_TOKEN = '<string>' ] ) } ]
>   [ ENCRYPTION = (   TYPE = 'AZURE_CSE' [ MASTER_KEY = '<string>' ]
>                    | TYPE = 'NONE' ) ]
>   [ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
> ```
>
> Copy code
>
> ```
> formatTypeOptions ::=
> -- If TYPE = CSV
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      RECORD_DELIMITER = '<string>' | NONE
>      FIELD_DELIMITER = '<string>' | NONE
>      MULTI_LINE = TRUE | FALSE
>      FILE_EXTENSION = '<string>'
>      PARSE_HEADER = TRUE | FALSE
>      SKIP_HEADER = <integer>
>      SKIP_BLANK_LINES = TRUE | FALSE
>      DATE_FORMAT = '<string>' | AUTO
>      TIME_FORMAT = '<string>' | AUTO
>      TIMESTAMP_FORMAT = '<string>' | AUTO
>      BINARY_FORMAT = HEX | BASE64 | UTF8
>      ESCAPE = '<character>' | NONE
>      ESCAPE_UNENCLOSED_FIELD = '<character>' | NONE
>      TRIM_SPACE = TRUE | FALSE
>      FIELD_OPTIONALLY_ENCLOSED_BY = '<character>' | NONE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
>      ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      EMPTY_FIELD_AS_NULL = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
>      ENCODING = '<string>' | UTF8
> -- If TYPE = JSON
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      DATE_FORMAT = '<string>' | AUTO
>      TIME_FORMAT = '<string>' | AUTO
>      TIMESTAMP_FORMAT = '<string>' | AUTO
>      BINARY_FORMAT = HEX | BASE64 | UTF8
>      TRIM_SPACE = TRUE | FALSE
>      MULTI_LINE = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
>      FILE_EXTENSION = '<string>'
>      ENABLE_OCTAL = TRUE | FALSE
>      ALLOW_DUPLICATE = TRUE | FALSE
>      STRIP_OUTER_ARRAY = TRUE | FALSE
>      STRIP_NULL_VALUES = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      IGNORE_UTF8_ERRORS = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
> -- If TYPE = AVRO
>      COMPRESSION = AUTO | GZIP | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      TRIM_SPACE = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = ORC
>      TRIM_SPACE = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = PARQUET
>      COMPRESSION = AUTO | LZO | SNAPPY | NONE
>      SNAPPY_COMPRESSION = TRUE | FALSE
>      BINARY_AS_TEXT = TRUE | FALSE
>      USE_LOGICAL_TYPE = TRUE | FALSE
>      TRIM_SPACE = TRUE | FALSE
>      USE_VECTORIZED_SCANNER = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = XML
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      IGNORE_UTF8_ERRORS = TRUE | FALSE
>      PRESERVE_SPACE = TRUE | FALSE
>      STRIP_OUTER_ELEMENT = TRUE | FALSE
>      DISABLE_AUTO_CONVERT = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
> ```

## Directory table syntax

Copy code

```
ALTER STAGE [ IF EXISTS ] <name> SET DIRECTORY = ( { ENABLE = TRUE | FALSE } )

ALTER STAGE [ IF EXISTS ] <name> REFRESH [ SUBPATH = '<relative-path>' ]
```

## Parameters

`name`
:   Specifies the identifier for the stage to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`RENAME TO new_name`
:   Specifies the new identifier for the stage; must be unique for the schema.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`SET ...`
:   Specifies the options/properties to set for the stage:

    `URL = ' ... '` , `STORAGE_INTEGRATION = ...` , `CREDENTIALS = ( ... )` , `ENCRYPTION = ( ... )`
    :   Modifies the cloud-specific URL, storage integration or credentials, and/or encryption for the external stage. For more details, see
        [External Stage Parameters](#label-alter-stage-externalstageparams) (in this topic).

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the stage.

`UNSET DCM PROJECT`

> Detaches the stage from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the stage and the DCM project without dropping the stage. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

> `FILE_FORMAT = ( FORMAT_NAME = 'file_format_name' )` or `FILE_FORMAT = ( TYPE = CSV | JSON | AVRO | ORC | PARQUET | XML | CUSTOM [ ... ] )`
> :   Modifies the file format for the stage, which can be either:
>
>     `FORMAT_NAME = file_format_name`
>     :   Specifies an existing file format object to use for the stage. The specified file format object determines the format type (CSV, JSON, etc.)
>         and other format options for data files.
>
>         Note that no additional format options are specified in the string. Instead, the named file format object defines the other file format
>         options used for loading/unloading data. For more information, see [CREATE FILE FORMAT](/sql-reference/sql/create-file-format).
>
>     `TYPE = CSV | JSON | AVRO | ORC | PARQUET | XML | CUSTOM [ ... ]`
>     :   Specifies the file format type for the stage:
>
>         > - Loading data from a stage (using [COPY INTO <table>](/sql-reference/sql/copy-into-table)) accommodates all of the supported file format types.
>         > - Unloading data into a stage (using [COPY INTO <location>](/sql-reference/sql/copy-into-location)) accommodates CSV, JSON, or PARQUET.
>
>         If a file format type is specified, additional format-specific options can be modified. For more details, see
>         [Format Type Options](/sql-reference/sql/alter-stage#label-alter-stage-formattypeoptions) (in this topic).
>
>         The `CUSTOM` format type specifies that the underlying stage holds unstructured data and can only be used with the `FILE_PROCESSOR` copy option.
>
>     Note
>
>     `FORMAT_NAME` and `TYPE` are mutually exclusive; you can only specify one or the other for a stage.

Note

Do not specify copy options using the CREATE STAGE, ALTER STAGE, CREATE TABLE, or ALTER TABLE commands. We recommend that you use the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command to specify copy options.

## External stage parameters (`externalStageParams`)

`URL = 'cloud_specific_url'`
:   If a stage does not have a URL, it is an internal stage

    Warning

    Modifying the `URL` parameter of a stage can break the following functionality for objects that rely on the stage:

    - Pipe objects that leverage cloud messaging to trigger data loads (i.e. where `AUTO_INGEST = TRUE`).
    - External tables that leverage cloud messaging to trigger metadata refreshes (i.e. where `AUTO_REFRESH = TRUE`).

    **Amazon S3**

    > `URL = 'protocol://bucket[/path/]'`
    > :   Modifies the URL for the external location (existing S3 bucket) used to store data files for loading/unloading, where:
    >
    >     - `protocol` is one of the following:
    >
    >       - `s3` refers to S3 storage in public AWS regions outside of China.
    >       - `s3china` refers to S3 storage in public AWS regions in China.
    >       - `s3gov` refers to S3 storage in [government regions](/user-guide/intro-regions#label-us-gov-regions).
    >
    >       Accessing cloud storage in a [government region](/user-guide/intro-regions#label-us-gov-regions) using a storage integration is limited to Snowflake
    >       accounts hosted in the same government region.
    >
    >       Similarly, if you need to access cloud storage in a region in China, you can use a storage integration only from a Snowflake
    >       account hosted in the same region in China.
    >
    >       In these cases, use the CREDENTIALS parameter in the [CREATE STAGE](/sql-reference/sql/create-stage) command (rather than using a storage
    >       integration) to provide the credentials for authentication.
    >     - `bucket` is the name of the S3 bucket or the [bucket-style alias](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-alias.html)
    >       for an S3 bucket access point. For an S3 access point, you must also specify a value for the
    >       `AWS_ACCESS_POINT_ARN` parameter.
    >     - `path` is an optional case-sensitive path for files in the cloud storage location (files have names that begin with
    >       a common string) that limits the set of files. Paths are alternatively called *prefixes* or *folders* by different cloud storage
    >       services.
    >
    > `AWS_ACCESS_POINT_ARN = 'string'`
    > :   Specifies the Amazon resource name (ARN) for your S3 access point. Required only when you specify an S3 access point alias
    >     for your storage `URL`.

    **Google Cloud Storage**

    > `URL = 'gcs://bucket[/path/]'`
    > :   Modifies the URL for the external location (existing GCS bucket) used to store data files for loading/unloading, where:
    >
    >     - `bucket` is the name of the GCS bucket.
    >     - `path` is an optional case-sensitive path for files in the cloud storage location (i.e. files have names that begin with a
    >       common string) that limits the set of files to load. Paths are alternatively called *prefixes* or *folders* by different cloud storage
    >       services.

    **Microsoft Azure**

    > `URL = 'azure://account.blob.core.windows.net/container[/path/]'`
    > :   Modifies the URL for the external location (existing Azure container) used to store data files for loading, where:
    >
    >     > - `account` is the name of the Azure account (e.g. `myaccount`). Use the `blob.core.windows.net` endpoint for all
    >     >   supported types of Azure blob storage accounts, including Data Lake Storage Gen2.
    >     > - `container` is the name of the Azure container (e.g. `mycontainer`).
    >     > - `path` is an optional case-sensitive path for files in the cloud storage location (i.e. files have names that begin with a
    >     >   common string) that limits the set of files to load. Paths are alternatively called *prefixes* or *folders* by different cloud storage
    >     >   services.

`STORAGE_INTEGRATION = integration_name` or `CREDENTIALS = ( cloud_specific_credentials )`
:   Required only if the Amazon S3, Google Cloud Storage, or Microsoft Azure is private; not required for public buckets/containers

    **Amazon S3**

    > `STORAGE_INTEGRATION = integration_name`
    > :   Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake
    >     identity and access management (IAM) entity. For more details, see [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration).
    >
    >     Note
    >
    >     We highly recommend the use of storage integrations. This option avoids the need to supply cloud storage credentials using the CREDENTIALS
    >     parameter when creating stages or loading data.
    >
    > `CREDENTIALS = ( AWS_KEY_ID = 'string' AWS_SECRET_KEY = 'string' [ AWS_TOKEN = 'string' ] )` or `CREDENTIALS = ( AWS_ROLE = 'string' )`
    > :   Modifies the security credentials for connecting to AWS and accessing the private S3 bucket where the files to load/unload are staged. For
    >     more information, see [Configuring secure access to Amazon S3](/user-guide/data-load-s3-config).
    >
    >     The credentials you specify depend on whether you associated the Snowflake access permissions for the bucket with an AWS IAM
    >     (Identity & Access Management) user or role:
    >
    >     - **IAM user:** IAM credentials are required. Temporary (aka “scoped”) credentials are generated by AWS Security Token Service (STS) and
    >       consist of three components:
    >
    >       - `AWS_KEY_ID`
    >       - `AWS_SECRET_KEY`
    >       - `AWS_TOKEN`
    >
    >       All three are required to access a private bucket. After a designated period of time, temporary credentials expire and can no
    >       longer be used. You must then generate a new set of valid temporary credentials.
    >
    >       Important
    >
    >       The COPY command also allows permanent (aka “long-term”) credentials to be used; however, for security reasons, Snowflake does not
    >       recommend using them. If you must use permanent credentials, Snowflake recommends periodically generating new permanent credentials for
    >       external stages.
    >     - **IAM role:** Omit the security credentials and access keys and, instead, identify the role using `AWS_ROLE` and specify the AWS
    >       role ARN (Amazon Resource Name).
    >
    >       Important
    >
    >       The ability to use an AWS IAM role to access a private S3 bucket to load or unload data is now deprecated (i.e. support will be removed
    >       in a future release, TBD). We highly recommend modifying any existing S3 stages that use this feature to instead reference storage
    >       integration objects. For instructions, see [Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration).

    **Google Cloud Storage**

    > `STORAGE_INTEGRATION = integration_name`
    > :   Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake
    >     identity and access management (IAM) entity. For more details, see [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration).

    **Microsoft Azure**

    > `STORAGE_INTEGRATION = integration_name`
    > :   Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake
    >     identity and access management (IAM) entity. For more details, see [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration).
    >
    >     Note
    >
    >     We highly recommend the use of storage integrations. This option avoids the need to supply cloud storage credentials using the CREDENTIALS
    >     parameter when creating stages or loading data.
    >
    > `CREDENTIALS = ( AZURE_SAS_TOKEN = 'string' )`
    > :   Modifies the SAS (shared access signature) token for connecting to Azure and accessing the private container where the files containing
    >     loaded data are staged. Credentials are generated by Azure.

`ENCRYPTION = ( cloud_specific_encryption )`
:   Required only for loading from/unloading into encrypted files; not required if storage location and files are unencrypted

    Data loading:
    :   Modifies the encryption settings used to decrypt encrypted files in the storage location and extract data.

    Data unloading:
    :   Modifies the encryption settings used to encrypt files unloaded to the storage location.

    **Amazon S3**

    > `ENCRYPTION = ( [ TYPE = 'AWS_CSE' ] MASTER_KEY = 'string' | TYPE = 'AWS_SSE_S3' | TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = 'string' ] | TYPE = 'NONE' )`
    > > `TYPE = ...`
    > > :   Specifies the encryption type used. Possible values are:
    > >
    > >     - `AWS_CSE`: Client-side encryption (requires a `MASTER_KEY` value). Currently, the client-side
    > >       [master key](https://csrc.nist.gov/glossary/term/master_key) you provide can only be a symmetric key. Note that, when a
    > >       `MASTER_KEY` value is provided, Snowflake assumes `TYPE = AWS_CSE` (i.e. when a `MASTER_KEY` value is
    > >       provided, `TYPE` is not required).
    > >     - `AWS_SSE_S3`: Server-side encryption that requires no additional encryption settings.
    > >     - `AWS_SSE_KMS`: Server-side encryption that accepts an optional `KMS_KEY_ID` value.
    > >
    > >     For more information about the encryption types, see the AWS documentation for
    > >     [client-side encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html)
    > >     or [server-side encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/serv-side-encryption.html).
    > >
    > >     - `NONE`: No encryption.
    > >
    > > `MASTER_KEY = 'string'` (applies to `AWS_CSE` encryption only)
    > > :   Specifies the client-side master key used to encrypt the files in the bucket. The master key must be a 128-bit or 256-bit key in
    > >     Base64-encoded form.
    > >
    > > `KMS_KEY_ID = 'string'` (applies to `AWS_SSE_KMS` encryption only)
    > > :   Optionally specifies the ID for the AWS KMS-managed key used to encrypt files unloaded into the bucket. If no value is provided,
    > >     your default KMS key ID is used to encrypt files on unload.
    > >
    > >     Note that this value is ignored for data loading.
    > >
    > > Default: `NONE`

    **Google Cloud Storage**

    > `ENCRYPTION = ( TYPE = 'GCS_SSE_KMS' [ KMS_KEY_ID = 'string' ] | TYPE = 'NONE' )`
    > > `TYPE = ...`
    > > :   Specifies the encryption type used. Possible values are:
    > >
    > >     - `GCS_SSE_KMS`: Server-side encryption that accepts an optional `KMS_KEY_ID` value.
    > >
    > >       For more information, see the Google Cloud documentation:
    > >
    > >       - <https://cloud.google.com/storage/docs/encryption/customer-managed-keys>
    > >       - <https://cloud.google.com/storage/docs/encryption/using-customer-managed-keys>
    > >     - `NONE`: No encryption.
    > >
    > > `KMS_KEY_ID = 'string'` (applies to `GCS_SSE_KMS` encryption only)
    > > :   Optionally specifies the ID for the Cloud KMS-managed key that is used to encrypt files unloaded into the bucket. If no value
    > >     is provided, your default KMS key ID set on the bucket is used to encrypt files on unload.
    > >
    > >     Note that this value is ignored for data loading. The load operation should succeed if the service account has sufficient permissions
    > >     to decrypt data in the bucket.
    > >
    > > Default: `NONE`

    **Microsoft Azure**

    > `ENCRYPTION = ( TYPE = 'AZURE_CSE' MASTER_KEY = 'string' | TYPE = 'NONE' )`
    > > `TYPE = ...`
    > > :   Specifies the encryption type used. Possible values are:
    > >
    > >     - `AZURE_CSE`: Client-side encryption (requires a MASTER\_KEY value). For information, see the
    > >       [Client-side encryption information](https://docs.microsoft.com/en-us/azure/storage/common/storage-client-side-encryption) in
    > >       the Microsoft Azure documentation.
    > >     - `NONE`: No encryption.
    > >
    > > `MASTER_KEY = 'string'` (applies to AZURE\_CSE encryption only)
    > > :   Specifies the client-side master key used to encrypt or decrypt files. The master key must be a 128-bit or 256-bit key in Base64-encoded
    > >     form.
    > >
    > > Default: `NONE`

`USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }`
:   Specifies whether to use [private connectivity](/user-guide/private-connectivity-outbound) for an external stage to harden your
    security posture.

    If the external stage uses a storage integration, and that integration is configured for private connectivity, set this parameter to
    FALSE.

    For information about using this parameter, see one of the following:

    - [Private connectivity to external stages for Amazon Web Services](/user-guide/data-load-aws-private).
    - [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](/user-guide/data-load-azure-private).

## Directory table parameters

`ENABLE = { TRUE | FALSE }`
:   Specifies whether to add a directory table to the stage. When the value is TRUE, a directory table is added to the stage.

    Note

    Setting this parameter to TRUE is not supported for [S3-compatible external stages](/user-guide/data-load-s3-compatible-storage). The metadata for S3-compatible external stages cannot be refreshed automatically.

    Default: `FALSE`

`REFRESH`
:   Accesses the staged data files referenced in the directory table definition and updates the table metadata:

    - New files in the path are added to the table metadata.
    - Changes to files in the path are updated in the table metadata.
    - Files no longer in the path are removed from the table metadata.

    You can execute this command each time files are added to the stage, updated, or dropped. This step synchronizes
    the metadata with the latest set of associated files in the stage definition for the directory table.

`SUBPATH = 'relative-path'`
:   Optionally specify a relative path to refresh the metadata for a specific subset of the data files.

## Format type options (`formatTypeOptions`)

Depending on the file format type specified (`FILE_FORMAT = ( TYPE = ... )`), you can include one or more of the following format-specific options (separated by blank spaces, commas, or new lines):

# TYPE = CSV

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   - When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        - When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified when loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`

`RECORD_DELIMITER = 'string' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   One or more singlebyte or multibyte characters that separate records in an input file (data loading) or unloaded file (data unloading). Accepts common escape sequences or the following singlebyte or multibyte characters:

        Singlebyte characters:
        :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

        Multibyte characters:
        :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

            The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (For example, `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

        The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

        Also accepts a value of `NONE`.

    Default:
    :   Data loading:
        :   New line character. Note that “new line” is logical such that `\r\n` will be understood as a new line for files on a Windows platform.

        Data unloading:
        :   New line character (`\n`).

`FIELD_DELIMITER = 'string' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   One or more singlebyte or multibyte characters that separate fields in an input file (data loading) or unloaded file (data unloading). Accepts common escape sequences or the following singlebyte or multibyte characters:

        Singlebyte characters:
        :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

        Multibyte characters:
        :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

            The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (For example, `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

            > Note
            >
            > For non-ASCII characters, you must use the hex byte sequence value to get a deterministic behavior.

        The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

        Also accepts a value of `NONE`.

    Default:
    :   comma (`,`)

`MULTI_LINE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether multiple lines are allowed. If MULTI\_LINE is set to `FALSE` and the specified record delimiter is present within a CSV field, the record containing the field will be interpreted as an error.

    Default:
    :   `TRUE`

    Note

    If you are loading large uncompressed CSV files (greater than 128MB) that follow the RFC4180 specification, Snowflake supports parallel scanning of these CSV files when MULTI\_LINE is set to `FALSE`, COMPRESSION is set to `NONE`, and ON\_ERROR is set to `ABORT_STATEMENT` or `CONTINUE`.

`FILE_EXTENSION = 'string' | NONE`
:   Use:
    :   Data unloading only

    Definition:
    :   Specifies the extension for files unloaded to a stage. Accepts any extension. The user is responsible for specifying a file extension that can be read by any desired software or services.

    Default:
    :   null, meaning the file extension is determined by the format type: `.csv[compression]`, where `compression` is the extension added by the compression method, if `COMPRESSION` is set.

    Note

    If the `SINGLE` copy option is `TRUE`, then the COPY command unloads a file without a file extension by default. To specify a file extension, provide a file name and extension in the
    `internal_location` or `external_location` path (For example, `copy into @stage/data.csv`).

`PARSE_HEADER = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to use the first row headers in the data files to determine column names.

    This file format option is applied to the following actions only:

    > - Automatically detecting column definitions by using the INFER\_SCHEMA function.
    > - Loading CSV data into separate columns by using the INFER\_SCHEMA function and MATCH\_BY\_COLUMN\_NAME copy option.

    If the option is set to TRUE, the first row headers will be used to determine column names. The default value FALSE will return column names as c\*, where \* is the position of the column.

    Note

    - This option isn’t supported for external tables.
    - The SKIP\_HEADER option isn’t supported if you set `PARSE_HEADER = TRUE`.

    Default:
    :   `FALSE`

`SKIP_HEADER = integer`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Number of lines at the start of the file to skip.

    Note that SKIP\_HEADER does not use the RECORD\_DELIMITER or FIELD\_DELIMITER values to determine what a header line is; rather, it simply skips the specified number of CRLF (Carriage Return, Line Feed)-delimited lines in the file. RECORD\_DELIMITER and FIELD\_DELIMITER are then used to determine the rows of data to load.

    Default:
    :   `0`

`SKIP_BLANK_LINES = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies to skip any blank lines encountered in the data files; otherwise, blank lines produce an end-of-record error (default behavior).

    Default:
    :   `FALSE`

`DATE_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of date values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [DATE\_INPUT\_FORMAT](/sql-reference/parameters#label-date-input-format) (data loading) or [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`TIME_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of time values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [TIME\_INPUT\_FORMAT](/sql-reference/parameters#label-time-input-format) (data loading) or [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`TIMESTAMP_FORMAT = string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of timestamp values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format) (data loading) or [TIMESTAMP\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`BINARY_FORMAT = HEX | BASE64 | UTF8`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the encoding format for binary input or output. The option can be used when loading data into or unloading data from binary columns in a table.

    Default:
    :   `HEX`

`ESCAPE = 'character' | NONE`
:   Use:
    :   Data loading and unloading

    Definition:
    :   A singlebyte character string used as the escape character for enclosed or unenclosed field values. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_OPTIONALLY_ENCLOSED_BY` character in the data as literals.

        Accepts common escape sequences, octal values, or hex values.

    Loading data:
    :   Specifies the escape character for enclosed fields only. Specify the character used to enclose fields by setting `FIELD_OPTIONALLY_ENCLOSED_BY`.

        Note

        This file format option supports singlebyte characters only. Note that UTF-8 character encoding represents high-order ASCII characters
        as multibyte characters. If your data file is encoded with the UTF-8 character set, you cannot specify a high-order ASCII character as
        the option value.

        In addition, if you specify a high-order ASCII character, we recommend that you set the `ENCODING = 'string'` file format
        option as the character encoding for your data files to ensure the character is interpreted correctly.

    Unloading data:
    :   If this option is set, it overrides the escape character set for `ESCAPE_UNENCLOSED_FIELD`.

    Default:
    :   `NONE`

`ESCAPE_UNENCLOSED_FIELD = 'character' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   A singlebyte character string used as the escape character for unenclosed field values only. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_DELIMITER` or `RECORD_DELIMITER` characters in the data as literals. The escape character can also be used to escape instances of itself in the data.

        Accepts common escape sequences, octal values, or hex values.

    Loading data:
    :   Specifies the escape character for unenclosed fields only.

        Note

        - The default value is `\\`. If a row in a data file ends in the backslash (`\`) character, this character escapes the newline or
          carriage return character specified for the `RECORD_DELIMITER` file format option. As a result, the load operation treats
          this row and the next row as a single row of data. To avoid this issue, set the value to `NONE`.
        - This file format option supports singlebyte characters only. Note that UTF-8 character encoding represents high-order ASCII characters
          as multibyte characters. If your data file is encoded with the UTF-8 character set, you cannot specify a high-order ASCII character as
          the option value.

          In addition, if you specify a high-order ASCII character, we recommend that you set the `ENCODING = 'string'` file format
          option as the character encoding for your data files to ensure the character is interpreted correctly.

    Unloading data:
    :   If `ESCAPE` is set, the escape character set for that file format option overrides this option.

    Default:
    :   backslash (`\\`)

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to remove white space from fields.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        As another example, if leading or trailing spaces surround quotes that enclose strings, you can remove the surrounding spaces using this option and the quote character using the
        `FIELD_OPTIONALLY_ENCLOSED_BY` option. Note that any spaces within the quotes are preserved. For example, assuming `FIELD_DELIMITER = '|'` and `FIELD_OPTIONALLY_ENCLOSED_BY = '"'`:

        Copy code

        ```
        |"Hello world"|    /* loads as */  >Hello world<
        |" Hello world "|  /* loads as */  > Hello world <
        | "Hello world" |  /* loads as */  >Hello world<
        ```

        (the brackets in this example are not loaded; they are used to demarcate the beginning and end of the loaded strings)

    Default:
    :   `FALSE`

`FIELD_OPTIONALLY_ENCLOSED_BY = 'character' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   Character used to enclose strings. Value can be `NONE`, single quote character (`'`), or double quote character (`"`). To use the single quote character, use the octal or hex representation (`0x27`) or the double single-quoted escape (`''`).

        Data unloading only:
        :   When a field in the source table contains this character, Snowflake escapes it using the same character for unloading. For example, if the value is the double quote character and a field contains the string `A "B" C`, Snowflake escapes the double quotes for unloading as follows:

            `A ""B"" C`

    Default:
    :   `NONE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   String used to convert to and from SQL NULL:

        - When loading data, Snowflake replaces these values in the data load source with SQL NULL. To specify more than one string, enclose
          the list of strings in parentheses and use commas to separate each value.

          Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as
          a value, all instances of `2` as either a string or number are converted.

          For example:

          `NULL_IF = ('\N', 'NULL', 'NUL', '')`

          Note that this option can include empty strings.
        - When unloading data, Snowflake converts SQL NULL values to the first value in the list.

    Default:
    :   `\N` (that is, NULL, which assumes the `ESCAPE_UNENCLOSED_FIELD` value is `\\`)

`ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to generate a parsing error if the number of delimited columns (i.e. fields) in an input file does not match the number of columns in the corresponding table.

        If set to `FALSE`, an error is not generated and the load continues. If the file is successfully loaded:

        - If the input file contains records with more fields than columns in the table, the matching fields are loaded in order of occurrence in the file and the remaining fields are not loaded.
        - If the input file contains records with fewer fields than columns in the table, the non-matching columns in the table are loaded with NULL values.

        This option assumes all the records within the input file are the same length (i.e. a file containing records of varying length return an error regardless of the value specified for this parameter).

    Default:
    :   `TRUE`

    Note

    When [transforming data during loading](/user-guide/data-load-transform) (i.e. using a query as the source for the COPY command), this option is ignored. There is no requirement for your data files to have
    the same number and ordering of columns as your target table.

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`).

    If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

    If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`EMPTY_FIELD_AS_NULL = TRUE | FALSE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   - When loading data, specifies whether to insert SQL NULL for empty fields in an input file, which are represented by two successive delimiters (For example, `,,`).

          If set to `FALSE`, Snowflake attempts to cast an empty field to the corresponding column type. An empty string is inserted into columns of type STRING. For other column types, the COPY command produces an error.
        - When unloading data, this option is used in combination with `FIELD_OPTIONALLY_ENCLOSED_BY`. When `FIELD_OPTIONALLY_ENCLOSED_BY = NONE`, setting `EMPTY_FIELD_AS_NULL = FALSE` specifies to unload empty strings in tables to empty string values without quotes enclosing the field values.

          If set to `TRUE`, `FIELD_OPTIONALLY_ENCLOSED_BY` must specify a character to enclose strings.

    Default:
    :   `TRUE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

`ENCODING = 'string'`
:   Use:
    :   Data loading and external tables

    Definition:
    :   String (constant) that specifies the character set of the source data when loading data into a table.

        | Character Set | `ENCODING` Value | Supported Languages | Notes |
        | --- | --- | --- | --- |
        | Big5 | `BIG5` | Traditional Chinese |  |
        | EUC-JP | `EUCJP` | Japanese |  |
        | EUC-KR | `EUCKR` | Korean |  |
        | GB18030 | `GB18030` | Chinese |  |
        | IBM420 | `IBM420` | Arabic |  |
        | IBM424 | `IBM424` | Hebrew |  |
        | IBM949 | `IBM949` | Korean |  |
        | ISO-2022-CN | `ISO2022CN` | Simplified Chinese |  |
        | ISO-2022-JP | `ISO2022JP` | Japanese |  |
        | ISO-2022-KR | `ISO2022KR` | Korean |  |
        | ISO-8859-1 | `ISO88591` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |  |
        | ISO-8859-2 | `ISO88592` | Czech, Hungarian, Polish, Romanian |  |
        | ISO-8859-5 | `ISO88595` | Russian |  |
        | ISO-8859-6 | `ISO88596` | Arabic |  |
        | ISO-8859-7 | `ISO88597` | Greek |  |
        | ISO-8859-8 | `ISO88598` | Hebrew |  |
        | ISO-8859-9 | `ISO88599` | Turkish |  |
        | ISO-8859-15 | `ISO885915` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish | Identical to ISO-8859-1 except for 8 characters, including the Euro currency symbol. |
        | KOI8-R | `KOI8R` | Russian |  |
        | Shift\_JIS | `SHIFTJIS` | Japanese |  |
        | UTF-8 | `UTF8` | All languages | For loading data from delimited files (CSV, TSV, etc.), UTF-8 is the default.     For loading data from all other supported file formats (JSON, Avro, etc.), as well as unloading data, UTF-8 is the only supported character set. |
        | UTF-16 | `UTF16` | All languages |  |
        | UTF-16BE | `UTF16BE` | All languages |  |
        | UTF-16LE | `UTF16LE` | All languages |  |
        | UTF-32 | `UTF32` | All languages |  |
        | UTF-32BE | `UTF32BE` | All languages |  |
        | UTF-32LE | `UTF32LE` | All languages |  |
        | windows-874 | `WINDOWS874` | Thai |  |
        | windows-949 | `WINDOWS949` | Korean |  |
        | windows-1250 | `WINDOWS1250` | Czech, Hungarian, Polish, Romanian |  |
        | windows-1251 | `WINDOWS1251` | Russian |  |
        | windows-1252 | `WINDOWS1252` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |  |
        | windows-1253 | `WINDOWS1253` | Greek |  |
        | windows-1254 | `WINDOWS1254` | Turkish |  |
        | windows-1255 | `WINDOWS1255` | Hebrew |  |
        | windows-1256 | `WINDOWS1256` | Arabic |  |

        Expand

        Show lessSee more

    Default:
    :   `UTF8`

    Note

    Snowflake stores all data internally in the UTF-8 character set. The data is converted into UTF-8 before it is loaded into Snowflake.

## TYPE = JSON

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   - When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        - When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`

`DATE_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of date string values in the data files. If a value is not specified or is `AUTO`, the value for the [DATE\_INPUT\_FORMAT](/sql-reference/parameters#label-date-input-format) parameter is used.

        This file format option is applied to the following actions only:

        - Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        - Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`TIME_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of time string values in the data files. If a value is not specified or is `AUTO`, the value for the [TIME\_INPUT\_FORMAT](/sql-reference/parameters#label-time-input-format) parameter is used.

        This file format option is applied to the following actions only:

        - Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        - Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`TIMESTAMP_FORMAT = string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of timestamp string values in the data files. If a value is not specified or is `AUTO`, the value for the [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format) parameter is used.

        This file format option is applied to the following actions only:

        - Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        - Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`BINARY_FORMAT = HEX | BASE64 | UTF8`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the encoding format for binary string values in the data files. The option can be used when loading data into binary columns in a table.

        This file format option is applied to the following actions only:

        - Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        - Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `HEX`

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading JSON data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`MULTI_LINE = TRUE | FALSE`
:   Use: Data loading and external tables

    Definition:
    :   Boolean that specifies whether multiple lines are allowed. If MULTI\_LINE is set to `FALSE` and a new line is present within a JSON record, the record containing the new line will be interpreted as an error.

    Default:
    :   `TRUE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading JSON data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

`FILE_EXTENSION = 'string' | NONE`
:   Use:
    :   Data unloading only

    Definition:
    :   Specifies the extension for files unloaded to a stage. Accepts any extension. The user is responsible for specifying a file extension that can be read by any desired software or services.

    Default:
    :   null, meaning the file extension is determined by the format type: `.json[compression]`, where `compression` is the extension added by the compression method, if `COMPRESSION` is set.

`ENABLE_OCTAL = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that enables parsing of octal numbers.

    Default:
    :   `FALSE`

`ALLOW_DUPLICATE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies to allow duplicate object field names (only the last one will be preserved).

    Default:
    :   `FALSE`

`STRIP_OUTER_ARRAY = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that instructs the JSON parser to remove outer brackets (i.e. `[ ]`).

    Default:
    :   `FALSE`

`STRIP_NULL_VALUES = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that instructs the JSON parser to remove object fields or array elements containing `null` values. For example, when set to `TRUE`:

        | Before | After |
        | --- | --- |
        | `[null]` | `[]` |
        | `[null,null,3]` | `[,,3]` |
        | `{"a":null,"b":null,"c":123}` | `{"c":123}` |
        | `{"a":[1,null,2],"b":{"x":null,"y":88}}` | `{"a":[1,,2],"b":{"y":88}}` |

        Expand

        Show lessSee more

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`IGNORE_UTF8_ERRORS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether UTF-8 encoding errors produce error conditions. It is an alternative syntax for `REPLACE_INVALID_CHARACTERS`.

    Values:
    :   If set to `TRUE`, any invalid UTF-8 sequences are silently replaced with the Unicode character `U+FFFD` (i.e. “replacement character”).

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

## TYPE = AVRO

`COMPRESSION = AUTO | GZIP | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading only

    Definition:
    :   - When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        - When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`.

Note

We recommend that you use the default `AUTO` option because it will determine both the file and codec compression. Specifying a compression option refers to the compression of files, not the compression of blocks (codecs).

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Avro data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Avro data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

## TYPE = ORC

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Orc data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading and external tables

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Orc data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

## TYPE = PARQUET

`COMPRESSION = AUTO | LZO | SNAPPY | NONE`
:   Use:
    :   Data unloading and external tables

    Definition:

    - When unloading data, specifies the compression algorith for columns in the Parquet files.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically. Supports the following compression algorithms: Brotli, gzip, Lempel-Ziv-Oberhumer (LZO), LZ4, Snappy, or Zstandard v0.8 (and higher).    When unloading data, unloaded files are compressed using the [Snappy](https://google.github.io/snappy/) compression algorithm by default. |
        | `LZO` | When unloading data, files are compressed using the Snappy algorithm by default. If unloading data to LZO-compressed files, specify this value. |
        | `SNAPPY` | When unloading data, files are compressed using the Snappy algorithm by default. You can optionally specify this value. |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`

`SNAPPY_COMPRESSION = TRUE | FALSE`
:   Use:
    :   Data unloading only

        | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | Unloaded files are compressed using the [Snappy](https://google.github.io/snappy/) compression algorithm by default. |
        | `SNAPPY` | May be specified if unloading Snappy-compressed files. |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Definition:
    :   Boolean that specifies whether unloaded file(s) are compressed using the SNAPPY algorithm.

    Note

    Deprecated. Use `COMPRESSION = SNAPPY` instead.

    Limitations:
    :   Only supported for data unloading operations.

    Default:
    :   `TRUE`

`BINARY_AS_TEXT = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to interpret columns with no defined logical data type as UTF-8 text. When set to `FALSE`, Snowflake interprets these columns as binary data.

    Default:
    :   `TRUE`

    Note

    Snowflake recommends that you set BINARY\_AS\_TEXT to FALSE to avoid any potential conversion issues.

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Parquet data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`USE_LOGICAL_TYPE = TRUE | FALSE`
:   Use:
    :   Data loading, data querying in staged files, and schema detection.

    Definition:
    :   Boolean that specifies whether to use Parquet logical types. With this file format option, Snowflake can interpret Parquet logical types during data loading. For more information, see [Parquet Logical Type Definitions](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md). To enable Parquet logical types, set USE\_LOGICAL\_TYPE as TRUE when you create a new file format option.

    Limitations:
    :   Not supported for data unloading.

`USE_VECTORIZED_SCANNER = TRUE | FALSE`
:   Use:
    :   Data loading and data querying in staged files

    Definition:
    :   Boolean that specifies whether to use a vectorized scanner for loading Parquet files.

    Default:
    :   `FALSE`. In a future BCR, the default value will be `TRUE`.

    Using the vectorized scanner can significantly reduce the latency for loading Parquet files, because this scanner is well suited for the columnar format of a [Parquet](https://parquet.apache.org/docs/file-format/) file. The scanner only downloads relevant sections of the Parquet file into memory, such as the subset of selected columns.

    If `USE_VECTORIZED_SCANNER` is set to `TRUE`, the vectorized scanner has the following behaviors:

    > - The `BINARY_AS_TEXT` option is always treated as `FALSE` and the `USE_LOGICAL_TYPE` option is always treated as `TRUE`, no matter what the actual value is being set to.
    > - The vectorized scanner supports Parquet map types. The output of scanning a map type is as follows:
    >
    > > Copy code
    > >
    > > ```
    > > "my_map":
    > >   {
    > > "k1": "v1",
    > > "k2": "v2"
    > >   }
    > > ```
    >
    > - The vectorized scanner shows `NULL` values in the output, as the following example demonstrates:
    >
    > > Copy code
    > >
    > > ```
    > > "person":
    > >  {
    > >   "name": "Adam",
    > >   "nickname": null,
    > >   "age": 34,
    > >   "phone_numbers":
    > >   [
    > >  "1234567890",
    > >  "0987654321",
    > >  null,
    > >  "6781234590"
    > >   ]
    > >   }
    > > ```
    >
    > - The vectorized scanner handles Time and Timestamp as follows:
    >
    > > | Parquet | Snowflake vectorized scanner |
    > > | --- | --- |
    > > | TimeType(isAdjustedToUtc=True/False, unit=MILLIS/MICROS/NANOS) | TIME |
    > > | TimestampType(isAdjustedToUtc=True, unit=MILLIS/MICROS/NANOS) | TIMESTAMP\_LTZ |
    > > | TimestampType(isAdjustedToUtc=False, unit=MILLIS/MICROS/NANOS) | TIMESTAMP\_NTZ |
    > > | INT96 | TIMESTAMP\_LTZ |
    > >
    > > Expand
    > >
    > > Show lessSee more

    If `USE_VECTORIZED_SCANNER` is set to `FALSE`, the scanner has the following behaviors:

    > - This option does not support Parquet maps. The output of scanning a map type is as follows:
    >
    > > Copy code
    > >
    > > ```
    > > "my_map":
    > >  {
    > >   "key_value":
    > >   [
    > > {
    > >        "key": "k1",
    > >        "value": "v1"
    > >    },
    > >    {
    > >        "key": "k2",
    > >        "value": "v2"
    > >    }
    > >  ]
    > >   }
    > > ```
    >
    > - This option does not explicitly show `NULL` values in the scan output, as the following example demonstrates:
    >
    > > Copy code
    > >
    > > ```
    > > "person":
    > >  {
    > >   "name": "Adam",
    > >   "age": 34
    > >   "phone_numbers":
    > >   [
    > > "1234567890",
    > > "0987654321",
    > > "6781234590"
    > >   ]
    > >  }
    > > ```
    >
    > - This option handles Time and Timestamp as follows:
    >
    > > | Parquet | When USE\_LOGICAL\_TYPE = TRUE | When USE\_LOGICAL\_TYPE = FALSE |
    > > | --- | --- | --- |
    > > | TimeType(isAdjustedToUtc=True/False, unit=MILLIS/MICROS) | TIME | - TIME (If ConvertedType present) - INTEGER (If ConvertedType not present) |
    > > | TimeType(isAdjustedToUtc=True/False, unit=NANOS) | TIME | INTEGER |
    > > | TimestampType(isAdjustedToUtc=True, unit=MILLIS/MICROS) | TIMESTAMP\_LTZ | TIMESTAMP\_NTZ |
    > > | TimestampType(isAdjustedToUtc=True, unit=NANOS) | TIMESTAMP\_LTZ | INTEGER |
    > > | TimestampType(isAdjustedToUtc=False, unit=MILLIS/MICROS) | TIMESTAMP\_NTZ | - TIMESTAMP\_LTZ (If ConvertedType present) - INTEGER (If ConvertedType not present) |
    > > | TimestampType(isAdjustedToUtc=False, unit=NANOS) | TIMESTAMP\_NTZ | INTEGER |
    > > | INT96 | TIMESTAMP\_NTZ | TIMESTAMP\_NTZ |
    > >
    > > Expand
    > >
    > > Show lessSee more

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Parquet data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

## TYPE = XML

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading only

    Definition:
    :   - When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        - When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`

`IGNORE_UTF8_ERRORS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether UTF-8 encoding errors produce error conditions. It is an alternative syntax for `REPLACE_INVALID_CHARACTERS`.

    Values:
    :   If set to `TRUE`, any invalid UTF-8 sequences are silently replaced with the Unicode character `U+FFFD` (i.e. “replacement character”).

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`PRESERVE_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser preserves leading and trailing spaces in element content.

    Default:
    :   `FALSE`

`STRIP_OUTER_ELEMENT = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser strips out the outer XML element, exposing 2nd level elements as separate documents.

    Default:
    :   `FALSE`

`DISABLE_AUTO_CONVERT = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser disables automatic conversion of numeric and Boolean values from text to native representation.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip any BOM (byte order mark) present in an input file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Stage | Required to alter the stage properties and to enable or disable a directory table on the stage using ALTER STAGE … SET DIRECTORY.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| WRITE | Stage | Required to refresh the metadata using ALTER STAGE … REFRESH. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- For external stages that use an S3 access point:

  - If you’re using a storage integration, you must configure the IAM policy for the integration
    to grant permission to your S3 access point. For more information, see [Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration).
  - Multi-region access points aren’t supported.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename `my_int_stage` to `new_int_stage`:

> Copy code
>
> ```
> ALTER STAGE my_int_stage RENAME TO new_int_stage;
> ```

Alter `my_ext_stage` (created in the [CREATE STAGE](/sql-reference/sql/create-stage) examples) to change the URL to reference a sub-folder named `new` in the
`files` folder. If a [COPY INTO <table>](/sql-reference/sql/copy-into-table) command that references this stage encounters a data error on any of the
records, it skips the file. All other copy options are set to the default values.

If the S3 bucket is in a region in China, use the `s3china://` protocol for the URL parameter.

> Copy code
>
> ```
> ALTER STAGE my_ext_stage
> SET URL='s3://loading/files/new/'
> COPY_OPTIONS = (ON_ERROR='skip_file');
> ```

Alter `my_ext_stage` to replace the supplied credentials with a reference to a storage integration named `myint` :

> Copy code
>
> ```
> ALTER STAGE my_ext_stage SET STORAGE_INTEGRATION = myint;
> ```

Alter `my_ext_stage` to specify a new access key ID and secret access key for the stage:

> Copy code
>
> ```
> ALTER STAGE my_ext_stage SET CREDENTIALS=(AWS_KEY_ID='d4c3b2a1' AWS_SECRET_KEY='z9y8x7w6');
> ```
>
> (the credentials values used in the above example are for illustration purposes only)

Alter `my_ext_stage3` to change the encryption type to `AWS_SSE_S3` server-side encryption for the stage:

> Copy code
>
> ```
> ALTER STAGE my_ext_stage3 SET ENCRYPTION=(TYPE='AWS_SSE_S3');
> ```

## Directory table examples

Add a directory table to an existing stage named `mystage`:

Copy code

```
ALTER STAGE mystage SET DIRECTORY = ( ENABLE = TRUE );
```

Manually refresh the directory table metadata in a stage named `mystage`:

Copy code

```
ALTER STAGE mystage REFRESH;

+-------------------------+----------------+-------------------------------+
| file                    | status         | description                   |
|-------------------------+----------------+-------------------------------|
| data/json/myfile.json   | REGISTERED_NEW | File registered successfully. |
+-------------------------+----------------+-------------------------------+
```

Manually refresh the directory table metadata for the files in the `data` path in a stage named `mystage`:

Copy code

```
ALTER STAGE mystage REFRESH SUBPATH = 'data';
```
