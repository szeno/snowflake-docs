# SHOW CONFIGURATIONS

Lists the [configurations](/developer-guide/native-apps/app-configuration) in the specified app for which you have access privileges.

See also:
:   [DESCRIBE CONFIGURATION](/sql-reference/sql/desc-configuration)

## Syntax

Copy code

```
SHOW CONFIGURATIONS [ IN APPLICATION <app> ]
```

## Parameters

`app`
:   The name of the app to show the configurations for. If an app runs this command, the parameter is optional. If this command is run directly using a workspace or the Snowflake CLI, the `app` parameter is required.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | The name of the configuration. |
| `created_on` | The timestamp when the configuration object was created. |
| `updated_on` | The timestamp when the configuration object was last updated. |
| `type` | One of the following values: `APPLICATION_NAME`, `STRING`, or `SECRET_AUTHORIZATION`. |
| `status` | One of the following values: `PENDING` or `DONE`. |
| `value` | The value set by the consumer. |
| `value_updated_on` | The timestamp when the value was set or unset. |
| `label` | A user-friendly name to be displayed in the UI. |
| `description` | A description of the configuration. |
| `application_roles` | The app roles that have access to the configuration. This field returns the most up-to-date names of the app roles, but the value may have been updated. If an app role has been dropped, it will not be returned in this field. |

Expand

Show lessSee more

## Usage notes

- When this command is run outside of an app, a configuration will only be returned if the consumer role is granted an application role
  that has access to the configuration. However, if the consumer role has MONITOR or OWNERSHIP privilege on the app, the consumer can
  see all the configurations in that app, regardless of which application roles they have been granted.
