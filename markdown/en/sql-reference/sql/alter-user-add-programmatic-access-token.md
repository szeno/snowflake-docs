# ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)

Creates a [programmatic access token](/user-guide/programmatic-access-tokens) for a user.

See also:
:   [ALTER USER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-modify-programmatic-access-token) ,
    [ALTER USER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-rotate-programmatic-access-token) ,
    [ALTER USER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-remove-programmatic-access-token) ,
    [SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] ADD { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF NOT EXISTS ] <token_name>
  [ ROLE_RESTRICTION = '<string_literal>' ]
  [ DAYS_TO_EXPIRY = <integer> ]
  [ MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT = <integer> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`ADD { PROGRAMMATIC ACCESS TOKEN | PAT } token_name`
:   Creates a programmatic access token with the specified name.

    You can use the keyword PAT as a shorter way of specifying the keywords PROGRAMMATIC ACCESS TOKEN.

## Optional parameters

`IF NOT EXISTS`
:   Creates the programmatic access token only if a token with the specified name doesn’t already exist for the user. If a token
    with the same name already exists, the command does nothing and completes successfully without creating a new token or
    returning a token secret.

    Use this clause to run the command idempotently, for example when re-running a provisioning script.

`username`
:   The name of the user that the token is associated with. A user cannot use another user’s programmatic access token to
    authenticate.

    To create programmatic access tokens on behalf of a user, administrators must specify the name of that user in the ALTER USER
    command.

    If `username` is omitted, the command generates a programmatic access token for the user who is currently logged in (the
    active user of this session).

`ROLE_RESTRICTION = 'string_literal'`
:   The name of the role used for privilege evaluation and object creation. This must be one of the roles that has already been
    granted to the user.

    Note

    By default, this parameter is required for service users (TYPE=SERVICE or TYPE=LEGACY\_SERVICE) and optional for person users
    (TYPE=PERSON or TYPE=NULL). An authentication policy can be configured to change this behavior, see [Configuring role restrictions for programmatic access tokens](/user-guide/programmatic-access-tokens#label-pat-configure-role-restrictions).

    If the user is subject to an authentication policy with a BLOCKED\_ROLES\_LIST, the specified role cannot be one of
    the blocked roles. See [Blocking specific roles](/user-guide/programmatic-access-tokens#label-pat-configure-blocked-roles).

    When you use this token for authentication, any objects that you create are owned by this role, and this role is used for
    privilege evaluation.

    Note

    Secondary roles are not used, even if [DEFAULT\_SECONDARY\_ROLES](/sql-reference/sql/create-user#label-create-user-default-secondary-roles) is set to
    (‘ALL’) for the user.

    If this role is revoked from the user associated with the programmatic access token, any attempts to use the token for
    authentication will fail.

    Note

    Specifying a role as the ROLE\_RESTRICTION value does not grant the specified role to the programmatic access token. The user
    must have already been granted this role.

    If you omit ROLE\_RESTRICTION, any objects that you create owned by your primary role, and privileges are evaluated against
    your primary and secondary roles (as explained in [Authorization through primary role and secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement)).

`DAYS_TO_EXPIRY = integer`
:   The number of days that the programmatic access token can be used for authentication.

    You can specify a value ranging from `1` to the [maximum expiration time](/user-guide/programmatic-access-tokens#label-pat-maximum-expiration-time).

    Default: `15`

`MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT = integer`
:   The number of minutes during which a user can use this token to access Snowflake without being subject to an active
    [network policy](/user-guide/network-policies).

    You can set this for a token for a person (if the USER object has TYPE=PERSON) if that person is not subject to a network policy
    but needs to use a programmatic access token for authentication. See [Network policy requirements](/user-guide/programmatic-access-tokens#label-pat-prerequisites-network).

    Note

    Setting MINS\_TO\_BYPASS\_NETWORK\_POLICY\_REQUIREMENT does not allow users to bypass the network policy itself.

    You can set this to a value in the range of `1` to `1440` (1 day).

    Default: `0`

`COMMENT = 'string_literal'`
:   Descriptive comment about the programmatic access token. This comment is displayed in the
    [list of programmatic access tokens](/user-guide/programmatic-access-tokens#label-pat-list) in Snowsight.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required only when generating a programmatic access token for a user other than yourself. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command output provides information about the newly generated programmatic access token in the following columns:

| Column | Description |
| --- | --- |
| `token_name` | Name of the generated token. |
| `token_secret` | The token itself. Use this to authenticate to an endpoint. Note The token only appears in the output of the ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN command. No other SQL command or function prints out or returns the token. If you need to access this token programmatically, you can use [Snowflake Scripting](/developer-guide/snowflake-scripting/index) to execute this command and retrieve the token from the [RESULTSET](/developer-guide/snowflake-scripting/resultsets). |

Expand

Show lessSee more

## Usage notes

- Each user can have a maximum of 15 programmatic access tokens.
  - This number includes [tokens that have been disabled](/user-guide/programmatic-access-tokens#label-pat-disabled).
  - This number does not include tokens that have expired.

## Examples

Create a programmatic access token named `example_token` that is associated with the user `example_user`, and inherits all
privileges from the associated user:

Copy code

```
ALTER USER IF EXISTS example_user ADD PROGRAMMATIC ACCESS TOKEN example_token
  COMMENT = 'a reference example';
```

Create a programmatic access token named `example_token` that is associated with the user `example_user`, inherits all
privileges from the role `example_role`, and expires after 15 days:

Copy code

```
ALTER USER IF EXISTS example_user ADD PROGRAMMATIC ACCESS TOKEN example_token
  ROLE_RESTRICTION = 'example_role'
  DAYS_TO_EXPIRY = 15;
```

Create a programmatic access token named `example_token` only if a token with that name doesn’t already exist for the user
`example_user`. If the token already exists, the command completes successfully without creating a new token:

Copy code

```
ALTER USER IF EXISTS example_user ADD PROGRAMMATIC ACCESS TOKEN IF NOT EXISTS example_token;
```
