Categories:

[Table functions](/sql-reference/functions-table) (Tables)

# APPLICATION\_CONFIGURATION\_VALUE\_HISTORY

Provides a history of the value changes for [application configurations](/developer-guide/native-apps/app-configuration) in the specified Snowflake Native App.

You can call this function to check the history of the value changes for an application configuration. For information, see
[Application configuration](/developer-guide/native-apps/app-configuration).

## Syntax

Copy code

```
APPLICATION_CONFIGURATION_VALUE_HISTORY(
  [ APPLICATION_NAME => '<application_name>' ]
  [ , CONFIGURATION_NAME => '<config_name>' ]
)
```

## Arguments

**Required:**

`application_name`
:   Name of the application that the configuration is in.

**Optional:**

`config_name`
:   Name of the configuration. If not provided, the function returns the history for all configurations in the application.

## Returns

The function returns the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| NAME | STRING | The name of the configuration, defined by the provider. |
| APPLICATION\_NAME | STRING | The name of the application that the configuration is in. |
| CREATED\_ON | TIMESTAMP | The timestamp when the configuration object was created. |
| UPDATED\_ON | TIMESTAMP | The timestamp when the configuration object was last updated. |
| TYPE | STRING | The type of the configuration. Possible values are APPLICATION\_NAME and STRING. |
| STATUS | STRING | The status of the configuration. Possible values are PENDING and DONE. |
| SENSITIVE | BOOLEAN | Whether the value is sensitive or not. |
| VALUE | STRING | The value that is set by the consumer.  For application configurations of the APPLICATION\_NAME type, this is the most up-to-date name of the application specified by the consumer. This may not be the same as initially provided if the application has been renamed. If the application has been dropped, no value will be shown here, as if the value is not set.  When `SENSITIVE=TRUE`, the value is hidden, unless the executing role is the application owning the configuration. |
| VALUE\_UPDATED\_ON | TIMESTAMP | The last updated timestamp when the value was set or unset. |
| LABEL | STRING | A user-friendly name to be displayed in the UI, provided by the provider. |
| DESCRIPTION | STRING | The description of the configuration. |
| APPLICATION\_ROLES | STRING | The comma-separated app role names that have access to the configuration.  This displays the most up-to-date names, even if roles have been renamed. If an application role has been dropped, it will not be included in the output list. |

Expand

Show lessSee more

## Usage notes

- The view only displays configurations for which the current role for the session has been granted access privileges.
- The view does not include configurations that have been dropped.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Retrieve the history of the value changes for the `config_name` application configuration
in the `application_name` application:

Copy code

```
SELECT * FROM TABLE(information_schema.application_configuration_value_history(application_name => 'my_app', configuration_name => 'my_configuration'));
```
