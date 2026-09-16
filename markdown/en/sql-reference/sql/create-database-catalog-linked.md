# CREATE DATABASE (catalog-linked)

Creates a new [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) for Apache Iceberg™ tables that use
an external Iceberg REST catalog.

## Syntax

Copy code

```
CREATE DATABASE <name>
  LINKED_CATALOG = ( catalogParams ),
  [ EXTERNAL_VOLUME = '<external_vol>' ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ CATALOG_CASE_SENSITIVITY = { CASE_SENSITIVE | CASE_INSENSITIVE } ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
```

Where:

> Copy code
>
> ```
> catalogParams ::=
>   CATALOG = '<catalog_int>',
>   [ ALLOWED_NAMESPACES = ('<namespace1>', '<namespace2>', ... ) ]
>   [ BLOCKED_NAMESPACES = ('<namespace1>', '<namespace2>', ... ) ]
>   [ ALLOWED_WRITE_OPERATIONS = { NONE | ALL } ]
>   [ NAMESPACE_MODE = { IGNORE_NESTED_NAMESPACE | FLATTEN_NESTED_NAMESPACE } ]
>   [ NAMESPACE_FLATTEN_DELIMITER = '<string_literal>' ]
>   [ SYNC_INTERVAL_SECONDS = <value> ]
> ```

## Required parameters

`name`
:   Specifies the identifier for the catalog-linked database; must be unique for your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`EXTERNAL_VOLUME = my_external_vol`
:   Specifies an [external volume](/sql-reference/sql/create-external-volume)
    that provides access to the data and metadata for your remote Iceberg tables.

    Not required if using [vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials).

`COMMENT = 'string_literal'`
:   Specifies a comment for the database.

    Default: No value

`CATALOG_CASE_SENSITIVITY = { CASE_SENSITIVE | CASE_INSENSITIVE }`
:   Specifies the case sensitivity that your external Iceberg catalog uses for identifiers.

    - `CASE_SENSITIVE`: The external Iceberg catalog uses case-sensitive identifiers. For example, Snowflake Open Catalog is a
      case-sensitive catalog.

      - Snowflake matches identifiers exactly as they appear, including case. Snowflake automatically converts unquoted identifiers to
        uppercase, but quoted identifiers must match exactly the case in your external catalog.
      - However, if the external Iceberg catalog is actually case insensitive, and normalizes to lowercase, you must surround identifiers in
        double quotes.

      These requirements only apply to identifying existing schemas, tables, and table columns.
    - `CASE_INSENSITIVE`: The external Iceberg catalog uses case-insensitive identifiers. For example, Unity Catalog and AWS Glue are
      case-insensitive catalogs.

      - Snowflake resolves unquoted identifiers in a case-insensitive manner for all SQL statements, including queries and
        DDL commands such as CREATE ICEBERG TABLE, CREATE SCHEMA, and ALTER ICEBERG TABLE. You don’t need to
        double-quote identifiers. When you create objects using DDL, Snowflake normalizes object names to lowercase on the
        remote catalog. For double-quoted identifiers and [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case),
        see [Requirements for identifier resolution in a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database#label-catalog-linked-identifier-requirements).
      - However, if the external Iceberg catalog is actually case sensitive, Snowflake treats unquoted identifiers as case-insensitive and
        automatically converts unquoted identifiers to uppercase. When you create or query objects, Snowflake matches identifiers regardless
        of case, as long as they are unquoted.

        Using this pattern is discouraged because Snowflake can’t resolve two different identifiers that differ in casing. This pattern only
        works when no two identifiers are different in casing only.

    Default: `CASE_INSENSITIVE`

    For more information on the requirements for identifier resolution, including examples, see [Requirements for identifier resolution in a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database#label-catalog-linked-identifier-requirements).

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](/user-guide/contacts-using).

    Specify the WITH CONTACT clause after all other clauses except the AS clause (if that clause is supported by this command).

## Catalog parameters (catalogParams)

`CATALOG = catalog_int`
:   Specifies the name of your catalog integration.

`ALLOWED_NAMESPACES = ('namespace1', 'namespace2', ... )`
:   Optionally specifies one or more namespaces in your remote catalog to limit the scope of automatic table discovery.
    Snowflake syncs the specified namespaces and all namespaces and tables that are nested under them.
    If a nested namespace is in the ALLOWED\_NAMESPACES list but you set the NAMESPACE\_MODE parameter to IGNORE\_NESTED\_NAMESPACE,
    Snowflake does not sync the nested namespace or any schemas and tables under it.

`BLOCKED_NAMESPACES = ('namespace1', 'namespace2', ... )`
:   Optionally specifies one or more namespaces in your remote catalog to block for automatic table discovery.

    Snowflake blocks the specified namespaces and all namespaces and tables that are nested under them.

    If you specify both ALLOWED\_NAMESPACES and BLOCKED\_NAMESPACES, the BLOCKED\_NAMESPACES list takes precedence.
    For example, if `ns1.ns2` is allowed, but `ns1` is blocked, then Snowflake won’t sync `ns1.ns2`.

`ALLOWED_WRITE_OPERATIONS = { NONE | ALL }`
:   Specifies whether your catalog-linked database is read-only or writable.

    - `NONE`: Your catalog-linked database is read-only.

      When your catalog-linked database is read only, any operation that you run that requires committing to the catalog fails. For
      example, DROP ICEBERG TABLE.
    - `ALL`: Your catalog-linked database is writable.

      Warning

      When your catalog-linked database has write permissions enabled, Snowflake propagates table drops to the remote catalog, which removes
      the table and data from both systems.

    Default: `ALL`

`NAMESPACE_MODE = { IGNORE_NESTED_NAMESPACE | FLATTEN_NESTED_NAMESPACE }`
:   Specifies how Snowflake handles namespaces for Iceberg tables in the catalog-linked database.

    - `IGNORE_NESTED_NAMESPACE`: Snowflake links only tables in the first namespace level for your catalog.
    - `FLATTEN_NESTED_NAMESPACE`: Snowflake links tables in all namespace levels for your catalog. For a table in a nested namespace, Snowflake
      uses the NAMESPACE\_FLATTEN\_DELIMITER parameter to construct a flattened namespace. With this option, you must set
      the NAMESPACE\_FLATTEN\_DELIMITER parameter.

      For example, consider a table named `iceberg_table_5` in the `namespace3aa` namespace:

      Copy code

      ```
      my_catalog_linked_db
      |-- namespace3
      |   |-- namespace3a
      |       |-- namespace3aa
      |           |-- iceberg_table_5
      ```

      If you set `NAMESPACE_FLATTEN_DELIMITER = "/"`, you can specify
      `"my_catalog_linked_db"."namespace3/namespace3a/namespace3aa"."iceberg_table_5"` to reference the table.

    Default: `IGNORE_NESTED_NAMESPACE`

    `FLATTEN_NESTED_NAMESPACE` is supported only when your catalog integration uses a catalog that supports nested namespaces. For other REST catalogs,
    setting this option returns an error.

`NAMESPACE_FLATTEN_DELIMITER = 'string_literal'`
:   Required if you set NAMESPACE\_MODE = FLATTEN\_NESTED\_NAMESPACE.
    Specifies a delimiter, which Snowflake uses to construct flattened namespaces for tables in your catalog.

    Important

    The character that you choose for a delimiter can’t appear in your remote namespaces. During the autodiscovery process,
    Snowflake skips any namespace that contains the delimiter and does not create a corresponding schema in your catalog-linked database.

    Valid characters: One or more punctuation characters, symbols, or digits. Letters and whitespace aren’t allowed.

`SYNC_INTERVAL_SECONDS = value`
:   Specifies the time interval in seconds that Snowflake should use for automatically discovering schemas and tables in your remote catalog.

    Values: 30 to 86400 (1 day), inclusive

    Default: 30 seconds

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE DATABASE | Account | Required to create a new database.  Only the SYSADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed. |
| USAGE | External Volume | Required to reference an existing external volume. |
| USAGE | Catalog integration | Required to reference an existing catalog integration. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Supported only when you use a catalog integration for Iceberg REST (for example, Snowflake Open Catalog).
- To limit automatic table discovery to a specific set of namespaces, use the ALLOWED\_NAMESPACES parameter. You can also use the
  BLOCKED\_NAMESPACES parameter to block a set of namespaces.
- Snowflake doesn’t sync remote catalog access control for users or roles.
- You can create schemas, externally managed Iceberg tables, or database roles in a catalog-linked database. Creating other Snowflake objects
  isn’t currently supported.
- When you create a catalog-linked database, you can’t specify the default Iceberg version or merge-on-read behavior to use for
  Iceberg tables.

  However, you can modify these properties for an existing database by using the [ALTER DATABASE (catalog-linked)](/sql-reference/sql/alter-database-catalog-linked)
  command to set the following parameters:

  - ICEBERG\_VERSION\_DEFAULT
  - ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR
- For Iceberg tables in a catalog-linked database:

  - Snowflake bidirectionally syncs table and column descriptions between the remote catalog and Snowflake. Sync can
    update a description to a new value, but never replaces a non-empty description with an empty one. Other remote catalog
    table properties, such as retention policies or buffers, aren’t copied, and altering table properties isn’t currently
    supported.
  - [Automated refresh](/user-guide/tables-iceberg-auto-refresh) is enabled by default. If the `table-uuid` of an external table
    and the catalog-linked database table don’t match, refresh fails and Snowflake drops the table from the catalog-linked database; Snowflake doesn’t change the remote table.
  - If you drop a table from the remote catalog, Snowflake drops the table from the catalog-linked database.
    This action is asynchronous, so you might not see the change in the remote catalog right away.
  - If you rename a table in the remote catalog, Snowflake drops the existing table from the catalog-linked database and creates a table with the new name.
  - Masking policies and tags are supported. Other Snowflake-specific features, including replication and cloning, aren’t supported.
  - The character that you choose for the NAMESPACE\_FLATTEN\_DELIMITER parameter can’t appear in your remote namespaces. During the auto discovery process,
    Snowflake skips any namespace that contains the delimiter, and doesn’t create a corresponding schema in your catalog-linked database.
  - If you specify anything other than `_`, `$`, or numbers for the NAMESPACE\_FLATTEN\_DELIMITER parameter,
    you must put the schema name in quotes when you query the table.
  - To check whether a namespace is nested under another namespace, use the [SHOW SCHEMAS](/sql-reference/sql/show-schemas) command
    and check the `is_nested` column in the output.
  - For databases linked to AWS Glue, you must use lowercase letters and surround the schema, table, and column names in double quotes.
    This is also required for other Iceberg REST catalogs that only support lowercase identifiers.

    The following example shows a valid query:

    Copy code

    ```
    CREATE SCHEMA "s1";
    ```

    The following statements aren’t valid, because they use uppercase letters or omit the double quotes:

    Copy code

    ```
    CREATE SCHEMA s1;
    CREATE SCHEMA "Schema1";
    ```
  - Using UNDROP ICEBERG TABLE isn’t supported.
  - Sharing:

    - Sharing with a listing isn’t currently supported
    - Direct sharing is supported
- For writing to tables in a catalog-linked database:

  - Creating and writing to tables in nested namespaces is supported only when your catalog integration uses a catalog that
    supports nested namespaces. For other REST catalogs, creating and writing to tables in nested namespaces isn’t supported.
  - Don’t use a period (`.`) in a namespace name unless period is the value you set for NAMESPACE\_FLATTEN\_DELIMITER and
    NAMESPACE\_MODE is set to FLATTEN\_NESTED\_NAMESPACE. Otherwise, the namespace won’t be created.
  - Position [row-level deletes](https://iceberg.apache.org/spec/#row-level-deletes) are supported for tables stored
    on Amazon S3, Azure, or Google Cloud. Row-level deletes with equality delete files aren’t supported. For more information about row-level deletes,
    see [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes). To turn off position deletes, which enable
    running the Data Manipulation Language (DML) operations in copy-on-write mode, set the `ICEBERG_MERGE_ON_READ_BEHAVIOR` parameter to `'DISABLED'` at the table, schema, or
    database level.

- For ALLOWED\_NAMESPACES and BLOCKED\_NAMESPACES, Snowflake doesn’t store nested namespaces if the set already contains the parent namespace.
  For example, if you create a database and specify `ALLOWED_NAMESPACES = ('ns1', 'ns1.ns2', 'ns1.ns3')`, Snowflake only stores `ns1` since the other two are automatically included.
  If you use [GET\_DDL](/sql-reference/functions/get_ddl) on the example database, Snowflake returns `ALLOWED_NAMESPACES = ('ns1')`. The same applies for BLOCKED\_NAMESPACES.
- You can create [database roles](/sql-reference/sql/create-database-role) in a catalog-linked database to manage
  access control for objects in the database. For example, you can grant privileges on schemas and tables in a catalog-linked database
  to a database role, and then grant the database role to account roles.
- For querying tables in a catalog-linked database:

  - Snowflake automatically converts unquoted identifiers (table and column names) to uppercase.
    If your external Iceberg catalog uses case-sensitive identifiers, you must surround table and column names in double quotes.

    For more information about object identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a catalog-linked database with flattened, nested namespaces that uses an external volume.

Copy code

```
CREATE DATABASE my_linked_db
  LINKED_CATALOG = (
    CATALOG = 'my_catalog_int',
    NAMESPACE_MODE = FLATTEN_NESTED_NAMESPACE,
    NAMESPACE_FLATTEN_DELIMITER = '-'
  )
  EXTERNAL_VOLUME = 'my_external_vol';
```

Create a catalog-linked database that uses vended credentials and specifies one allowed namespace:

Copy code

```
CREATE DATABASE my_linked_db
  LINKED_CATALOG = (
    CATALOG = 'my_catalog_int_vended_creds',
    ALLOWED_NAMESPACES = ('my_namespace')
  );
```

Create a database role in a catalog-linked database and grant privileges:

Copy code

```
CREATE DATABASE ROLE my_linked_db.analyst;

GRANT USAGE ON SCHEMA my_linked_db.my_namespace TO DATABASE ROLE my_linked_db.analyst;

GRANT SELECT ON ALL ICEBERG TABLES IN SCHEMA my_linked_db.my_namespace TO DATABASE ROLE my_linked_db.analyst;

GRANT DATABASE ROLE my_linked_db.analyst TO ROLE data_consumer;
```
