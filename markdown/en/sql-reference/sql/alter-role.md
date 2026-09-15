# ALTER ROLE

Modifies the properties for an existing [custom role](/user-guide/security-access-control-overview#label-access-control-overview-roles-custom). Currently, the only supported
operations are renaming a role or adding/overwriting/removing a comment for a role.

See also:
:   [CREATE ROLE](/sql-reference/sql/create-role) , [DROP ROLE](/sql-reference/sql/drop-role) , [SHOW ROLES](/sql-reference/sql/show-roles)

## Syntax

Copy code

```
ALTER ROLE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER ROLE [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER ROLE [ IF EXISTS ] <name> UNSET COMMENT

ALTER ROLE [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER ROLE [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER ROLE [ IF EXISTS ] <name> UNSET DCM PROJECT
```

## Parameters

`name`
:   Specifies the identifier for the role to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`RENAME TO new_name`
:   Specifies the new identifier for the role; must be unique for your account.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies the properties to set for the role:

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the role.

`UNSET ...`
:   Specifies the properties to unset for the role, which resets them to the defaults.

    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

`UNSET DCM PROJECT`

> Detaches the role from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the role and the DCM project without dropping the role. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

## Usage notes

- Only the role owner (i.e. the role with the OWNERSHIP privilege on the role), or a higher role, can execute this command.
- To rename a role (using the `RENAME TO new_name` parameter) the role that executes this command must also have the global CREATE ROLE
  privilege.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename role `role1` to `role2`:

> Copy code
>
> ```
> ALTER ROLE role1 RENAME TO role2;
> ```

Add a comment for role `myrole`:

> Copy code
>
> ```
> ALTER ROLE myrole SET COMMENT = 'New comment for role';
> ```
