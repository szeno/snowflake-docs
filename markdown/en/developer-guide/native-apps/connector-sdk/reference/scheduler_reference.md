# Ingestion scheduler reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following procedures are created by the file `scheduler/scheduler.sql`.

### PUBLIC.CREATE\_SCHEDULER()

This procedure acts as the entry point between SQL and Java. It will create a task running according to the schedule available in `APP_STATE` table.
This task will execute below `PUBLIC.RUN_SCHEDULER_ITERATION()` procedure when executed.

### PUBLIC.RUN\_SCHEDULER\_ITERATION()

This procedure is an entry point to the Java implementation of the actual scheduling task. It will
be invoked whenever the scheduler task is executed.

It needs `com.snowflake:telemetry` package in order to emit metrics to event table.

### PUBLIC.ON\_INGESTION\_SCHEDULED (process\_id VARCHAR)

This procedure defines the ingestion flow for a single process that was taken by the scheduler for execution. The default implementation does nothing.
We recommend implementing this in Java using the `OnIngestionScheduledCallback` interface.

#### Related features

Other related features:

- `Task Reactor`
- `Ingestion`

### Related Java objects

Java implementations and related classes:

- `CreateSchedulerHandler`
- `RunSchedulerIterationHandler`
- `RunSchedulerIterationHandlerBuilder`
- `OnIngestionScheduledCallback`
- `OnIngestionFinishedCallback`

### Custom handler

Ingestion scheduler feature consists of two different handlers acting as entry point from SQL to Java:

- `CreateSchedulerHandler`
- `RunSchedulerIterationHandler`

We recommend customizing only the latter one.

### Builder approach

`RunSchedulerIterationHandler` can be customized using `RunSchedulerIterationHandlerBuilder`.
This helper objects allows for custom implementations of the underlying interfaces:

- `ConnectorErrorHelper`
- `OnIngestionScheduledCallback`

In case they are not provided the default implementations will be used.

Copy code

```
class CustomOnIngestionScheduledCallback implements OnIngestionScheduledCallback {
    @Override
    public void onIngestionScheduled(String processId) {
        // CUSTOM LOGIC
    }
}

class CustomHandler {

    // Path to this method needs to be specified in the PUBLIC.RUN_SCHEDULER_ITERATION procedure using SQL
    public static Variant runIteration(Session session) {
        return RunSchedulerIterationHandler.builder(session)
            .withOnIngestionScheduledCallback(new CustomOnIngestionScheduledCallback())
            .build()
            .runIteration()
            .toVariant();
    }
}
```
