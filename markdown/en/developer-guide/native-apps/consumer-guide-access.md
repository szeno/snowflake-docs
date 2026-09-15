# Grant access to a Native App

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## The foundation: dual protection

The Snowflake Native App Framework has a dual responsibility: to protect your data from the app, and to protect the
provider’s intellectual property from you. Both protections are on by default.

The app is a special type of database that is owned by the app itself. The app’s provider decides
what data, functions, and procedures to expose to users in your account, and what to keep under the
app’s own control. From the consumer side, the app starts with zero access to your account beyond
what it creates for itself. It cannot read your tables, query your views, or access any object you
own until you explicitly grant it permission.

Access is structured into three distinct categories, described below. Understanding the categories
helps you make informed decisions at installation time and throughout the app’s lifecycle, because
apps may request additional access not just at installation, but during upgrades and during active
use.

## Category 1: Automatically grantable privileges

Six privileges are available for the app to request. These allow the app to create operational
resources in your account. They do not, by themselves, grant the app access to your data. That
happens only through Category 3.

**`CREATE WAREHOUSE`:** The app can create compute warehouses to run its workloads. Credits
consumed by these warehouses appear in your account usage. App-created warehouses are typically
exclusive to the app and not intended to be shared with other apps or your other workloads. You can
use budgets rather than grants to control how compute is used.

**`CREATE TASK`:** The app can create scheduled tasks to automate its operations.

**`CREATE MANAGED TASK`:** The app can create serverless tasks.

**`CREATE DATABASE`:** The app can create databases within its scope.

**`CREATE COMPUTE POOL`:** The app can create a Snowpark Container Services compute pool to run
containerized workloads. Applicable to apps with containers only.

**`BIND SERVICE ENDPOINT`:** The app can expose a service endpoint to allow external access to a
running SPCS service.

The set of Category 1 privileges the app requests is shown at installation time. You decide whether
to proceed with the installation given those requests. There is no option to grant only a subset of
the privileges.

If the app requests new Category 1 privileges during an upgrade, the provider must disclose this to
you in advance. These additional requests do not appear silently. You will be notified before the
upgrade proceeds.

Note

Even with all six Category 1 privileges granted, the app cannot read or move your data without
Category 3 grants. These are operational resource grants only.

## Category 2: Application Specifications (App Specs)

Some apps need to do things that carry higher risk than creating operational resources: making
outbound network calls to external services, authenticating with external systems via OAuth, or
sharing data back via a Snowflake listing. These actions require your explicit prior approval,
enforced through the Application Specification mechanism.

**How it works:** when an app needs one of these capabilities, it creates the corresponding
integration object (an External Access Integration, a Security Integration, or a Listing object) in
an inactive state. The inactive object is surfaced to you as an Application Specification for
review. The object remains inactive and non-functional until you approve it. Only upon your approval
does it become active and usable by the app.

You can approve none, some, or all of an app’s App Specs. Each is an independent decision. If you
are not comfortable with a particular App Spec, you can decline it. The app will not have access
to that capability. Some app functionality may be limited or unavailable if certain App Specs are
not approved, but the app will not receive the capability without your approval.

All pending App Specs can be reviewed as a batch by an account admin or their delegate, so
approvals do not need to be handled one at a time.

You can list all App Specs for a given app at any time from the Snowsight app management interface,
or by querying:

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_SPECIFICATIONS
WHERE APPLICATION_NAME = '<app_name>';
```

Each App Spec has a status: `Pending`, `Approved`, or `Declined`. You can decline an approved App
Spec at any time. Declining deactivates the corresponding object immediately.

**What each type of App Spec means:**

**External Access Integration (EAI):** the app will make outbound network calls to a specific named
external endpoint. The endpoint is defined in the integration. You’re approving access to that
specific destination, not open-ended internet access. Verify that the endpoint is a legitimate
destination for this type of app (for example, a known ERP or CRM API endpoint for a connector app).

**Security Integration (OAuth):** the app will use OAuth to authenticate with an external service.
Review what service is being accessed and what OAuth scopes are being requested.

**Listing:** the app will share some data back via a Snowflake listing. Ask the provider to specify
exactly what data is included before approving.

**Connection:** the app may need to connect to another app from the same or a different provider
to provide richer functionality. Approval of this type of App Spec enables
[Inter-App Communication](/developer-guide/native-apps/inter-app-communication).

For full instructions on reviewing and approving App Specs, see
[Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

## Category 3: Explicitly granted privileges

Category 3 is how the app gets access to your data. Nothing in Categories 1 or 2 touches your
data. Category 3 may be app-requested but is entirely consumer-controlled. You choose what to
grant, when, and to what scope. Everything is revocable at any time.

The principle is **minimum necessary access**: grant the app access to the data and objects it
actually needs for its stated purpose, and nothing more. The security review in
[Evaluate a Native App before installing](/developer-guide/native-apps/consumer-guide-evaluate) should inform what that minimum is before
you grant anything.

Three mechanisms are available:

**References:**
References are an object-level mechanism where the app pre-declares a named reference “slot” (for
example, “I need a table matching this shape” or “I need a table with an ID column”) and you bind a
specific object to that slot. References work at the level of individual named objects only. There
is no database-level reference, and references do not cover objects created in the future (for
example, new views added to a database after the reference is established).

**Direct object grants:**
You grant the app access to specific named objects: individual views, tables, schemas, or stored
procedures. This is the most explicit and auditable approach. Grant only what the app needs.

Examples:

- Salesforce connector: grant `WRITE` access to the specific database you want the connector to
  land incoming Salesforce data into. The app can write to that database; it cannot access other
  databases.
- Identity resolver app: grant `SELECT` access to the specific views containing the customer
  records the app uses for identity resolution. The app can read those views; it cannot read other
  data.

**Database role grants (database scope, use deliberately):**
Grant a database role to the app. Database role grants typically apply at the database level and
can cover future objects created in that database scope after the grant is made. Use this level of
access deliberately and only when the app genuinely needs broad, forward-looking access within a
database.

You may grant additional privileges to an app at any point after installation. For example, a data
quality assurance app working against one database could be reconfigured later to cover additional
databases at your discretion. Regardless, you control access to your database objects, at
installation and throughout the app’s lifecycle.

For full instructions, see [Allow access to a consumer account](/developer-guide/native-apps/ui-consumer-granting-privs).

## Feature policies: limiting what the app can create

Feature policies give you a governance lever that is orthogonal to the three access categories: you
can cap what the app is allowed to create even if you have granted it broad Category 1 privileges.
For example, you can limit the number of warehouses the app can create, the number of compute pools,
or the number of tasks.

Use feature policies when you want to allow the app to create resources but want to bound the
potential impact on your account.

For full instructions, see
[Use feature policies to limit the objects an app can create](/developer-guide/native-apps/ui-consumer-feature-policies).

## Restricted Callers Rights (RCR)

By default, the app runs with owner’s rights: it has access to the objects it owns plus whatever
access you have explicitly granted it. In this model, the app’s access is consistent regardless of
which user is interacting with it.

Restricted Callers Rights (RCR) enables a different mode: the app runs with the rights of the
caller, the Snowflake user currently executing a request. The app can only access what that user
can access, further bounded by the restrictions defined in the RCR grant. For example, an app may
be allowed access to all that a user can access but only in a specific database. An account admin
can choose to allow caller’s rights by imposing no restrictions, but use such elevated privileges
carefully, especially if highly privileged users intend to use the app.

This model is appropriate for apps where per-user data access is the intended design, for example,
a notebook-style app where different users should see different data based on their own Snowflake
roles. It is not appropriate for apps that should run under a consistent, predictable access
profile. For the latter case, use appropriate grants and let the app run in the default owner’s
rights mode.

For full instructions, see
[Grant restricted caller’s rights to an executable in an app](/developer-guide/native-apps/ui-consumer-restricted-callers-rights).
