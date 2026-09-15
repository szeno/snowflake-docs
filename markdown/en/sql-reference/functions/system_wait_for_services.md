Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$WAIT\_FOR\_SERVICES

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Waits for one or more [Snowpark Container Services services](/developer-guide/snowpark-container-services/working-with-services) to reach the READY state (or becomes upgraded) before returning.

- All services with names passed to the system function have READY status.
- Any of the named services has the FAILED status.
- The pause duration has reached the specified time duration, in seconds.

You might use this function, for example, in a Native App scenario to pause the native app (with containers) setup script to allow for the services to upgrade correctly. For more information, see [Upgrade an app with containers](/developer-guide/native-apps/update-app-upgrade).

See also:
:   [Snowpark Container Services](/developer-guide/snowpark-container-services/overview)

## Syntax

Copy code

```
SYSTEM$WAIT_FOR_SERVICES( <seconds_to_pause>, '<service_name>' [, ...] )
```

## Arguments

`seconds_to_pause`
:   Number of seconds to pause.

`service_name [ , ... ]`
:   Names of one or more services to wait for.

## Returns

‘OK’ or fails in case of timeout.

## Usage notes

- The current role must have the MONITOR privilege on the services listed in the command.

## Examples

The following statement causes the setup script to pause until one of the following occurs:

- All the three named services passed to the system function have the READY status.
- Any of the named services has the FAILED status.
- 600 seconds have passed.

Copy code

```
SELECT SYSTEM$WAIT_FOR_SERVICES(600, 'service-name-1', 'service-name-2', 'service-name-3');
```
