# APPLICATION\_CONFIGURATION\_VALUE\_HISTORY view

This Account Usage view provides a history of value changes for application configurations in the account.

For more information about application configuration, see [Application configuration](/developer-guide/native-apps/app-configuration).
The retention time for this view is 365 days, meaning that data older than 365 days will not be available in the view.

## Columns

The following table provides definitions for the `APPLICATION_CONFIGURATION_VALUE_HISTORY` view columns.

| Column | Data type | Description |
| --- | --- | --- |
| ID | STRING | The system-generated unique identifier for the app configuration. |
| NAME | STRING | The system-generated unique identifier for the app configuration. |
| APPLICATION\_ID | STRING | The system-generated unique identifier for the application that contains the configuration. |
| APPLICATION\_NAME | STRING | The name of the application that the configuration is in. |
| CREATED\_ON | TIMESTAMP | The timestamp when the configuration object was created. |
| MODIFIED\_ON | TIMESTAMP | The timestamp when the configuration object was last updated. |
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

## Examples

Retrieve the history of value changes for application configurations in the current account:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_CONFIGURATION_VALUE_HISTORY;
```
