# DESCRIBE NETWORK POLICY

Describes the properties specified for a network policy.

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP NETWORK POLICY](/sql-reference/sql/drop-network-policy) , [ALTER NETWORK POLICY](/sql-reference/sql/alter-network-policy) , [CREATE NETWORK POLICY](/sql-reference/sql/create-network-policy) , [SHOW NETWORK POLICIES](/sql-reference/sql/show-network-policies)

## Syntax

Copy code

```
DESC[RIBE] NETWORK POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the network policy to describe. If the identifier contains spaces or special characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Only the network policy owner (i.e. role with the OWNERSHIP privilege on the network policy) or higher can execute this command.

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

Describe a network policy named `mypolicy`:

> Copy code
>
> ```
> DESC NETWORK POLICY mypolicy;
> ```
>
> ```
> -----------------+---------------+
>       name       |     value     |
> -----------------+---------------+
>  ALLOWED_IP_LIST | 192.168.0.100 |
>  BLOCKED_IP_LIST | 192.168.0.101 |
> -----------------+---------------+
> ```
