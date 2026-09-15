# ALTER EXTERNAL CONSUMER

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Modifies the properties of an existing external consumer, or manages its Programmatic Access Tokens (PATs).

See also:
:   [CREATE EXTERNAL CONSUMER](/sql-reference/sql/create-external-consumer) ,
    [DROP EXTERNAL CONSUMER](/sql-reference/sql/drop-external-consumer) ,
    [ALTER EXTERNAL CONSUMER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-remove-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-rotate-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-modify-programmatic-access-token) ,
    [SHOW EXTERNAL CONSUMERS](/sql-reference/sql/show-external-consumers)

## Syntax

Copy code

```
ALTER EXTERNAL CONSUMER [ IF EXISTS ] <name> SET
  [ COMMENT = '<string_literal>' ]
  [ EMAIL = '<email_address>' ]
```

Copy code

```
ALTER EXTERNAL CONSUMER [ IF EXISTS ] <name> UNSET
  [ COMMENT ]
  [ EMAIL ]
```

Copy code

```
ALTER EXTERNAL CONSUMER [ IF EXISTS ] <name> RENAME TO <new_name>
```

For PAT operations, see:

- [ALTER EXTERNAL CONSUMER … ADD PAT](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token)
- [ALTER EXTERNAL CONSUMER … REMOVE PAT](/sql-reference/sql/alter-external-consumer-remove-programmatic-access-token)
- [ALTER EXTERNAL CONSUMER … ROTATE PAT](/sql-reference/sql/alter-external-consumer-rotate-programmatic-access-token)
- [ALTER EXTERNAL CONSUMER … MODIFY PAT](/sql-reference/sql/alter-external-consumer-modify-programmatic-access-token)

## Parameters

`IF EXISTS`
:   Applies the change only if an external consumer with the specified name exists. If no external consumer with that name exists,
    the command does nothing and completes successfully instead of returning an error.

`name`
:   Specifies the identifier for the external consumer to modify.

`COMMENT = 'string_literal'`
:   Specifies a new comment for the external consumer.

`EMAIL = 'email_address'`
:   Specifies a new email address for the external consumer.

`RENAME TO new_name`
:   Renames the external consumer to the specified identifier.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External Consumer | Required to modify the properties of the consumer. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Update the comment on an external consumer:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer SET COMMENT = 'Updated contact for Acme Corp';
```

Rename an external consumer:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer RENAME TO acme_corp_consumer;
```

Remove the email from an external consumer:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer UNSET EMAIL;
```
