# CREATE DATABASE ROLE

Create a new [database role](/user-guide/security-access-control-considerations#label-access-control-considerations-database-roles) or replace an existing database role in the system.

After creating database roles, you can grant object privileges to the database role and then grant the database role to other database
roles or account roles to enable access control security for objects in the system.

This command supports the following variants:

- [CREATE OR ALTER DATABASE ROLE](#label-create-or-alter-db-role-syntax): Creates a new database role if it doesn’t exist or alters an existing database role.

See also:
:   [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege), [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role), [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership), [DROP DATABASE ROLE](/sql-reference/sql/drop-database-role), [ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role),
    [SHOW DATABASE ROLES](/sql-reference/sql/show-database-roles), [CREATE <object> … CLONE](/sql-reference/sql/create-clone)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] DATABASE ROLE [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
```

## Variant syntax

### CREATE OR ALTER DATABASE ROLE

Creates a new database role if it doesn’t already exist, or transforms an existing database role into the role defined in the statement.
A CREATE OR ALTER DATABASE ROLE statement follows the syntax rules of a CREATE DATABASE ROLE statement and has the same limitations as an
[ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role) statement.

Copy code

```
CREATE OR ALTER DATABASE ROLE <name>
  [ COMMENT = '<string_literal>' ]
```

For more information, see [CREATE OR ALTER DATABASE ROLE usage notes](#label-create-or-alter-db-role-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

## Required parameters

`name`
:   Specifies the identifier (that is, the name) for the database role; must be unique in the database in which the role is created.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    If the identifier is not fully qualified in the form of `db_name.database_role_name`, the command creates the database role
    in the current database for the session.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the database role.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE DATABASE ROLE | Database | A role with the OWNERSHIP privilege on the database can grant the CREATE DATABASE ROLE privilege to another account role. |
| OWNERSHIP | Database role | Required to execute a [CREATE OR ALTER DATABASE ROLE](#label-create-or-alter-db-role-syntax) statement for an *existing* database role.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## General usage notes

- You can create database roles in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).
- When you create a database role, the USAGE privilege on the database that contains the database role is granted to the database role
  automatically.

Caution

Avoid recreating a database role (using the OR REPLACE keywords). Behind the scenes, recreating an object (using CREATE OR REPLACE
*<object>*) first drops and then creates the object. Recreating a database role drops the database role from any shares that it is
granted to. You must grant the database role to these shares again.

If you must recreate a database role, notify any data consumers of a share that includes the database role. They must grant the database
role to their own account roles again.

Regarding metadata:

> Attention
>
> Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## CREATE OR ALTER DATABASE ROLE usage notes

- All limitations of the [ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role) command apply.
- Setting or unsetting a tag is not supported; however, existing tags are not altered by a CREATE OR ALTER DATABASE ROLE statement and remain
  unchanged.

## Examples

Create database role `dr1` in database `d1`:

> Copy code
>
> ```
> CREATE DATABASE ROLE d1.dr1;
> ```

Create a database role in a catalog-linked database:

> Copy code
>
> ```
> CREATE DATABASE ROLE my_linked_db.reader_role
>   COMMENT = 'Read-only role for catalog-linked database';
> ```
