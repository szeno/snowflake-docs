# ALTER APPLICATION SET CONFIGURATION DEFINITION

Creates or updates an [app configuration](/developer-guide/native-apps/app-configuration) for a Snowflake Native App.

Note

This command can only be used by a Snowflake Native App.

See also:
:   [ALTER APPLICATION DROP CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-drop-configuration-definition)

## Syntax

For `APPLICATION_NAME`:

Copy code

```
ALTER APPLICATION SET CONFIGURATION DEFINITION <config>
  TYPE = APPLICATION_NAME
  LABEL = '<label>'
  DESCRIPTION = '<description>'
  APPLICATION_ROLES = ( <app_role1> [ , <app_role2> ... ] );
```

For `STRING`:

Copy code

```
ALTER APPLICATION SET CONFIGURATION DEFINITION <config>
  TYPE = STRING
  LABEL = '<label>'
  DESCRIPTION = '<description>'
  APPLICATION_ROLES = ( <app_role1> [ , <app_role2> ... ] )
  SENSITIVE = { TRUE | FALSE };
```

For `SECRET_AUTHORIZATION`:

Copy code

```
ALTER APPLICATION SET CONFIGURATION DEFINITION <config>
  TYPE = SECRET_AUTHORIZATION
  SECRET = <schema>.<secret>
  LABEL = '<label>'
  DESCRIPTION = '<description>'
  APPLICATION_ROLES = ( <app_role1> [ , <app_role2> ... ] );
```

## Parameters

`config`
:   Identifier for the app configuration.

`TYPE`
:   Specifies the type of app configuration. Supported values are:

    - `APPLICATION_NAME`
    - `STRING`
    - `SECRET_AUTHORIZATION`

`SECRET = schema.secret`
:   Specifies the secret that the consumer populates with tokens during the OAuth flow. Required
    when `TYPE = SECRET_AUTHORIZATION`. The secret must be owned by the application creating
    the configuration.

    The name can be specified as `schema.secret`, in which case the app’s own database
    is implied, or as the fully qualified `database.schema.secret`. In either form,
    the secret must be owned by the app.

    On configuration creation, the system validates that the secret has been granted MODIFY to
    all the specified application roles. For more information, see
    [Request OAuth authorization from consumers](/developer-guide/native-apps/app-configuration-secret-authorization).

`LABEL = 'label'`
:   Specifies a label for the app configuration to be displayed in the Snowsight.

`DESCRIPTION = 'description'`
:   Specifies a description of the app configuration. Snowflake recommends
    including information about the app configuration type and why it is
    required by the app.

`APPLICATION_ROLES = ( <app_role1> [ , <app_role2> ... ] )`
:   Specifies the application roles that will have access to the app configuration object.

`SENSITIVE = \{ TRUE | FALSE \}`
:   Specifies whether the configuration value should be treated as sensitive. When set to `TRUE`,
    the value is not displayed in the output of SHOW CONFIGURATIONS or DESCRIBE CONFIGURATION.
    Required when `TYPE = STRING`. Not valid for other configuration types. Specifying
    `SENSITIVE` with `SECRET_AUTHORIZATION` or `APPLICATION_NAME` returns a
    compilation error. For more information, see
    [Sensitive configurations](/developer-guide/native-apps/app-configuration#label-native-apps-app-configuration-sensitive).

## Usage notes

- This command can only be used by a Snowflake Native App.
- When creating a configuration definition for the server app name for inter-app communication, you must set the `LABEL` and `DESCRIPTION` parameters to the same values as the `LABEL` and `DESCRIPTION` parameters of the associated `APPLICATION SPECIFICATION` object.
