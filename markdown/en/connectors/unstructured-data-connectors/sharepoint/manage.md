# Manage the Snowflake Connector for SharePoint

[Preview Feature](/release-notes/preview-features) — Open

Support for this feature is available to accounts in most Snowflake regions. See [Regional availability](/connectors/unstructured-data-connectors/sharepoint/about#label-sharepoint-regional-availability) for a full list of regions.

Note

The Snowflake Connector for SharePoint is subject to the [Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Important

Thank you for your interest in the Snowflake Connector for SharePoint.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements is not guaranteed. The new solution is available as [Openflow Connector for SharePoint](/user-guide/data-integration/openflow/connectors/sharepoint/about) and
includes better performance, customizability, and enhanced deployment options.

This topic describes how to manage your Snowflake Connector for SharePoint after you have [installed and configured it](/connectors/unstructured-data-connectors/sharepoint/setup).

You can perform the following tasks to manage the connector:

- Modify the refresh frequency
- Pause or resume the connector
- View the list of source folders

## Modify the refresh frequency

You can modify the refresh frequency to refresh content, metadata and permissions every day, every week, or every month.

To modify the refresh frequency, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for SharePoint and select it.
4. In the connector navigation menu, select **Data sync** » **Manage Content Refresh**.
5. Select **Edit**.
6. In the **Refresh** drop-down list, select either **every day**, **every week**, or **every month**.

You can perform refresh on-demand by running the following SQL command:

Copy code

```
CALL PUBLIC.REFRESH_SHAREPOINT_CONTENT();
```

Note

You must have been assigned the role ACCOUNTADMIN to call the PUBLIC.REFRESH\_SHAREPOINT\_CONTENT procedure.

## Pause or resume the connector

Pausing the connector only pauses the data ingestion from SharePoint and
the processing with the document parsing function of Cortex, and not the Cortex Search service.
The Cortex Search service continues to process previously ingested data. Pausing the connector may
still result in credits consumed by Cortex Search.

Once you resume the connector, the data ingestion and processing restarts and the connector
fetches all changes to files, metadata and permissions since the previous refresh.
The connector also refreshes Cortex Search to use the latest content and permissions.

To pause or resume the connector, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for SharePoint and select it.
4. In the connector navigation menu, select **Data sync** » **Manage Content Refresh**.
5. Select **Pause** or **Resume**.

## View source folders list

To view the list of folders from which the connector ingests your data, use the following command:

Copy code

```
SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_SHAREPOINT.PUBLIC.AVAILABLE_FOLDERS;
```

## Next step

[Monitor the Snowflake Connector for SharePoint](/connectors/unstructured-data-connectors/sharepoint/monitor).
