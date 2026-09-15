# DROP EXTERNAL CONSUMER

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Removes an external consumer from the account. Dropping an external consumer immediately revokes access for any listings
that were shared with that consumer.

See also:
:   [CREATE EXTERNAL CONSUMER](/sql-reference/sql/create-external-consumer) ,
    [ALTER EXTERNAL CONSUMER](/sql-reference/sql/alter-external-consumer) ,
    [SHOW EXTERNAL CONSUMERS](/sql-reference/sql/show-external-consumers) ,
    [DESCRIBE EXTERNAL CONSUMER](/sql-reference/sql/desc-external-consumer)

## Syntax

Copy code

```
DROP EXTERNAL CONSUMER [ IF EXISTS ] <name>
```

## Parameters

`IF EXISTS`
:   Drops the external consumer only if one with the specified name exists. If no external consumer with that name exists, the command
    does nothing and completes successfully instead of returning an error.

`name`
:   Specifies the identifier for the external consumer to drop.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External Consumer | Required to drop the external consumer. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Dropping an external consumer revokes access to all listings shared with that consumer. The listings themselves are not affected.
- All Programmatic Access Tokens associated with the external consumer are invalidated when the consumer is dropped.
- Dropped external consumers cannot be recovered.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop an external consumer:

Copy code

```
DROP EXTERNAL CONSUMER acme_consumer;
```

Drop an external consumer if it exists:

Copy code

```
DROP EXTERNAL CONSUMER IF EXISTS acme_consumer;
```
