# CREATE OR ALTER VERSIONED SCHEMA

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a new versioned schema or modifies an existing versioned schema. This command is only supported for application instances in the
Native Apps Framework.

See also:
:   [CREATE APPLICATION](/sql-reference/sql/create-application), [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package)

## Syntax

Copy code

```
CREATE OR ALTER VERSIONED SCHEMA <name>
  [ WITH MANAGED ACCESS ]
  [ DATA_RETENTION_TIME_IN_DAYS = ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the schema; must be unique for the application instance in which the schema is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`WITH MANAGED ACCESS`
:   Specifies a managed versioned schema. Managed access versioned schemas centralize privilege
    management with the schema owner.

    In regular versioned schemas, the owner of an object (i.e. the role that has the OWNERSHIP
    privilege on the object) can grant further privileges on their objects to other roles.

    In managed schemas, the schema owner manages all privilege grants, including
    [future grants](/user-guide/security-access-control-configure#label-granting-future-privs-on-schema-objects), on objects in the schema.
    Object owners retain the OWNERSHIP privileges on the objects, however, only the schema owner can
    manage privilege grants on the objects.

`DATA_RETENTION_TIME_IN_DAYS = integer`
:   Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the schema, as well as specifying the
    default Time Travel retention time for all tables created in the schema. For more details, refer
    [Understanding & using Time Travel](/user-guide/data-time-travel).

    For a detailed description of this object-level parameter, as well as more information about object parameters, refer to
    [Parameters](/sql-reference/parameters). For more information about table-level retention time, refer to
    [CREATE TABLE](/sql-reference/sql/create-table) and [Understanding & using Time Travel](/user-guide/data-time-travel).

    Values:

    > - Standard Edition: `0` or `1`
    > - Enterprise Edition:
    >   - `0` to `90` for permanent schemas
    >   - `0` or `1` for transient schemas

    Default:

    > - Standard Edition: `1`
    > - Enterprise Edition (or higher): `1` (unless a different default value was specified at the database or account level)

    Note

    A value of `0` effectively disables Time Travel for the schema.

`MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
:   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in
    the schema to prevent streams on the tables from becoming stale.

    For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days).

`DEFAULT_DDL_COLLATION = 'collation_specification'`
:   Specifies a default [collation specification](/sql-reference/collation#label-collation-specification) for all tables added to the schema. The default
    can be overridden at the individual table level.

    For more details about the parameter, see [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation).

`COMMENT = 'string_literal'`
:   Specifies a comment for the schema.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SCHEMA | Application | If the schema already exists and you want to modify the schema, the OWNERSHIP privilege on the application is required. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

Note

While you typically create a versioned schema in the set up script, a versioned schema can be created:

- From an owner’s rights stored procedure.
- In the consumer account using an application role that has the CREATE SCHEMA privilege on the application.

## Usage notes

- If the schema does not exist, Snowflake creates a versioned schema.
- If the schema exists and already matches command, Snowflake views this as a no-operation.
- If the schema exists and does not match the command, Snowflake modifies the versioned schema to match the command.
