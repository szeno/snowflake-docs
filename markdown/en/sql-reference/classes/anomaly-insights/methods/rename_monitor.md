# ANOMALY\_INSIGHTS!RENAME\_MONITOR

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Changes the name of an existing [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors).

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!RENAME_MONITOR(
  '<alias>',
  '<new_alias>' )
```

## Arguments

`'alias'`
:   Current name of the monitor. The name isn’t case-sensitive.

    Data type: VARCHAR

`'new_alias'`
:   New name for the monitor. The name must be unique within the account and isn’t case-sensitive.

    Data type: VARCHAR

## Output

Returns a VARCHAR status message that confirms the operation.

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

## Usage notes

- The method fails if no monitor with the specified name exists in the account, or if the new name is already in use.
- Renaming a monitor preserves its configuration, anomaly history, and notification list. No recalculation is triggered.

## Example

Rename the monitor `Eng-Platform` to `Eng-Foundations`:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!RENAME_MONITOR(
  'Eng-Platform', 'Eng-Foundations');
```
