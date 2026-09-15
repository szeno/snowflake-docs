Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# IS\_INSTANCE\_ROLE\_IN\_SESSION

Verifies whether the user’s active primary or secondary role hierarchy for the session inherits the specified instance role.

See also:
:   [Instance roles](/sql-reference/snowflake-db-classes#label-instance-roles) , [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session) , [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session)

## Syntax

Copy code

```
IS_INSTANCE_ROLE_IN_SESSION( '<instance_name>' , '<instance_role_name>' )
```

## Arguments

`'instance_name'`
:   Specifies the name of the instance.

`'instance_role_name'`
:   Specifies the name of the instance role.

## Returns

- `TRUE` if the current user’s active [primary role or secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) in the session
  inherit the specified instance role.

  When the `DEFAULT_SECONDARY_ROLES` value is `ALL`, any role granted to the user inherits the privileges of the
  specified instance role.
- `FALSE` if the specified instance role is not in the role hierarchy of the user’s current primary or secondary roles.

## Examples

Verify whether the current role for the session inherits the specified instance role:

> Copy code
>
> ```
> USE ROLE my_role;
>
> SELECT IS_INSTANCE_ROLE_IN_SESSION('my_db.my_schema.my_anomaly_detector', 'user');
> ```
>
> ```
> +----------------------------------------------------------------------------+
> | IS_INSTANCE_ROLE_IN_SESSION('MY_DB.MY_SCHEMA.MY_ANOMALY_DETECTOR', 'USER') |
> +----------------------------------------------------------------------------+
> | TRUE                                                                       |
> +----------------------------------------------------------------------------+
> ```
