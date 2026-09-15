Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LIST\_APPLICATION\_RESTRICTED\_FEATURES

Returns a JSON object containing a list of restricted features that the consumer has
allowed a Snowflake Native App to use.

Note

Currently, only [external and Apache Iceberg™ tables](/developer-guide/native-apps/preparing-data-content#label-native-apps-ext-table) are supported.

## Syntax

Copy code

```
SYSTEM$LIST_APPLICATION_RESTRICTED_FEATURES( '<app_name>' )
```

## Arguments

`app_name`
:   Name of the Snowflake Native App.

    Note

    This argument is ignored when the system function is called by the app.

## Returns

Returns a JSON-formatted string which lists all restricted feature settings allowed for the app.
The JSON-formatted string has the following structure:

Copy code

```
"{""external_data"":{""allowed_cloud_providers"":""all""}}"
```

## Usage notes

- When an app runs this system function, the `app_name` parameter is not required and is ignored if provided.
  In this context, all the apps restricted features are listed.
- When a provider or consumer runs this system function, `app_name` parameter is required and
  lists the restricted features of the app and whether they are enabled or not.

## Examples

To call the function:

Copy code

```
SELECT SYSTEM$LIST_APPLICATION_RESTRICTED_FEATURES('hello_snowflake_app');
```

Sample output:

Copy code

```
[
    {"external_data":{"allowed_cloud_providers":"all"}}
]
```
