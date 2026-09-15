# Evaluate a Native App before installing

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Three stakeholder groups typically review a Snowflake Native App before procurement approval: the business
team establishing value, the finance team assessing cost and risk, and the security and legal teams
conducting compliance and risk review. Not every reviewer needs every section. Use the headings
below to navigate to the relevant parts.

## Business evaluation: does it meet the business objective?

The business review focuses on one question: does this app deliver the outcome we need?
Documentation can support but not substitute for this judgment.

**Define the business objective before evaluating the app.** A clear statement of expected outcome
(for example, “reduce time to identify high-value customers by 30%”) makes it easier to assess
whether the app’s capabilities are a genuine fit.

**Require the provider to document the value proposition.** A provider willing to commit to
expected outcomes in writing gives you a baseline for post-install measurement and a basis for
escalation if the app underperforms.

**Understand what data the app needs.** The data access the app requires should be proportionate to
the business benefit it delivers. If an app needs broad access to many of your most sensitive
datasets to produce a modest improvement, that is a signal worth examining before proceeding.

## How Snowflake reviews apps

Snowflake applies two layers of review to apps published on the Snowflake Marketplace:

**Marketplace review (at listing time):** Before an app can be discovered and installed by
consumers, Snowflake reviews and approves it for publication. This is a one-time gate.

**Security review (for every version and patch):** Snowflake runs security scans on each new
version and patch submitted by the provider. This process is largely automated; manual review
occurs in exceptional cases. This means the app you install has been scanned not just when it was
first published, but each time the provider releases a new version or patch.

These reviews establish a baseline. They are not a substitute for consumer due diligence.

Important

**Shared responsibility notice**

Provider is the seller of record, not Snowflake.

Consumer is responsible for security, privacy, compliance, and all other necessary reviews of the
provider’s app. Any security scanning or other vetting done by Snowflake is not a substitute for a
consumer’s due diligence.

Any additional privileges requested by the application beyond what the Snowflake Native App Framework grants by default must
be scrutinized by the consumer before grants are made. The impact of such additional privileges is
for the consumer to determine before granting them.

## Understanding the app’s technical security posture

Before approving an app’s installation, review the privilege requests and App Spec requests it will
present. This is the concrete artifact your security team needs to assess the app’s security
posture.

**Privilege requests to understand:**

`CREATE WAREHOUSE`, `CREATE TASK`, `CREATE MANAGED TASK`, `CREATE DATABASE`, `CREATE COMPUTE POOL`,
`BIND SERVICE ENDPOINT`. These allow the app to create operational resources. They do not, by
themselves, grant the app access to your data. See
for the full list.

**App Spec requests (higher risk, requiring explicit approval):**

App Specs are requests for capabilities that go beyond creating operational resources, for example,
making outbound network calls, using OAuth to connect to external services, sharing data back, or
connecting to another app. The provider should disclose expected App Specs during procurement so you
are not surprised by them at installation or upgrade time.

Any App Spec request that you cannot explain in terms of the app’s stated purpose is a reason to
ask the provider for clarification before approving. For a full description of each App Spec type
and how approvals work, see
.

After installation, you can monitor what the app actually has access to at any time using the
monitoring queries in [Monitor and audit a Native App](/developer-guide/native-apps/consumer-guide-monitor).

## Involving your security team: a structured handoff

To support a thorough security review, provide your security team with the following before
installation:

- The Snowflake Marketplace listing URL (for the provider’s published description, trust signals, and
  contact information)
- A screenshot or export of the privilege request screen (the Category 1 privileges the app will
  request)
- The list of App Specs the app will present, including EAI endpoint names, OAuth service names,
  and listing details if applicable
- The provider’s documentation of what data access the app will need (Category 3 grants)
- The formal shared-responsibility framework: see
  [Separation of responsibilities for Native Apps](/developer-guide/native-apps/consumer-guide-responsibility)

After installation, direct your security team to
[Monitor and audit a Native App](/developer-guide/native-apps/consumer-guide-monitor), which provides the ACCOUNT\_USAGE queries
to monitor what the app currently has access to and what it is doing.

## Understanding the cost

**Listing price:** Apps on the Snowflake Marketplace may be free, paid, or offered on a trial basis.
For trial apps: when the trial period expires, Snowflake automatically suspends the app unless you
convert to a full paid listing. Data written inside the app is retained while the app is suspended,
as long as you do not drop the app. Convert before expiry. Once suspended, resumption is not
guaranteed if the provider has changed the version or if there are unresolved state issues.

**Snowflake charges for the cost of running the app.** The app runs in your account, so it may incur
consumption-based charges when it runs. For a full list of possible charges, see
[Cost & billing](/guides-overview-cost).

**Snowflake compute consumed by the app:** The app runs its workloads on Snowflake compute. If it
creates warehouses (Category 1 privilege), those warehouses consume credits in your account. For
apps with containers, the compute pool also consumes credits. Monitor this using
`APPLICATION_DAILY_USAGE_HISTORY`. See
.

**Storage consumed:** Objects the app creates inside the APPLICATION boundary, and any databases or
tables it creates outside it with your permission, consume storage in your account. Monitor this
using `APPLICATION_DAILY_USAGE_HISTORY`.

**Serverless features:** The app may create serverless tasks or other serverless objects. Monitor
this using `APPLICATION_DAILY_USAGE_HISTORY`.
