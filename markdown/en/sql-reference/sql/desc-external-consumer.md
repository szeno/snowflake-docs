# DESCRIBE EXTERNAL CONSUMER

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Describes an external consumer, including its properties and current configuration.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE EXTERNAL CONSUMER](/sql-reference/sql/create-external-consumer) ,
    [ALTER EXTERNAL CONSUMER](/sql-reference/sql/alter-external-consumer) ,
    [DROP EXTERNAL CONSUMER](/sql-reference/sql/drop-external-consumer) ,
    [SHOW EXTERNAL CONSUMERS](/sql-reference/sql/show-external-consumers)

## Syntax

Copy code

```
{ DESC | DESCRIBE } EXTERNAL CONSUMER <name>
```

## Parameters

`name`
:   Specifies the identifier for the external consumer to describe.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or USAGE | External Consumer | Required to describe the external consumer. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Describe an external consumer:

Copy code

```
DESC EXTERNAL CONSUMER acme_consumer;
```
