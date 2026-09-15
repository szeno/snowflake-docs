# Create and access objects in a consumer account

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can develop a Snowflake Native App to create objects in the
consumer account or access existing objects.

Tip

For new apps, use [automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs) and
[app specifications](/developer-guide/native-apps/requesting-app-specs) to manage privileges and external
connections. Use [references](/developer-guide/native-apps/requesting-refs) to access existing objects in the
consumer account. This topic also covers the manual granting of privileges for legacy apps.

## Overview of creating and accessing objects in a consumer account

Snowflake Native Apps often need to create or access objects in a consumer account. For example,
even a basic app that allows the consumer to query shared data would require the app
to create and use a warehouse in the consumer account. An app may also need to connect to external
services that are outside Snowflake.

The Snowflake Native App Framework provides two ways of requesting privileges to create objects in the consumer account.

### Automatically granting privileges to an app

The Snowflake Native App Framework allows providers to request certain safe privileges and then grants them automatically. Providers add these privileges to the manifest file of the app. During installation or upgrade of the app, Snowflake automatically grants these privileges to the app.

For more information on configuring an app to have privileges granted automatically, see [Configure the privileges required by an app](/developer-guide/native-apps/requesting-auto-privs).

From the provider perspective, automated granting of privileges streamlines app development because the
app does not have to determine if a consumer has granted the requested privileges or created the required
objects in their account.

From the consumer perspective, automated granting of privileges simplifies app installation and configuration. However, it also gives the consumer less control by default over what an app can do in their account. To allow consumers more control over what an app can do, the Snowflake Native App Framework provides the following features:

App specifications:
:   Allow consumers to control the external endpoints that an app can connect to. To access services outside
    Snowflake, an app may need to create an external access integration or service integration depending on
    the type of service. Using automated granting of privileges, the app can create these objects in the
    consumer account. However, an account admin of the consumer account must approve the app specification
    that allows the app to perform the external connection.

    For information on developing an app to use app specifications, see [Use app specifications to request controlled access](/developer-guide/native-apps/requesting-app-specs).
    For information on how the consumer approves an app specification, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

Feature policies:
:   Feature policies allow consumers to override the automatic granting of privileges. Before installing or
    upgrading an app, consumers can create a feature policy to prohibit the app from creating specific types
    of objects. For example, a consumer may need to configure a feature policy to prohibit an app from creating a
    warehouse. If an app attempts to create a warehouse during installation or upgrade, the installation fails.

    For information on how a consumer creates feature policies, see [Use feature policies to limit the objects an app can create](/developer-guide/native-apps/ui-consumer-feature-policies).

### Manually granting privileges to an app

For apps that were created before the release of
[automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs), for example an app that was installed and does not
have the necessary privileges to create objects in the consumer account, consumers must manually grant
privileges to the app using SQL or Snowsight, depending on how the app is configured. For more
information, see [Request global privileges from consumers](/developer-guide/native-apps/requesting-privs).

### Accessing existing objects in the consumer account

In some contexts an app needs to access existing objects in a consumer account that exist outside the app. For example, an app might need to access existing tables in a consumer database. To allow the app to create objects, the Snowflake Native App Framework uses references that enable the customer to specify the name and schema for an object and enable access to the object.

For more information, see [Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

## Comparison of automatic and manual privileges

| App requirement | Automatically granting privileges | Manually granting of privileges |
| --- | --- | --- |
| Privileges to create objects | Apps have privileges to create objects, with some exceptions. | Consumers must explicitly grant privileges to the app using Snowsight or SQL. |
| Access external services | Apps can create network rules and external access integrations.  Consumers must approve external access using app specifications. | Consumers must manually create the required network rules and external access integrations and bind the integration using references. |
| Access external identity providers | Apps can create security integrations for external API Authentication.  Consumers must approve the external connection using app specification. | Consumers must manually create the required security integrations and bind the integration with references |
| Access to existing objects | Providers must use references to access existing objects.  Consumers approve access to the references. | Providers must use references to access existing objects.  Consumers approve access to the references. |
| App development | Providers do not have to write code to determine if the consumer has granted a certain privilege. | Providers must write code that checks if the consumer has granted a certain privilege. |
| App installation | Consumers do not have to manually create objects or grant privileges. | Consumers must manually create objects in their account or explicitly grant privileges to the app using Snowsight or SQL. |

Expand

Show lessSee more

## Security considerations when using auto privileges with app specifications

App specifications only control communications to endpoints outside
Snowflake. Consumers can approve or decline app specifications to
allow or prevent the app making connection to these endpoints.

App specifications do not prevent the app from creating
Snowflake objects that control external connections: network rules,
external access integrations, and security integrations. Privileges
to create these objects are granted using automated granting of
privileges.

App specifications do not provide data validation. In addition,
they do not place any restrictions on secrets or tokens referenced
by an external access integration or security integration.

For example, if a provider configures an external access integration
of an app to use ALLOWED\_AUTHENTICATION\_SECRETS and the consumer
approves the app specification for that integration, the app can later
modify the secrets and tokens that it uses.

However, if a provider modifies the app to use a different endpoint,
the sequence number of the app specification would change and the
consumer would need to re-approve or decline the new version.
