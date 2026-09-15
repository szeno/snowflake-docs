# Approve app specifications

This topic describes how consumers can use app specifications to approve
requests for external connections, data sharing, and other controlled operations for a Snowflake Native App.

## About app specifications

App specifications allow providers to specify the external (outside of Snowflake) endpoints and
resources that an app requires. Consumers can view the end points that the app is requesting and
approve or decline them as appropriate.

After a consumer approves the app specification, the app has permissions to connect to these endpoints.
App specifications only allow a consumer to approve connections to external resources.

The app can also request privileges to create objects, including external access integrations. For
more information, see [Allow an app to create resources in the consumer account](/developer-guide/native-apps/ui-consumer-auto-privs).

### Status of an app specification

An app specification has a status that indicates whether a consumer has approved or declined it.
The possible statuses are:

- `PENDING` The consumer has not approved or declined the app specification.
  This is the default status.
- `APPROVED` The consumer has approved the app specification.
- `DECLINED` The consumer has declined the app specification.

For information on determining the status of an app specification, see [View the external end points required by the app](#label-native-apps-app-spec-desc).

### Sequence numbers of an app specification

Sequence numbers are used to uniquely identify a version of the app specification. Sequence numbers
are automatically incremented when a provider changes the definition of the app specification.
The definition of an app specification includes configuration and other required information. Fields
that are not part of the definition, such as `description`, do not trigger an update to the
sequence number.

Sequence numbers allow providers and consumers to know the current status of the app specification and
which external endpoints have been enabled.

## View the app specifications of an app

To view the external endpoints requested by an app, consumers can use the
[SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications) command as shown in the following example:

Copy code

```
SHOW SPECIFICATIONS IN APPLICATION hello_snowflake_app;
```

This command lists information about the app specifications of the app named
`hello_snowflake_app`.

The `status` column shows whether the app specification has been approved, declined, or is
still pending. See [Status of an app specification](#label-native-apps-app-spec-status) for more information.

## View the external end points required by the app

To view the external endpoints required by the app, consumers can view the details of
the app specification by using the [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification) or
[SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications) commands as shown in the following examples:

Copy code

```
DESC SPECIFICATION my_app_specification IN APPLICATION hello_snowflake_app;
SHOW SPECIFICATIONS IN APPLICATION hello_snowflake_app;
```

For each sequence number, this command displays the properties of the app specification and
their values.

The `definition` field contains a list of the external hosts ports that the app is requesting.
See [Sequence numbers of an app specification](#label-native-apps-app-spec-sequence-cons).

## Approve an app specification by using Snowsight

Using Snowsight, consumers can approve or deny an app specification.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the app.
4. Select the **Settings** icon in the toolbar.
5. Select **Connections**.
6. Next to the connection you want to approve, expand **Details**.

   Snowsight displays the external access integrations, network rules, and requested
   endpoints for the app.
7. Approve or deny the requested endpoints:

   - To approve the endpoints, select **…**, then select **Approve**.
   - To deny the endpoints, select **…**, then select **Deny**.

## Approve or decline an app specification by using SQL

Consumers can approve or decline an app specification to allow the app to connect to
external endpoints.

### Privileges required to approve or decline an app specification

To approve or decline an app specification, a role must have the
MANAGE APPLICATION SPECIFICATIONS privilege on the account. This privilege is granted by default to
the SECURITYADMIN role. Users with the SECURITYADMIN role can grant this privilege to
other roles as required.

Note

Because approving an app specification allows an app to access endpoints outside Snowflake,
a role must have the MANAGE APPLICATION SPECIFICATIONS privilege on the account as
delegated by the security administrator of the consumer account. Being
the owner of the app does not grant the necessary privileges.

### Approve an app specification by using SQL

To approve an app specification, consumers can run the [ALTER APPLICATION](/sql-reference/sql/alter-application)
command as shown in the following example:

Copy code

```
ALTER APPLICATION hello-snowflake-app APPROVE SPECIFICATION
  my-app-spec SEQUENCE_NUMBER = 2;
```

This command approves the app specification named `my-app-spec` for the app named
`hello-snowflake-app`.

Consumers can obtain the value for `SEQUENCE_NUMBER` by running the
[DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification) or [SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications) command.

### Decline an app specification by using SQL

To decline an app specification, consumers can run the [ALTER APPLICATION](/sql-reference/sql/alter-application) command
as shown in the following example:

Copy code

```
ALTER APPLICATION hello-snowflake-app DECLINE SPECIFICATION
  my-app-spec SEQUENCE_NUMBER = 2;
```
