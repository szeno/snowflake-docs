# DESCRIBE APPLICATION SERVICE

Describes the properties of an
[Application Service](/sql-reference/sql/create-application-service),
including the deployed package and version and lifecycle state.

`DESC` is an alias for `DESCRIBE`.

See also:
:   [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service) ,
    [ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service) ,
    [DROP APPLICATION SERVICE](/sql-reference/sql/drop-application-service) ,
    [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services)

## Syntax

Copy code

```
{ DESC | DESCRIBE } APPLICATION SERVICE <name>
```

## Parameters

`name`
:   Specifies the identifier for the Application Service.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR or USAGE | Application Service | Required to view service properties and status. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

`DESCRIBE APPLICATION SERVICE` returns a single row with the same columns as
[SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services#label-show-application-services-output).

## Examples

Copy code

```
DESCRIBE APPLICATION SERVICE my_app;
```
