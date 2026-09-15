# ALTER USER … ADD KEY PAIR

Registers a named [key pair](/user-guide/key-pair-auth) for a user.

See also:
:   [ALTER USER … MODIFY KEY PAIR](/sql-reference/sql/alter-user-modify-key-pair) ,
    [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair) ,
    [ALTER USER … REMOVE KEY PAIR](/sql-reference/sql/alter-user-remove-key-pair) ,
    [SHOW USER KEY PAIRS](/sql-reference/sql/show-user-key-pairs)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] ADD KEY PAIR <key_pair_name>
  PUBLIC_KEY = '<string_literal>'
  [ ROLE_RESTRICTION = '<string_literal>' ]
  [ DAYS_TO_EXPIRY = <integer> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`ADD KEY PAIR key_pair_name`
:   Registers a key pair with the specified name.

    The names `PUBLIC_KEY_1` and `PUBLIC_KEY_2` are reserved for keys assigned with the legacy `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` user properties (see [ALTER USER](/sql-reference/sql/alter-user)) and can’t be used as a key pair name.

`PUBLIC_KEY = 'string_literal'`
:   The user’s public key, used for [key pair authentication](/user-guide/key-pair-auth). The public key must be unique among all of the user’s active keys.

## Optional parameters

`username`
:   The name of the user that the key pair is associated with. A user cannot authenticate with another user’s key pair.

    To register a key pair on behalf of another user, administrators must specify the name of that user in the ALTER USER command.

    If `username` is omitted, the command registers the key pair for the user who is currently logged in (the active user of this session).

`ROLE_RESTRICTION = 'string_literal'`
:   The name of the role used for privilege evaluation when a session is authenticated with this key pair. This must be one of the roles that has already been granted to the user.

    When ROLE\_RESTRICTION is set, the key pair can only be used to authenticate if the role requested in the JWT matches this role. If this role is revoked from the user associated with the key pair, any attempts to use the key pair for authentication will fail.

    Note

    Specifying a role as the ROLE\_RESTRICTION value does not grant the specified role to the key pair. The user must have already been granted this role.

    If you omit ROLE\_RESTRICTION, any objects that you create are owned by your primary role, and privileges are evaluated against your primary and secondary roles (as explained in [Authorization through primary role and secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement)).

`DAYS_TO_EXPIRY = integer`
:   The number of days that the key pair can be used for authentication. Must be `1` or greater.

    Default: No value (the key pair has no expiration and remains valid until rotated, disabled, or removed).

`COMMENT = 'string_literal'`
:   Specifies a comment for the key pair.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required to register a key pair. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Each user can have a maximum of 10 key pairs by default. Rotated-out key pairs that are still within their grace period count toward this limit until they expire.
- Both RSA and EC public keys are supported. For EC keys, only the `P-256`, `P-384`, and `P-521` curves are accepted.
- Creating a key pair does not return a secret. The user retains the matching private key, Snowflake only stores the public key.

## Examples

Register a key pair named `my_key` for the user `example_user`:

Copy code

```
ALTER USER IF EXISTS example_user ADD KEY PAIR my_key
  PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgK...'
  COMMENT = 'primary workload key';
```

Register a key pair that inherits privileges from the role `example_role` and expires after 90 days:

Copy code

```
ALTER USER IF EXISTS example_user ADD KEY PAIR scoped_key
  PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgK...'
  ROLE_RESTRICTION = 'example_role'
  DAYS_TO_EXPIRY = 90;
```
