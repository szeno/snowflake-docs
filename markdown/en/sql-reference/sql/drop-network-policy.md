# DROP NETWORK POLICY

Removes the specified network policy from the system.

Note

Only security administrators (i.e. users with the SECURITYADMIN role) can drop network policies.

See also:
:   [CREATE NETWORK POLICY](/sql-reference/sql/create-network-policy) , [ALTER NETWORK POLICY](/sql-reference/sql/alter-network-policy) , [SHOW NETWORK POLICIES](/sql-reference/sql/show-network-policies) , [DESCRIBE NETWORK POLICY](/sql-reference/sql/desc-network-policy)

    [ALTER ACCOUNT](/sql-reference/sql/alter-account)

## Syntax

Copy code

```
DROP NETWORK POLICY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the network policy to drop. If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Only the network policy owner (i.e. role with the OWNERSHIP privilege on the network policy) or higher can execute this command.
- Dropped network policies cannot be recovered; they must be recreated.
- A network policy cannot be dropped if it is currently assigned to an account, security integration, or user.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop a network policy named `mypolicy`:

> Copy code
>
> ```
> DROP NETWORK POLICY mypolicy;
> ```
