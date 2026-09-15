Categories:
:   [Organization user and organization user group functions](/sql-reference/functions-organization-users)

# IS\_ORGANIZATION\_USER\_GROUP

Returns TRUE if the specified [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) was created when an administrator added an
[organization user group](/user-guide/organization-users#label-org-users-groups) to the account.

## Syntax

Copy code

```
IS_ORGANIZATION_USER_GROUP( '<role>' )
```

## Arguments

`'role'`
:   Role in the current account.

## Returns

Returns TRUE if the specified role was created from or linked to an organization user group.

## Usage notes

In data sharing contexts, this function returns NULL if it is called from a consumer account that exists in a *different organization* than
the provider account. Calling the function from a consumer account in the *same organization* as the provider returns TRUE or FALSE.

## Examples

Determine if the role `data_stewards` in the current account was created from an organization user group.

Copy code

```
SELECT IS_ORGANIZATION_USER_GROUP('data_stewards');
```
