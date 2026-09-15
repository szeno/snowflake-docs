# SHOW USER PROGRAMMATIC ACCESS TOKENS FOR EXTERNAL CONSUMER

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists the Programmatic Access Tokens (PATs) associated with an external consumer.

See also:
:   [ALTER EXTERNAL CONSUMER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-remove-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-rotate-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-modify-programmatic-access-token)

## Syntax

Copy code

```
SHOW USER PROGRAMMATIC ACCESS TOKENS FOR EXTERNAL CONSUMER <name>
```

Alias:

Copy code

```
SHOW USER PATS FOR EXTERNAL CONSUMER <name>
```

## Parameters

`name`
:   Specifies the identifier for the external consumer whose tokens you want to list.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or USAGE | External Consumer | Required to list the PATs for the external consumer. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

- Token secrets are never returned by this command. To obtain a token secret, use [ALTER EXTERNAL CONSUMER … ADD PAT](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token) or [ALTER EXTERNAL CONSUMER … ROTATE PAT](/sql-reference/sql/alter-external-consumer-rotate-programmatic-access-token).

## Examples

List all PATs for an external consumer:

Copy code

```
SHOW USER PROGRAMMATIC ACCESS TOKENS FOR EXTERNAL CONSUMER acme_consumer;
```

Using the alias:

Copy code

```
SHOW USER PATS FOR EXTERNAL CONSUMER acme_consumer;
```
