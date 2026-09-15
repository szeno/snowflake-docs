Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$REPORT\_HEALTH\_STATUS

Sends [application health information](/developer-guide/native-apps/monitoring#label-nativeapps-monitor-consumer-app-health) from a consumer app to the provider account.

## Syntax

Copy code

```
SYSTEM$REPORT_HEALTH_STATUS( '<status>' )
```

## Arguments

`'status'`
:   A string literal of type VARCHAR that indicates the health status of the
    application. You can specify one of the following values:

- `'OK'`: The consumer instance is healthy.
- `'FAILED'`: The consumer instance is in an error state.
- `'PAUSED'`: The consumer manually paused the app.

## Usage notes

- This function is intended to be called by consumer applications. Your application
  should call this function periodically to report its health status to the
  provider account.
- Your application logic determines what health status to report based on its own
  monitoring and error handling.
- The health status reported by this function is visible to the provider account
  in the [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view)
  (columns `LAST_HEALTH_STATUS` and `LAST_HEALTH_STATUS_UPDATED_ON`). Providers
  should query `APPLICATION_STATE` periodically to monitor the health of consumer
  instances. Consider setting up alerts to notify you when a consumer instance
  reports a `FAILED` status, a `PAUSED` status, or stops reporting its status.
- Snowflake only retains the most recent health status reported by each
  consumer instance of the application.
- To avoid excessive load on Snowflake, this function is rate limited. If the
  function is called again within 55 minutes from the same consumer instance, it
  will return `false` to indicate that the status report was not accepted.
  Exception: a status of `PAUSED` can be reported even if the last report was
  less than 55 minutes ago, as long as the current status isn’t already `PAUSED`.
  This allows an instance to report a paused state based on a user action and
  then shut down background reporting tasks without the paused state being lost.
- For more information about monitoring application health from the provider side,
  see [Monitor a native app](/developer-guide/native-apps/monitoring).

## Return value

- This function returns TRUE if the health status was successfully reported.
- This function returns FALSE if the status report failed due to being
  rate limited.
