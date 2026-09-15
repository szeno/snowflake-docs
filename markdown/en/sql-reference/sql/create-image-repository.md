# CREATE IMAGE REPOSITORY

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Creates a new [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository) in the
current schema.

See also:
:   [DROP IMAGE REPOSITORY](/sql-reference/sql/drop-image-repository) , [SHOW IMAGE REPOSITORIES](/sql-reference/sql/show-image-repositories)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] IMAGE REPOSITORY [ IF NOT EXISTS ] <name>
  [ ENCRYPTION = ( TYPE = 'SNOWFLAKE_FULL' | TYPE = 'SNOWFLAKE_SSE' ) ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
```

## Required parameters

`name`
:   Specifies the identifier (that is, the name) for the image repository; it must be unique for the schema in which the repository is created.

    Quoted names for special characters or case-sensitive names are not supported. The same constraint also applies to database and
    schema names where you create an image repository. That is, database and schema names without quotes are valid when creating an
    image repository.

## Optional parameters

`ENCRYPTION = ( TYPE = 'SNOWFLAKE_FULL' | TYPE = 'SNOWFLAKE_SSE' )`
:   Specifies the type of encryption to use for binaries stored in the image repository. You cannot change the encryption type after you create the image repository.

    `TYPE = ...`
    :   Specifies the encryption type to use.

    Important

    If you require Tri-Secret Secure for security compliance, use the `SNOWFLAKE_FULL` encryption type for internal stages.
    `SNOWFLAKE_SSE` does not support Tri-Secret Secure.

    Possible values are the following:

    - `SNOWFLAKE_FULL`: On-host (image registry host) and server-side encryption. Data is first encrypted by Snowflake’s image registry service before sending the data to cloud service provider storage (for example, Amazon S3) where your Snowflake account is hosted.

      Snowflake uses AES-GCM with a 128-bit encryption key by default.
      You can configure a 256-bit key by setting the [CLIENT\_ENCRYPTION\_KEY\_SIZE](/sql-reference/parameters#label-client-encryption-key-size) parameter. All binaries are also automatically encrypted using AES-256 strong encryption on the server side.

      Note

      With SNOWFLAKE\_FULL encryption, Snowflake might throttle requests against the public image repository API. This throttling is triggered only when Snowflake detects an unusually large number of parallel requests against the repository. Note that, the service creation will never be impacted.
    - `SNOWFLAKE_SSE`: Server-side encryption only. The binaries are encrypted by the cloud service provider (for example, Amazon S3) where your Snowflake account is hosted when they arrive on the image repository storage area.

    Default: `SNOWFLAKE_FULL`

`COMMENT = 'string_literal'`
:   Specifies a comment for the image repository.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE IMAGE REPOSITORY | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create an image repository:

Copy code

```
CREATE OR REPLACE IMAGE REPOSITORY tutorial_repository;
```

Create an image repository with SNOWFLAKE\_FULL encryption:

Copy code

```
CREATE OR REPLACE IMAGE REPOSITORY tutorial_repository
ENCRYPTION = (type = 'SNOWFLAKE_SSE');
```

Create an image repository with a comment and a tag:

Copy code

```
CREATE IMAGE REPOSITORY tutorial_repository
  COMMENT = 'Repository for tutorial images'
  WITH TAG (cost_center = 'engineering');
```
