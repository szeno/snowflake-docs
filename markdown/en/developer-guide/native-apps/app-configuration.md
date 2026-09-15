# Application configuration

This topic describes how a Snowflake Native App can use application configuration objects to request
input from the consumer.

## Application configuration: Overview

An application configuration is a key-value pair that provides a coordination mechanism between
a Snowflake Native App and the consumer. When a Snowflake Native App requires input from the consumer, it
defines a configuration key along with a description explaining the purpose of the configuration.
The consumer then provides the value for that key.

Application configuration supports the following types:

`APPLICATION_NAME`
:   The consumer provides the name of an installed app in the consumer account. This type
    is used for [inter-app communication](/developer-guide/native-apps/inter-app-communication).

`STRING`
:   The consumer provides an arbitrary string value. This type can be used for a variety of
    use cases, such as providing external URLs, account identifiers, or other app-specific settings.

`SECRET_AUTHORIZATION`
:   The consumer completes an OAuth flow to populate a secret with tokens. This type is used
    when the provider creates the security integration and secret, and the consumer completes
    third-party authentication directly. For more information, see
    [Request OAuth authorization from consumers](/developer-guide/native-apps/app-configuration-secret-authorization).

The application configuration workflow involves the following steps:

1. The app creates a configuration definition using `ALTER APPLICATION SET CONFIGURATION DEFINITION`,
   specifying the type of information needed and the app roles that have access to the configuration.
2. The consumer views incoming configuration requests using `SHOW CONFIGURATIONS` or Snowsight.
3. The consumer provides the requested value using `ALTER APPLICATION SET CONFIGURATION VALUE` or Snowsight.
4. The app retrieves the value and uses it to perform further operations,
   such as creating an application specification for a connection.

The Snowflake Native App Framework provides callbacks to notify the app when a configuration value is set or changed.
For more information, see [Configuration callbacks](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks).

## Terminology

Application configuration uses the following terms:

Configuration definition
:   An object that the app creates to request a specific piece of information from the consumer.
    The configuration definition specifies the type of information requested, a label, a description,
    and the app roles that have access to the configuration.

Configuration value
:   The value that the consumer provides in response to a configuration definition request.

## Using configurations

This section describes how to create, display, and manage configurations.

- [Create a configuration request](#label-native-apps-app-configuration-create-request-sql)
- [View configuration requests](#label-native-apps-app-configuration-view-requests)
- [Provide the configuration value](#label-native-apps-app-configuration-provide-value)
- [Update the value of a configuration](#label-native-apps-app-configuration-update-value)
- [Unset the value of a configuration](#label-native-apps-app-configuration-unset-value)
- [Retrieve the value of a configuration](#label-native-apps-app-configuration-retrieve-value)

### Create a configuration request

To request a configuration value from the consumer, the app creates a configuration definition
in the setup script or at runtime. The configuration definition specifies the type of value
expected, a label and description that are displayed to the consumer, and the app roles that
can view the configuration and edit the value.

The following example shows how to create a configuration definition of type `STRING` that requests a
company URL from the consumer:

Copy code

```
ALTER APPLICATION SET CONFIGURATION DEFINITION company_url
  TYPE = STRING
  LABEL = 'Company URL'
  DESCRIPTION = 'Provide the company website URL'
  APPLICATION_ROLES = (app_user)
  SENSITIVE = FALSE;
```

The following properties control how the configuration is displayed and managed:

- `LABEL`: The name displayed to the consumer in Snowsight.
- `DESCRIPTION`: A description that helps the consumer understand the purpose of the
  configuration.
- `APPLICATION_ROLES`: The app roles that can view and set the value for this configuration.
  Consumer roles that are granted one of the specified app roles can view the configuration and edit its value.
- `SENSITIVE`: Specifies whether the configuration value should be treated as sensitive. When
  set to `TRUE`, the value is not displayed in the output of `SHOW CONFIGURATIONS`. Required
  when `TYPE = STRING`. For more information, see [Sensitive configurations](#label-native-apps-app-configuration-sensitive).

### View configuration requests

After an app creates a configuration request, the consumer can view pending requests
using Snowsight or SQL.

SnowsightSQL

To view the configuration requests and details of a configuration definition using Snowsight, do the following:

1. Sign in to Snowsight.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the app.
4. Open the **Configurations** tab. The **Configurations** section displays the string configurations in the **Other configurations** section. Each string configuration shows the following:
   - The label of the configuration.
   - A description of what the configuration is for.
   - A **Review** button.

To view the configuration requests and details of a configuration definition using SQL, use the [SHOW CONFIGURATIONS](/sql-reference/sql/show-configurations) and [DESCRIBE CONFIGURATION](/sql-reference/sql/desc-configuration) commands:

Copy code

```
SHOW CONFIGURATIONS IN APPLICATION example_app;

DESCRIBE CONFIGURATION company_url IN APPLICATION example_app;
```

### Provide the configuration value

After the app creates a configuration request, the consumer provides the requested value using Snowsight or SQL.

SnowsightSQL

To provide a value for the configuration using Snowsight, do the following:

1. In the configuration’s details page in Snowsight, click the **Review** button. The configuration details page displays the following:

   - The label of the configuration.
   - A description of what the configuration is for.
   - If the configuration is sensitive, a **Sensitive data protection** banner is displayed. For more information, see [Sensitive configurations](#label-native-apps-app-configuration-sensitive).
2. Provide the value for the configuration in the **Value** field.
3. Click the **Save** button to submit the value for the configuration. **Configuration updated successfully** is displayed. The configuration list is refreshed to display the new value.

To provide a value for the configuration using SQL, use the [ALTER APPLICATION SET CONFIGURATION VALUE](/sql-reference/sql/alter-application-set-configuration-value) command:

Copy code

```
ALTER APPLICATION <app> SET CONFIGURATION <config> VALUE = '<value>';
```

### Update the value of a configuration

You can update the value of a configuration using Snowsight or SQL.

SnowsightSQL

To update the value of a configuration using Snowsight, do the following:

1. In the configuration’s details page in Snowsight, if a configuration has a value set, the following information displays:

   - A **Configured** banner.
   - If the configuration is not sensitive, the value is displayed.
   - If the configuration is sensitive, the value is masked.
   - An **Update** button.
   - A **Clear value** button.
2. Click the **Update** button to update the value for the configuration.
3. Provide the new value for the configuration in the **Value** field.
4. Click the **Save** button to submit the new value for the configuration. **Configuration updated successfully** is displayed. The configuration list is refreshed to display the new value.

To update a configuration value, use the same syntax as setting the initial value:

Copy code

```
ALTER APPLICATION <app> SET CONFIGURATION <config> VALUE = '<value>';
```

### Unset the value of a configuration

You can unset the value of a configuration using Snowsight or SQL.

SnowsightSQL

To unset the value of a configuration using Snowsight, do the following:

1. In the configuration’s details page in Snowsight, click the **Clear value** button.
2. Confirm the action. The configuration list is refreshed to display the unset configuration.

To unset the value of a configuration using SQL, use the [ALTER APPLICATION UNSET CONFIGURATION](/sql-reference/sql/alter-application-unset-configuration) command:

Copy code

```
ALTER APPLICATION <app> UNSET CONFIGURATION <config>;
```

### Retrieve the value of a configuration

In addition to SHOW CONFIGURATIONS or DESCRIBE CONFIGURATION, an app can retrieve the value of a configuration that the consumer provided using the [get\_configuration\_value](/sql-reference/functions/get_configuration_value) function. The following example shows how to retrieve the value of a configuration:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$APPLICATION', 'GET_CONFIGURATION_VALUE' , '<config_name>')
```

Note

Only the app can retrieve the configuration value from the system context. To view the configuration value as a consumer, you can view the configuration details either using SQL or Snowsight. For more information, see [View configuration requests](#label-native-apps-app-configuration-view-requests).

## Sensitive configurations

When an app creates a configuration, it can mark the configuration as sensitive by setting
`SENSITIVE = TRUE`. This is useful when the app needs to request sensitive information
from the consumer, such as a personal access token or an API key.

Note

The `SENSITIVE` property is only supported for configurations of type `STRING`.

When a configuration is sensitive, the consumer-provided value is protected from other consumer
users and roles. The Snowflake Native App Framework applies protections similar to those used for
[SECRET objects](/sql-reference/sql/create-secret) in Snowflake:

- After the consumer sets a value, the query history for the
  `ALTER APPLICATION SET CONFIGURATION VALUE` command redacts the value so that it is not
  exposed to other consumer roles or users.
- The value is not displayed in the output of `SHOW CONFIGURATIONS`,
  `DESCRIBE CONFIGURATION`, INFORMATION\_SCHEMA views, or ACCOUNT\_USAGE views.

The app that creates the configuration can always retrieve the consumer-provided value,
even when the configuration is sensitive. This is by design, because the purpose of an
application configuration is for the consumer to provide a value to the app.

### Changing the SENSITIVE property

An app cannot change the `SENSITIVE` property while the configuration has a value set
(that is, when the configuration is not in a `PENDING` state). This restriction prevents the
consumer’s value from being accidentally exposed. If the app attempts to change the
`SENSITIVE` property while a value is set, the command completes without error but has
no effect.

To change the `SENSITIVE` property, the consumer must first unset the configuration value
using `ALTER APPLICATION UNSET CONFIGURATION`.

## SQL reference

The following SQL commands, functions, and views are used to manage application configurations.

### SQL commands

- [ALTER APPLICATION SET CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-set-configuration-definition): Creates or updates an application configuration definition that requests a value from the consumer.
- [ALTER APPLICATION DROP CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-drop-configuration-definition): Deletes an application configuration definition.
- [ALTER APPLICATION SET CONFIGURATION VALUE](/sql-reference/sql/alter-application-set-configuration-value): Sets a value in an application configuration.
- [ALTER APPLICATION UNSET CONFIGURATION](/sql-reference/sql/alter-application-unset-configuration): Unsets the value of an application configuration.
- [SHOW CONFIGURATIONS](/sql-reference/sql/show-configurations): Lists all of the application configurations in an app.
- [DESCRIBE CONFIGURATION](/sql-reference/sql/desc-configuration): Describes the details of an application configuration.

### SQL functions

- [IS\_CONFIGURATION\_SET (SYS\_CONTEXT function)](/sql-reference/functions/is_configuration_set): Returns whether or not the configuration has a value set.
- [GET\_CONFIGURATION\_VALUE (SYS\_CONTEXT function)](/sql-reference/functions/get_configuration_value): Returns the current value of a configuration.

### Information schema views and functions

- [APPLICATION\_CONFIGURATIONS view](/sql-reference/info-schema/application_configurations): This Information Schema view displays a row for each application configuration currently defined in the specified or current database where the INFORMATION\_SCHEMA is located.
- [APPLICATION\_CONFIGURATION\_VALUE\_HISTORY](/sql-reference/functions/application_configuration_value_history): Returns the history of values for a configuration.

### Account usage schema views

- [APPLICATION\_CONFIGURATIONS view](/sql-reference/account-usage/application_configurations): This Account Usage view displays a row for each application configuration in the account.
- [APPLICATION\_CONFIGURATION\_VALUE\_HISTORY view](/sql-reference/account-usage/application_configuration_value_history): This Account Usage view displays the history of values for a configuration.

## Callbacks

When a configuration value changes, the Snowflake Native App Framework can invoke lifecycle callbacks registered in the
app’s [manifest](/developer-guide/native-apps/manifest-reference) file. These callbacks let the app validate, prepare for, or react to
configuration changes. For example, when configuring inter-app communication, a common use case is to use the
[before\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-before-configuration-change)
callback to automatically create or update a connection specification when the consumer sets
the server app name. This avoids requiring the consumer to perform additional manual steps
after setting the configuration value. For more information about inter-app communication, see [Inter-app Communication](/developer-guide/native-apps/inter-app-communication).

The following configuration callbacks are available:

[validate\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-validate-configuration-change)
:   A synchronous callback called as part of the `ALTER APPLICATION SET CONFIGURATION VALUE`
    command. Lets the app perform custom validation on the provided value. If the callback
    returns an error, the command fails and the new value is not set.

[before\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-before-configuration-change)
:   A synchronous callback called as part of the `ALTER APPLICATION SET CONFIGURATION VALUE`
    and `ALTER APPLICATION UNSET CONFIGURATION` commands. Lets the app perform operations
    based on the configuration value before it is saved.

[after\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-after-configuration-change)
:   An asynchronous callback called after the `ALTER APPLICATION SET CONFIGURATION VALUE`
    or `ALTER APPLICATION UNSET CONFIGURATION` commands complete. Lets the app react to
    the change, for example for notification or tracking purposes.

For complete callback signatures and return values, see
[Callbacks](/developer-guide/native-apps/callbacks).

## Using the Permission SDK with application configurations

If your app includes a Streamlit frontend, you can use the Python Permission SDK to prompt
consumers to review and set values for configurations. The SDK provides the following
functions for working with application configurations:

[get\_application\_configurations()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-get-application-configurations)
:   Returns all configurations defined for the app. This is equivalent to running
    SHOW CONFIGURATIONS.

[request\_application\_configuration\_value()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-request-application-configuration-value)
:   Opens a dialog in the Streamlit app that allows the consumer to review and set values
    for application configurations.

[request\_application\_connection\_review()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-request-application-connection-review)
:   Opens a dialog for the consumer to approve an application connection for
    [inter-app communication](/developer-guide/native-apps/inter-app-communication).

For more information, see the [Permission SDK reference](/developer-guide/native-apps/requesting-permission-sdk-ref).
