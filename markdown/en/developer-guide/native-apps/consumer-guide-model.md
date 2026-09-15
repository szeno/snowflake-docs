# How a Snowflake Native App works in your account

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## What gets installed

When you install a Snowflake Native App, Snowflake creates an APPLICATION object in your account. This
object is the container for everything the app does in your environment. During installation, the
app’s setup script runs and creates the objects the app needs inside this boundary: schemas, stored
procedures, Streamlit applications, and (for apps with containers) services.

![](/static/images/native-apps/na-consumer-account-model.png)

The APPLICATION object has a clear boundary. Objects inside it belong to the app. Objects outside
it (whether pre-existing objects you own or new objects the app creates with your permission)
belong to you and remain under your ownership.

## The access model: what the app can and cannot touch

The Snowflake Native App Framework intentionally restricts what a Snowflake Native App can see and do by default. It does not
provide any access to consumer data by default.

The app operates with its own internal roles, which are separate from your account roles. It has
access to all the objects it creates during installation: tables, views, stored procedures, and so
on. But outside its own database and objects it creates, the app can only access objects you have
explicitly granted it access to. It cannot read arbitrary tables, cannot take data outside the
account boundary without your approval, and cannot escalate its own privileges. For example, an
identity resolution app may bring its proprietary data and put it into tables in the database that
Snowflake creates during installation for the app contents. It would own the procedures it creates
in that database as well. But those procedures cannot access your data without explicit grants from
you.

This restriction is mutual. While the Framework protects your data from the app, it also protects
the provider’s intellectual property from you: the implementation details, proprietary provider
data, and proprietary provider logic inside the app are not visible to you as the consumer. The app
can create multiple [application roles](/developer-guide/native-apps/creating-setup-script#about-application-roles)
to expose different capabilities or data that it owns, and for you to grant differentiated access to
roles in your organization. The app manifest lists the available application roles that you can then
grant to roles in your account (for example, granting `app_role_marketing` to your `marketing`
role so the app shows what is meant for marketing to that role but not what is meant for finance.

Both restrictions can be selectively relaxed by the respective owner. You can grant the app access
to data and objects that it needs for its intended purpose. The app can expose specific data and
objects to its users in your account, as configured by the provider. All such relaxation happens
through explicit actions under Snowflake RBAC.

For more detail on the formal allocation of responsibilities between Snowflake, the provider, and
the consumer, see [Separation of responsibilities for Native Apps](/developer-guide/native-apps/consumer-guide-responsibility).

## How your data is protected

Three properties of the Snowflake Native App Framework protect consumer data:

**Your data does not leave Snowflake by default.** The app processes your data inside your account.
Data movement outside Snowflake (for example, an app calling an external API) requires a
separately approved External Access Integration (App Spec) that you control.

**The provider cannot query your data.** The provider publishes the app logic but has no direct
access to your Snowflake account or to any data in it. Event and log data can be shared with the
provider to help with troubleshooting, but only if you opt in. This sharing is not enabled by
default.

**Query history is redacted.** The full query profile of services running in the app is collapsed
into a single empty node in your query history, protecting both your query patterns and the
provider’s implementation details.

## Provider vs. consumer responsibilities at a glance

**Provider responsibilities:**

- Defines the app logic, schema, and setup script
- Publishes versioned releases and maintains compatibility
- Declares what privileges and App Specs the app will request
- Is the seller of record and is responsible for supporting the app
- Cannot see consumer data

**Consumer responsibilities:**

- Decides what privileges to grant and what App Specs to approve
- Decides when to complete upgrades (within the allowed window)
- Decides whether to share optional event data with the provider
- Monitors the app’s resource usage via budgets or relevant ACCOUNT\_USAGE views
- Can uninstall the app at any time
- Is responsible for security, privacy, and compliance review of the app

For the full, legally reviewed allocation of responsibilities, see
[Separation of responsibilities for Native Apps](/developer-guide/native-apps/consumer-guide-responsibility).

## Apps with containers (SPCS): what’s additionally involved

Some Native Apps run containerized workloads using Snowpark Container Services (SPCS). These apps
with containers follow the same trust model as all Native Apps, with a few additions:

A compute pool is created inside your account to run the containers. The consumer can grant the app
the `CREATE COMPUTE POOL` privilege to create this automatically, or provision it manually before
install.

Container apps can make outbound network calls if you approve the corresponding External Access
Integration App Spec. The specific endpoints must be authorized before any outbound call is
permitted.

Query history for container services is redacted in your account to protect both your query
patterns and the provider’s implementation. See
[Monitor and audit a Native App](/developer-guide/native-apps/consumer-guide-monitor) for the monitoring implications.

For installation specifics for apps with containers, see
[Install and manage an app with containers](/developer-guide/native-apps/ui-consumer-installing-container). For security considerations
specific to apps with containers, see
[Consumer security best practices for an app with containers](/developer-guide/native-apps/ui-consumer-security).
