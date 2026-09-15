# CREATE ICEBERG TABLE (AWS Glue as the Iceberg catalog)

Important

To integrate with AWS Glue, we recommend that you instead use
[AWS Glue Iceberg REST](https://docs.aws.amazon.com/glue/latest/dg/connect-glu-iceberg-rest.html),
which supports additional Iceberg table features such as catalog-vended credentials.

For instructions, see [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) and [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest).

Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema using
an Iceberg table that is registered in the AWS Glue Data Catalog.
This type of Iceberg table requires a [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def)
to connect Snowflake to AWS Glue.

This topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

Note

Before creating a table, you must create the [external volume](/sql-reference/sql/create-external-volume) where the Iceberg metadata
and data files are stored.
For instructions, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

You also need a catalog integration for the table.
To learn more, see [Configure a catalog integration for AWS Glue](/user-guide/tables-iceberg-configure-catalog-integration-glue).

See also:
:   [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table) , [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  [ EXTERNAL_VOLUME = '<external_volume_name>' ]
  [ CATALOG = '<catalog_integration_name>' ]
  CATALOG_TABLE_NAME = '<catalog_table_name>'
  [ CATALOG_NAMESPACE = '<catalog_namespace>' ]
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
```

## Required parameters

`table_name`
:   Specifies the identifier (name) for the table; must be unique for the schema in which the table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CATALOG_TABLE_NAME = 'catalog_table_name'`
:   Specifies the table name as recognized by the AWS Glue Data Catalog. For an example of using
    `CATALOG_TABLE_NAME` when you create an Iceberg table,
    see [Examples](#examples) (in this topic).

    This parameter cannot be changed after you create the table.

## Optional parameters

`EXTERNAL_VOLUME = 'external_volume_name'`
:   Specifies the identifier (name) for the external volume where the Iceberg table stores its metadata files and data in Parquet
    format. Iceberg metadata and manifest files store the table schema, partitions, snapshots, and other metadata.

    If you don’t specify this parameter, the Iceberg table defaults to the external volume for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

`CATALOG = 'catalog_integration_name'`
:   Specifies the identifier (name) of the catalog integration for this table.
    You must specify a catalog integration that you have configured for AWS Glue. For information,
    see [Configure a catalog integration for AWS Glue](/user-guide/tables-iceberg-configure-catalog-integration-glue).

    If not specified, the Iceberg table defaults to the catalog integration for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

`CATALOG_NAMESPACE = 'catalog_namespace'`
:   Optionally specifies the namespace (for example, `my_glue_database`)
    for the AWS Glue Data Catalog source. By specifying a namespace with the catalog integration and then at the table level, you can use a single catalog integration for AWS Glue to create Iceberg tables across different databases. If you don’t specify a namespace with the table, the table uses the default catalog namespace associated with the catalog integration

    If a default namespace isn’t specified with the catalog integration, you must specify a namespace for the AWS Glue Data Catalog to set a
    catalog namespace for the table.

`REPLACE_INVALID_CHARACTERS = { TRUE | FALSE }`
:   Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results.
    You can only set this parameter for tables that use an external Iceberg catalog.

    - `TRUE` replaces invalid UTF-8 characters with the Unicode replacement character.
    - `FALSE` leaves invalid UTF-8 characters unchanged. Snowflake returns a user error message when it encounters invalid UTF-8
      characters in a Parquet data file.

    If not specified, the Iceberg table defaults to the parameter value for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

    Default: `FALSE`

`AUTO_REFRESH = { TRUE | FALSE }`
:   Specifies whether Snowflake should automatically poll the external Iceberg catalog that is associated with the table for metadata updates.

    If no value is specified for the `REFRESH_INTERVAL_SECONDS` parameter on the catalog integration, Snowflake uses a default
    refresh interval of 30 seconds.

    For more information, see [automated refresh](/user-guide/tables-iceberg-auto-refresh).

    Default: FALSE

    > Note
    >
    > Using AUTO\_REFRESH with INFER\_SCHEMA isn’t supported.

`COMMENT = 'string_literal'`
:   Specifies a comment for the table.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](/user-guide/contacts-using).

    Specify the WITH CONTACT clause after all other clauses except the AS clause (if that clause is supported by this command).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ICEBERG TABLE | Schema |  |
| CREATE EXTERNAL VOLUME | Account | Required to create a new external volume. |
| USAGE | External Volume | Required to reference an existing external volume. |
| CREATE INTEGRATION | Account | Required to create a new catalog integration. |
| USAGE | Catalog integration | Required to reference an existing catalog integration. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Considerations for running this command:

  - If you created your external volume or catalog integration using a double-quoted identifier,
    you must specify the identifier exactly as created (including the double quotes) in your CREATE ICEBERG TABLE statement.
    Failure to include the quotes might result in an `Object does not exist` error (or
    similar type of error).

    To view an example, see the [Examples](#examples) (in this topic) section.
- Considerations for creating tables:

  > - A schema cannot contain tables and/or views with the same name. When creating a table:
  > > - If a view with the same name already exists in the schema, an error is returned and the table is not created.
  > > - If a table with the same name already exists in the schema, an error is returned and the table is not created, unless the optional
  > >   `OR REPLACE` keyword is included in the command.
  >
  > - CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
  >
  >   This means that any queries concurrent with the CREATE OR REPLACE ICEBERG
  >   TABLE operation use either the old or new table version.
  > - The `OR REPLACE` and `IF NOT EXISTS` clauses are mutually exclusive. They can’t both be used in the same statement.
  > - Similar to [reserved keywords](/sql-reference/reserved-keywords), ANSI-reserved function names
  >   ([CURRENT\_DATE](/sql-reference/functions/current_date), [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp), etc.) cannot be used as column names.
  > - Recreating a table (using the optional `OR REPLACE` keyword) drops its history, which makes any stream on the table stale. A stale
  >   stream is unreadable.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### Create an Iceberg table with AWS Glue as the catalog

This example creates an Iceberg table that uses the AWS Glue Data Catalog. To override the default catalog namespace and set a
catalog namespace for the table, the statement uses the optional `CATALOG_NAMESPACE` parameter.

Copy code

```
CREATE ICEBERG TABLE glue_iceberg_table
  EXTERNAL_VOLUME='glue_catalog_volume'
  CATALOG='glue_catalog_integration'
  CATALOG_TABLE_NAME='my_glue_catalog_table'
  CATALOG_NAMESPACE='icebergcatalogdb2'
  AUTO_REFRESH = TRUE;
```

### Specify an external volume or catalog integration with a double-quoted identifier

This example creates an Iceberg table with an external volume and catalog integration
whose identifiers contain double quotes. Identifiers enclosed in double quotes are case-sensitive and often contain special characters.

The identifiers `"glue_volume_1"` and `"glue_catalog_integration_1"` are specified exactly as created (including the double quotes).
Failure to include the quotes might result in an `Object does not exist` error (or similar type of error).

To learn more, see [Double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier).

Copy code

```
CREATE OR REPLACE ICEBERG TABLE itable_with_quoted_catalog
  EXTERNAL_VOLUME = '"glue_volume_1"'
  CATALOG = '"glue_catalog_integration_1"'
  CATALOG_TABLE_NAME='my_glue_catalog_table'
  CATALOG_NAMESPACE='icebergcatalogdb2'
  AUTO_REFRESH = TRUE;
```
