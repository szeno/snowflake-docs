# ALTER USER … REMOVE KEY PAIR

Removes a named [key pair](/user-guide/key-pair-auth) from a user.

See also:
:   [ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair) ,
    [ALTER USER … MODIFY KEY PAIR](/sql-reference/sql/alter-user-modify-key-pair) ,
    [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair) ,
    [SHOW USER KEY PAIRS](/sql-reference/sql/show-user-key-pairs)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] REMOVE KEY PAIR <key_pair_name>
```

## Parameters

`username`
:   The name of the user that the key pair is associated with.

    If you omit this parameter, the command removes the key pair for the user who is currently logged in (the active user in the current session).

`REMOVE KEY PAIR key_pair_name`
:   Removes the named key pair.

    The names `PUBLIC_KEY_1` and `PUBLIC_KEY_2` are reserved for keys assigned with the legacy `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` user properties and can’t be removed through this command. Use [ALTER USER … UNSET RSA\_PUBLIC\_KEY](/sql-reference/sql/alter-user) to remove those legacy keys.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required to remove a key pair. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You cannot use a removed key pair for authentication.
- You cannot recover a removed key pair. To reinstate the same public key, run [ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair) again with the desired public key.
- The removed key pair’s name becomes available immediately and can be reused in a subsequent ALTER USER … ADD KEY PAIR. (Rotated-out key pairs, by contrast, retain their `_ROTATED_<epoch_ms>` tombstone name until they expire.)
- If you only want to temporarily block a key pair from being used for authentication, use [ALTER USER … MODIFY KEY PAIR … SET DISABLED = TRUE](/sql-reference/sql/alter-user-modify-key-pair) instead.

## Examples

Remove a key pair named `my_key` from the user `example_user`:

Copy code

```
ALTER USER IF EXISTS example_user REMOVE KEY PAIR my_key;
```
