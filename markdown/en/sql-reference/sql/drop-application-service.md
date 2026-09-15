# DROP APPLICATION SERVICE

Removes the specified
[Application Service](/sql-reference/sql/create-application-service)
from the current or specified schema and stops its containers.

See also:
:   [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service) ,
    [ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service) ,
    [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service) ,
    [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services)

## Syntax

Copy code

```
DROP APPLICATION SERVICE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier of the Application Service to drop.

## Access control requirements

Your role must have the following [privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on objects:

| Privilege | Object |
| --- | --- |
| OWNERSHIP | Application Service that you remove |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Dropping an Application Service stops and deletes its containers. The
  underlying package in the artifact repository isn’t affected.
- Grants on the service are revoked automatically when the service is dropped.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Copy code

```
DROP APPLICATION SERVICE IF EXISTS my_app;
```
