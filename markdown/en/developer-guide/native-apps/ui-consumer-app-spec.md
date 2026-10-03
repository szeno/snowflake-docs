# Approve app specifications

This topic describes how consumers can use app specifications to approve
requests for external connections, data sharing, and other controlled operations for a Snowflake Native App.

## About app specifications

App specifications allow providers to request approval for controlled
operations, such as connecting to resources outside Snowflake or changing an
app setting. Consumers can review and approve or decline each request.

After a consumer approves an app specification, the app receives the permission
described by that specification. For example, an approved external access
specification lets the app connect to the listed endpoints. An approved
`SETTING` specification lets the app use the requested setting.

For more information about available `SETTING` specifications, see
[Request permission for restricted operations](/developer-guide/native-apps/requesting-app-specs-setting).

The app can also request privileges to create objects, including external access integrations. For
more information, see [Allow an app to create resources in the consumer account](/developer-guide/native-apps/ui-consumer-auto-privs).

### Status of an app specification

An app specification has a status that indicates whether a consumer has approved or declined it.
The possible statuses are:

- `PENDING` The consumer has not approved or declined the app specification.
  This is the default status.
- `APPROVED` The consumer has approved the app specification.
- `DECLINED` The consumer has declined the app specification.

For information on determining the status of an app specification, see [View the details of an app specification](#label-native-apps-app-spec-desc).

### Sequence numbers of an app specification

Sequence numbers are used to uniquely identify a version of the app specification. Sequence numbers
are automatically incremented when a provider changes the definition of the app specification.
The definition of an app specification includes configuration and other required information. Fields
that are not part of the definition, such as `description`, do not trigger an update to the
sequence number.

Sequence numbers allow providers and consumers to know the current status and
approved definition of the app specification.

## View the app specifications of an app

To view the app specifications requested by an app, consumers can use the
[SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications) command as shown in the following example:

Copy code

```
SHOW SPECIFICATIONS IN APPLICATION hello_snowflake_app;
```

This command lists information about the app specifications of the app named
`hello_snowflake_app`.

The `status` column shows whether the app specification has been approved, declined, or is
still pending. See [Status of an app specification](#label-native-apps-app-spec-status) for more information.

## View the details of an app specification

To view the requested operation, consumers can view the details of
the app specification by using the [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification) or
[SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications) commands as shown in the following examples:

Copy code

```
DESC SPECIFICATION my_app_specification IN APPLICATION hello_snowflake_app;
SHOW SPECIFICATIONS IN APPLICATION hello_snowflake_app;
```

For each sequence number, this command displays the properties of the app specification and
their values.

The `definition` field describes the requested operation. For example, the
definition can contain a list of external hosts and ports or a requested
setting. For more information about specification versions, see
[Sequence numbers of an app specification](#label-native-apps-app-spec-sequence-cons).

## Approve an app specification by using Snowsight

Using Snowsight, consumers can approve or deny an `EXTERNAL_ACCESS`
app specification. To approve a `SETTING` app specification, use SQL. Other
app specification types can have type-specific Snowsight workflows.

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

Consumers can approve or decline an app specification to grant or deny the
requested permission.

### Privileges required to approve or decline an app specification

To approve or decline an app specification, a role must have the
MANAGE APPLICATION SPECIFICATIONS privilege on the account. This privilege is granted by default to
the SECURITYADMIN role. Users with the SECURITYADMIN role can grant this privilege to
other roles as required.

Note

Approving an app specification grants an app permission to perform a
controlled operation, such as accessing endpoints outside Snowflake or
changing an app setting. A role must therefore have the MANAGE APPLICATION
SPECIFICATIONS privilege on the account as delegated by the security
administrator of the consumer account. Being the owner of the app doesn’t
grant the necessary privileges.

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
