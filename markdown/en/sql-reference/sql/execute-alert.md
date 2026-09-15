# EXECUTE ALERT

Manually executes an [alert](/user-guide/alerts) independent of the schedule for the alert.

Note

You cannot use EXECUTE ALERT to execute an [alert on new data](/user-guide/alerts#label-alerts-type-streaming).

See also:
:   [CREATE ALERT](/sql-reference/sql/create-alert) , [ALTER ALERT](/sql-reference/sql/alter-alert) , [DROP ALERT](/sql-reference/sql/drop-alert) , [SHOW ALERTS](/sql-reference/sql/show-alerts) , [DESCRIBE ALERT](/sql-reference/sql/desc-alert)

## Syntax

Copy code

```
EXECUTE ALERT <name>
```

## Parameters

`name`
:   Identifier for the alert to execute.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| EXECUTE ALERT | Account |  |
| OWNERSHIP or OPERATE | Alert |  |
| USAGE | Warehouse | Required on the warehouse used for the alert. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Alerts always run with the privileges of the owner of the alert, even if a different role with the OPERATE privilege uses
  EXECUTE ALERT to execute the alert.
- If the alert is currently suspended, the EXECUTE ALERT command executes the alert but does not resume the alert. The alert
  remains suspended.
- If the alert is currently running (meaning that the state of the alert in the [ALERT\_HISTORY](/sql-reference/functions/alert_history)
  table function output or the [ALERT\_HISTORY view](/sql-reference/account-usage/alert_history) is `EXECUTING`), the
  EXECUTE ALERT command schedules another run of the alert to start immediately after the current run is completed.
- If the alert is currently scheduled (meaning that the state of the alert in the ALERT\_HISTORY table function output or the
  ALERT\_HISTORY view is `SCHEDULED`), the scheduled run is replaced with the requested run and the current timestamp is set
  to the scheduled time.

  However, if the scheduled time has passed but the alert has not yet transitioned to the `EXECUTING` state, the scheduled run
  occurs as usual. (The scheduled run is not replaced with the run requested by the EXECUTE ALERT command.)

## Examples

The following statement manually triggers an alert named `myalert`:

Copy code

```
EXECUTE ALERT myalert;
```
