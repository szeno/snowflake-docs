# ALTER USER … MODIFY KEY PAIR

Changes the name of a [key pair](/user-guide/key-pair-auth) or a property of the key pair.

See also:
:   [ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair) ,
    [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair) ,
    [ALTER USER … REMOVE KEY PAIR](/sql-reference/sql/alter-user-remove-key-pair) ,
    [SHOW USER KEY PAIRS](/sql-reference/sql/show-user-key-pairs)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] MODIFY KEY PAIR <key_pair_name>
  RENAME TO <new_key_pair_name>

ALTER USER [ IF EXISTS ] [ <username> ] MODIFY KEY PAIR <key_pair_name> SET
  [ DISABLED = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]

ALTER USER [ IF EXISTS ] [ <username> ] MODIFY KEY PAIR <key_pair_name> UNSET
  [ DISABLED ]
  [ COMMENT ]
```

## Parameters

`username`
:   The name of the user that the key pair is associated with.

    If `username` is omitted, the command modifies the key pair for the user who is currently logged in (the active user of this session).

`MODIFY KEY PAIR key_pair_name`
:   Modifies the named key pair.

    The names `PUBLIC_KEY_1` and `PUBLIC_KEY_2` are reserved for keys assigned with the legacy `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` user properties and can’t be modified through this command. Use [ALTER USER](/sql-reference/sql/alter-user) to update those legacy keys.

`RENAME TO new_key_pair_name`
:   Specifies a new name for the key pair. The names `PUBLIC_KEY_1` and `PUBLIC_KEY_2` are reserved for keys assigned with the legacy `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` user properties (see [ALTER USER](/sql-reference/sql/alter-user)) and can’t be used as a new name.

`SET ...`
:   Specifies one or more properties to set for the key pair (separated by blank spaces, commas, or new lines):

    `DISABLED = { TRUE | FALSE }`
    :   Disables or enables the key pair. A disabled key pair cannot be used to authenticate, but its metadata is retained and it can later be re-enabled by setting DISABLED to FALSE.

    `COMMENT = '<string_literal>'`
    :   Specifies a comment for the key pair.

`UNSET ...`
:   Unsets one or more properties for the key pair, which resets the properties to their defaults:

    - `DISABLED`
    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required to modify a key pair. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t change the public key, role restriction, or expiration time with MODIFY KEY PAIR. To change the public key, use [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair). To change any other property, remove the key pair and create a new one.

## Examples

Rename a key pair associated with the user `example_user`:

Copy code

```
ALTER USER IF EXISTS example_user MODIFY KEY PAIR old_key_name
  RENAME TO new_key_name;
```

Disable a key pair so that it can no longer be used for authentication:

Copy code

```
ALTER USER IF EXISTS example_user MODIFY KEY PAIR my_key
  SET DISABLED = TRUE;
```

Change the comment associated with a key pair:

Copy code

```
ALTER USER IF EXISTS example_user MODIFY KEY PAIR my_key
  SET COMMENT = 'updated key description';
```
