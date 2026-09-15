# DESCRIBE AUTHENTICATION POLICY

Describes the properties of an [authentication policy](/user-guide/authentication-policies).

See also:
:   [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy), [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy), [DROP AUTHENTICATION POLICY](/sql-reference/sql/drop-authentication-policy), [SHOW AUTHENTICATION POLICIES](/sql-reference/sql/show-authentication-policies)

## Syntax

Copy code

```
{ DESC | DESCRIBE } AUTHENTICATION POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the authentication policy to describe. If the identifier contains spaces or special characters, you must enclose
    the string in double quotation marks. Identifiers enclosed in double quotation marks are case-sensitive. The identifier must meet the
    [identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY AUTHENTICATION POLICY | Account | Only the SECURITYADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed. |
| OWNERSHIP | Authentication policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

Describe an authentication policy named `my_auth_policy`:

Copy code

```
DESC AUTHENTICATION POLICY my_auth_policy;
```

Use the [pipe operator](/sql-reference/operators-flow) to select specific output from the DESCRIBE AUTHENTICATION POLICY command:

Copy code

```
DESCRIBE AUTHENTICATION POLICY go_driver_policy
  ->> SELECT "property", "value"
        FROM $1
        WHERE "property" IN('NAME', 'CLIENT_TYPES', 'CLIENT_POLICY');
```

```
+---------------+--------------------------------------+
| property      | value                                |
|---------------+--------------------------------------|
| NAME          | GO_DRIVER_POLICY                     |
| CLIENT_TYPES  | [DRIVERS]                            |
| CLIENT_POLICY | {GO_DRIVER={MINIMUM_VERSION=3.14.1}} |
+---------------+--------------------------------------+
```
