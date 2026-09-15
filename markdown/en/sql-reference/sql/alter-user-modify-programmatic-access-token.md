# ALTER USER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)

Changes the name of a [programmatic access token](/user-guide/programmatic-access-tokens) or a property of the token.

Note

You cannot modify or rename a programmatic access token in a session where you used a programmatic access token for
authentication.

See also:
:   [ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-add-programmatic-access-token) ,
    [ALTER USER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-rotate-programmatic-access-token) ,
    [ALTER USER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-remove-programmatic-access-token) ,
    [SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] MODIFY { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF EXISTS ] <token_name>
  RENAME TO <new_token_name>

ALTER USER [ IF EXISTS ] [ <username> ] MODIFY { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF EXISTS ] <token_name> SET
  [ DISABLED = { TRUE | FALSE } ]
  [ MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT = <integer> ]
  [ COMMENT = '<string_literal>' ]

ALTER USER [ IF EXISTS ] [ <username> ] MODIFY { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF EXISTS ] <token_name> UNSET
  [ DISABLED ]
  [ MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT ]
  [ COMMENT ]
```

## Parameters

`username`
:   The name of the user that the token is associated with.

    If `username` is omitted, the command modifies the programmatic access token for the user who is currently logged in
    (the active user of this session).

`MODIFY { PROGRAMMATIC ACCESS TOKEN | PAT } token_name`
:   Modifies a programmatic access token with the specified name.

    You can use the keyword PAT as a shorter way of specifying the keywords PROGRAMMATIC ACCESS TOKEN.

`IF EXISTS`
:   Modifies the programmatic access token only if a token with the specified name exists for the user. If no token with that
    name exists, the command does nothing and completes successfully instead of returning an error.

`RENAME TO new_token_name`
:   Specifies a new name for a programmatic access token.

`SET ...`
:   Specifies one (or more) properties to set for the programmatic access token (separated by blank spaces, commas, or new lines).

    `DISABLED = { TRUE | FALSE }`
    :   Disables or enables the programmatic access token.

        If a user is disabled or Snowflake locks a user, the programmatic tokens associated with that user are disabled automatically.
        If the user is subsequently enabled or Snowflake unlocks the user, the programmatic access tokens remain disabled. To enable
        the tokens again, set DISABLED to FALSE.

        For information, see [Re-enabling a disabled programmatic access token](/user-guide/programmatic-access-tokens#label-pat-disabled).

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

`UNSET ...`
:   Unsets one or more specified properties or parameters for the programmatic access token, which resets the properties to their
    defaults:

    - `DISABLED`
    - `MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT`
    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required only when modifying a programmatic access token for a human user other than yourself or a service user. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

You cannot modify or rename a programmatic access token in a session where you used a programmatic access token for
authentication.

## Examples

Change the name of a programmatic access token associated with the user `example_user`:

Copy code

```
ALTER USER IF EXISTS example_user MODIFY PROGRAMMATIC ACCESS TOKEN old_token_name
  RENAME TO new_token_name;
```

Change the comment associated with a programmatic access token:

Copy code

```
ALTER USER IF EXISTS example_user MODIFY PROGRAMMATIC ACCESS TOKEN token_name
  SET COMMENT = 'my new comment';
```
