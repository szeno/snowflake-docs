# SHOW MAINTENANCE POLICIES

Lists the [maintenance policies](/developer-guide/native-apps/consumer-maintenance-policies) applied to the specified account or app.

See also:
:   [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy), [ALTER MAINTENANCE POLICY](/sql-reference/sql/alter-maintenance-policy), [DROP MAINTENANCE POLICY](/sql-reference/sql/drop-maintenance-policy)

## Syntax

Copy code

```
SHOW MAINTENANCE POLICIES { ON | IN } { ACCOUNT | APPLICATION <app_name> | <entity_type> <entity_name> }
```

`ACCOUNT`
:   Shows the maintenance policies applied to the account.

`{APPLICATION <app_name>}`
:   Shows the maintenance policies applied to the specified app.

## Parameters

`{ ON | IN }`
:   Specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `APPLICATION app_name`
    :   Returns records for the specified app.

    `IN entity_type entity_name`
    :   Returns records for the specified entity. Specify one of the following for the `entity_type`:

        - `DATABASE`
        - `APPLICATION PACKAGE`
        - `SCHEMA`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY MAINTENANCE POLICY | Account |  |
| OWNERSHIP | Maintenance policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

## Examples

The following example shows all maintenance policies applied to the account:

Copy code

```
SHOW MAINTENANCE POLICIES ON ACCOUNT;
```

Show maintenance policies for a specific app:

Copy code

```
SHOW MAINTENANCE POLICIES ON APPLICATION my_app;
```

Show maintenance policies for a specific database:

Copy code

```
SHOW MAINTENANCE POLICIES IN DATABASE my_database;
```

Show maintenance policies for a specific app package:

Copy code

```
SHOW MAINTENANCE POLICIES IN APPLICATION PACKAGE my_app_package;
```

Show maintenance policies for a specific schema:

Copy code

```
SHOW MAINTENANCE POLICIES IN SCHEMA my_schema;
```
