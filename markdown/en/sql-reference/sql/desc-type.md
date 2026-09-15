# DESCRIBE TYPE

Describes a [user-defined type](/sql-reference/data-types-user-defined).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE TYPE](/sql-reference/sql/create-type) , [ALTER TYPE](/sql-reference/sql/alter-type) , [SHOW TYPES](/sql-reference/sql/show-types) , [DROP TYPE](/sql-reference/sql/drop-type) , [UNDROP TYPE](/sql-reference/sql/undrop-type)

## Syntax

Copy code

```
{ DESC | DESCRIBE } TYPE <name>
```

## Parameters

`name`
:   Specifies the identifier for the user-defined type to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The command output provides user-defined type properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Name of the user-defined type. |
| `type` | Snowflake type definition that is the base type for the user-defined type. |
| `created_on` | Date and time when the user-defined type was created. |
| `database_name` | Database in which the user-defined type is stored. |
| `schema_name` | Schema in which the user-defined type is stored. |
| `owner` | Name of the role that owns the user-defined type, which is the role that has the OWNERSHIP privilege on the user-defined type. |
| `comment` | The comment set for the type, if any; otherwise, it is `NULL`. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any | User-defined type |  |

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

Use the DESCRIBE TYPE command to list details about the `age` user-defined type:

Copy code

```
DESC TYPE age;
```

```
+------+-------------+-------------------------------+---------------+-------------+--------------+---------+
| name | type        | created_on                    | database_name | schema_name | owner        | comment |
|------+-------------+-------------------------------+---------------+-------------+--------------+---------|
| AGE  | NUMBER(3,0) | 2025-11-06 09:23:59.882 -0800 | MY_DB         | MY_SCHEMA   | MY_ROLE      | NULL    |
+------+-------------+-------------------------------+---------------+-------------+--------------+---------+
```
