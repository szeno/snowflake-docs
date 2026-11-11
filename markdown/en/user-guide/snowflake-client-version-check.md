# View the Snowflake client version

To view the version of the Snowflake client used to execute SQL statements in Snowflake, use the **Client Driver** column on
the **Query History** page in Snowsight.

Use this information to determine if the client versions actively used by users in your account meet the
[minimum requirements](/release-notes/requirements). You can also use this information, if applicable, to identify the
client version when submitting cases to [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

To view the versions of Snowflake clients used recently in your account:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Switch role** » **ACCOUNTADMIN**.
3. In the navigation menu, select **Monitoring** » **Query History**.
4. Locate the **Client Driver** column, containing the version of the client or driver that submitted the query:

   If the column isn’t visible, select **Columns** and choose **Client Driver**.
5. Note the client version in the row for each SQL statement.

   For clients and drivers, the column includes an icon that indicates if the client version is supported,
   unsupported, or nearing the end of support. You can hover over the icon to display a tooltip that indicates the
   current status of the client version.

   Snowflake updates the information on which versions are supported every three months. See [Client versions & support policy](/release-notes/requirements).

## Use SQL to view client versions

To list the Snowflake clients and versions used to create sessions in your account, query the
[SESSIONS view](/sql-reference/account-usage/sessions) view. The CLIENT\_APPLICATION\_ID column identifies the Snowflake-provided client
application (for example, `JDBC 3.8.7`), and the CLIENT\_APPLICATION\_VERSION column contains its version number.

Use a role with access to the SESSIONS view. Data in the view can be delayed by up to three hours, and the view doesn’t
track SQL API transient sessions. The query counts sessions, not queries or unique users.

For example, the following query counts the sessions created in the last 30 days by each client application and version:

Copy code

```
SELECT client_application_id,
       client_application_version,
       COUNT(*) AS session_count
  FROM SNOWFLAKE.ACCOUNT_USAGE.SESSIONS
  WHERE created_on >= DATEADD(day, -30, CURRENT_TIMESTAMP())
  GROUP BY client_application_id, client_application_version
  ORDER BY session_count DESC;
```
