# DESCRIBE NETWORK RULE

Describes the properties specified for a network rule.

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP NETWORK RULE](/sql-reference/sql/drop-network-rule) , [ALTER NETWORK RULE](/sql-reference/sql/alter-network-rule) , [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) , [SHOW NETWORK RULES](/sql-reference/sql/show-network-rules)

## Syntax

Copy code

```
DESC[RIBE] NETWORK RULE <name>
```

## Parameters

`name`
:   Specifies the identifier for the network rule you want to describe.

    If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are case-sensitive.

## Output

The command output provides network rule properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the network rule was created. |
| `name` | Name of the network rule. |
| `database_name` | Database that contains the schema in which the network rule was created. |
| `schema_name` | Schema in which the network rule was created. |
| `owner` | Role that has the OWNERSHIP privilege on the network rule. |
| `comment` | Descriptive text associated with the network rule. |
| `type` | Value of the network rule’s `TYPE` property. |
| `mode` | Value of the network rule’s `MODE` property. |
| `value_list` | Network identifiers defined in the `VALUE_LIST` property of the network rule. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Network Rule | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

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

## Example

Describe a network rule named `myrule`:

> Copy code
>
> ```
> DESC NETWORK RULE myrule;
> ```
