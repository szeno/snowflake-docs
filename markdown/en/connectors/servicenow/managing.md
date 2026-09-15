# Managing, updating, and uninstalling the Snowflake Connector for ServiceNow®

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

This topic and its sections describe typical tasks you might need to perform after installing and configuring the connector.

## Pausing and resuming the Snowflake Connector for ServiceNow®

The following sections describe how to pause and resume the connector.

### Pausing the Snowflake Connector for ServiceNow®

To stop all tasks started by the connector, call the `PAUSE_CONNECTOR` stored procedure:

Copy code

```
CALL PAUSE_CONNECTOR();
```

Pausing the connector disables interaction with it (e.g. enabling/disabling tables or configuring the connector) until the connector is resumed by calling the `RESUME_CONNECTOR` stored procedure.

Pausing the connector also stops any cost generation for the connector.

### Resuming the Snowflake Connector for ServiceNow®

To resume all tasks stopped by `PAUSE_CONNECTOR` stored procedure, call `RESUME_CONNECTOR` stored procedure:

Copy code

```
CALL RESUME_CONNECTOR();
```

## Changing the warehouse used by the connector

If you want to change the warehouse used by the connector or add a dedicated warehouse, do this by calling:

> Copy code
>
> ```
> CALL UPDATE_WAREHOUSE('<warehouse_name>');
> ```

Where:

`warehouse_name`
:   Specifies the name of the warehouse that the connector should use.

Note

Before configuring the connector to use a different warehouse, verify that the
[connector application](/connectors/servicenow/installing-sql#label-connector-servicenow-install-v2)
has the USAGE privilege for the new warehouse.

Additionally, the connector has to be in the `paused` state. See [pausing the connector](#label-servicenow-connector-stop-connector-v2).

## Deleting tables

To delete table state data (including configuration, statistics, internal connector data, related tasks) and not display the table in the
[views for monitoring the connector](/connectors/servicenow/monitoring#label-monitoring-the-servicenow-connector-v2), use the following procedure:

> Copy code
>
> ```
> CALL DELETE_TABLE('<table_name>', <drop_related_objects>);
> ```

Where:

`table_name`
:   Specifies the name of the table to be deleted. This table must be [disabled](/connectors/servicenow/ingestion#label-servicenow-connector-configure-enable-sync-v2)
    and not in the process of [reloading](/connectors/servicenow/ingestion#label-servicenow-connector-cancel-reload-table-v2).

`drop_related_objects` *(optional)*
:   Specifies whether to drop the related objects. If set to `true`, the procedure also drops all objects created for this table in the destination database,
    including views, raw data and event log tables. If set to `false`, the table state is dropped, but the related objects remain intact.

Note

By default, the `DELETE_TABLE` procedure does not remove the objects created for this table in the destination database that contain the ServiceNow® data in Snowflake
(such as [raw data table](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-raw-v2), [event logs table](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-event-logs-v2),
and [flattened views](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-flattened-v2)). You can either provide the *drop\_related\_objects* parameter or drop these objects manually.

To drop these elements manually, you must first transfer the ownership of them from the connector using a role with *MANAGE GRANTS* privilege. For example:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT OWNERSHIP ON TABLE <destination_database>.<destination_schema>.<table_name> TO ROLE ACCOUNTADMIN REVOKE CURRENT GRANTS;
DROP TABLE <destination_database>.<destination_schema>.<table_name>;
```

## Updating the refresh token used by the connector

If you set up the connector with OAuth authentication, you must update the refresh token regularly. Otherwise, once the token expires,
the connector cannot access ServiceNow® anymore. By default, the token expires 90 days after its generation.

If you configure [email alerts](/connectors/servicenow/monitoring#label-monitoring-the-servicenow-connector-email-alerts-v2) for the connector,
you get a reminder to update the refresh token on the first day of each month. If the token expires, you get an email
once the connector encounters issues accessing ServiceNow®.

### Updating the refresh token for the connector installed using Snowsight

To update the refresh token if the connector was [installed using Snowsight](/connectors/servicenow/installing-snowsight#label-connector-servicenow-install-ui-v2), do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.

   Note

   Make sure that the Snowsight URL you are using matches Snowsight URL that was used when OAuth redirect URL was
   configured. That is, if OAuth redirect URL set in ServiceNow® was provided by Snowsight accessed via Private Link,
   you should be signed in to Snowsight via Private Link to refresh the token. Similarly, when redirect URL was
   configured with publicly accessible Snowsight URL, the refresh should be done by Snowsight accessible with public
   URL.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the **Snowflake Connector for ServiceNow**, then select the tile for the connector.
4. In the top navigation menu select **Settings** » **Authentication** » **Reauthenticate**.

   > Note
   >
   > Make sure you are logged in to ServiceNow® as the same user the connector was initially configured with.
   > You can check the currently logged in user in the upper right corner of the dialog.
5. To confirm that you allow the connector to connect to your ServiceNow® account, select **Allow** in the dialog.
   The refresh token is now updated.

To learn how to update the refresh token using SQL commands, refer to [Updating the refresh token using SQL commands](#label-servicenow-connector-updating-refresh-token-sql-v2).

### Updating the refresh token using SQL commands

To update the refresh token using SQL commands do the following:

1. Get a new [OAuth refresh token](/connectors/servicenow/installing-sql#label-servicenow-connector-generate-oauth-refresh-token-v2).
   Make sure you use the same `client_id`, `client_secret` and user credentials that the connector is using at the moment.
2. Find out the fully qualified name of the secret object by querying the [CONNECTOR\_CONFIGURATION view](/connectors/servicenow/monitoring#label-monitoring-the-servicenow-connector-v2):

   Copy code

   ```
   SELECT value FROM connector_configuration WHERE config_key = 'secret';
   ```
3. Update the secret object by running the [ALTER SECRET](/sql-reference/sql/alter-secret) commands, changing the following parameters:

   - Set `OAUTH_REFRESH_TOKEN` to the OAuth refresh token that you retrieved in the first step.
   - Set `OAUTH_REFRESH_TOKEN_EXPIRY_TIME` to the refresh token expiration timestamp in UTC timezone. You can calculate
     this by adding the refresh token lifespan from ServiceNow® to the date when the token was issued. By default, the
     token expires in 100 days.

   For example, to update the `secretsdb.apiauth.servicenow_creds_oauth_code` secret, run the following command:

   Copy code

   ```
   ALTER SECRET secretsdb.apiauth.servicenow_creds_oauth_code SET OAUTH_REFRESH_TOKEN = '34n;vods4nQsdg09wee4qnfvadH', OAUTH_REFRESH_TOKEN_EXPIRY_TIME = '2022-01-06 20:00:00';
   ```

   Note

   To update the secret, you must use the role with OWNERSHIP privilege.

   - If you [installed the connector using Snowsight](/connectors/servicenow/installing-snowsight#label-connector-servicenow-install-ui-v2), the role is ACCOUNTADMIN.
   - If you [installed the connector using SQL commands](/connectors/servicenow/installing-sql#label-servicenow-connector-prereqs-secret-create-v2), the role is secretadmin.

## Updating the ServiceNow® password for basic authentication

To update the password you need to find an existing secret and modify it using the [ALTER SECRET](/sql-reference/sql/alter-secret) command.

1. Determine the fully qualified name of the secret object using either Snowsight or SQL command.

   1. To get a secret using Snowsight, do the following:

      1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the `ACCOUNTADMIN` role.
      2. In the navigation menu, select **Catalog** » **Apps**.
      3. Search for the **Snowflake Connector for ServiceNow**, then select the tile for the connector.
      4. In the top navigation menu select **Settings** » **Authentication**.

         The **Authentication** section shows the secret object, for example: `CONNECTORS_UI.SERVICENOW_GZSTZTP0KHD.SECRET`.
   2. To get the fully qualified name of the secret object using SQL command, query the [CONNECTOR\_CONFIGURATION view](/connectors/servicenow/monitoring#label-monitoring-the-servicenow-connector-v2):

      Copy code

      ```
      SELECT value FROM connector_configuration WHERE config_key = 'secret';
      ```
2. [Pause](#label-servicenow-connector-stop-connector-v2) the connector.
3. Update the secret object by running the [ALTER SECRET](/sql-reference/sql/alter-secret) command, changing the `PASSWORD` parameter.
4. [Resume](#label-servicenow-connector-resume-connector-v2) the connector.
   The password is now updated and used by the connector.

Note

Similar to changing the password, you have the option to update the username using [ALTER SECRET](/sql-reference/sql/alter-secret) command. Simply set the `USERNAME` parameter to the new username.
Before changing the username, ensure that the new username has, at the very least, the same privileges as the previous one, otherwise, the connector may not function properly.

## Updating the connection to ServiceNow® instance

It’s possible to update the connection to ServiceNow® instance. It lets you change External Access Integration and Secret
used by the connector. It also lets you fix the issue when the Secret was detached from the External Access UDF in the
connector.

The connection configuration can be updated with the following procedure:

Copy code

```
CALL UPDATE_CONNECTION_CONFIGURATION({
  'service_now_url': '<servicenow_base_url>',
  'secret': '<secret_name>',
  'external_access_integration': '<external_access_integration_name>'
});
```

Where:

> `servicenow_base_url`
> :   Specifies the URL of the ServiceNow® instance that the connector should use. The URL must be set to the same value
>     as during connector installation and should be in the following format:
>
>     Copy code
>
>     ```
>     https://<servicenow_instance_name>.service-now.com
>     ```
>
>     Change of the ServiceNow® instance URL is not supported.
>
> `secret_name`
> :   Specifies the fully qualified name of the
>     [secret object containing the credentials for authenticating to ServiceNow®](/connectors/servicenow/installing-sql#label-servicenow-connector-prereqs-secret-create-v2).
>
>     You must specify the fully qualified name of the secret object in the following format:
>
>     Copy code
>
>     ```
>     <database_name>.<schema_name>.<secret_name>
>     ```
>
>     The names of the database, schema, and secret must be valid [object identifiers](/sql-reference/identifiers-syntax).
>
> `external_access_integration_name`
> :   Specifies the name of the
>     [external access integration for ServiceNow®](/connectors/servicenow/installing-sql#label-servicenow-connector-prereqs-external-access-integration-v2).
>
>     The name of the integration must be a valid [object identifier](/sql-reference/identifiers-syntax).

For example, to update the connection to a ServiceNow® instance that:

- Has the URL `https://myinstance.service-now.com`.
- Uses the secret stored in `secretsdb.apiauth.servicenow_creds_oauth_code`.
- Uses the external access integration named `servicenow_external_access_integration`.

Run the following command:

Copy code

```
CALL UPDATE_CONNECTION_CONFIGURATION({
  'service_now_url': 'https://myinstance.service-now.com',
  'secret': 'SECRETSDB.APIAUTH.SERVICENOW_CREDS_OAUTH_CODE',
  'external_access_integration': 'SERVICENOW_API_INTEGRATION'
});
```

The update of the configuration can be performed only by a user with a grant to the `ADMIN` application role. Additionally,
to run the procedure the connector has to be in the `paused` state. See [pausing the connector](#label-servicenow-connector-stop-connector-v2).

## Exporting the connector state

It’s possible to export a snapshot of the current connector state and configuration. The snapshot with the exported connector state is useful when
reinstalling the connector to preserve already enabled tables and the ingestion state, or when replication of the
destination schema to the failover region is configured to aid with disaster recovery.

The state can be exported with the following procedure:

> Copy code
>
> ```
> CALL EXPORT_CONNECTOR_STATE();
> ```

The procedure creates a new `__CONNECTOR_STATE_EXPORT` table in the destination schema with an exported state. To perform an
export the following conditions must be met:

- The export can be performed only by a user with a grant to the `ADMIN` application role.
- There is no ongoing table [reload](/connectors/servicenow/ingestion#label-servicenow-connector-cancel-reload-table-v2).

Note

The `__CONNECTOR_STATE_EXPORT` table contains all information necessary to restore the connector state during reinstallation,
but it’s worth noting some information is missing:

- The destination database and destination schema, warehouse, Data Reader role, ServiceNow URL, Secret object, External Access
  Integration and name of journal table (if configured) aren’t exported. This information must be provided again when reinstalling the connector.
  This can be used as an opportunity to e.g. change Secret object or name of journal table used by the Connector, provided that
  after the reinstallation the same ServiceNow instance and destination schema will be used.
- For each ingested table and ingestion mode only the newest ingestion state is exported. As a result after the connector state import,
  historical data and statistics won’t be available.

Configuration is also exported automatically each time the connector triggers the ingestion according to [configured schedule](/connectors/servicenow/ingestion#label-servicenow-connector-configure-schedule),
provided the following conditions are met:

- At least one table is enabled for ingestion.
- There is no ongoing table reload.

## Uninstalling the application

This section explains how to uninstall the application with Snowsight and with worksheets and how to remove
the objects created by the connector, but which need to be intentionally removed by the user.

### Uninstalling the application using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the **Snowflake Connector for ServiceNow**, then select the three-dot menu to open the contextual view and select **Uninstall**.
4. If all the ingested data staying in the destination database should be preserved, choose **Transfer object ownership to another role**
   and choose the role which should be granted ownership on all the objects owned by the application. Otherwise, select
   **Delete all objects** to remove all the data.

   Note

   Too see what objects would be transferred to the selected role (or removed), expand **Show objects** menu.
5. Select **Uninstall** to confirm the changes. The connector’s application is now uninstalled.

### Uninstalling the application using worksheets

Data ingested by the connector remains in the selected destination database and schema, which are owned by the role
used for connector’s installation (usually it will be ACCOUNTADMIN). However, all sink tables and views containing your ServiceNow® data within the destination schema
are owned by the Snowflake Connector for ServiceNow® application. Therefore if you uninstall the connector before transferring the ownership of these tables and views
to an account role, they will be deleted as well.

Note

If you do not want data to be deleted along with the connector, transfer the ownership of all tables and views in the destination schema to an account role and revoke current grants from the application.

To prevent disruption in existing pipelines using ingested data, we recommend that all pipelines use dedicated Data Owner role to access the data, to which the ownership should be temporarily transferred.

If you have granted additional privileges on the tables and views in the destination schema that your pipelines rely on, you can run the ownership transfer query below with COPY CURRENT GRANTS clause instead of REVOKE CURRENT GRANTS to keep these grants.

To transfer ownership of all tables and views in the destination schema to an account role, run the following queries:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> GRANT OWNERSHIP ON ALL TABLES IN SCHEMA <destination_database>.<destination_schema>
> TO ROLE <account_role>
> REVOKE CURRENT GRANTS;
>
> GRANT OWNERSHIP ON ALL VIEWS IN SCHEMA <destination_database>.<destination_schema>
> TO ROLE <account_role>
> REVOKE CURRENT GRANTS;
> ```

To ensure the connector does not own any objects you do not want removed, run the following query:

> Copy code
>
> ```
> SHOW OBJECTS OWNED BY APPLICATION <application_name>;
> ```

Finally, to drop the connector application, run the following query:

> Copy code
>
> ```
> DROP APPLICATION <application_name>;
> ```

Warning

If you have decided not to transfer the ownership of tables and views in the destination schema away from the connector, you can run this query to drop them alongside the connector instead:

> Copy code
>
> ```
> DROP APPLICATION <application_name> CASCADE;
> ```

### Deleting the objects created during the installation

Removing the connector database does not delete the ingested data that is stored in a separate database or the
objects that were created during the installation performed using Snowsight.

To see objects created during the installation, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the **Snowflake Connector for ServiceNow**, then select it.
4. In the top navigation menu select **Settings** » **Authentication**.

   **Secret**, **External Access Integration** and **Security Integration** are the objects that you need to remove manually.
   In addition to these objects, there might be also a **Network Rule** object staying in the same schema as the secret (if the application was installed using Snowsight).

   Warning

   Secret’s and network rule’s database and schema can also be dropped. However, be careful if you are also using other Snowflake’s connectors,
   for example Snowflake Connector for Google Analytics Raw Data. Objects of such application might also be located in the same database.

To delete those objects run the [DROP <object>](/sql-reference/sql/drop) command.

For example, to delete the secret, run the [DROP SECRET](/sql-reference/sql/drop-secret) statement.

## Upgrading the connector

The connector is upgraded automatically meaning that the user does not need to perform any action in order to have an up to date application.

## Scaling the connector

If there’s many ServiceNow® tables to be ingested and you want to increase the number of concurrently ingested tables, you can change the parameter by:

> Copy code
>
> ```
> CALL CONFIGURE_CONCURRENCY(<number>);
> ```

Where:

`number`
:   Specifies the maximum number of workers able to ingest tables concurrently. By default this value is set to 10.

    Tables with continuous schedule use separate pool of dedicated workers and are not counted towards the concurrency limit.

Increasing the concurrency should be considered along with changing the size of the warehouse used for data ingestion.
If you are experiencing any slowdowns, try resizing the warehouse. See [Working with warehouses](/user-guide/warehouses-tasks) for more information.

Warning

Increasing the concurrency may result in an overloaded ServiceNow® instance, which will result in overall lower performance
and ingestion errors. Compare connector’s performance and stability before and after any scaling changes to find the best parameters.

## Reinstalling the connector with the same database and schema for ServiceNow® data

To reinstall the connector, follow the process below:

1. Query the `TABLES_STATE` view and verify that none of the tables is currently in `RELOADING` status:

   Copy code

   ```
   SELECT TABLE_NAME FROM TABLES_STATE WHERE STATUS = 'RELOADING';
   ```
2. If any tables are currently reloading, wait for reloads to complete or [cancel them](/connectors/servicenow/ingestion#label-servicenow-connector-cancel-reload-table-v2).
3. Stop the connector by calling the following stored procedure:

   Copy code

   ```
   CALL PAUSE_CONNECTOR();
   ```
4. Export connector’s state and configuration. See [this section](#label-servicenow-connector-exporting-connector-state-v2) for details.

   Important

   It’s recommended to export a connector’s state and configuration **before** dropping the connector application.
   This will allow the preservation of all custom options (for example, tables enabled for synchronization and their schedules) and state
   with their most fresh changes in the new installation.

   If you have already removed the connector but left the database and schema containing the ingested data intact, you can still reinstall the connector
   relying on the automatically exported state but the reinstalled connector might repeat ingestion of some records.
5. [Remove the connector](#label-deleting-the-servicenow-connector-manually-v2), transferring the ownership of tables and views in the destination schema.
6. Reinstall the connector by:

   - [reinstalling the connector using Snowsight](/connectors/servicenow/installing-snowsight#label-connector-servicenow-install-ui-v2) (preferred).
   - [reinstalling the connector using SQL](/connectors/servicenow/installing-sql).

During the installation process:

- Provide the previously used database and schema.

  After installation the connector will detect that database and schema contain ingested data and will continue the ingestion
  from the place it was left before reinstallation. If you exported connector state and it’s successfully imported during
  installation, previously ingested tables will be automatically enabled with the same schedules and configuration. Otherwise,
  you will have to manually enable all tables and e.g. configure their schedules to restore the ingestion.

  When reinstalling with SQL commands, remember to transfer the ownership of views and tables in the destination schema
  to the connector, as described in the SQL installation guide. Otherwise the connector will not have access to these tables
  and views, preventing it from resuming the ingestion.
- Provide the same ServiceNow® instance name.
- For the other arguments, you can reuse [the objects that you created when installing the connector](/connectors/servicenow/installing-sql#label-connector-servicenow-set-up-v2), or you can use new objects.
