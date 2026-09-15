# Request access to external and Apache Iceberg™ tables

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how a provider can configure an app to request that a consumer allow the app to
access external and Apache Iceberg™ tables that a provider shares in an app.

## About external and Iceberg tables in a Snowflake Native App

The Snowflake Native App Framework allows providers to share [external tables](/user-guide/tables-external-intro) and
[Apache Iceberg™ tables](/user-guide/tables-iceberg) with consumers. For general information,
see [Support for external and Iceberg tables](/developer-guide/native-apps/preparing-data-content#label-native-apps-ext-table).

To include an external or Iceberg table in an app:

1. Add the table to the app. See [Share data content in a Snowflake Native App](/developer-guide/native-apps/preparing-data-content).
2. [Add an entry for external and Iceberg tables to the manifest](#label-native-apps-ext-table-manifest).
3. [Request permissions to access external and Iceberg tables](#label-native-apps-ext-table-sdk).

Caution

Before an app can access a shared external or Iceberg table,
the consumer must explicitly give the app permission to use the table. For more information, see [Enable external and Apache Iceberg™ tables](/developer-guide/native-apps/ui-consumer-granting-privs#label-enable-ext-iceberg-tables).

## Add an entry for external and Iceberg tables to the manifest

To include external or Iceberg tables in an app, providers must add
an entry in the manifest file as shown in the following example:

Copy code

```
restricted_features:
  - external_data:
     description: “The reason for enabling an external or Iceberg table.”
```

## Request permissions to access external and Iceberg tables

For security and cost considerations, consumers must explicitly give an app permissions
to use an external or Iceberg table.

Note

If an app attempts to resolve an external or Iceberg table directly in setup script
the setup script fails if the consumer has not yet given permission to the app. To access external
data, for example to create a view from an external table, providers should create the view
in a stored procedure in the setup script. The app can then call the stored procedure after the
consumer gives the app permission.

To allow a custom Streamlit app to access external and Iceberg tables, the Python Permission SDK provides the following functions:

`request_external_data() -> None`
:   Causes Snowsight to display a dialog that prompts the consumer to allow the app to
    access the external or Iceberg tables required by the app.

`is_external_data_enabled() -> boolean`
:   Determines if the consumer has allowed the app to use external or Iceberg tables. Returns
    `True` if allowed. Returns `False`, otherwise.

Alternatively, a consumer can run the [SYSTEM$SET\_APPLICATION\_RESTRICTED\_FEATURE\_ACCESS](/sql-reference/functions/system_set_application_restricted_feature_access) system function to allow an app access to external and Iceberg tables.
