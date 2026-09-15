Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$LINK\_ACCOUNT\_OBJECTS\_BY\_NAME

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Adds a global identifier to account objects in the target (current) account that were created using scripts
and that match objects with the same names in the source account.

Global identifiers are only added to account objects that are included in a replication or failover group for the
following object types:

- `RESOURCE_MONITOR`
- `ROLE`
- `USER`
- `WAREHOUSE`

For more information, refer to [Apply global IDs to objects created by scripts in target accounts](/user-guide/account-replication-config#label-apply-global-ids-to-objects).

## Syntax

Copy code

```
SYSTEM$LINK_ACCOUNT_OBJECTS_BY_NAME('<group_name>')
```

## Arguments

`group_name`
:   Specifies the identifier for the replication or failover group.

## Usage notes

- Only account administrators (users with the ACCOUNTADMIN role) can execute this SQL function.
- To retain account objects that exist only in the target account, replicate them
  manually in the source account before executing this function.

## Examples

Copy code

```
SELECT SYSTEM$LINK_ACCOUNT_OBJECTS_BY_NAME('myfg');
```
