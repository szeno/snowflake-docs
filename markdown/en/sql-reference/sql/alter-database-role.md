# ALTER DATABASE ROLE

Modifies the properties for an existing database role.

Currently, the only supported operations are renaming a database role or adding/overwriting/removing a comment for a database role.

See also:
:   [CREATE DATABASE ROLE](/sql-reference/sql/create-database-role) , [DROP DATABASE ROLE](/sql-reference/sql/drop-database-role) , [SHOW DATABASE ROLES](/sql-reference/sql/show-database-roles)

## Syntax

Copy code

```
ALTER DATABASE ROLE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER DATABASE ROLE [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER DATABASE ROLE [ IF EXISTS ] <name> UNSET COMMENT

ALTER DATABASE ROLE [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER DATABASE ROLE [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER DATABASE ROLE [ IF EXISTS ] <name> UNSET DCM PROJECT
```

## Parameters

`name`
:   Specifies the identifier (i.e. name) for the database role; must be unique in the database in which the role is created.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    If the identifier is not fully qualified in the form of `db_name.database_role_name`, the command looks for the database role
    in the current database for the session.

`RENAME TO new_name`
:   Specifies the new identifier for the database role; must be unique for your account.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note that when specifying the fully-qualified name of the database role, you cannot specify a different database. The name of
    the database, `db_name`, must remain the same. Only the `database_role_name` can change during a rename operation.

`SET ...`
:   Specifies the properties to set for the database role:

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the database role.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies the properties to unset for the database role, which resets them to the defaults.

    - `COMMENT`
    - `TAG tag_name [ , tag_name ... ]`

`UNSET DCM PROJECT`

> Detaches the database role from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the database role and the DCM project without dropping the database role. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

## Access control privileges

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Database role | Only the database role owner (i.e. the database role with the OWNERSHIP privilege on the database role), or a higher role, can execute this command.  The owner role does not inherit any permissions granted to the owned database role. To inherit permissions from a database role, that database role must be granted to another role, creating a parent-child relationship in a role hierarchy. |
| APPLY | Tag | Enables setting a tag on a database role. |

Expand

Show lessSee more

## Usage notes

Regarding metadata:

> Attention
>
> Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename database role `dr1` to `dbr2` in database `d1`:

> Copy code
>
> ```
> ALTER DATABASE ROLE d1.dr1 RENAME TO d1.dbr2;
> ```

Add a comment for database role `d1.dbr2`:

> Copy code
>
> ```
> ALTER DATABASE ROLE d1.dbr2 SET COMMENT = 'New comment for database role';
> ```
