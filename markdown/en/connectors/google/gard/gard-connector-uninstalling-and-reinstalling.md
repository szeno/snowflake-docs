# Uninstalling and reinstalling the Snowflake Connector for Google Analytics Raw Data

This topic provides information on uninstalling and reinstalling the Snowflake Connector for Google Analytics Raw Data.

## Uninstalling the Snowflake Connector for Google Analytics Raw Data

Data ingested by the connector remains in the selected destination database and schema, which are owned by the
customer’s role. However, all sink tables and views containing your Google Analytics data within the destination schema
are owned by the Snowflake Connector for Google Analytics Raw Data application. Therefore if you uninstall the connector before transferring the ownership of these tables and views
to an account role, they will be deleted as well.

Note

If you do not want data to be deleted along with the connector, transfer the ownership of all tables and views in the destination schema to an account and revoke current grants from the application.

To transfer ownership of all tables and views in the destination schema to an account role, run the following queries:

> Copy code
>
> ```
> GRANT OWNERSHIP ON ALL TABLES IN SCHEMA <destination database>.<destination schema>
> TO ROLE <account role>
> REVOKE CURRENT GRANTS;
>
> GRANT OWNERSHIP ON ALL VIEWS IN SCHEMA <destination database>.<destination schema>
> TO ROLE <account role>
> REVOKE CURRENT GRANTS;
> ```

To ensure the connector does not own any objects you do not want removed, run the following query:
:   Copy code

    ```
    SHOW OBJECTS OWNED BY APPLICATION <application name>;
    ```

During the connector configuration some Snowflake objects which are not owned by the application are created and they will not
be removed automatically during the uninstallation. If you want to remove them as well, you are able to do so by dropping them manually using SQL queries.
Objects are:

- A network rule inside the `CONNECTORS_SECRET.<application name>` schema.
- A secret listed in the **Settings** » **Authentication** tab.
- An external access integration listed in the **Settings** » **Authentication** tab.
- A security integration listed in the **Settings** » **Authentication** tab.

To drop these objects, run the following queries:

> Copy code
>
> ```
> DROP SECRET CONNECTORS_SECRET.<application name>.SECRET;
>
> DROP NETWORK RULE CONNECTORS_SECRET.<application name>.NETWORK_RULE;
>
> DROP EXTERNAL ACCESS INTEGRATION <external access integration name>;
>
> DROP SECURITY INTEGRATION <security integration name>;
> ```

For the secret and network rule, you may also want to drop their enclosing database and/or schema.

In order to uninstall the Snowflake Connector for Google Analytics Raw Data follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for Google Analytics Raw Data.
4. Select **Uninstall**.

## Reinstalling the connector with the same database and schema

If you removed the connector but left the database and schema containing the ingested data intact, you can later reinstall the connector and resume data ingestion from the point where the connector was last run.

Note

To ensure data consistency, ensure that the current ingestion has completed and stopped before uninstalling the connector.

After uninstalling the connector, you can reinstall the connector by selecting **Catalog** » **Apps** in the navigation menu.

During the installation process:

- Provide the previously used database and schema.
- Provide the connector configuration.
- Provide the same ingestion configuration.

By providing the same configuration information, the connector can resume the ingestion process instead of starting over.
However, you need to ensure that the previously ingested data is available in the destination table before finalizing the configuration.
If you manually ingest the data once the connector is running, the ingestion process will start from the beginning.

Note

If you uninstalled the connector during an ongoing ingestion, incomplete data from the last daily table whose ingestion was interrupted is deleted and re-ingested.
