Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$SEND\_NOTIFICATIONS\_TO\_CATALOG

Sends a notification to [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) to update Snowflake-managed [Apache Iceberg™ tables](/user-guide/tables-iceberg) in Open Catalog with the latest table changes, and
returns whether the notification was sent successfully along with an error code and error message for the failure, if applicable.

Notifications are a mechanism for keeping Snowflake-managed Iceberg tables that are synced to Open Catalog updated with the latest table
changes. When tables are synced to Open Catalog, notifications are continuously sent to them. However, if notifications aren’t being
sent to a table, you can call this function and use the error message it returns to diagnose the reason for the sync failure.

## Syntax

Copy code

```
SYSTEM$SEND_NOTIFICATIONS_TO_CATALOG( '<domain>' , '<entity_name>' [ , '<notification_type>'] [ , '<catalog_sync_integration_name>'] )
```

## Arguments

**Required:**

`domain`
:   The domain at which to send the notification. You can specify one of the following domains:

    - `DATABASE`
    - `SCHEMA`
    - `TABLE`

    For example, if you want to send a notification to tables under a certain schema, specify `SCHEMA`.

`entity_name`
:   The name of an entity for the given `domain`. Depending on the given domain, `entity_name` specifies the name of a
    database, schema, or table.

**Optional:**

`notification_type`
:   The type of notification to send to Open Catalog. You can specify one of the following types of notifications:

    - `UPDATE`: Updates the state of the table in Open Catalog. If the table doesn’t yet exist, Open Catalog, creates the table.
    - `DROP`: Drops the table from Open Catalog if it exists.

    Default: `UPDATE`

`catalog_sync_integration_name`
:   The name of a catalog integration for Open Catalog to which you want to scope the notifications. The notifications are only sent to a given
    table if the `CATALOG_SYNC` parameter for the table is set to this catalog integration.

    Important

    If you need to specify a value for `catalog_sync_integration_name`, you can’t leave `notification_type` empty to use
    its default value. In other words, if you need to specify a value for `catalog_sync_integration_name` instead of using the
    default, you must first specify `UPDATE` or `DROP` for `notification_type`.

    Default: If the argument is not specified, notifications are sent to all the tables in the domain specified by the required arguments,
    regardless of their catalog sync integration. For example, if you specify `SCHEMA` for `domain` and `schema1` for `entity_name`
    and use the default for `catalog_sync_integration_name`, all tables under `schema1` are notified. This argument is used to limit
    the scope of notifications to a single catalog sync integration.

## Returns

The function returns a JSON object with the properties described below:

| Property | Description |
| --- | --- |
| TABLENAME | Table name that the notification was sent to. It’s presented as the fully qualified table name (Database.Schema.Table). |
| NOTIFICATIONSTATUS | Status of the notification. Returns `TRUE` if the notification was sent successfully to Open Catalog or `FALSE` if it wasn’t sent successfully. |
| ERRORCODE | Error code for the send notification failure. If the notification was sent successfully, this field is empty. |
| ERRORMESSAGE | Error message describing why the notification failed. If the notification was sent successfully, this field is empty. |

Expand

Show lessSee more

## Usage Notes

`domain`, `entity_name`, `notification_type`, and `catalog_sync_integration_name` are all a string data
type, so each must be enclosed in single quotes.

## Examples

Send an `UPDATE` notification to any Snowflake-managed Iceberg table in Open Catalog that is under the `testSchema` schema in Snowflake and is
synced to Open Catalog.

Copy code

```
SELECT VALUE[0]::STRING AS tableName,
       VALUE[1]::BOOLEAN notificationStatus,
       VALUE[2]::STRING errorCode,
       VALUE[3]::STRING errorMessage
  FROM TABLE(FLATTEN(PARSE_JSON(
    SELECT SYSTEM$SEND_NOTIFICATIONS_TO_CATALOG(
      'SCHEMA',
      'testSchema'))));
```

Send a `DROP` notification to any Snowflake-managed Iceberg table in Open Catalog that is named `icebergTable` and is synced to
Open Catalog through the `my_catalog_sync_integration` catalog integration.

Copy code

```
SELECT VALUE[0]::STRING AS tableName,
       VALUE[1]::BOOLEAN notificationStatus,
       VALUE[2]::STRING errorCode,
       VALUE[3]::STRING errorMessage
   FROM TABLE(FLATTEN(PARSE_JSON(
     SELECT SYSTEM$SEND_NOTIFICATIONS_TO_CATALOG(
       'TABLE',
       'icebergTable',
       'DROP',
       'my_catalog_sync_integration'))));
```
