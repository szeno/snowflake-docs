# DROP GATEWAY

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Removes the specified [gateway](/developer-guide/snowpark-container-services/gateway) from the current
or specified schema.

See also:
:   [CREATE GATEWAY](/sql-reference/sql/create-gateway) , [ALTER GATEWAY](/sql-reference/sql/alter-gateway), [SHOW GATEWAYS](/sql-reference/sql/show-gateways) , [DESCRIBE GATEWAY](/sql-reference/sql/desc-gateway)

## Syntax

Copy code

```
DROP GATEWAY [ IF EXISTS ] <name>
```

## Required parameters

`name`
:   Specifies the identifier for the gateway to be dropped.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Gateway | Required to drop the gateway. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

The following example drops the gateway named `split_gateway`:

Copy code

```
DROP GATEWAY split_gateway;
```

```
+-------------------------------------+
| status                              |
|-------------------------------------|
| SPLIT_GATEWAY successfully dropped. |
+-------------------------------------+
```
