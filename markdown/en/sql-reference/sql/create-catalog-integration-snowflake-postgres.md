# CREATE CATALOG INTEGRATION (Snowflake Postgres)

Creates a new catalog integration in the account or replaces an existing catalog integration for
Snowflake Postgres to access Apache Iceberg™ tables managed by a Snowflake Postgres instance.

See also:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration), [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration), [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations), [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [ IF NOT EXISTS ] <name>
  CATALOG_SOURCE = SNOWFLAKE_POSTGRES
  TABLE_FORMAT = ICEBERG
  [ CATALOG_NAMESPACE = '<namespace>' ]
  REST_CONFIG = (
    restConfigParams
  )
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

Where:

Copy code

```
restConfigParams ::=

POSTGRES_INSTANCE = '<instance_name>'
ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
[ CATALOG_NAME = '<database_name>' ]
```

## Parameters

`name`
:   String that specifies the identifier (name) for the catalog integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CATALOG_SOURCE = SNOWFLAKE_POSTGRES`
:   Specifies that the catalog source is a Snowflake Postgres instance.

`TABLE_FORMAT = ICEBERG`
:   Specifies ICEBERG as the table format supplied by the catalog.

`CATALOG_NAMESPACE = 'namespace'`
:   Optionally specifies the default schema namespace for tables discovered through this catalog
    integration. For example, `'public'`.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether the catalog integration is available to use for Iceberg tables.

    > - `TRUE` allows users to create new Iceberg tables that reference this integration.
    > - `FALSE` prevents users from creating new Iceberg tables that reference this integration.

    The value is case-insensitive.

    The default is `TRUE`.

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

### REST configuration parameters (restConfigParams)

`POSTGRES_INSTANCE = 'instance_name'`
:   Specifies the name of the Snowflake Postgres instance. Required. The Postgres instance
    must be in READY state. To create a Postgres instance, see
    [CREATE POSTGRES INSTANCE](/sql-reference/sql/create-postgres-instance).

`ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`
:   Specifies the access delegation mode for accessing table data and metadata in cloud storage.
    The only supported value is `VENDED_CREDENTIALS`.

`CATALOG_NAME = 'database_name'`
:   Optionally specifies the default Postgres database name. You can override this value
    per table or per catalog-linked database.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| USAGE | Postgres instance | Required on the Postgres instance specified by `POSTGRES_INSTANCE`. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example creates a catalog integration for a Snowflake Postgres instance:

Copy code

```
CREATE CATALOG INTEGRATION my_postgres_catalog_int
  CATALOG_SOURCE = SNOWFLAKE_POSTGRES
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'public'
  REST_CONFIG = (
    POSTGRES_INSTANCE = 'my_pg_instance'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
    CATALOG_NAME = 'my_database'
  )
  ENABLED = TRUE;
```
