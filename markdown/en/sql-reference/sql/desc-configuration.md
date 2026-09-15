# DESCRIBE CONFIGURATION

Describes the properties of a [configuration](/developer-guide/native-apps/app-configuration).

DESCRIBE can be abbreviated to DESC.

See also:
:   [SHOW CONFIGURATIONS](/sql-reference/sql/show-configurations)

## Syntax

Copy code

```
{ DESC | DESCRIBE } CONFIGURATION <configuration_name> [ IN APPLICATION <app> ]
```

## Parameters

`configuration_name`
:   Specifies the identifier for the configuration to describe.

`app`
:   The name of the app to describe the configuration for.

    If an app runs this command, the parameter is optional and ignored. Listing configurations for another app from within an app is not supported.

    If this command is run directly using a workspace or the Snowflake CLI (that is, by a consumer), the `app` parameter is required.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `property` | The name of the configuration. |
| `value` | The current value set for the configuration. |

Expand

Show lessSee more

## Usage notes

- When this command is run outside of an app, the consumer role must be granted an application role
  that has access to the configuration. If not, an error is thrown.
- If the consumer role has the MONITOR or OWNERSHIP privilege on the app, the consumer can see all
  configurations in that app, regardless of which application roles they have been granted.
