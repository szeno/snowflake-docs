# CREATE SHARE

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all, accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire
about enabling it, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new, empty [share](/user-guide/data-sharing-intro). Once the share is created, you can include a database and
objects from the database (schemas, tables, and views) in the share using the [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) command. You can then use
[ALTER SHARE](/sql-reference/sql/alter-share) to add one or more accounts to the share.

This command supports the following variants:

- [CREATE OR ALTER SHARE](#label-create-or-alter-share-syntax): Creates a share if it doesn’t exist or alters an existing share.

See also:
:   [DROP SHARE](/sql-reference/sql/drop-share), [ALTER SHARE](/sql-reference/sql/alter-share), [SHOW SHARES](/sql-reference/sql/show-shares), [DESCRIBE SHARE](/sql-reference/sql/desc-share)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SHARE [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
```

## Variant syntax

### CREATE OR ALTER SHARE

Creates a new share if it doesn’t already exist, or transforms an existing share into the share defined in the statement.
A CREATE OR ALTER SHARE statement follows the syntax rules of a CREATE SHARE statement and has the same limitations as an
[ALTER SHARE](/sql-reference/sql/alter-share) statement.

The following modifications are supported when altering a share:

- Adding, updating, or removing a COMMENT.

For more information, see [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER SHARE <name>
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the share; must be unique for the account in which the share is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the share.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SHARE | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| OWNERSHIP | Share | Required to execute a [CREATE OR ALTER SHARE](#label-create-or-alter-share-syntax) statement for an *existing* share. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For more information about access control requirements for Snowflake Secure Data Sharing specifically, see
[Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

### CREATE OR ALTER SHARE

- All limitations of the [ALTER SHARE](/sql-reference/sql/alter-share) command apply.
- Adding or removing accounts from the share is not supported. Use [ALTER SHARE](/sql-reference/sql/alter-share) to add or remove consumer accounts.
- Setting or unsetting a tag is not supported.
- Renaming a share is not supported.

## Examples

Create an empty share named `sales_s`:

> Copy code
>
> ```
> CREATE SHARE sales_s;
> ```
>
> ```
> +-----------------------------------------+
> | status                                  |
> |-----------------------------------------|
> | Share SALES_S successfully created.     |
> +-----------------------------------------+
> ```

After you create the share, complete it by running the following commands:

> 1. Run the [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) command to add a database (and objects in the database) to the share.
> 2. Run the [ALTER SHARE](/sql-reference/sql/alter-share) command to add accounts to the share.

### CREATE OR ALTER SHARE

Create a new share or update the comment for an existing share:

Copy code

```
CREATE OR ALTER SHARE sales_s
  COMMENT = 'Sales data share for consumer accounts';
```
