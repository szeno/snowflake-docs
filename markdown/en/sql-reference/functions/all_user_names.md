Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# ALL\_USER\_NAMES

Returns all user names in the current account.

## Syntax

Copy code

```
ALL_USER_NAMES()
```

## Arguments

None.

## Returns

The data type of the returned value is `ARRAY`.

## Usage notes

- Users with any active role can retrieve the list of all usernames in the current account. However, simply knowing the usernames does not
  allow a role the ability to perform further actions on the users. User management requires a minimum set of privileges.
- Usernames (i.e. the `NAME` property value) are the unique identifier of the user object in Snowflake, while login names (i.e. the `LOGIN_NAME` property value) are used to authenticate to Snowflake. Usernames are not sensitive data and are returned by other commands and functions (e.g. [SHOW GRANTS](/sql-reference/sql/show-grants)). Login names are sensitive data.
- As a best practice, username and login name values should be different. To update existing username or login name values, execute the [ALTER USER](/sql-reference/sql/alter-user) command. When creating new users with the [CREATE USER](/sql-reference/sql/create-user) command, ensure that the `NAME` and `LOGIN_NAME` values are different.

## Examples

Return all user names for the current account.

> Copy code
>
> ```
> select all_user_names();
>
> +---------------------------+
> | ALL_USER_NAMES()          |
> +---------------------------+
> | [ "user1", "user2", ... ] |
> +---------------------------+
> ```
