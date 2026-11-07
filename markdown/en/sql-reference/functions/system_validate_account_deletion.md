Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$VALIDATE\_ACCOUNT\_DELETION

Returns every condition that blocks [dropping an account](/user-guide/organizations-manage-accounts-delete). The function is read-only: it doesn’t drop the account or change any objects.

An [organization administrator](/user-guide/organization-administrators) can call this function for the account they plan to drop. The result lists every blocker in one response, including blockers you can remove and blockers that require [Snowflake Support](/user-guide/contacting-support).

See also:
:   [DROP ACCOUNT](/sql-reference/sql/drop-account)

## Syntax

Copy code

```
SYSTEM$VALIDATE_ACCOUNT_DELETION( '<account_name>' )
```

## Arguments

`account_name`
:   Name of the account to check. Specify the account name, not the account locator. For example, if the account identifier is `myorg-account123`, specify `account123`.

## Returns

Returns a JSON object:

| Key | Data type | Description |
| --- | --- | --- |
| account | STRING | Name of the account that was checked. |
| blocked | BOOLEAN | `true` when one or more conditions block `DROP ACCOUNT`. `false` when the account can be dropped. |
| errors | ARRAY | Objects that describe each blocker. See the following table. |

Expand

Show lessSee more

Each object in the `errors` array contains the following keys:

| Key | Data type | Description |
| --- | --- | --- |
| code | STRING | Error code. See [Error codes](#label-validate-account-deletion-error-codes). |
| message | STRING | Error message. The message can include the names or types of the objects that block the drop. A long list of names can be truncated. |

Expand

Show lessSee more

### Error codes

If `DROP ACCOUNT` fails, use the error code to find what to remove or who to contact before you retry the command. The condition column summarizes why the drop is blocked. The `message` value in the function output can be more specific and can name the blocking objects.

| Error code | Condition | Resolution |
| --- | --- | --- |
| `003772` | Cannot drop account with active listings, please drop all listings in the account then retry, might need to retire marketplace listings first. | [ALTER LISTING](/sql-reference/sql/alter-listing), [DROP LISTING](/sql-reference/sql/drop-listing) |
| `003773` | Cannot drop account with shares attached to listings, please drop all listings attached to the shares then retry, might need to retire marketplace listings first. | [DROP LISTING](/sql-reference/sql/drop-listing), [DROP SHARE](/sql-reference/sql/drop-share) |
| `004001` | Cannot drop account owning organization profiles with associated listings. To unblock dropping this account, drop the associated listings first or reach out to Support for additional help. | [DROP ORGANIZATION PROFILE](/sql-reference/sql/drop-organization-profile) |
| `003830` | The account has secondary connections. | [DROP CONNECTION](/sql-reference/sql/drop-connection) |
| `003831` | The account has a primary connection with secondary connections. | [DROP CONNECTION](/sql-reference/sql/drop-connection), [ALTER CONNECTION](/sql-reference/sql/alter-connection) |
| `003832` | The account has primary and secondary connections. | [DROP CONNECTION](/sql-reference/sql/drop-connection), [ALTER CONNECTION](/sql-reference/sql/alter-connection) |
| `003155` | The account hosts a global database or a replication group. | [DROP REPLICATION GROUP](/sql-reference/sql/drop-replication-group), [DROP FAILOVER GROUP](/sql-reference/sql/drop-failover-group), [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) |
| `060173` | Organization users or organization user groups still exist. | [DROP ORGANIZATION USER GROUP](/sql-reference/sql/drop-organization-user-group), [DROP ORGANIZATION USER](/sql-reference/sql/drop-organization-user) |
| `511836` | A backup is under a legal hold. | [ALTER BACKUP SET](/sql-reference/sql/alter-backup-set) |
| `060014` | Drop account is not supported for Organization Accounts. Please contact support if you wish to drop this Organization account. | [Snowflake Support](/user-guide/contacting-support) |
| `060182` | The organization has an outstanding billing balance. | [Snowflake Support](/user-guide/contacting-support) |
| `003746` | The organization is locked for maintenance. | [Snowflake Support](/user-guide/contacting-support) |

Expand

Show lessSee more

## Access control requirements

Only an [organization administrator](/user-guide/organization-administrators) can call this function.

## Usage notes

The function doesn’t drop the account. After you remove the blockers, run [DROP ACCOUNT](/sql-reference/sql/drop-account).

## Examples

The following example checks whether the account `ACCOUNT1` can be dropped. The account is blocked by active listings and a replication group:

Copy code

```
CALL SYSTEM$VALIDATE_ACCOUNT_DELETION('ACCOUNT1');
```

Output:

Copy code

```
{
  "account": "ACCOUNT1",
  "blocked": true,
  "errors": [
    {
      "code": "003772",
      "message": "Cannot drop account with active listings, please drop all listings in the account then retry, might need to retire marketplace listings first. Active listing: LISTING_1"
    },
    {
      "code": "003773",
      "message": "Cannot drop account with shares attached to listings, please drop all listings attached to the shares then retry, might need to retire marketplace listings first. Active listing: LISTING_1"
    },
    {
      "code": "003155",
      "message": "Account is currently hosting replication objects of the following types: Replication group. Please drop these objects and retry."
    }
  ]
}
```
