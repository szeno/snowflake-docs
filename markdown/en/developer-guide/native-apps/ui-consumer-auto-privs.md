# Allow an app to create resources in the consumer account

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This topic describes how consumers can use automated granting of privileges to allow a Snowflake Native App to
create objects in the consumer account.

## Overview of automated granting of privileges

Often, an app needs to create or access objects or perform other actions in a consumer
account. This requires the consumer to grant the required privileges that allow the app
to perform these actions.

Auto privileges allow providers to specify the required privileges in the manifest file of
an app. When the consumer installs or upgrades an app, the privileges specified in the manifest
are automatically granted to the app by Snowflake.

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

## Privileges granted by automated granting of privileges

When using automated granting of privileges, a provider can add the following privileges to the manifest
file of the app:

- EXECUTE TASK
- EXECUTE MANAGED TASK
- CREATE WAREHOUSE
- CREATE COMPUTE POOL
- BIND SERVICE ENDPOINT
- CREATE DATABASE
- CREATE EXTERNAL ACCESS INTEGRATION
- CREATE SECURITY INTEGRATION

Note

For restrictions on the CREATE EXTERNAL ACCESS INTEGRATION privilege, see
[Restrictions on the CREATE EXTERNAL ACCESS INTEGRATION and CREATE SECURITY INTEGRATION](#label-native-apps-auto-privs-eai-restrictions).

## Restrictions on the CREATE EXTERNAL ACCESS INTEGRATION and CREATE SECURITY INTEGRATION

The CREATE EXTERNAL ACCESS INTEGRATION and CREATE SECURITY INTEGRATION privileges allows an app
to create the objects in the consumer account that are required to connect to an external endpoint.
However, to allow connections to an external endpoint, consumers must also approve the app specification
which allows the app to connect to external hosts. If a consumer does not approve the app specification,
the external connection remains disabled.

For more information, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).
