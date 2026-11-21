Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# EXTERNAL\_BI\_OBJECTS view

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This Account Usage view displays a row for each object that [Horizon Catalog metadata connectors](/user-guide/snowflake-horizon/connectors)
collect from external BI tools, such as Tableau and Power BI. The view includes both leaf objects, such as dashboards and charts,
and the containers that hold them, such as folders, projects, and datasets.

For objects collected from databases, data warehouses, and data pipeline tools, see the
[EXTERNAL\_DWH\_OBJECTS view](/sql-reference/account-usage/external_dwh_objects).

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| REFERENCE\_ID | TEXT | Snowflake-generated identifier of the object. This value is always present and uniquely identifies the object. |
| EXTERNAL\_ID | TEXT | Identifier of the object in the BI tool, when known. Otherwise, NULL. |
| NAME | TEXT | Name of the object in the BI tool. |
| OBJECT\_TYPE | TEXT | Type of the object. Rows for containers have one of the following values: `PROJECT`, `FOLDER`, or `DATASET`. Rows for other objects have one of the following values: `TABLE`, `VIEW`, `DATA_SOURCE`, `DASHBOARD`, `DASHBOARD_ELEMENT`, `CHART`, `PAGE`, `REPORT_QUERY`, or `NOTEBOOK`. |
| PARENT\_REFERENCE\_ID | TEXT | `REFERENCE_ID` of the object’s immediate parent in this view. NULL for top-level objects, such as a root folder. |
| CONNECTOR | TEXT | Display name of the metadata connector that collected the object. This is the connector’s name only, not a fully qualified name. |
| CONNECTOR\_TYPE | TEXT | Vendor or type of the BI tool, such as `TABLEAU`. |
| COMMENT | TEXT | Description of the object. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the object was created, as reported by the BI tool. The value comes from the BI tool’s own clock for each object type. For object types that have no creation time in the BI tool, NULL. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the object was last updated, as reported by the BI tool. The value comes from the BI tool’s own clock for each object type, such as the dashboard update time for dashboards. For object types that have no update time in the BI tool, NULL. |
| DELETED | TIMESTAMP\_LTZ | Date and time when Snowflake observed that the object was removed from the BI tool. NULL if the object still exists. |
| PROPERTIES | VARIANT | Additional properties of the object, as an OBJECT. The following keys can be present:   - `bi_object_type`: Type of the object as the BI tool defines it. The possible values depend on the kind of object. - `external_type`: Free-form text that the connector supplies to describe the type of the object.   Both values are passed through from the connector without changes. |
| FOLDER\_PATH | TEXT | Path of the folder that contains the object in the BI tool. Only rows for dashboards and Tableau data sources have a value. For all other object types, including folders, NULL. |
| URL | TEXT | Link to the object in the BI tool, when the tool provides one. Often NULL for containers. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- The view includes objects that were removed from the BI tool. The `DELETED` column is non-NULL for those objects, and their
  rows remain in the view; no retention limit currently applies. To list only current objects, filter on `DELETED IS NULL`.
- The hierarchy depends on the BI tool, for example project, then folder, then dashboard, then chart, or dataset, then report query,
  then page. Use `PARENT_REFERENCE_ID` and `OBJECT_TYPE` to walk it.
- Users and roles that have been granted the OBJECT\_VIEWER database role can access this view. For more information, see
  [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles).
- Access to this view isn’t controlled by privileges on metadata connectors. A role that can query the view sees the objects
  from every connector in the account, including connectors it has no `USAGE` or `READ EXTERNAL METADATA` privilege on.

## Examples

List the dashboards that changed in the last 7 days, with the name of the parent folder:

Copy code

```
SELECT d.name, d.object_type, d.folder_path, d.url, d.connector, d.last_altered,
       f.name AS folder_name
  FROM snowflake.account_usage.external_bi_objects d
  LEFT JOIN snowflake.account_usage.external_bi_objects f
    ON f.reference_id = d.parent_reference_id
  WHERE d.object_type = 'DASHBOARD'
    AND d.last_altered > DATEADD('day', -7, CURRENT_TIMESTAMP())
    AND d.deleted IS NULL;
```
