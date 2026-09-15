# Manage the

This topic describes typical tasks you might need to perform after installing and configuring the connector.

## Setting up alerts

To set up alerts, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the , then select the tile for the connector.
4. Go to the **Settings** section and then select **Email alerts** from the menu on the left.
5. In the **Email Address** field, provide a Snowflake verified email address.

   Note

   You must specify an email address that is associated with the Snowflake account.
6. In the **Email Frequency** field, select how often you would like to receive alerts:

   - **Immediately** - you will receive notifications after each ingestion failure but at most every 30 minutes.
   - **Once per day** - you will receive notifications once a day at 12PM UTC.

   Note

   Alerts are sent only when an ingestion failure occurs.
7. Select **Save changes** to start receiving email alerts.

### Disabling alerts

To stop receiving alerts, select **Stop receiving alerts** in the email alerts configuration page.

## Upgrading the connector

The connector upgrades are managed automatically by the provider of the application.

## Re-authentication of the Connector

In order to change the secret, external access integration, or the security integration used by the connector without re-installation,
you need to execute the `UPDATE_CONNECTION_CONFIGURATION` procedure defined in the `PUBLIC` schema.
Ensure that all of the new objects are defined as described in [Configure the using SQL](/connectors/google/gaad/gaad-connector-configuring-sql) and that the connector has all of the required grants.

Copy code

```
USE ROLE accountadmin;
CALL UPDATE_CONNECTION_CONFIGURATION(
    PARSE_JSON('{"external_access_integration": "<external access integration name>", "secret": "<full path to the secret>", "security_integration": "<security integration name>"}')
);
```

Replace the placeholders with actual values, as in the following example.

Copy code

```
USE ROLE accountadmin;
CALL UPDATE_CONNECTION_CONFIGURATION(
    PARSE_JSON('{"external_access_integration": "SNOWFLAKE_CONNECTOR_FOR_GOOGLE_ANALYTICS_AGGREGATE_DATA_EXTERNAL_ACCESS_INTEGRATION", "secret": "CONNECTORS_SECRET.SNOWFLAKE_CONNECTOR_FOR_GOOGLE_ANALYTICS_AGGREGATE_DATA.SECRET", "security_integration": "SNOWFLAKE_CONNECTOR_FOR_GOOGLE_ANALYTICS_AGGREGATE_DATA_SECURITY_INTEGRATION"}')
);
```

Note

Values passed to UPDATE\_CONNECTION\_CONFIGURATION should be unqualified, uppercase identifiers.

## Changing the warehouse for the Connector

It is possible to change the warehouse that the uses for its internal tasks without reinstalling the connector.
First, make sure that the connector is paused. It can be done either via UI or using the `PAUSE_CONNECTOR` procedure.
Then, you need to grant the connector access to the new warehouse:

Copy code

```
GRANT USAGE ON WAREHOUSE <new_warehouse_name> TO APPLICATION snowflake_connector_for_google_analytics_aggregate_data;
```

After the access is granted, execute the `UPDATE_WAREHOUSE` procedure defined in the `PUBLIC` schema:

Copy code

```
CALL UPDATE_WAREHOUSE('<new_warehouse_name>');
```

Replace the placeholder with the actual value, as in the following example.

Copy code

```
CALL UPDATE_WAREHOUSE('NEW_WH');
```

Note

Values passed to UPDATE\_WAREHOUSE should be unqualified, uppercase identifiers.

## Uninstalling the connector

Removing the connector database does not delete the ingested data that is stored in a separate database or the
objects that were created during the installation performed using Snowsight.

Note

To see objects created during the installation, select » **Settings** » **Objects**.

To uninstall the connector, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the .
4. Select **Uninstall**.
