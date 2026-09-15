# DROP CONNECTION

[Business Critical Feature](/user-guide/intro-editions)

This command is part of the [client redirect](/user-guide/client-redirect) feature.
It requires Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You use client redirect in combination with the
[account replication](/user-guide/account-replication-intro) feature
for business continuity and disaster recovery.

Removes a connection from the account.

See also:
:   [CREATE CONNECTION](/sql-reference/sql/create-connection) , [ALTER CONNECTION](/sql-reference/sql/alter-connection) , [SHOW CONNECTIONS](/sql-reference/sql/show-connections)

## Syntax

Copy code

```
DROP CONNECTION [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the connection to drop.

## Usage notes

- Only account administrators (users with the ACCOUNTADMIN role) can execute this SQL command.
- A primary connection can’t be dropped if it has one or more secondary connections. To drop the primary connection, first promote a secondary
  connection to serve as the primary connection, and then drop the former primary connection. Alternatively, drop all of the secondary connections,
  and then drop the primary connection.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop a connection:

> Copy code
>
> ```
> SHOW CONNECTIONS LIKE 't2%';
>
>
> DROP CONNECTION t2;
>
>
> SHOW CONNECTIONS LIKE 't2%';
> ```

Drop the connection again, but don’t raise an error if the connection doesn’t exist:

> Copy code
>
> ```
> DROP CONNECTION IF EXISTS t2;
> ```
