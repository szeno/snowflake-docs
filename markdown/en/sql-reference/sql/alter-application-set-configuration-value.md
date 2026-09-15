# ALTER APPLICATION SET CONFIGURATION VALUE

Sets a value in an [app configuration definition](/developer-guide/native-apps/app-configuration) for a Snowflake Native App.

See also:
:   [ALTER APPLICATION SET CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-set-configuration-definition), [ALTER APPLICATION DROP CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-drop-configuration-definition)

## Syntax

Copy code

```
ALTER APPLICATION <app> SET CONFIGURATION <config> VALUE = '<value>';
```

## Parameters

`app`
:   Identifier for the Snowflake Native App that contains the configuration.

`config`
:   Identifier for the app configuration definition.

`VALUE = 'value'`
:   Specifies the value to set for the app configuration definition.

## Usage notes

- This command can only be used by a consumer. This command cannot be used by the Snowflake Native App itself.
- For a configuration definition of type `APPLICATION_NAME`, the value must be the name of a Snowflake Native App that is installed in the current account.
- For a configuration definition of type `SECRET_AUTHORIZATION`, the only accepted value is `'configured'`. The Snowflake Native App Framework verifies that the associated secret is populated with tokens before accepting the value. For more information, see [Request OAuth authorization from consumers](/developer-guide/native-apps/app-configuration-secret-authorization).
- In order to set a configuration, the current role must be granted an application role that has access to the configuration (that is, one of the application roles specified in the `APPLICATION_ROLES` field in the `ALTER APPLICATION SET CONFIGURATION DEFINITION` command).
