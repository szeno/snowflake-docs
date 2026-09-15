Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$SET\_EVENT\_SHARING\_ACCOUNT\_FOR\_REGION

Sets the event account for a region.

See also:
:   [SYSTEM$UNSET\_EVENT\_SHARING\_ACCOUNT\_FOR\_REGION](/sql-reference/functions/system_unset_event_sharing_account_for_region)

## Syntax

Copy code

```
SYSTEM$SET_EVENT_SHARING_ACCOUNT_FOR_REGION( '<snowflake_region>' , '<region_group>' , '<account_name>' )
```

## Arguments

`snowflake_region`
:   Specifies the region where the account is located, for example: `AWS_US_WEST_2, AWS_US_EAST_1`.

`region_group`
:   Specifies the region group, for example: `PUBLIC`. Refer to
    [Region groups](/user-guide/admin-account-identifier#label-region-groups) for details.

`account_name`
:   Specifies the account name. If another account is already set as the events account in the
    specified region, calling this function changes the events account to be the account
    specified here.

## Access control requirements

- Only [organization administrators](/user-guide/organization-administrators) can execute this SQL function.

## Examples

Copy code

```
SELECT SYSTEM$SET_EVENT_SHARING_ACCOUNT_FOR_REGION('aws_us_west_2', 'public', 'myaccount');
```
