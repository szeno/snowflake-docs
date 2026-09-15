# SHOW USER KEY PAIRS

Lists the named [key pairs](/user-guide/key-pair-auth) associated with a user.

See also:
:   [ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair),
    [ALTER USER … MODIFY KEY PAIR](/sql-reference/sql/alter-user-modify-key-pair),
    [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair),
    [ALTER USER … REMOVE KEY PAIR](/sql-reference/sql/alter-user-remove-key-pair)

## Syntax

Copy code

```
SHOW USER KEY PAIRS [ FOR USER <username> ]
```

## Parameters

`FOR USER username`
:   Lists the key pairs for the specified user.

    Default: Lists the key pairs for the current user.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

The command output includes the following columns, which provide properties and metadata for each key pair:

| Column | Description |
| --- | --- |
| `name` | The name of the key pair. Rotated-out key pairs are shown with a suffix of the form `_ROTATED_<epoch_ms>`, where `<epoch_ms>` is the rotation time as a Unix epoch millisecond integer. |
| `user_name` | The username associated with the key pair. |
| `fingerprint` | The SHA-256 fingerprint of the public key. |
| `role_scope` | The name of the role that the key pair inherits privileges from, or NULL if none is set. |
| `status` | The status of the key pair. One of:  - `ACTIVE`: The key pair can be used for authentication. - `EXPIRED`: The key pair has passed its expiration time and cannot be used for authentication. - `DISABLED`: The key pair has been explicitly disabled and cannot be used for authentication.   If a key pair is both disabled and past its expiration time, the status is reported as `DISABLED`. |
| `comment` | A user-provided comment about the key pair. |
| `created_on` | The date when the key pair was registered. |
| `created_by` | The username of the user who registered the key pair, or the user ID if that user has since been removed. |
| `last_used_on` | The date and time when the key pair was most recently used to authenticate, or NULL if the key pair has never been used. |
| `expires_at` | The date and time when the key pair expires, or NULL if no expiration time is set. |
| `rotated_to` | For a rotated-out key pair, the name of the key pair that replaced it. NULL for active key pairs. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required only when listing key pairs for a user other than yourself. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command lists all key pairs for a given user, not all key pairs in the account.
- The public key is returned only via the `fingerprint` column. The raw public key value is not echoed back.
- Rotated-out key pairs are listed until they expire.

## Examples

Show information about the key pairs associated with the user `example_user`:

Copy code

```
SHOW USER KEY PAIRS FOR USER example_user;
```
