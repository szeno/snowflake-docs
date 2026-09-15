# Upgrades and app lifecycle

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## Versions and patches: the versioning model

Each Snowflake Native App has a major version and a patch. These are not just version labels — they encode
specific compatibility commitments that the provider is required to maintain.

A **major version** represents a significant release of the app. An app can have at most two major
versions in existence at any point in time.

A **patch** is a release within a major version. Patches are typically used for bug fixes and
improvements that do not require schema changes.

**Understanding what is preserved across upgrades:**

An app is composed of two types of components:

- **Code (stateless):** procedures, functions, Streamlit apps, and other application logic. Code is
  replaced on each version or patch upgrade.
- **Data (stateful):** tables and stored results inside the APPLICATION boundary. Data is preserved
  across upgrades.

This distinction is important: when your app upgrades, the app’s behavior and code change, but the
data it has accumulated in your account does not disappear. Your stored results, configuration data,
and any other tables inside the APPLICATION boundary are preserved.

**Compatibility guarantees:**

- **Across patches:** providers are required to maintain high compatibility. A patch must be
  compatible with the code running from all other patches of the same version. Schema changes are
  generally not introduced in patches.
- **Across two consecutive versions:** providers must maintain compatibility between the immediately
  prior version and the current version. This gives providers a manageable compatibility window and
  allows them to evolve their schema gradually. Version n can introduce a change from n-1, but it must
  still maintain compatibility with n-1 and perform whatever migration is needed. In version n+1,
  compatibility with n-1 is no longer required as migrations for n-1 to n are complete and there
  is no expectation of an n-1 to n+1 upgrade.

The practical consumer implication: an automatic upgrade to a new patch or version should not break
your usage of the app. If an upgrade does cause a problem, that is a provider issue to resolve —
see [Get support for a Native App](/developer-guide/native-apps/consumer-guide-support).

## Why upgrades are automatic, and why that benefits you

Snowflake automatically upgrades Native Apps when a provider releases a new version or patch. This
is directly analogous to how Snowflake itself is upgraded — in the background, progressively rolling
out to accounts even while the application is in use.

The reason upgrades are automatic is structural: Snowflake enforces a maximum of two major versions
in existence at any time. For a provider to release a new major version (version 3), they must
first upgrade all consumer accounts off the oldest version (version 1). This constraint keeps the
compatibility obligation tractable — providers only ever need to reason about compatibility with the
immediately prior version, so they can maintain strong guarantees.

Consumers benefit from this structure: the two-version limit forces providers to invest in upgrade
quality and compatibility. It is not in the provider’s interest to ship an upgrade that breaks
consumer installations, because they cannot move forward until all consumers are successfully
upgraded.

## Consumer control over upgrade timing

You are not without control over when upgrades happen. You can specify a maintenance schedule:
frequency and time when application upgrades can be performed. For example, you might set the
application upgrade schedule to midnight on Monday mornings. Snowflake will try not to initiate an
upgrade at different times.

Note that the application provider must explicitly opt in to this feature to honor consumer
maintenance schedules when releasing new upgrades.

Keep in mind that upgrades cannot be deferred indefinitely. If an upgrade is available but your
maintenance schedule is too sparse, Snowflake will apply the upgrade after a grace period defined
by the provider.

For full instructions, see [Consumer-controlled maintenance policies](/developer-guide/native-apps/consumer-maintenance-policies).

## What happens during an upgrade, and what doesn’t change

During an upgrade, the setup script re-runs. This may add, modify, or replace procedures, Streamlit
apps, schemas, and functions inside the APPLICATION boundary. Code changes; data does not.

**What is preserved:**

- All data tables inside the APPLICATION boundary (subject to the provider’s schema compatibility
  guarantee)
- Objects the app created outside the APPLICATION boundary (these belong to you and are not
  affected by the upgrade)
- Your existing privilege grants to the app

**Long-running queries are protected (finalization):** if you have a long-running stored procedure
or query executing inside the app when an upgrade happens, it completes on the version it started
on. The query is “pinned” to its version until it finishes. No mid-execution version switch occurs.
This is why a version upgrade can complete in the background while a long-running query started
before the upgrade continues to completion normally.

The app may be briefly unavailable during the upgrade window while the setup script runs. Snowflake
provides means to always ensure non-disruptive upgrades, but not all applications can easily comply
with this best practice.
