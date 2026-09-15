# Prerequisites

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

The prerequisites step is the first step of the wizard phase of the connector. This step is completely optional,
but it is recommended, if the end user needs to perform some additional setup outside of the native app or even whole Snowflake context.
An example of this could be setting up authentication and authorization in the source system from which the data will be ingested.

To setup prerequisites they must be inserted to the `STATE.PREREQUISITES` table during the connector installation.
Most of the columns in that table should be self-explanatory. The URL columns should be used to provide
the end user with more information on the required setups. In case there is a need to provide something more
custom in the prerequisites the `custom_properties` column should be used.

The prerequisites phase consists of 2 steps:

1. Marking prerequisites as done
2. Completing the step

## Requirements

Prerequisites require at least the following sql files to be executed during native app installation:

- `core.sql`
- `configuration/prerequisites.sql`

### Marking prerequisites as done

This step can be achieved in two different ways. Either prerequisites can be marked one by one as completed or all of them together.
The end result is the same, each of the prerequisites has its `is_completed` value set to `true`.
This step is handled by the following procedures:

- PUBLIC.MARK\_ALL\_PREREQUISITES\_AS\_DONE()
- PUBLIC.UPDATE\_PREREQUISITE(ID VARCHAR, IS\_COMPLETED BOOLEAN)

Both of those procedures require the connector to be in the `CONFIGURING` status and the configuration status to not be `FINALIZED`.

## Completing the step

To complete the prerequisites step call `PUBLIC.COMPLETE_PREREQUISITES_STEP()` procedure.
This procedure has no effect unless the connector is in the `CONFIGURING` status with configuration status `INSTALLED`.

If that’s the case then the status will be updated to the following value:

Copy code

```
{
    "status": "CONFIGURING",
    "configurationStatus": "PREREQUISITES_DONE"
}
```

This procedure requires the connector to be in the `CONFIGURING` status and the configuration status to not be `FINALIZED`.
