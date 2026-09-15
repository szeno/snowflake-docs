# ANOMALY\_INSIGHTS!DROP\_MONITOR

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Permanently deletes an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) and all of its state from the current account.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!DROP_MONITOR(
  '<alias>' )
```

## Arguments

`'alias'`
:   Name of the monitor. The name isn’t case-sensitive.

    Data type: VARCHAR

## Output

Returns a VARCHAR status message that confirms the operation.

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

## Usage notes

- The method fails if no monitor with the specified name exists in the account.
- Dropping a monitor removes its configuration, anomaly history, and notification list. You can’t recover a dropped monitor.
- The method is atomic and either drops the monitor completely or makes no changes.

## Example

Delete the monitor named `Eng-Foundations`:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!DROP_MONITOR('Eng-Foundations');
```
