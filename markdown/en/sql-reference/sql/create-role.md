# CREATE ROLE

Create a new role or replace an existing role in the system.

After creating roles, you can grant object privileges to the role and then grant the role to other roles or individual users to enable
access control security for objects in the system.

This command supports the following variants:

- [CREATE OR ALTER ROLE](#label-create-or-alter-role-syntax): Creates a role if it doesn’t exist or alters an existing role.

See also:
:   [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege), [GRANT ROLE](/sql-reference/sql/grant-role), [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership), [DROP ROLE](/sql-reference/sql/drop-role), [ALTER ROLE](/sql-reference/sql/alter-role), [SHOW ROLES](/sql-reference/sql/show-roles)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] ROLE [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
```

## Variant syntax

### CREATE OR ALTER ROLE

Creates a new role if it doesn’t already exist, or transforms an existing role into the role defined in the statement.
A CREATE OR ALTER ROLE statement follows the syntax rules of a CREATE ROLE statement and has the same limitations as an
[ALTER ROLE](/sql-reference/sql/alter-role) statement.

Copy code

```
CREATE OR ALTER ROLE <name>
  [ COMMENT = '<string_literal>' ]
```

For more information, see [CREATE OR ALTER ROLE usage notes](#label-create-or-alter-role-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

## Required parameters

`name`
:   Identifier for the role; must be unique for your account.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (for example, `"My role"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the role.

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
| CREATE ROLE | Account | Only the USERADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed. |
| OWNERSHIP | Role | Required to execute a [CREATE OR ALTER ROLE](#label-create-or-alter-role-syntax) statement for an *existing* role.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## General usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## CREATE OR ALTER ROLE usage notes

- All limitations of the [ALTER ROLE](/sql-reference/sql/alter-role) command apply.
- Setting or unsetting a tag is not supported; however, existing tags are not altered by a CREATE OR ALTER ROLE statement and remain
  unchanged.

## Examples

Copy code

```
CREATE ROLE myrole;
```
