Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$OPT\_OUT\_INTERNAL\_STAGE\_NETWORK\_LOGS

Stops record collection of network access attempts to internal stage locations for this account. You can view these records in the
[INTERNAL\_STAGE\_NETWORK\_ACCESS\_HISTORY view](/sql-reference/account-usage/internal_stage_network_access_history).

See also:
:   [SYSTEM$OPT\_IN\_INTERNAL\_STAGE\_NETWORK\_LOGS](/sql-reference/functions/system_opt_in_internal_stage_network_logs)

## Syntax

Copy code

```
SYSTEM$OPT_OUT_INTERNAL_STAGE_NETWORK_LOGS()
```

## Arguments

None.

## Returns

Returns a VARCHAR status message, which states that record collection of network access attempts to internal stage locations has ended.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can execute this function.

## Usage notes

Latency between running this function and stopping record collection is up to 6 hours.

## Example

Stop record collection of network access attempts to internal stage locations for this account:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$OPT_OUT_INTERNAL_STAGE_NETWORK_LOGS();
```

```
+--------------------------------------------------------------------+
| Record collection has been successfully disabled for this account. |
+--------------------------------------------------------------------+
```
