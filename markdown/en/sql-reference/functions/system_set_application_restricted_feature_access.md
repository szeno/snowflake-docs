Categories:
:   [System functions](/sql-reference/functions-system) (Control)

# SYSTEM$SET\_APPLICATION\_RESTRICTED\_FEATURE\_ACCESS

Enables a restricted feature for a Snowflake Native App. Currently, only external and Apache Iceberg™ tables are
supported.

## Syntax

Copy code

```
SYSTEM$SET_APPLICATION_RESTRICTED_FEATURE_ACCESS(
  '<app_name>',
  '<type>',
  '<parameters>'
)
```

## Arguments

`app_name`
:   Name of the Snowflake Native App.

`type`
:   The type of restricted feature. Currently only `EXTERNAL_DATA` is supported.

`parameters`
:   A JSON object that contains configuration parameters for the restricted feature. Currently,
    only JSON objects of the following format are supported:

    Copy code

    ```
    {"allowed_cloud_providers" : "all"}
    ```

    The supported values for `allowed_cloud_providers` are `all` and `none`.

## Returns

A JSON object containing a list of external features whose value the consumer has set. The JSON
object has the following structure:

Copy code

```
"{""external_data"":{""allowed_cloud_providers"":""all""}}"
```

## Examples

To call the function:

Copy code

```
SELECT SYSTEM$SET_APPLICATION_RESTRICTED_FEATURE_ACCESS('hello_snowflake_app', 'external_data', '{"allowed_cloud_providers" : "none"}');
```

Sample output:

```
"SYSTEM$SET_APPLICATION_RESTRICTED_FEATURE_ACCESS('EXTERNAL_DATA_DEMO_APP', 'EXTERNAL_DATA', '{""ALLOWED_CLOUD_PROVIDERS"" : ""NONE""}')"
"{""external_data"":{""allowed_cloud_providers"":""none""}}"
```
