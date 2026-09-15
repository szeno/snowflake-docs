# DROP TAG

Removes a tag from the system.

For information about this command and tag references, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

See also:
:   [CREATE TAG](/sql-reference/sql/create-tag) , [ALTER TAG](/sql-reference/sql/alter-tag) , [SHOW TAGS](/sql-reference/sql/show-tags) , [UNDROP TAG](/sql-reference/sql/undrop-tag)

## Syntax

Copy code

```
DROP TAG [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Identifier for the tag.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Tag | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on tag DDL and privileges, see [Access control privileges](/user-guide/object-tagging/work#label-object-tags-privileges).

## Usage notes

- Prior to dropping a tag, determine all of the objects the tag is assigned to by calling the Account Usage table function
  [TAG\_REFERENCES\_WITH\_LINEAGE](/sql-reference/functions/tag_references_with_lineage).
- A tag can be dropped if it is currently assigned to an [object](/user-guide/object-tagging/introduction#label-object-tag-supported-objects). If dropping the tag was
  unintentional, execute an [UNDROP TAG](/sql-reference/sql/undrop-tag) command. Note that the UNDROP TAG command restores the tag assignments
  prior to the DROP TAG operation.
- A tag cannot be dropped if a masking policy is [assigned](/sql-reference/sql/alter-tag) to the tag.

  In this scenario, unset the masking policy from the tag first and then execute the DROP TAG statement.
- For more information on tag DDL authorization, see [required privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Example

The following example drops a tag:

> Copy code
>
> ```
> DROP TAG cost_center;
> ```
