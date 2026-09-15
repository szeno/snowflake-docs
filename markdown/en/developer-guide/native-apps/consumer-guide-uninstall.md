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
Category 3 grants), those objects belong to you, but they may be owned by the app object. Transfer
ownership to one of your own roles before dropping the app, or they may become inaccessible.

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
- Objects the app created outside the APPLICATION boundary (warehouses, databases, stages) remain
  in your account and are now fully owned by you.
- Your event table, if configured, is not affected: it belongs to you.
- Paid listing subscriptions must be canceled separately.
