# ALTER USER … ROTATE KEY PAIR

Rotates a [key pair](/user-guide/key-pair-auth) by replacing the stored public key with a new public key supplied by the user. The original key pair’s name is preserved for the new key. The prior key is retained for a configurable grace period so that in-flight clients can transition without downtime.

The prior key is retained under a generated name of the form `<key_pair_name>_ROTATED_<epoch_ms>`, where `<epoch_ms>` is the rotation time as a Unix epoch millisecond integer. The prior key is set to expire after the configured number of hours (or disabled immediately if `EXPIRE_ROTATED_KEY_PAIR_AFTER_HOURS = 0`). You can inspect the prior key using [SHOW USER KEY PAIRS](/sql-reference/sql/show-user-key-pairs).

Comment, expiration duration, and role restriction are inherited from the rotated key pair.

See also:
:   [ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair) ,
    [ALTER USER … MODIFY KEY PAIR](/sql-reference/sql/alter-user-modify-key-pair) ,
    [ALTER USER … REMOVE KEY PAIR](/sql-reference/sql/alter-user-remove-key-pair) ,
    [SHOW USER KEY PAIRS](/sql-reference/sql/show-user-key-pairs)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] ROTATE KEY PAIR <key_pair_name>
  PUBLIC_KEY = '<string_literal>'
  [ EXPIRE_ROTATED_KEY_PAIR_AFTER_HOURS = <integer> ]
```

## Required parameters

`ROTATE KEY PAIR key_pair_name`
:   Rotates the named key pair.

    The names `PUBLIC_KEY_1` and `PUBLIC_KEY_2` are reserved for keys assigned with the legacy `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` user properties and can’t be rotated through this command. Use [ALTER USER … SET RSA\_PUBLIC\_KEY](/sql-reference/sql/alter-user) to update those legacy keys.

`PUBLIC_KEY = 'string_literal'`
:   The new public key to associate with `key_pair_name`. The public key must be unique among all of the user’s active keys.

## Optional parameters

`username`
:   The name of the user that the key pair is associated with.

    If you omit this parameter, the command rotates the key pair for the user who is currently logged in (the active user in the current session).

`EXPIRE_ROTATED_KEY_PAIR_AFTER_HOURS = integer`
:   Sets the expiration time of the prior key pair (the rotated-out key), in hours.

    You can set this to a value of `0` to disable the prior key pair immediately.

    You can set this to a value in the range of `0` to the number of hours remaining before the current key pair expires.

    Default: `24`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required to rotate a key pair. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- During the grace period, both the new key and the prior (renamed) key are stored, and both count toward the per-user limit of 10 key pairs. A user that is already at the limit cannot rotate a key until rotated-out tombstones expire.
- You cannot rotate a key pair that has itself already been rotated (a `<name>_ROTATED_<epoch_ms>` tombstone key). Rotate the active key pair with the original name instead.

## Examples

Rotate a key pair associated with the user `example_user`, allowing clients up to 24 hours to pick up the new key:

Copy code

```
ALTER USER IF EXISTS example_user ROTATE KEY PAIR my_key
  PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgK...';
```

Rotate a key pair and immediately expire the prior key pair (useful when responding to a suspected private-key compromise):

Copy code

```
ALTER USER IF EXISTS example_user ROTATE KEY PAIR my_key
  PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgK...'
  EXPIRE_ROTATED_KEY_PAIR_AFTER_HOURS = 0;
```
