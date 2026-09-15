# Access the ServiceNow® data in Snowflake

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

This topic describes how to access ServiceNow® data from your Snowflake account.

For each table in ServiceNow® that is configured for synchronization, the connector creates the following tables
and views:

- A table with the same name that contains the data in raw form, where each record is contained in a single
  VARIANT column.
- A table named `table_name__event_log` that contains the history of changes made to ServiceNow® records.
- A view named `table_name__view` that contains the data in flattened form, where the view contains a
  column for each column in the original table and a row for each record that is present in the original table.
- A view named `table_name__view_with_deleted` that contains the same data as
  `table_name__view` as well as rows for records that have been deleted in ServiceNow®.

Note

After starting the connector, it may take some time for the views to be created.

View creation depends on data in the ServiceNow® `sys_db_object`, `sys_dictionary` and `sys_glide_object` tables.
The connector loads metadata from these tables after a business table is enabled for synchronization.
When the metadata tables are ingested, a background task will create flattened views of the enabled tables.
The task is run as often as the schedule of the most frequent table ingestion. After the metadata tables are synced,
the task also captures any table schema changes and updates the already created views accordingly (only the views
with the suffixes `__view` and `__view_with_deleted`, but not with `__view_with_display_values`).

As it’s not an immediate process, status of view creation process is available under the `CONFIGURED_TABLES` view.
If the view creation takes too long, the `CONNECTOR_ERRORS` view can also be checked for any related errors.

Warning

If you plan to set [ROW ACCESS POLICIES](/user-guide/security-row-using) on the tables
and views created by the connector, make sure they do not block access to the role with the same name as the connector application.
For example, if your connector application instance is called `MY_CONNECTOR_SERVICENOW`, then your policies cannot
block a role named `MY_CONNECTOR_SERVICENOW`. Otherwise, the policies will interfere with the data ingestion process.

The following sections explain how to grant the privileges to access this data and how to access the data from
these tables and views.

## Grant privileges for accessing the ServiceNow® data in Snowflake

After the Snowflake Connector for ServiceNow® synchronizes the data with Snowflake, to access the ServiceNow® data a role needs:

- USAGE privilege on the database and schema that contain the ServiceNow® data in Snowflake, and
- a [DATA\_READER application role](https://other-docs.snowflake.com/en/connectors/servicenow/v2/application-roles#data-reader-application-role).

Snowflake recommends creating a dedicated role with these privileges that can be granted to users who need
access to the ingested ServiceNow® data. If the connector has been [installed with Snowsight](/connectors/servicenow/installing-snowsight#label-connector-servicenow-install-ui-v2)
then the role provided during [Configure](/connectors/servicenow/installing-snowsight#label-connector-servicenow-install-ui-configure-v2) step already has the necessary privileges.

For example, if you configured the connector application called `my_connector_servicenow` to store the ServiceNow®
data in the `dest_db` database and `dest_schema` schema, you can create a role named
`servicenow_data_reader_role` and grant the privileges for accessing the data to that role.

The following example shows how to grant these privileges:

> Copy code
>
> ```
> CREATE ROLE servicenow_data_reader_role;
> GRANT USAGE ON DATABASE dest_db TO ROLE servicenow_data_reader_role;
> GRANT USAGE ON SCHEMA dest_db.dest_schema TO ROLE servicenow_data_reader_role;
> GRANT APPLICATION ROLE my_connector_servicenow.DATA_READER to role servicenow_data_reader_role;
> ```

Note

- Do not run `GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA` on the schema that contains the ServiceNow® data
  in Snowflake. Also, do not change the ownership of the tables that are already created by the connector.
  Changing the ownership prevents the connector from ingesting the data to the table.
- Do not change the ownership of the views in the schema that contains the ServiceNow® data in Snowflake.
  Changing the ownership prevents the connector from updating the views when changes occur in the
  ServiceNow® table schema.

## Access the raw data

For each ServiceNow® table that you synchronize, the Snowflake Connector for ServiceNow® creates a new table with
the same name in the database and schema for the ServiceNow® data in Snowflake.

For example, if you configured the connector to store the ServiceNow® data in the `dest_db` database and
`dest_schema` schema, and if you configured the connector to synchronize the `incident` table in
ServiceNow®, the connector creates the table named `dest_db.dest_schema.incident`.

This table contains raw data ingested from ServiceNow®. This table contains the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| `sys_id` | VARCHAR | The value of the `sys_id` of the record in ServiceNow®. |
| `raw` | VARIANT | The data for the record in raw form. |
| `is_deleted` | BOOLEAN | Specifies whether or not the record was deleted in ServiceNow®. |
| `last_update_date` | TIMESTAMP\_NTZ | The last time the record was updated in Snowflake. Note that the displayed timestamp is provided in the UTC timezone with no offset, which may differ from the timezone of dates displayed in the ServiceNow instance. |

Expand

Show lessSee more

The following is an example of the output for a SELECT statement that retrieves the data for the
`dest_db.dest_schema.incident` table:

> Copy code
>
> ```
> SELECT * FROM DEST_DB.DEST_SCHEMA.INCIDENT LIMIT 5;
>
> +----------------------------------+-------------------------+-------------+--------------------------+
> | SYS_ID                           | RAW:ACTIVE              |  IS_DELETED | LAST_UPDATE_DATE         |
> +----------------------------------+-------------------------+-------------+--------------------------+
> | caa04d36db8ba0106e9643c81396197b | {"active": "true", ...} |  FALSE      |  2021-08-24 12:59:23.932 |
> | cea045be1b03e010eac562c4bd4bcbb2 | {"active": "true", ...} |  FALSE      |  2021-08-24 12:59:23.932 |
> | caa0c9bedb8be010f9f19c41ba961934 | {"active": "true", ...} |  FALSE      |  2021-08-24 12:59:23.932 |
> | caa0c9bedb8be010f9f19c41ba961969 | {"active": "true", ...} |  FALSE      |  2021-08-24 12:59:23.932 |
> | b9a0c53adb436410d6fa2b691396190a | {"active": "true", ...} |  FALSE      |  2021-08-24 12:59:23.932 |
> +----------------------------------+-------------------------+-------------+--------------------------+
> ```

## Access the flattened data

For each table that contains data, the connector creates two flattened views over the raw data.
The names of the views are the names of the table with the suffixes `__view` and
`__view_with_deleted`. For example, for the ServiceNow® table named `incident`, the connector creates
the following views:

- `dest_db.dest_schema.incident__view`
- `dest_db.dest_schema.incident__view_with_deleted`

The view with the `__view` suffix contains the records that are in the ServiceNow® table. The view with
the `__view_with_deleted` suffix includes these same records as well as the records that were deleted
from the ServiceNow® table.

Note the following:

- The names of the columns in these views are in uppercase. You cannot use lowercase names to access these
  columns.
- Columns with time and timestamps are always saved using the UTC timezone, regardless of the timezone set in the
  ServiceNow instance. As a result, depending on the ServiceNow instance configuration, their displayed values may
  differ from the values displayed in the ServiceNow instance. The difference relates only to displayed values, timestamps both
  in ServiceNow and Snowflake are referring to the same point in time.
- There are no views for empty tables. After data appears in the table in ServiceNow®, the view is created.
- Although the connector handles changes to the schema, the connector does not reload the data.

  As a result, in the case of schema changes, records from the old schema are not updated.

The following is an example of the output for a SELECT statement that retrieves the data from the
`dest_db.dest_schema.incident_view` view. In this example, the `incident` table in ServiceNow® has columns
named `ACTIVE`, `APPROVAL`, `CATEGORY`, and `ESCALATION`.

> Copy code
>
> ```
> SELECT ACTIVE, APPROVAL, CATEGORY, ESCALATION
> FROM DEST_DB.DEST_SCHEMA.INCIDENT__VIEW LIMIT 5;
>
> +--------+----------------+------------------+------------+
> | ACTIVE | APPROVAL       | CATEGORY         | ESCALATION |
> +--------+----------------+------------------+------------+
> | TRUE   | not requested  | software         | 0          |
> | TRUE   | not requested  | Cloud Management | 0          |
> | TRUE   | not requested  | software         | 0          |
> | TRUE   | not requested  | network          | 0          |
> | TRUE   | not requested  | database         | 0          |
> +--------+----------------+------------------+------------+
> ```

## View the event logs for a table

The Snowflake Connector for ServiceNow® can track the changes made to records in ServiceNow®. This tracking
information is stored in tables called event logs.

For every ServiceNow® table enabled for synchronization, the connector creates an event log table within
Snowflake named `<destination_db>.<destination_schema>.<table_name>__event_log`.

Each event log table has the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| `sys_id` | VARCHAR | The value of the `sys_id` of the record in ServiceNow®. |
| `sys_updated_on` | VARCHAR | The date the record was last updated in ServiceNow®. If there is no `sys_updated_on` field in the ServiceNow® table, this column contains null values. Note that the displayed timestamp is provided in the UTC timezone with no offset, which may differ from the timezone of dates displayed in the ServiceNow instance. |
| `event_date` | TIMESTAMP\_NTZ | The date the event was inserted in the event log. Note that the displayed timestamp is provided in the UTC timezone with no offset, which may differ from the timezone of the dates displayed in the ServiceNow instance. |
| `raw` | VARIANT | The current data of the record event. For DELETE events, this is the data of the record at the time of deletion. |
| `event_type` | VARCHAR | Specifies if the record was inserted, updated, or deleted from ServiceNow®. |

Expand

Show lessSee more

The event log reflects the history of data changes in the corresponding ServiceNow® table. For example, if a
new record is inserted into the `u_ip_port` table in ServiceNow®, a record with `event_type` set to
`INSERT` event type is added to the `dest_db.dest_schema.u_ip_port__event_log` table in Snowflake.

Similarly, if a record is updated or deleted in a table in ServiceNow®, a record with `event_type` set to
`UPDATE` or `DELETE` is added to the `dest_db.dest_schema.u_ip_port__event_log` table.

The tables in Snowflake that contain the raw data (`dest_db.dest_schema.table_name`) are derived
from the corresponding event log tables (`dest_db.dest_schema.table_name__event_log`). For example:

- If a record for an `INSERT` event is added to `table_name__event_log`, the connector adds a
  corresponding record to the `table_name` table.
- If an `UPDATE` event for the given `sys_id` is added to the event log table, the connector
  updates the corresponding record with the `sys_id` in the `table_name` table with new data.
- If a `DELETE` event occurs, the `is_deleted` flag of the corresponding record in
  `table_name` is set to `true`.

## Get the display value of a reference field

In ServiceNow® tables, some fields are [reference fields](https://docs.servicenow.com/bundle/washingtondc-platform-administration/page/administer/field-administration/concept/c_ReferenceField.html), which contain references to records in other tables.

In the example below, the field `opened_by` in the `incident` table is a reference field that
contains a reference to the record with the `sys_id` `<sys_id>` in another
table (`sys_user`):

> Copy code
>
> ```
> {
>   "link": "https://myinstance.service-now.com/api/now/table/sys_user/<sys_id>",
>   "value": "<sys_id>"
> }
> ```

To show the reference fields in the table, call the `SHOW_REFERENCES_OF_TABLE` stored procedure with the following
argument:

> Copy code
>
> ```
> CALL SHOW_REFERENCES_OF_TABLE('<table_name>');
> ```

Where:

`table_name`
:   Specifies the name of the table you want to show the reference fields for.

This stored procedure inspects the schema of the table and returns a JSON list of objects containing the following properties:

| Property | Description |
| --- | --- |
| `columnName` | Name of the reference field. |
| `referencedColumnName` | Name of the field that the reference points to. |
| `referencedTableName` | Name of the referenced table. |

Expand

Show lessSee more

### Enable data synchronization for referred tables

If a table contains references to other tables, you can enable data synchronization of the referred tables.
To synchronize data for referred tables, call the `ENABLE_REFERENCED_TABLES` stored procedure with the following argument:

> Copy code
>
> ```
> CALL ENABLE_REFERENCED_TABLES('<table_name>');
> ```

Where:

`table_name`
:   Specifies the name of the table (with the table reference fields) for which you want to enable data synchronization.

### Create a view containing reference fields

If the table containing the reference fields and the tables referenced by the those fields have been processed, you can
create a view that replaces the references with display values.

To create this view, call the `CREATE_VIEW_WITH_DISPLAY_VALUES` stored procedure.

Copy code

```
CALL CREATE_VIEW_WITH_DISPLAY_VALUES('<table_name>');
```

Where:

`table_name`
:   Specifies the name of the table containing the table reference fields for which you want to create a view with display value.

Note

Only [reference fields](https://docs.servicenow.com/bundle/washingtondc-platform-administration/page/administer/field-administration/concept/c_ReferenceField.html) with the `sys_id` as [reference key](https://docs.servicenow.com/bundle/washingtondc-platform-administration/page/administer/field-administration/task/t_DefineTheReferenceKey.html) are supported.

Important

This procedure is only run manually, therefore each time the table schema is changed the view must be recreated manually
to reflect the schema change.

After the view is created successfully, the stored procedure returns the name of the newly created view.
The view name is the table name with the `__view_with_references` suffix added.
For example, for a ServiceNow® table named `incident`, the stored procedure creates the view `incident__view_with_references`.
Reference fields are replaced with display values and a new metadata column is added for each reference field.

The display value column has the same name as the reference column being replaced and may be null when if the display value is null or
the reference is not resolved. The metadata column name is the name of the reference column with the `__metadata` suffix.
For example, for a reference column named `user`, the procedure creates a column named `user__metadata`.
The content of this column is a JSON object with a field named `reference_field` with the following properties:

| Property | Description |
| --- | --- |
| `key` | `sys_id` of the referred row. If the reference column or reference column field `value` is null, this property is also null. |
| `reference_table` | Name of the referenced table. If the reference is not resolved this property is null. |
| `link` | ServiceNow® link to the referred row. If the reference column or reference column field `link` is null, this property is also null. |
| `display_value` | Display value. If the reference is not resolved this property is null. |
| `resolved` | `true` if display value is resolved. `false` when the connector cannot resolve the reference. |
| `reason` | Reason the reference failed to resolve. For example `Display value is not ingested yet`. If the reference is resolved this property is not displayed. |

Expand

Show lessSee more

The following example shows how a pair of display value and metadata columns in a view created by the stored procedure
`CREATE_VIEW_WITH_DISPLAY_VALUES` looks like.
The example table `incident` has `opened_by` column which references (by `sys_id` as reference key) to the `sys_user` table.

The `incident__view_with_references` view created by the stored procedure resolves the reference, so the displayed values can be obtained with a simple `SELECT`.

Copy code

```
SELECT OPENED_BY, OPENED_BY__METADATA
  FROM DEST_DB.DEST_SCHEMA.INCIDENT__VIEW_WITH_REFERENCES;
```

This command displays information in the following format:

```
+-----------+------------------------------------+
| OPENED_BY | OPENED_BY__METADATA                |
+-----------+------------------------------------+
| "JOHN"    | {                                  |
|           |   "reference_field": {             |
|           |     "display_value": "JOHN",       |
|           |     "key": "b177...",              |
|           |     "link": "https://...",         |
|           |     "reference_table": "sys_user", |
|           |     "resolved": true               |
|           |   }                                |
|           | }                                  |
+-----------+------------------------------------+
```

### Configure reference link checking for views

When the connector resolves a reference field in a view created by [`CREATE_VIEW_WITH_DISPLAY_VALUES`](#label-servicenow-connector-create-view-with-display-values), it checks
the `link` property of the raw ServiceNow® row and expects the `link` value to end with `/<table>/<sys_id>`.
References whose links are null or do not follow this format are not resolved.

If your instance uses non-standard reference links, or your ACL configuration prevents the connector from accessing links,
you can disable this check by calling the `CONFIGURE_CHECK_LINK_IN_VIEW_WITH_REFERENCES` stored procedure:

Copy code

```
CALL CONFIGURE_CHECK_LINK_IN_VIEW_WITH_REFERENCES(false);
```

This setting applies the next time you create a view with `CREATE_VIEW_WITH_DISPLAY_VALUES`. To apply it to
views that already exist, recreate them.
