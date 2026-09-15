# ALTER APPLICATION UNSET CONFIGURATION

Unsets an [app configuration definition](/developer-guide/native-apps/app-configuration) for a Snowflake Native App.

See also:
:   [ALTER APPLICATION SET CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-set-configuration-definition), [ALTER APPLICATION DROP CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-drop-configuration-definition)

## Syntax

Copy code

```
ALTER APPLICATION <app> UNSET CONFIGURATION <config>;
```

## Parameters

`app`
:   Identifier for the Snowflake Native App that contains the configuration.

`config`
:   The name of the app configuration definition to unset.

## Usage notes

- This command can only be used by a consumer. This command cannot be used by the Snowflake Native App itself.
- After unsetting a configuration, the app’s status is updated to `PENDING`.
- To unset a configuration, the current role must be granted an application role that has access to the configuration (that is, one of the application roles specified in the `APPLICATION_ROLES` field in the `ALTER APPLICATION SET CONFIGURATION DEFINITION` command).
