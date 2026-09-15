# DROP INTEGRATION

Removes an integration from the account.

See also:
:   [CREATE INTEGRATION](/sql-reference/sql/create-integration) , [ALTER INTEGRATION](/sql-reference/sql/alter-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

API integrations:
:   [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)

catalog integrations:
:   [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration)

External access integrations:
:   [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration)

Notification integrations:
:   [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration)

Security integrations:
:   [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration)

Storage integrations:
:   [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)

## Syntax

Copy code

```
DROP [ { API | CATALOG | EXTERNAL ACCESS | NOTIFICATION | SECURITY | STORAGE } ] INTEGRATION [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the integration to drop. If the identifier contains spaces, special characters, or mixed-case characters,
    the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive
    (e.g. `"My Object"`).

`API | CATALOG | EXTERNAL ACCESS | NOTIFICATION | SECURITY | STORAGE`
:   Specifies the integration type.

## Usage notes

- Dropped integrations cannot be recovered; they must be recreated.
- Disabling or dropping the integrations may not take effect immediately, since integrations may be cached.
  It is recommended to remove the integration privilege from the cloud provider to take effect sooner.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop an integration:

> Copy code
>
> ```
> SHOW INTEGRATIONS LIKE 't2%';
>
> DROP INTEGRATION t2;
>
> SHOW INTEGRATIONS LIKE 't2%';
> ```

Drop the integration again, but don’t raise an error if the integration does not exist:

> Copy code
>
> ```
> DROP INTEGRATION IF EXISTS t2;
> ```
