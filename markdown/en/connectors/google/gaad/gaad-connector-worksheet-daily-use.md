# Stored procedures for daily maintenance

## Introduction

The provides several stored procedures that allow you to manage your data ingestion and connector configuration programmatically.
Below are detailed descriptions of each stored procedure, including their usage, parameters, and examples.

### Configuring a new report

The `CONFIGURE_REPORT` procedure configures a new report for data ingestion from Google Analytics 4 (GA4) into Snowflake.
This procedure takes the report’s parameters as an input, including dimensions, metrics, and ingestion schedule.

> Copy code
>
> ```
> CALL CONFIGURE_REPORT( <report_name>, <property_id>, <dimensions>, <metrics>, <start_date>, <refresh_interval>[, <keep_empty_rows>][, <avoid_sampling>]);
> ```

Where:

`report_name`
:   A string that specifies the name of the report to configure. This name will be used as a prefix for the tables with a raw data created in the destination database.
    After initial ingestion, the report name will be used as a name for the views created in the destination database. **Required.**

    The report name must:
    :   - start with either a letter (uppercase or lowercase) or an underscore.
        - continue with one or more characters that can be letters (uppercase or lowercase), digits, or underscores.
        - be 150 characters or less.

`property_id`
:   A string that specifies the Google Analytics 4 property id to use for the report. The property id has a form of a number obtainable from GA4 account.
    Ensure that the PROPERTY\_ID corresponds to a GA4 property accessible by the connectors authentication method (oauth2 or service account). **Required.**

`dimensions`
:   A comma-separated list of GA4 dimensions to include in the report. The dimensions must be separated by commas.
    If `date` dimension is not explicitly specified, it will be added automatically.
    At most nine dimensions can be specified (including `date`). **Required.**

    Example: `'country,city,deviceCategory,sessions'`

`metrics`
:   A comma-separated list of GA4 metrics to include in the report.
    At least one metric is required, with a maximum of ten metrics. **Required.**

    Example: `'sessions,pageViews'.`

`start_date`
:   A string that specifies the start date for the report. The date must be in the format `YYYY-MM-DD`.
    Data from this date onwards will be ingested. **Required.**

`refresh_interval`
:   A string that specifies the refresh interval for the report. **Required.** The interval must have one of the following formats:

    > - `'EVERY <number of minutes> MINUTE'`
    > - `'EVERY <number of hours> HOUR'`
    > - `'EVERY <number of days> DAY'`

`keep_empty_rows`
:   Optional. Default value is `false`. If `true`, the output table includes records with dimension combinations where all metrics are zero.
    Useful for analyzing dimension combinations with no events.

`avoid_sampling`
:   Optional. Default value is `false`. If `true`, the connector may adjust the way it fetches the data from GA4 API to try to avoid data sampling.
    Can improve data accuracy but may increase API call frequency.

    Note

    There is no guarantee that the data will be unsampled. The connector will try to avoid sampling, but it may not be possible in all cases.
    This is due to the limitations of the GA4 API.

    **Example:**

    Copy code

    ```
    CALL CONFIGURE_REPORT(
        REPORT_NAME => 'USER_ENGAGEMENT_REPORT',
        PROPERTY_ID => '123456789',
        DIMENSIONS => 'country,deviceCategory',
        METRICS => 'activeUsers,newUsers',
        START_DATE => '2023-01-01',
        REFRESH_INTERVAL => 'EVERY 1 DAY',
        KEEP_EMPTY_ROWS => TRUE,
        AVOID_SAMPLING => TRUE
    );
    ```

### Removing existing report

The `DELETE_REPORT` procedure deletes an existing report configuration from the connector, stopping any further data ingestion for that report. Data that has already been ingested will not be removed.

> Copy code
>
> ```
> CALL DELETE_REPORT( <report_name> );
> ```

Where:

`report_name`
:   A string that specifies the name of the report to delete.
    Must match the REPORT\_NAME used in CONFIGURE\_REPORT. **Required.**

    **Example:**

    Copy code

    ```
    CALL DELETE_REPORT('USER_ENGAGEMENT_REPORT');
    ```

### Listing properties from Google Analytics 4 account

The `GET_PROPERTIES` procedure returns a list of all the Google Analytics 4 properties that are available for ingestion by the connector.

> Copy code
>
> ```
> CALL GET_PROPERTIES();
> ```

Example output from the procedure:

> Copy code
>
> ```
> {[
>   { "propertyName": "test1", "propertyId": "1" },
>   { "propertyName": "test2", "propertyId": "2" },
>   { "propertyName": "test3", "propertyId": "3" }
> ]}
> ```
>
> Note
>
> The connector must have the necessary permissions to access the properties. If a result is empty, verify access rights in GA4.

### Fetching dimensions and metric for GA4 property

The `GET_DIMENSIONS_AND_METRICS` procedure retrieves the list of available dimensions and metrics for a specified GA4 property.

> Copy code
>
> ```
> CALL GET_DIMENSIONS_AND_METRICS( <property_id> );
> ```

Where:

`property_id`
> A string that specifies the Google Analytics 4 property id to use for the report. The property id has a form of a number obtainable from GA4 account.
> Ensure that the `property_id` corresponds to a GA4 property accessible by the connectors authentication method (oauth2 or service account). **Required.**
>
> **Example:**
>
> > Copy code
> >
> > ```
> > CALL GET_DIMENSIONS_AND_METRICS('123456789');
> > ```
>
> **Example output from the procedure:**
>
> Copy code
>
> ```
> {
>   "dimensions": [
>     {
>       "dimension": "achievementId", "category": "Other", "description": "Some description."
>     }
>   ],
>   "metrics": [
>     {
>       "metric": "active1DayUsers", "category": "User", "description": "Some description."
>     },
>     {
>       "metric": "active28DayUsers", "category": "User", "description": "Some description."
>     }
>   ]
> }
> ```
>
> Note
>
> The available dimensions and metrics may vary between properties.

### Pausing the connector

The `PAUSE_CONNECTOR` procedure pauses the connector, stopping all data ingestion and processing.

> Copy code
>
> ```
> CALL PAUSE_CONNECTOR();
> ```
>
> Note
>
> - Pausing the connector halts data ingestion for all configured reports.
> - Data ingestion can be resumed using RESUME\_CONNECTOR.
> - Existing data remains accessible during the pause.

### Resuming the connector

The `RESUME_CONNECTOR` procedure resumes the connector, starting all data ingestion and processing that was previously paused.
Data ingestion will continue from the point where it was paused.

> Copy code
>
> ```
> CALL RESUME_CONNECTOR();
> ```

### On demand ingestion

The `INGEST_NOW` procedure schedules data ingestion for the specified report in the connector.
This procedure can be used to manually initiate data ingestion for a specific report outside of the scheduled intervals.

> Note
>
> The procedure schedules immediate ingestion for the specified report using `EXECUTE TASK ...`.
> That means that the ingestion will start as soon as possible, but it may not be instantaneous
> especially if ingestion for the same report is already in progress. Ensure that the connector is not paused before calling this procedure.
>
> Copy code
>
> ```
> CALL INGEST_NOW('<report_name>');
> ```

Where:

`report_name`
:   A string that specifies the name of the report to ingest.
    Must match the REPORT\_NAME used in CONFIGURE\_REPORT. **Required.**

    **Example:**

    Copy code

    ```
    CALL INGEST_NOW('USER_ENGAGEMENT_REPORT');
    ```

### Getting the current status of the connector

> Note
>
> Connector `state` and connector `status` are used interchangeably in the context of this document.
> The status/state of the connector can be retrieved using the `GET_CONNECTOR_STATUS` procedure.
>
> Copy code
>
> ```
> CALL GET_CONNECTOR_STATUS();
> ```
>
> Example output from the procedure:
>
> Copy code
>
> ```
> {
>   "response_code": "OK",
>   "status": "STARTED",
>   "configurationStatus": "PREREQUISITES_DONE"
> }
> ```

The procedure returns a JSON object with the following fields:

- `response_code` - If the procedure has been executed successfully **OK** value is returned. Response code other than **OK** indicates an error.
- `status` - The current status of the connector. This status can change only when you re/install, pause, resume connector or finalize the configuration process.
  It can have one of the following values:

  - `CONFIGURING` - This is the default state set after the connector is installed from the listing or application package.
    The connector remains in this state until the configuration process is finalized. After the configuration is finalized,
    the connector transitions to the STARTED state.
  - `STARTED` - Once the connector is fully configured or resumed it transitions to the STARTED state.
  - `PAUSED` - When the connector is successfully paused it transitions to the PAUSED state.
  - `ERROR` - If the connector encounters an irreversible error, it transitions to the ERROR state, indicating it cannot be actively used.
    When in this state, `RECOVER_CONNECTOR_STATE` procedure can be used in order to transition to a valid state.
- `configurationStatus` - This is a sub-status of the main `CONFIGURING` status. The connector configuration process is divided into few steps
  which are being tracked by this sub-status. It can have one of the following values:

  - `INSTALLED` - The configuration starts in the INSTALLED state after the connector instance has been created.
  - `PREREQUISITES_DONE` - After the user completes the prerequisites and calls `MARK_ALL_PREREQUISITES_AS_DONE` procedure
    the configuration transitions to the PREREQUISITES\_DONE state.
    Prerequisites are manual steps that needs to be executed by the user, e.g. configuring the connection to third party data source
    or creating destination database.
  - `CONFIGURED` - The `CONFIGURE_CONNECTOR(VARIANT)` procedure has been called.
  - `CONNECTED` - The `SET_CONNECTION_CONFIGURATION(VARIANT)` procedure has been called.
  - `FINALIZED` - Finally, after completing the configuration, the configuration transitions to the FINALIZED state
    (the `FINALIZE_CONNECTOR_CONFIGURATION(VARIANT)` procedure has been called).

### Restarting configuration process

The `RESET_CONFIGURATION` stored procedure resets the connector’s configuration to its default state.
This procedure can be used to reset the connector’s configuration before the configuration has been finalized.
In order for the procedure to work, the connector must be in `CONFIGURING` status.
To know more about the connector main statuses and configuration sub-statuses refer to [Getting the current status of the connector](#label-getting-current-status).

If configuration phase is completed (FINALIZED) this procedure will return an error.

> Copy code
>
> ```
> CALL RESET_CONFIGURATION();
> ```

### Recovering from intermediate or erroneous state

The `RECOVER_CONNECTOR_STATE` procedure is intended to recover the connector when it is stuck in an intermediate or error state (`ERROR`, `STARTING`, `PAUSING`)
by manually setting its status to either `STARTED` or `PAUSED`.
Some operations may leave the connector in an inconsistent state and it may happen for various reasons.
For example when the user will drop permissions to certain database objects the connector needs.

The procedure will return an error if the new state is not valid or if the connector is in not in one of predetermined states.
The following transitions are allowed:

> - ERROR -> PAUSED
> - ERROR -> STARTED
> - PAUSING -> PAUSED
> - PAUSING -> STARTED
> - STARTING -> PAUSED
> - STARTING -> STARTED
>
> Copy code
>
> ```
> CALL RECOVER_CONNECTOR_STATE('<new_state>');
> ```

Where:

`new_state`
:   A string that specifies the new state for the connector. The state must be either `STARTED` or `PAUSED`. **Required.**

    **Example:**

    Copy code

    ```
    CALL RECOVER_CONNECTOR_STATE('STARTED');
    ```

### Recovering reports after a connector has been dropped

The `IMPORT_STATE` procedure is used to recover configured reports and ingestion history after the connector has been uninstalled.
This procedure is intended to be used after the connector has been reinstalled and the new connector has been configured to use the same
database that was used by the uninstalled one. The state that is being imported is located in the destination database used by the previous instance of the connector in the form of tables
with `SFSDKEXPORT` suffix. To read more about the process read the [Disaster recovery](/connectors/google/gaad/gaad-connector-disaster-recovery) guide. The procedure will not overwrite
the existing state in the connector if it detects the state is not pristine unless the `force` parameter is set to `true`. Pristine state is a state right after configuration process
is finalized and no reports are configured. If reports were configured but later deleted the state is also assumed to be not pristine.

> Note
>
> When the connector was uninstalled (dropped) with the *CASCADE* options this procedure will not work.
>
> Copy code
>
> ```
> CALL IMPORT_STATE([force]);
> ```

Where:

`force`
:   Optional. Default value is `false`. If `true`, the procedure will overwrite the existing state in the connector. Including any reports that are already configured.
    If `false`, the procedure will return an error if it detects that the state is not pristine.

    **Example:**

    Copy code

    ```
    CALL IMPORT_STATE();
    ```
