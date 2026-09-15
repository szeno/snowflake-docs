# DESCRIBE RESTRICTED SESSION SCOPE

Describes the properties of a [restricted session scope](/user-guide/restricted-session-scope),
including the YAML definition body.

DESCRIBE can be abbreviated to DESC. `RSS` is a shorthand alias for `RESTRICTED SESSION SCOPE`. You
can use either form in this statement.

See also:
:   [CREATE RESTRICTED SESSION SCOPE](/sql-reference/sql/create-restricted-session-scope) ,
    [ALTER RESTRICTED SESSION SCOPE](/sql-reference/sql/alter-restricted-session-scope) ,
    [DROP RESTRICTED SESSION SCOPE](/sql-reference/sql/drop-restricted-session-scope) ,
    [SHOW RESTRICTED SESSION SCOPES](/sql-reference/sql/show-restricted-session-scopes)

## Syntax

Copy code

```
{ DESCRIBE | DESC } { RESTRICTED SESSION SCOPE | RSS } <name>
```

## Parameters

`name`
:   Identifier for the restricted session scope to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| USAGE, MODIFY, or OWNERSHIP | Restricted session scope |

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

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the restricted session scope was created. |
| `name` | Name of the restricted session scope. |
| `comment` | Comment for the restricted session scope, if any. |
| `definition` | YAML document that defines the privilege ceiling. |

Expand

Show lessSee more

## Example

Copy code

```
DESC RESTRICTED SESSION SCOPE mydb.governance.agent_scope;
```
