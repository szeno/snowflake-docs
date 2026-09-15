# REVOKE SERVICE ROLE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Revokes a service role from an account role, application role, or database role. For more information, see [Managing service-related privileges](/developer-guide/snowpark-container-services/working-with-services#label-spcs-manage-service-related-privileges).

See also:
:   [GRANT SERVICE ROLE](/sql-reference/sql/grant-service-role), [SHOW ROLES IN SERVICE](/sql-reference/sql/show-roles-in-service), [SHOW GRANTS](/sql-reference/sql/show-grants)

## Syntax

Copy code

```
REVOKE SERVICE ROLE <name> FROM
{
  ROLE <role_name>                     |
  APPLICATION ROLE <application_role_name>  |
  DATABASE ROLE <database_role_name>
}
```

## Parameters

`name`
:   Specifies the identifier for the service role to revoke. If the identifier contains spaces or special
    characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    Specify the service role name in the following format:

    > `service-name!service-role-name`

    For example, `echo_service!echoendpoint_role`.

`ROLE role_name`
:   Name of the account role to revoke the service role from.

`APPLICATION ROLE application_role`
:   Name of the application role to revoke the service role from.

`DATABASE ROLE database_name`
:   Name of the database role to revoke the service role from.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege or role | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Service | Only the service owner can revoke the service role. |

Expand

Show lessSee more

## Examples

The following command revokes the `echoendpoint_role` service role defined in the `echo_service` service specification from the `service_function_user_role` role.

Copy code

```
REVOKE SERVICE ROLE echo_service!echoendpoint_role FROM ROLE service_function_user_role;
```
