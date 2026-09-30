# Optimized Refresh and RPO Assurance

Optimized Refresh and RPO Assurance make replication of Snowflake [failover groups](/user-guide/account-replication-intro) more
efficient and predictable. Optimized Refresh processes only the metadata changes since the previous refresh, so refresh duration scales
with your rate of change rather than the number of objects in the failover group. RPO Assurance provides a Recovery Point Objective
(RPO) target. Snowflake manages continuous refreshes for you and, for covered pairs, commits to the RPO target under the SLA. For
the current target, and when it is backed by a service-level agreement (SLA), see [SLA eligibility and coverage](#label-rpo-assurance-sla).

Failover groups that you have today keep running as *Replication Classic* by default. Snowflake recommends migrating to Optimized
Refresh or RPO Assurance for the best replication experience.

You can mix modes in the same account. Some failover groups can use Optimized Refresh, some can use RPO Assurance, and others can stay on
Replication Classic. Replication, failover, and failback work the same way regardless of refresh mode.

## Optimized Refresh

Optimized Refresh for failover groups makes refreshes more efficient and predictable as the number of objects in your account grows.
Each refresh scans and applies only the metadata changes since the previous refresh. Table data replication is already incremental in
every mode. Optimized Refresh is what makes metadata processing incremental too.

You opt in per failover group by setting a single property on the primary failover group: `OPTIMIZED_REFRESH = TRUE`.

### Benefits

- **Lower, more predictable refresh duration as you grow.**
  Accounts with large numbers of databases, schemas, tables, roles, and grants see the largest improvement.
- **Faster refreshes on stable workloads.** Periods of low metadata change result in correspondingly small refresh cycles.
- **Simpler, more forecastable pricing.** The pricing model that applies to Optimized Refresh is anchored primarily on the volume of
  replicated data, with a generous monthly free allowance on the per-object-change dimension. For details, see
  [Pricing for Optimized Refresh and RPO Assurance](/user-guide/account-replication-cost#label-optimized-refresh-pricing).
- **Drop-in compatibility.** Optimized Refresh works with the same failover group SQL surface you already use. Replication, failover, and
  failback semantics are unchanged.

### Requirements

When you enable Optimized Refresh on a failover group:

- The failover group must have a [REPLICATION\_SCHEDULE](/sql-reference/sql/create-failover-group) set, and the schedule interval must be
  no more than 6 hours. If the most recent successful refresh for the failover group is older than 6 hours, the next refresh falls back
  to a full refresh that re-establishes the baseline before incremental refreshes resume.
- The `OPTIMIZED_REFRESH` property can be set on the primary failover group only. Setting it on a secondary failover group fails.
- Business Critical Edition (or higher) is required (inherited from the failover group feature itself).

Tip

For the best experience with Optimized Refresh, Snowflake recommends a `REPLICATION_SCHEDULE` of `10 MINUTE` or less. Frequent refreshes
keep each incremental cycle small, which delivers the low RPO and the most predictable refresh durations.

### Enable Optimized Refresh on a new failover group

Run this on the source account. The example creates a failover group named `myfg` that uses Optimized Refresh to replicate database `db1`
to the target account `myaccount2`, refreshing every 10 minutes:

Copy code

```
CREATE FAILOVER GROUP myfg
  OBJECT_TYPES = DATABASES
  ALLOWED_DATABASES = db1
  ALLOWED_ACCOUNTS = myorg.myaccount2
  REPLICATION_SCHEDULE = '10 MINUTE'
  OPTIMIZED_REFRESH = TRUE;
```

On the target account, create the secondary failover group as usual. No additional property is required on the secondary:

Copy code

```
CREATE FAILOVER GROUP myfg
  AS REPLICA OF myorg.myaccount1.myfg;
```

### Switch an existing failover group to Optimized Refresh

Run this on the source account. If the existing failover group doesn’t already have a `REPLICATION_SCHEDULE` that meets the 6-hour
requirement, set or adjust it in the same statement:

Copy code

```
ALTER FAILOVER GROUP myfg SET
  REPLICATION_SCHEDULE = '10 MINUTE'
  OPTIMIZED_REFRESH = TRUE;
```

After the ALTER succeeds, the next refresh runs as Optimized Refresh, with the first-refresh behavior described in
[What to expect the first time you enable Optimized Refresh](/user-guide/account-replication-optimized-refresh#label-optimized-refresh-first-refresh).

### Switch a failover group back to Replication Classic

Optimized Refresh is fully reversible. To revert a failover group to Replication Classic, unset the property:

Copy code

```
ALTER FAILOVER GROUP myfg UNSET OPTIMIZED_REFRESH;
```

The next refresh runs under Replication Classic and is billed under Replication Classic compute pricing.

### Verify the current mode

Use [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups) to confirm which mode each group is using. The output includes an
`is_optimized_refresh_enabled` column:

Copy code

```
SHOW FAILOVER GROUPS;
```

A value of `TRUE` means subsequent refreshes for the group use Optimized Refresh. A value of `FALSE` means they use Replication Classic,
unless RPO Assurance is enabled.

You can also query the [REPLICATION\_GROUPS view](/sql-reference/account-usage/replication_groups) in ACCOUNT\_USAGE to see the
`IS_OPTIMIZED_REFRESH_ENABLED` column.

### What to expect the first time you enable Optimized Refresh

When you set `OPTIMIZED_REFRESH = TRUE` on an existing failover group, or create a new failover group with the property set, the first
refresh after enabling is a one-time bootstrapping refresh that establishes the metadata baseline that Optimized Refresh requires.
Subsequent metadata refreshes process changes from that baseline.

Plan for the following:

- The bootstrapping refresh takes longer than steady-state refreshes. Its duration is comparable to a Replication Classic refresh on the
  same failover group.
- The bootstrapping refresh is billed under the Optimized Refresh pricing model (replicated data volume plus changed objects, subject to
  the monthly free allowance). For details, see [Pricing for Optimized Refresh and RPO Assurance](/user-guide/account-replication-cost#label-optimized-refresh-pricing).
- Subsequent refreshes are faster. Beginning with the second refresh, only the metadata changes since the previous refresh are processed.

If you enable Optimized Refresh on a failover group whose `REPLICATION_SCHEDULE` would produce a refresh imminently, that refresh is the
one that runs as the bootstrapping refresh. You don’t need to trigger anything manually.

After the bootstrapping refresh, all standard failover group operations behave exactly as they did before. Scheduled refreshes, manual
refreshes, promotion, failover, and failback are unchanged.

### Limitations

A refresh can run as a full refresh instead of an incremental metadata refresh in the following cases. A full refresh takes longer than
usual.

- The first refresh after you create a failover group with Optimized Refresh enabled, and the first refresh after failover or failback.
  For details, see [What to expect the first time you enable Optimized Refresh](#label-optimized-refresh-first-refresh).
- After you change failover group membership, for example by running [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) to
  add or remove databases, shares, or other objects.
- When the failover group contains Native App application packages. Those refreshes currently fall back to a full refresh.
- Under certain rare conditions, for example a new Snowflake release that introduces replication support for a new feature.

## RPO Assurance

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical Edition (or higher).

RPO Assurance is a capability for Snowflake failover groups that provides a Recovery Point Objective (RPO) target. When you enable it
on a primary failover group, Snowflake automatically manages continuous replication refreshes to keep secondary accounts in sync with
the primary. For the current target, and when it is backed by a service-level agreement (SLA), see
[SLA eligibility and coverage](#label-rpo-assurance-sla).

Without RPO Assurance, you manage replication refreshes using `REPLICATION_SCHEDULE` or cron jobs, and there’s no system-managed
guarantee on how current the secondary remains. RPO Assurance removes this operational burden: Snowflake manages the refreshes for you
and, for covered pairs, commits to the RPO target under the SLA.

You can enable RPO Assurance on any failover group that meets the [prerequisites](#prerequisites). The SLA applies only to covered pairs.
See [SLA eligibility and coverage](#label-rpo-assurance-sla).

To request access, contact your Snowflake account team.

### Key benefits

- **Contractual, financially backed RPO SLA:** For covered pairs, the secondary stays within the RPO target for at least 99.9% of
  covered minutes each calendar month, so data loss in a failover is bounded. If Snowflake misses that level for a pair, you can
  request Feature Level Credits under the [Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).
  See [SLA eligibility and coverage](#label-rpo-assurance-sla).
- **Fully managed continuous refresh:** There’s no schedule to configure. Changes are replicated from the source account to the
  target account continuously, and Snowflake manages the entire refresh lifecycle for you.
- **Intelligent throughput:** Up to 2x higher throughput compared to Optimized Refresh. If Snowflake determines that the failover
  group can benefit from additional compute to achieve higher throughput, it allocates that compute automatically.
- **Highest priority:** Your disaster recovery (DR) workloads have the highest priority for replication compute and networking. If
  resource contention occurs because of a spike in traffic from other workloads, your DR workloads get first access to the
  available replication infrastructure to uphold the contractual SLA.

### Prerequisites

Before you enable RPO Assurance, make sure the following are true:

- You have a failover group configured between a primary and at least one secondary account. Failover groups require Business
  Critical Edition or higher.
- You set `RPO_ASSURANCE = TRUE` on the primary failover group.
- The failover group doesn’t have a `REPLICATION_SCHEDULE` set. RPO Assurance and manual replication schedules are mutually
  exclusive. You must unset any existing schedule before you enable RPO Assurance.
- You have sufficient privileges on the failover group to run [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group). This
  requires the `OWNERSHIP` privilege on the failover group, or the `REPLICATE` privilege at the account level.

### Enable RPO Assurance

You configure RPO Assurance on the primary failover group with a single `ALTER FAILOVER GROUP` statement. You can’t set it from a
secondary account.

#### Enable the feature

Run the following statement on the primary account:

Copy code

```
ALTER FAILOVER GROUP <name> SET RPO_ASSURANCE = TRUE;
```

When this statement runs successfully:

- A target lag is set on the failover group. Enabling the feature doesn’t by itself mean the pair is covered by the SLA. See
  [SLA eligibility and coverage](#label-rpo-assurance-sla).
- Continuous replication refreshes begin immediately on all secondary accounts where the failover group is active (not suspended).
- Optimized Refresh (log-based replication) is automatically enabled on the failover group for improved performance. No additional
  configuration is needed.

Note

If the failover group already has a `REPLICATION_SCHEDULE` set, the `ALTER FAILOVER GROUP` statement fails. You must first unset
the schedule:

Copy code

```
ALTER FAILOVER GROUP <name> UNSET REPLICATION_SCHEDULE;
```

#### Disable the feature

Run the following statement on the primary account. Both methods work, but using `UNSET` is the preferred method for consistency
with other Snowflake configuration commands:

Copy code

```
ALTER FAILOVER GROUP <name> UNSET RPO_ASSURANCE;
```

Alternatively:

Copy code

```
ALTER FAILOVER GROUP <name> SET RPO_ASSURANCE = FALSE;
```

Both statements have the same effect. When RPO Assurance is disabled, continuous refreshes stop and the failover group returns to a
state where no automatic refreshes are scheduled. You can then configure a `REPLICATION_SCHEDULE` manually if needed. A pair isn’t
covered by the SLA while RPO Assurance is disabled.

#### Verify RPO Assurance status

Use [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups) to confirm that RPO Assurance is enabled:

Copy code

```
SHOW FAILOVER GROUPS LIKE '<name>';
```

The output includes an `rpo_assurance` column that displays `TRUE` or `FALSE`.

### How RPO Assurance works

#### Continuous refresh cycle

When RPO Assurance is enabled, Snowflake manages the refresh lifecycle as follows:

1. A refresh from the source account to the target account is scheduled immediately.
2. The refresh replicates all metadata and data changes from the primary to the secondary. Refreshes happen continuously: when one
   refresh completes, the next one is scheduled immediately.
3. Each refresh captures a consistent snapshot of the primary at a specific point in time. Replication lag at any moment is how stale
   the secondary is relative to the primary.

This continuous cycle ensures the secondary is always converging toward the primary’s current state.

#### Target lag

The system targets the RPO target as the maximum lag between the primary and secondary. To achieve this, the system is designed to
complete each individual refresh well within the target lag window.

#### When replication falls behind

A large volume of changes can make a refresh take longer than usual and push replication lag above the RPO target. Whether that time
counts against the SLA depends on the rules in [Which minutes count](#label-rpo-assurance-which-minutes-count).

If your workload regularly exceeds the [change-volume limits](#label-rpo-assurance-change-volume-limits), contact your Snowflake
account team to discuss whether a different RPO target fits your workload. If the change rate consistently exceeds the recommended
guidelines, reach out to your Snowflake account team to evaluate how Snowflake can best support your requirements.

### SLA eligibility and coverage

RPO Assurance is backed by a service-level agreement in the RPO Assurance section of the
[Snowflake Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/)
(the SLA). This section holds the eligibility and coverage requirements, change-volume limits, and measurement rules the SLA refers
to. If this page and the SLA conflict, the SLA controls.

The SLA applies separately to each primary failover group and one of its secondary failover groups (a *replication pair*).

**RPO target:** 30 minutes, unless your written agreement with Snowflake specifies a different target.

#### Coverage requirements

A minute is covered by the SLA for a replication pair when all of the following are true:

- RPO Assurance is enabled on the primary failover group.
- The secondary failover group is active (not suspended).
- The primary and secondary accounts are in a supported region pair. See [Supported region pairs](#label-rpo-assurance-supported-region-pairs).
- The primary and secondary accounts are in regions of the same cloud provider. Cross-cloud pairs aren’t covered.
- The failover group contains only object types that are compatible with Optimized Refresh. See [Prerequisites](#prerequisites).
- The minute isn’t excluded under [Which minutes count](#label-rpo-assurance-which-minutes-count).

You can enable RPO Assurance on a pair that doesn’t meet these requirements, as long as it meets the prerequisites. The SLA
doesn’t apply to that pair.

#### Which minutes count

Snowflake measures replication lag once each minute from its replication records. A covered minute in which lag is above the RPO
target is a miss. Every covered minute counts toward the SLA, except minutes during these refreshes:

- The first refresh after you enable RPO Assurance.
- The first refresh after a failover or failback.
- A refresh caused by a change to what the failover group contains, such as adding a database.
- The first refresh after a Snowflake release adds support for a new object type.
- A refresh whose change volume exceeds a [change-volume limit](#label-rpo-assurance-change-volume-limits). Minutes stay excluded
  until replication lag is back at or below the RPO target.

Refreshes are excluded only when a full refresh is unavoidable or the event is customer-driven. Refreshes that Snowflake runs for
its own reasons count. Excluded refreshes still run. Excluded minutes count as neither meeting nor missing the target.

##### Change-volume limits

A refresh exceeds the limits when it involves more than either of the following:

| Limit | Value |
| --- | --- |
| Changed objects | 100,000 per five minutes |
| Data transfer | 100 GB per five minutes |

Expand

Show lessSee more

For example, a bulk load pushes a covered pair’s refresh over the 100 GB per five minutes limit. Minutes from that point are
excluded. Two hours later, lag is back at or below the RPO target, and minutes count again.

Lag history for each failover group is available through
[REPLICATION\_GROUP\_LAG\_HISTORY](/sql-reference/functions/replication_group_lag_history). Snowflake calculates the Monthly RPO
Percentage for each calendar month from its replication records, applying the exclusions above. The calculation, the credit
amounts, and how to request credits are in the RPO Assurance section of the
[Support Policy](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

#### Supported region pairs

The SLA covers only pairs whose primary and secondary accounts are in one of the following region pairs. All supported pairs are
within the same cloud provider; cross-cloud pairs aren’t covered. You can enable RPO Assurance on other pairs, but they aren’t
covered.

Each region in a pair can serve as the primary or the secondary. Cloud region IDs and region names match
[Supported cloud regions](/user-guide/intro-regions).

| Cloud platform | Cloud region ID | Region name | Cloud region ID | Region name |
| --- | --- | --- | --- | --- |
| Amazon Web Services (AWS) | us-east-1 | US East (N. Virginia) | us-west-2 | US West (Oregon) |
| Microsoft Azure | centralus | Central US (Iowa) | eastus2 | East US 2 (Virginia) |
| Microsoft Azure | westus2 | West US 2 (Washington) | eastus2 | East US 2 (Virginia) |
| Amazon Web Services (AWS) | us-east-1 | US East (N. Virginia) | us-east-2 | US East (Ohio) |
| Amazon Web Services (AWS) | us-east-2 | US East (Ohio) | us-west-2 | US West (Oregon) |
| Microsoft Azure | westus2 | West US 2 (Washington) | centralus | Central US (Iowa) |
| Microsoft Azure | southcentralus | South Central US (Texas) | eastus2 | East US 2 (Virginia) |
| Microsoft Azure | centralus | Central US (Iowa) | southcentralus | South Central US (Texas) |
| Microsoft Azure | westus2 | West US 2 (Washington) | southcentralus | South Central US (Texas) |
| Google Cloud Platform (GCP) | us-central1 | US Central1 (Iowa) | us-east4 | US East4 (N. Virginia) |
| Amazon Web Services (AWS) | us-gov-east-1 | US Gov East 1 (FedRAMP High Plus) | us-gov-west-1 | US Gov West 1 (FedRAMP High Plus) |
| Amazon Web Services (AWS) | ap-northeast-1 | Asia Pacific (Tokyo) | ap-northeast-3 | Asia Pacific (Osaka) |
| Microsoft Azure | westeurope | West Europe (Netherlands) | northeurope | North Europe (Ireland) |
| Amazon Web Services (AWS) | eu-west-1 | EU (Ireland) | eu-west-2 | Europe (London) |
| Amazon Web Services (AWS) | eu-central-1 | EU (Frankfurt) | eu-west-1 | EU (Ireland) |

Expand

Show lessSee more

If you’re looking for another region pair that isn’t currently listed, contact your Snowflake account team to see how Snowflake can
best support your requirements.

#### Constraints

The following constraints apply:

| Constraint | Details |
| --- | --- |
| Supported group types | Failover groups only (not replication groups). |
| Configuration location | Primary account only. |

Expand

Show lessSee more

For mutual exclusivity with `REPLICATION_SCHEDULE` and the required privileges, see [Prerequisites](#prerequisites).

### Failover and failback

RPO Assurance doesn’t change failover or failback semantics. You promote a secondary and fail back using the same steps as any
other failover group. For details, see [Replication and failover/failback of databases and accounts](/user-guide/account-replication-failover-failback).

The RPO Assurance configuration is preserved across failover and failback operations and survives the full round-trip, so you don’t
need to re-enable it after a failover. After the new secondary is resumed, continuous refreshes begin again. The first refresh after
a failover or failback is excluded from the SLA calculation. See [Which minutes count](#label-rpo-assurance-which-minutes-count).

### Monitor lag

#### REPLICATION\_GROUP\_LAG\_HISTORY table function

Use the [REPLICATION\_GROUP\_LAG\_HISTORY](/sql-reference/functions/replication_group_lag_history) Information Schema table function to
view historical lag for a failover group. This function shows lag history for a failover group. The monthly SLA calculation uses
Snowflake’s replication records and applies the exclusions in [Which minutes count](#label-rpo-assurance-which-minutes-count).

The output shows how lag evolves over time as a sawtooth pattern: lag increases between refreshes (as time passes without a new
snapshot), then drops when a refresh completes (a new, more recent snapshot is applied).

Basic usage (defaults to the last 24 hours):

Copy code

```
SELECT *
  FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_LAG_HISTORY(
    REPLICATION_GROUP_NAME => '<failover_group_name>'
  ));
```

With a custom time range:

Copy code

```
SELECT *
  FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_LAG_HISTORY(
    REPLICATION_GROUP_NAME => '<failover_group_name>',
    START_TIME => '2024-06-01 00:00:00'::TIMESTAMP_LTZ,
    END_TIME => '2024-06-07 00:00:00'::TIMESTAMP_LTZ
  ));
```

The output includes the following columns:

| Column | Type | Description |
| --- | --- | --- |
| `TIMESTAMP` | `TIMESTAMP_LTZ` | Point in time for the lag measurement. |
| `LAG_SECONDS` | `NUMBER` | The replication lag in seconds at that point in time. |
| `PRIMARY_SNAPSHOT_TIMESTAMP` | `TIMESTAMP_LTZ` | The primary snapshot timestamp from the most recent completed refresh. |

Expand

Show lessSee more

The output is structured for direct visualization in any charting tool.

##### Interpret the results

- **Healthy state:** Peak lag values (just before each refresh completes) remain at or below the RPO target.
- **Lag above target:** Lag above the RPO target is a miss only during covered minutes. A lag spike by itself doesn’t mean the SLA
  was missed for the month. To see why a refresh ran long, check
  [REPLICATION\_GROUP\_REFRESH\_HISTORY](/sql-reference/account-usage/replication_group_refresh_history).
- **No data points:** If no data points are returned for a time range, no refreshes completed during that period. This could
  indicate the failover group was suspended or that a single long-running refresh was in progress. A gap in the data doesn’t by
  itself show whether the pair was covered or whether the SLA was met.

#### REPLICATION\_GROUP\_REFRESH\_HISTORY view

For detailed per-refresh execution information, use the [REPLICATION\_GROUP\_REFRESH\_HISTORY](/sql-reference/account-usage/replication_group_refresh_history)
Account Usage view:

Copy code

```
SELECT
    REPLICATION_GROUP_NAME,
    PHASE_NAME,
    START_TIME,
    END_TIME,
    PRIMARY_SNAPSHOT_TIMESTAMP,
    TOTAL_BYTES
  FROM SNOWFLAKE.ACCOUNT_USAGE.REPLICATION_GROUP_REFRESH_HISTORY
  WHERE REPLICATION_GROUP_NAME = '<failover_group_name>'
  ORDER BY START_TIME DESC
  LIMIT 20;
```

This view shows individual refresh executions, durations, and data volumes. It’s useful for diagnosing why specific refreshes took
longer than expected.

### Billing

RPO Assurance is billed under a model similar to Optimized Refresh (log-based replication), with a higher rate for replicated data
volume. Because refreshes run continuously to maintain the RPO target, replication costs reflect the ongoing activity.

For rates and how they compare with Optimized Refresh and Replication Classic, see
[Pricing for Optimized Refresh and RPO Assurance](/user-guide/account-replication-cost#label-optimized-refresh-pricing).

### Get started

1. **Request access:** Contact your Snowflake account team to enable RPO Assurance on your account.
2. **Prepare the failover group:** Make sure no manual replication schedule is set:

   Copy code

   ```
   ALTER FAILOVER GROUP <name> UNSET REPLICATION_SCHEDULE;
   ```
3. **Enable RPO Assurance** (run on the primary account):

   Copy code

   ```
   ALTER FAILOVER GROUP <name> SET RPO_ASSURANCE = TRUE;
   ```
4. **Verify that RPO Assurance is active:**

   Copy code

   ```
   SHOW FAILOVER GROUPS LIKE '<name>';
   -- Check that the rpo_assurance column shows TRUE
   ```
5. **Monitor replication lag:**

   Copy code

   ```
   SELECT *
     FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_LAG_HISTORY(
       REPLICATION_GROUP_NAME => '<name>'
     ));
   ```

   Compare peak `LAG_SECONDS` values (in seconds) with the RPO target. For SLA coverage and the monthly calculation, see
   [SLA eligibility and coverage](#label-rpo-assurance-sla).
