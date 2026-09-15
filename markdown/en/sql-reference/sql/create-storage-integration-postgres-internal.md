# CREATE STORAGE INTEGRATION (Postgres Internal Storage)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a new storage integration in the account or replaces an existing storage integration for
Postgres internal storage to access the managed storage associated with a Snowflake Postgres instance.

Unlike the `POSTGRES_EXTERNAL_STORAGE` type (which requires you to provide your own S3 bucket and
IAM role), a `POSTGRES_INTERNAL_STORAGE` integration uses the managed storage that is automatically
allocated by the Postgres instance.

See also:
:   [ALTER STORAGE INTEGRATION](/sql-reference/sql/alter-storage-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations), [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] STORAGE INTEGRATION [ IF NOT EXISTS ] <name>
  TYPE = POSTGRES_INTERNAL_STORAGE
  POSTGRES_INSTANCE = '<instance_name>'
  [ ENABLED = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
```

## Parameters

`name`
:   String that specifies the identifier (name) for the storage integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = POSTGRES_INTERNAL_STORAGE`
:   Specifies that the integration type is for Postgres managed (internal) storage.

`POSTGRES_INSTANCE = 'instance_name'`
:   Specifies the name of the Snowflake Postgres instance. Required. The Postgres instance
    must be in READY state. To create a Postgres instance, see
    [CREATE POSTGRES INSTANCE](/sql-reference/sql/create-postgres-instance).

`ENABLED = { TRUE | FALSE }`
:   Specifies whether this storage integration is available for usage in stages.

    > - `TRUE` allows users to create new stages that reference this integration.
    > - `FALSE` prevents users from creating new stages that reference this integration.
    >   You can create a storage integration in a disabled state and enable it later using
    >   [ALTER STORAGE INTEGRATION](/sql-reference/sql/alter-storage-integration).

    The value is case-insensitive.

    Default: `TRUE`

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| OWNERSHIP | Postgres instance | Required on the Postgres instance specified by `POSTGRES_INSTANCE`. |
| CREATE STORAGE INTEGRATION | Account | Grants the ability to create storage integrations. This privilege does not grant the ability to create other types of integrations. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example creates a storage integration for Postgres internal storage. The
`ENABLED` parameter defaults to `TRUE` and is omitted:

Copy code

```
CREATE STORAGE INTEGRATION postgres_internal
  TYPE = POSTGRES_INTERNAL_STORAGE
  POSTGRES_INSTANCE = 'my_pg_instance';
```
