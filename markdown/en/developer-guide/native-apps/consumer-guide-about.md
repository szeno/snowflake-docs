# What is a Snowflake Native App?

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## Definition: from a consumer’s perspective

A Snowflake Native App is a data application published by a third party that is installed and runs
entirely inside your Snowflake account. Unlike a web application you log into, or a connected tool
that extracts your data to process it elsewhere, a Native App lives where your data already lives:
inside your Snowflake environment, under your governance, accessible through the same interface and
controls you already use.

## Why use a Native App?

Three properties set Native Apps apart from other ways of working with third-party applications:

**Your data stays where it is.** The app runs inside your Snowflake account and processes your data
there. There are no data copies, no external pipelines to maintain, and no data leaving your
governance perimeter without your explicit permission.

**Access is controlled by the same Snowflake roles and policies you already use.** You grant the app
access to the data it needs using standard Snowflake Role-Based Access Control (RBAC), the same
mechanisms your team already uses. Your existing masking policies, row-access policies, and
governance controls continue to apply inside the app’s scope.

**You decide when it upgrades, and you can remove it at any time.** Unlike SaaS tools that update on
the vendor’s schedule, Native Apps have versioned releases. You can set a maintenance window for
upgrades. Uninstalling is fully under your control.

## Native App versus Connected App versus SaaS: which model fits your needs?

**A Native App brings the app to your data, not your data to the app.**

![](/static/images/native-apps/na-ca-saas-comparison.png)

|  | Native App | Connected App | SaaS App |
| --- | --- | --- | --- |
| Where app runs | Inside your Snowflake account | Outside your Snowflake account | Vendor’s infrastructure |
| Where data lives | Stays in account | Leaves account temporarily | Vendor’s data silo |
| Data egress | You control it (explicit grants) | App vendor controls (connection creds) | Vendor controls (replication) |

Expand

Show lessSee more

**Connected apps**, such as a BI charting tool connecting via ODBC, run outside your Snowflake
security perimeter. They retrieve your data to process it elsewhere and return results. Your data
leaves your account, carrying compliance and governance implications that must be managed separately.

**SaaS apps** have their own data silo. You replicate or send data to the vendor’s system; results
live separately from the rest of your Snowflake data, creating an ongoing reconciliation burden.

**Three patterns show where Native Apps have a clear advantage:**

**Pattern 1: Data ingestion (example: Salesforce connector)**

A connector that pulls data from Salesforce into your Snowflake account needs to run close to the
data destination: your account. The app uses an External Access Integration (EAI) that you
explicitly authorize to make the outbound call to Salesforce. The data flows in; it does not flow
out. With a traditional connected connector, your Snowflake credentials and Salesforce credentials
would both reside on a vendor server outside your governance, creating two attack surfaces outside
your control.

**Pattern 2: Pure computation (example: knowledge graph builder)**

An app that builds a knowledge graph from your relational data runs inside your account as a
computational engine. No data movement is needed. You grant the app access to the tables it needs;
it processes them in place. A connected approach would require copying your relational data out to
the vendor’s system for processing.

**Pattern 3: Data collaboration (example: identity resolution)**

An identity resolution app brings the provider’s proprietary identity graph and joins it with your
customer data inside your account. Neither party’s raw data crosses the boundary: the provider’s
identity graph is protected from you (provider IP protection); your customer data never leaves
Snowflake (consumer data protection). Only the derived results (better-matched customer records)
are visible. This pattern cannot be done safely with a connected app, which would require sending
your customer data to the vendor’s infrastructure where the identity graph also lives.

For apps that process sensitive data or large data volumes, Native Apps offer a significantly better
security posture than the alternatives: your data stays within your control (unlike a connected app),
and there is no separate data silo to manage or reconcile (unlike a SaaS app).

## The consumer lifecycle

Working with a Native App follows five stages. Each stage maps to a section of this guide.

![](/static/images/native-apps/na-consumer-lifecycle.png)

**Stage 1: Evaluation**

Before committing to procurement, many organizations run a Proof-of-Concept (PoC) or
Proof-of-Value (PoV) with the provider to establish business value. This phase typically involves
lighter-weight security and procurement review. Even at this stage, be deliberate about what access
you grant, only what the PoC genuinely requires. See [Evaluate a Native App before installing](/developer-guide/native-apps/consumer-guide-evaluate)
for evaluation guidance and [Grant access to a Native App](/developer-guide/native-apps/consumer-guide-access) for access decisions.

**Stage 2: Procurement**

Once business value is established, the app goes through a full procurement process covering
security, legal, and financial review. The provider will typically disclose upfront which privileges
the app requests and which App Specs will require your approval after installation. See
[Evaluate a Native App before installing](/developer-guide/native-apps/consumer-guide-evaluate) for the structured review process and
[Separation of responsibilities for Native Apps](/developer-guide/native-apps/consumer-guide-responsibility) for the formal shared-responsibility framework.

**Stage 3: Installation and initial configuration**

An account admin or their delegate installs the app. At this stage the app presents its privilege
requests and initial App Specs for approval. This is also the right time to configure the explicit
data access grants the app needs and set up Restricted Caller’s Rights if appropriate. See
[Install a Native App](/developer-guide/native-apps/consumer-guide-install) for installation steps and
[Grant access to a Native App](/developer-guide/native-apps/consumer-guide-access) for access configuration.

**Stage 4: Active use**

The app delivers business value. Upgrades happen automatically via patches (high compatibility) or
new versions (two-version compatibility window). During active use, the app may occasionally request
additional privileges or new App Spec approvals. These deserve the same scrutiny as at installation.
See [Upgrades and app lifecycle](/developer-guide/native-apps/consumer-guide-upgrades) for upgrades and
[Monitor and audit a Native App](/developer-guide/native-apps/consumer-guide-monitor) for monitoring.

**Stage 5: Uninstallation**

If the app is no longer needed, transfer ownership of any objects the app created outside its own
boundary before uninstalling. See [Uninstall a Native App](/developer-guide/native-apps/consumer-guide-uninstall) for the
uninstall checklist.
