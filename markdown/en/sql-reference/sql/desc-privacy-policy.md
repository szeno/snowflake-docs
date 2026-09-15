# DESCRIBE PRIVACY POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Describes the properties of a [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE PRIVACY POLICY](/sql-reference/sql/create-privacy-policy) , [ALTER PRIVACY POLICY](/sql-reference/sql/alter-privacy-policy) , [DROP PRIVACY POLICY](/sql-reference/sql/drop-privacy-policy) , [SHOW PRIVACY POLICIES](/sql-reference/sql/show-privacy-policies)

## Syntax

Copy code

```
{ DESC | DESCRIBE } PRIVACY POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the privacy policy to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

> The command output provides privacy policy properties and metadata in the following columns:
>
> | Column | Description |
> | --- | --- |
> | `name` | Name of the privacy policy. |
> | `signature` | Signature of the privacy policy. All privacy policies have the same signature, which does not accept any arguments. |
> | `return_type` | Return type of the privacy policy. All privacy policies return PRIVACY\_BUDGET, which is an internal data type. |
> | `body` | SQL expression that determines whether the privacy policy returns a privacy budget, and if it does, which one. |
>
> Expand
>
> Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY PRIVACY POLICY | Account |  |
| APPLY | Privacy policy |  |
| OWNERSHIP | Privacy policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

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

The following example describes the privacy policy named `myprivpolicy`:

Copy code

```
DESCRIBE PRIVACY POLICY myprivpolicy;
```

```
+--------------------+---------------+--------------------+-----------------------------------------------+
|   name             |   signature   |   return_type      |   body                                        |
+--------------------+---------------+--------------------+-----------------------------------------------+
|   MYPRIVPOLICY     |   ()          |   PRIVACY_BUDGET   |   PRIVACY_BUDGET(BUDGET_NAME=>'new_budget')   |
+--------------------+---------------+--------------------+-----------------------------------------------+
```
