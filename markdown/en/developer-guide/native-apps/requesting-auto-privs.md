# Configure the privileges required by an app

This topic describes how to use automated granting of privileges to request the privileges
from a consumer when installing or upgrading a Snowflake Native App.

## Overview of automated granting of privileges

Often, an app needs to create objects or perform other actions in the consumer
account. This requires the consumer to grant the required privileges that allow the app
to perform these actions. For example, apps must have privileges to perform the following
types of tasks:

- Create and start warehouses and compute pools.
- Access data in the consumer account.
- Connect to external endpoints outside of Snowflake.

By using automated granting of privileges, providers can specify the required privileges in the
manifest file of an app. When the consumer installs or upgrades an app, the privileges specified
in the manifest are automatically granted to the app.

Caution

The provider must communicate these privileges and their potential impact so that they are
visible to the consumer when evaluating and installing the app. After privileges are
automatically granted during installation or upgrade, these privileges cannot be revoked.

## Security considerations when using automated granting of privileges

When a provider configures an app to use
`manifest_version: 2` in the manifest file, automated granting of
privileges is enabled. By default this allows Snowflake to automatically
grant certain privileges to the app. For information on the privileges
that can be automatically granted to the app, see
[Privileges granted by automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs#label-native-apps-auto-privs-supported-privs).

During installation, Snowsight displays a notification about
the privileges requested by the app. When a consumer installs an app
that uses automated granting of privileges, they agree that the app may
be granted these privileges during upgrades without requiring additional
consent.

Consumers can create feature policies that restrict the objects an app
can create. For more information on creating feature policies, see
[Use feature policies to limit the objects an app can create](/developer-guide/native-apps/ui-consumer-feature-policies).

## Request privileges for an app using automated granting of privileges

Providers can use automated granting of privileges to specify the privileges an app needs
to create and use objects in the consumer account. Automated granting of privileges grants the
required privileges to the app when the consumer installs or upgrades the app.

### Set the version of the manifest file

To enable automated granting of privileges for an app, set the version at the beginning of the
manifest file as shown in the following example:

Copy code

```
manifest_version: 2
```

### Specify the privileges in the manifest file

To specify the privileges required by the app, providers must declare them in the manifest file
of the app.

Note

To use automated granting of privileges, providers must specify `manifest_version: 2`.

The following example shows how to specify the CREATE WAREHOUSE privilege in the manifest file:

Copy code

```
manifest_version: 2
...
privileges:
  - CREATE WAREHOUSE:
    description: "Allows the app to create warehouses in the consumer account"
```

When a consumer installs the app, the CREATE WAREHOUSE privilege is automatically granted to the app.

Caution

If a provider changes the `manifest_version` property of the manifest file from `2` to `1`,
all automatic privileges are revoked from the app during upgrade. If the consumer has explicitly
granted privileges to the app, those privileges remain unchanged.

Note

Providers can only change the `manifest_version` property during major upgrades to a new
version of the app. The `manifest_version` cannot be changed in a patch release.

### Create the required objects in the setup script

Using automated granting of privileges, providers can add the SQL commands to the setup script to create and access objects in the consumer account.

The following example shows how to create a warehouse in the consumer account:

Copy code

```
CREATE OR REPLACE WAREHOUSE application_wh;
```

This command creates a warehouse named `application_wh` in the consumer account. The
automated granting of privileges feature allows the app to create the warehouse directly. The
provider does not have to add additional logic to check whether the consumer has granted the
required privileges.

## Privileges granted by automated granting of privileges

The following privileges are supported by automated granting of privileges:

- EXECUTE TASK
- EXECUTE MANAGED TASK
- CREATE WAREHOUSE
- CREATE COMPUTE POOL
- BIND SERVICE ENDPOINT
- CREATE DATABASE
- CREATE EXTERNAL ACCESS INTEGRATION
- CREATE SECURITY INTEGRATION
- CREATE SHARE
- CREATE LISTING

When a provider adds these privileges to the manifest file, they are automatically granted to
the app during installation and upgrade.

### Restrictions on privileges gated by app specifications

Note

Privileges gated by app specification require that `manifest_version: 2` be set in the
manifest file.

The following privileges allow apps to create objects, but require additional app specification approval:

CREATE EXTERNAL ACCESS INTEGRATION
:   Allows an app to create an external access integration in the consumer account. However, to allow
    connections to an external endpoint, consumers must also approve the app specification that allows
    the app to connect to external hosts.

CREATE SECURITY INTEGRATION
:   Allows an app to create a security integration in the consumer account. However, to enable OAuth
    authentication, consumers must also approve the app specification that defines the OAuth endpoints
    and scopes.

CREATE SHARE and CREATE LISTING
:   Allow an app to create shares and listings in the consumer account. However, to share data with
    target accounts, consumers must also approve the app specification that specifies the target accounts
    and auto-fulfillment settings.

For more information about app specifications, see [Use app specifications to request controlled access](/developer-guide/native-apps/requesting-app-specs).

### Privileges not granted by automated granting of privileges

Some privileges are not automatically granted to the app. Consumers must manually grant these
privileges when installing or upgrading an app. For example, the following privileges aren’t automatically granted to the app:

- MANAGE WAREHOUSES
- IMPORTED PRIVILEGES ON SNOWFLAKE DB
- READ SESSION
- EXECUTE ALERT

## Using automated granting of privileges during upgrades

When publishing a new version of an app, you might need to add or remove the privileges
required by the app. The setup script of the new version or patch runs with both the new auto
privileges specified in the manifest and the privileges required by the previous version. Any
excess privileges that are removed in the new version are revoked when the app upgrade is complete.

To ensure stability during upgrades, when the version of the manifest file is set to `2`, the
list of requested privileges in the manifest file cannot be modified as part of a patch. This
prevents providers from unintentionally breaking apps by removing required privileges in a patch.
