# Troubleshooting the

This topic provides guidelines for troubleshooting issues with the .

## Calling the get\_troubleshooting\_data procedure

The `GET_TROUBLESHOOTING_DATA` procedure returns information about the configuration of a connector, ingestion history, errors,
and additional information that can help you determine the root cause of an issue. This procedure may be called on
the connector in any state (configured, not configured, running, paused, and so on).

Note

To report an issue with the connector to snowflake Support, attach the output from this procedure.

`GET_TROUBLESHOOTING_DATA` takes two parameters: a ‘from’ timestamp and a ‘to’ timestamp. They limit the returned rows
to the relevant time frame. For example, to get troubleshooting data with an ingestion history for the last week, you can call:

Copy code

```
CALL GET_TROUBLESHOOTING_DATA(DATEADD(day, -7, SYSDATE()), SYSDATE());
```

## Verifying the connection to Google Analytics

To verify that the connector can access Google Analytics data, call the
`TEST_CONNECTION` stored procedure, which is defined in the PUBLIC schema of the connector’s installation database:

Copy code

```
CALL TEST_CONNECTION();
```

## Checking the connector stats and connector errors views

If you encounter problems with data ingestion, you can check the `CONNECTOR_STATS` view and the `CONNECTOR_ERRORS` view
from the `PUBLIC` schema in the connector’s installation database:

Copy code

```
SELECT * FROM PUBLIC.CONNECTOR_STATS;
SELECT * FROM PUBLIC.CONNECTOR_ERRORS;
```

For information about returned content, see [Monitoring the](/connectors/google/gaad/gaad-connector-monitoring) .

## Transferring ownership of tables and views in the destination schema

The connector must own all associated report tables and views. If ownership is transferred to another role,
it can be returned to the connector using the `SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION` function.

Copy code

```
USE ROLE accountadmin;
CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION(<connector_app>, true, <destination_database>, <destination_schema>);
```

The `SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION` is a system function provided by Snowflake that allows the transfer of
ownership of tables and views in a specified database or schema to the application. Only the ownership of regular tables and
regular views is transferred, e.g. ownership of dynamic tables, external tables, materialized views, etc. won’t be
transferred.

The function has the following signature:

Copy code

```
SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION(<to_app>, <should_copy_grants>, <from_database>, <from_schema>)
```

Where:

> `to_app`
> :   Specifies the name of the application to which the ownership of objects should be transferred.
>
> `should_copy_grants`
> :   If `TRUE` then copy existing grants, otherwise revoke. Copying grants requires `MANAGE GRANTS`
>     permission on the caller.
>
> `from_database`
> :   Name of the database containing objects whose ownership should be changed.
>
> `from_schema`
> :   (Optional) name of the schema containing objects whose ownership should be changed. If no schema is specified,
>     ownership is transferred on tables and views in all schemas in the provided database. Objects in managed schemas
>     are omitted during ownership transfer.

To execute the function the caller must meet one of the following conditions:

- It has `MANAGE GRANTS` permission (e.g. ACCOUNTADMIN or SECURITYADMIN role), or
- It contains role owning the application instance and role owning all objects to transfer the ownership. Objects on
  which the ownership is missing are omitted by the function.

For example, to return ownership to the connector that:

- Was installed as `snowflake_connector_for_google_analytics_aggregate_data`
- Uses the schema named `dest_db.dest_schema` for the Google Analytics data in Snowflake

Run the following command:

Copy code

```
USE ROLE accountadmin;
CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION('snowflake_connector_for_google_analytics_aggregate_data', true, 'dest_db', 'dest_schema');
```
