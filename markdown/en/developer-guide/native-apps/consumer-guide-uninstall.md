# Uninstall a Native App

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## Dropping a Native App is permanent

Dropping a Snowflake Native App is a permanent, irreversible action. The APPLICATION object and all objects
inside it are removed from your account. There is no undrop.

If your goal is to reduce compute costs temporarily without uninstalling the app, you can manage
the individual resources the app created rather than the app itself:

- **For apps with containers (SPCS):** suspend the app’s compute pool using
  `ALTER COMPUTE POOL ... SUSPEND`. This stops container workloads and their associated compute
  charges while the app remains installed.
- **For warehouse-based apps:** suspend the warehouses the app created. This stops compute charges
  while the app stays installed.

The app itself remains installed and subject to its upgrade schedule even while its resources are
suspended. Upgrades will still be applied during the configured maintenance window.

## Before you uninstall: checklist

Before dropping the app, complete the following steps to avoid losing access to objects or data you
want to keep:

**Transfer ownership of objects the app created outside the APPLICATION boundary.** If the app
created warehouses, databases, stages, or other objects in your account (using Category 1 or
Category 3 grants), the app might still own them. [DROP APPLICATION](/sql-reference/sql/drop-application)
without `CASCADE` returns an error when the app owns objects outside itself. To keep those objects,
use a role with the MANAGE GRANTS privilege to [transfer ownership](/sql-reference/sql/grant-ownership)
to one of your own roles before you drop the app. The new owner doesn’t have to be `ACCOUNTADMIN` or
hold the MANAGE GRANTS privilege. To remove the objects instead, run
`DROP APPLICATION ... CASCADE`. `CASCADE` also drops objects that your roles own inside an object
the app still owns, such as a schema or table in a database the app owns.

**For apps with containers: drop or transfer ownership of compute pools the app created.** If the
app is dropped while a compute pool still exists and is bound to it, the compute pool becomes
unusable and must be manually dropped. Even if you reinstall the same app from the same package and
version with the same name, the orphaned compute pool cannot be reused.

**Export any data inside the APPLICATION boundary that you want to retain.** Data inside the
APPLICATION object is removed when the app is dropped. If you need to keep any of it, work
with the provider or the app to ensure that you can export it via the app.

**Cancel a paid listing subscription if applicable.** Dropping the app does not automatically
cancel a paid listing subscription. Cancel the subscription separately through the Snowflake Marketplace
interface to avoid continued billing.

## What happens after uninstall

When the app is dropped:

- The APPLICATION object and all objects inside it (schemas, tables, procedures, Streamlit apps,
  services) are removed.
- Objects the app owned outside the APPLICATION boundary are dropped if you used `CASCADE`,
  including objects your roles own inside them. Objects whose ownership you transferred remain
  in your account.
- Your event table, if configured, is not affected: it belongs to you.
- Paid listing subscriptions must be canceled separately.
