# Sep 15, 2025: Snowflake Native Apps updates

The following features are generally available:

## Automated granting of privileges (General availability)

Snowflake Native App providers can use automated granting of privileges to add the privileges the app requires to
the manifest file. Automated granting of privileges allows an app to create objects in the consumer account
without requiring the consumer to explicitly grant privileges to the app or create objects manually. For more
information on using automated granting of privileges, see [Configure the privileges required by an app](/developer-guide/native-apps/requesting-auto-privs).

To maintain control over what the app can do in the consumer account, a consumer account administrator may use
feature policies.

## App specifications (General availability)

App specifications allow a Snowflake Native App provider to specify the connection information the app requests.
When the consumer installs the app, they review the app specification and approve or decline it as necessary.

For more information on using app specifications to request privileges from the consumer, see
[Use app specifications to request controlled access](/developer-guide/native-apps/requesting-app-specs).

For information on approving app specifications when configuring an app, see
[Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

## Feature policies (General availability)

Snowflake Native App consumer account administrators can create feature policies to limit the objects an app can create in the
consumer account. Administrators can review the privileges the app requires in the listing before installing the app.

For more information on using feature policies, see [Use feature policies to limit the objects an app can create](/developer-guide/native-apps/ui-consumer-feature-policies).
