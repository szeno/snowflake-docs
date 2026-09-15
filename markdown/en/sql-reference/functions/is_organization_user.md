Categories:
:   [Organization user and organization user group functions](/sql-reference/functions-organization-users)

# IS\_ORGANIZATION\_USER

Returns TRUE if the argument is a Snowflake user who is an [organization user](/user-guide/organization-users).

## Syntax

Copy code

```
IS_ORGANIZATION_USER( <exp> )
```

## Arguments

`exp`
:   Expression that resolves to the name of a Snowflake user object.

    If passing in the literal name of a user, surround it with single quotes (for example, `'joe'`).

## Returns

Returns TRUE if the argument is an organization user.

## Usage notes

In data sharing contexts, this function returns NULL if it is called from a consumer account that exists in a *different organization* than
the provider account. Calling the function from a consumer account in the *same organization* as the provider returns TRUE or FALSE.

## Examples

Determine if the user `joe` in the current account is an organization user:

Copy code

```
SELECT IS_ORGANIZATION_USER('joe');
```

Determine if the current user in the session is an organization user:

Copy code

```
SELECT IS_ORGANIZATION_USER(CURRENT_USER());
```
