Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_COMPUTE\_POOL\_PENDING\_MAINTENANCE

Retrieves information about pending Snowflake [maintenance actions for compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool#label-snowpark-containers-working-with-compute-pool-maintenance) in the current account.

See also:
:   [Snowpark Container Services: Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool)

## Syntax

Copy code

```
SYSTEM$GET_COMPUTE_POOL_PENDING_MAINTENANCE()
```

## Returns

- Returns a JSON object that provides an indication of whether maintenance is required and the upcoming maintenance window timeline. The JSON fields are:

  - `maintenanceRequired`. Boolean field that provides an indication of whether maintenance is required.
  - `start`. Start time of the maintenance window.
  - `end`. End time of the maintenance window.
- If there are no running compute pools in the Snowflake account, the function returns “No running Snowpark Container Services found.”
- If there is no scheduled maintenance window, the function returns “No pending maintenance actions.”

## Usage notes

- All roles have privilege to access this function.

## Examples

Copy code

```
SELECT SYSTEM$GET_COMPUTE_POOL_PENDING_MAINTENANCE();
```

Sample output:

```
+---------------------------------------------------------------------------------------------------------+
| SYSTEM$GET_COMPUTE_POOL_PENDING_MAINTENANCE()                                                           |
|---------------------------------------------------------------------------------------------------------|
| {"maintenanceRequired":false,"maintenanceWindow":{"start":"2025-02-27T23:00","end":"2025-02-28T00:00"}} |
+---------------------------------------------------------------------------------------------------------+
```

This output indicates that no maintenance is scheduled for the next maintenance window. If maintenance is required, `maintenanceRequired` is set to true.
