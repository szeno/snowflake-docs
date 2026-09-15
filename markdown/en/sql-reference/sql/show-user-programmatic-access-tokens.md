# SHOW USER PROGRAMMATIC ACCESS TOKENS

Lists the [programmatic access tokens](/user-guide/programmatic-access-tokens) associated with a user.

Note

The list includes programmatic access tokens that have expired within the past 30 days. To view information about tokens that
have expired more than 30 days ago, query the [CREDENTIALS view](/sql-reference/account-usage/credentials).

See also:
:   [ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-add-programmatic-access-token) ,
    [ALTER USER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-modify-programmatic-access-token) ,
    [ALTER USER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-rotate-programmatic-access-token) ,
    [ALTER USER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-remove-programmatic-access-token)

## Syntax

Copy code

```
SHOW USER { PROGRAMMATIC ACCESS TOKENS | PATS } [ FOR USER <username> ]
```

You can use the keyword PATS as a shorter way of specifying the keywords PROGRAMMATIC ACCESS TOKENS.

## Parameters

`FOR USER username`
:   Lists the programmatic access tokens for the specified user.

    Default: Lists the programmatic access tokens for the current user.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

The command output includes the following columns, which provide properties and metadata for each programmatic access token:

| Column | Description |
| --- | --- |
| `name` | The name of the programmatic access token. |
| `user_name` | The username associated with the programmatic access token.  If the user associated with the programmatic access token was removed from the account, then Snowflake returns the user ID instead of the username. You can find information about a removed user by using the [USERS view](/sql-reference/account-usage/users) in the [ACCOUNT\_USAGE](/sql-reference/account-usage) schema. |
| `role_restriction` | The name of the role that the programmatic access token inherits privileges from. |
| `expires_at` | The timestamp when the programmatic access token expires. |
| `status` | The status of the programmatic access token. This column can be one of the following values:  - `ACTIVE`: The programmatic access token can be used to authenticate and has not expired yet. - `EXPIRED`: The programmatic access token cannot be used to authenticate because the expiration date has passed. - `DISABLED`: The programmatic access token is [disabled](/user-guide/programmatic-access-tokens#label-pat-disabled) because user login access is disabled or   the user is locked out of logging in. |
| `comment` | A user-provided comment about the programmatic access token. |
| `created_on` | The date when the programmatic access token was created. |
| `created_by` | The username or user ID of the user who created the programmatic access token. |
| `mins_to_bypass_required_network_policy` | The number of minutes during which a user can use this token to access Snowflake without being subject to an active [network policy](/user-guide/network-policies). |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY | User | Required only when displaying programmatic access tokens for a human user other than yourself or a service user. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command lists all programmatic access tokens for a given user, not all programmatic access tokens for an account.
- The programmatic access token secret is never returned after creation.
- After seven days, expired programmatic access tokens are deleted and no longer appear in the output of the command.

## Examples

Show information about programmatic access tokens associated with the user `example_user`:

Copy code

```
SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER example_user;
```
