# Replication Group support in business continuity and disaster recovery

This page is for data providers who use replication groups to serve consumers in different regions
or clouds. It explains how to include replication groups and their dependencies in a failover
group when configuring [account replication and failover groups](/user-guide/account-replication-intro).
With failover groups, in the event of a failure, replication groups rely on the failover groups
for data replication and disaster recovery.

Note

If you’re a data provider who uses Listings, see [Listing support in Business Continuity and Disaster Recovery](/collaboration/listings-bcdr)
for how to set up disaster recovery and failover for listings.

Note

Be sure to review the [Constraints when a failover group includes replication groups](#label-rg-in-fg-constraints) section before using this feature.

## Understanding the need for business continuity and disaster recovery (BCDR)

In the event of a failure, business continuity and disaster recovery (BCDR) becomes crucial for customers.

- Customers must continue to support their data products with minimal interruptions during an outage.
- Customers must meet service level agreements (SLAs) with regards to RTO (Recovery Time Objective)
  and RPO (Recovery Point Objective) to avoid financial penalties.
- Customers need to maintain replicas of their data in other regions in the event of a service-specific outage.

### Replication groups without BCDR

Without BCDR, returning to the original region post-outage state after a failure causes disruptions
for the use of replication groups.

Customers typically can use replication groups and failover groups for [data replication and disaster recovery](/user-guide/replication-intro). However, after a failover, customers still need
to create the replication groups on the secondary account, leading to higher recovery times and
stale information. At the same time, they experience downtime from remounting new replication groups
and updating ETL scripts, both of which lead to added data transfer costs.

### Replication groups with BCDR

Snowflake’s BCDR for replication groups improves enterprise-readiness and decreases disruption from a failure.

- BCDR for replication groups eliminates the need to recreate replication groups after a failover.
- Customers can continue to refresh the replication groups without any impact to their experience.
- It doesn’t incur additional data transfer costs, because the new primary region doesn’t require
  data to be replicated again to the secondary accounts; only incremental changes are replicated.

With Snowflake’s BCDR support for replication groups, after a failover, the replication group
refreshes from the new primary. That way, you can still meet data freshness requirements.

## Workflow when BCDR includes replication groups

The following steps represent the typical sequence of events during a disaster recovery
when the replicated objects include replication groups:

1. An outage hits the region, affecting the primary region.

   While the primary region is down, replication groups in secondary regions can’t refresh.
2. The data recovery (DR) admin initiates the organization’s runbook.
3. The DR admin gets approval to failover to the secondary region.

   - This secondary region becomes the new primary region.
   - The replica of the new primary region is present in the failover group. This failover group
     becomes the new source of information for all objects.
4. The DR admin refreshes the failover group objects with the latest updates from the data sources
   (such as external tables, ETL pipelines, and so on).

   - The DR admin gets a snapshot of objects in the failover group with the most up-to-date data
   - After getting all of the objects, replication groups begin working again at the next refresh interval.
5. The DR admin audits the new primary region to confirm whether it is ready for production.
6. The DR admin creates a replica of this failover group in another region as a backup.

## Prerequisites for BCDR for replication groups

Not all replication groups are eligible for inclusion in a failover group. The following must be
true in order for a replication group to be selected for data recovery:

- The replication group only contains the object types DATABASES, SHARES, or both.
- The target account for the replication group is different from the target account of the failover group.

## Configuring BCDR for replication groups

This section describes how to configure BCDR for your replication groups, so that your replication groups
and their dependencies are better protected during an outage.

### Access control requirements

Refer to the [Replication privileges](/user-guide/account-replication-considerations#label-replication-privileges) topic to
see the roles that are required to perform replication and failover on group objects in the system.

### Step 1: Create a failover group on a replication group

To create a new failover group that includes your replication groups, use the [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group) command. To add a replication group to an existing
failover group, use the [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) command.

Note

You must include dependencies along with replication groups when adding replication groups to a
failover group. If your replication group includes dependencies that aren’t part of the failover
group (such as dangling references), Snowflake returns an error during the create or alter
process.

The example below uses CREATE FAILOVER GROUP to create a failover group named `provider_dr_fg` and
that includes a replication group. The object types included in the replication group include
a database named `provider_dr_db`, a share named `provider_dr_share` and its allowed account is
`myorg.myaccount1`. Finally, this example includes an allowed account named `myorg.myaccount2`.

Copy code

```
CREATE FAILOVER GROUP provider_dr_fg
  OBJECT_TYPES = DATABASES,SHARES,REPLICATION GROUPS
  ALLOWED_DATABASES = provider_dr_db
  ALLOWED_SHARES = provider_dr_share
  ALLOWED_ACCOUNTS = myorg.myaccount2;
```

### Step 2: Validate the primary failover group

To check which replication groups are in the failover group, run the following command:

Copy code

```
SHOW REPLICATION GROUPS IN FAILOVER GROUP provider_dr_fg;
```

### Step 3: Create a secondary failover group

To create a replica of the initial failover group on the allowed account from the original failover
group, run the following commands:

Copy code

```
CREATE FAILOVER GROUP provider_dr_fg_secondary
  AS REPLICA OF myorg.myaccount1.provider_dr_fg;

ALTER FAILOVER GROUP provider_dr_fg_secondary REFRESH;
```

### Step 4: Validate the secondary failover group

To check that the replication group resolves, run the following command:

Copy code

```
SHOW REPLICATION GROUPS IN FAILOVER GROUP provider_dr_fg_secondary;
```

## Constraints when a failover group includes replication groups

When you use a failover group that includes replication groups,
you must set up the failover group to meet certain constraints.
You’re also prevented from making changes to the failover group
or its associated replication groups that would violate these constraints.

### Constraints on failover group object types

When a failover group contains databases or shares that are referenced by replication groups, the
failover group must include REPLICATION GROUPS in its OBJECT\_TYPES parameter. For example,
the following CREATE FAILOVER GROUP command includes REPLICATION GROUPS in the allowed object types.
Because the replication groups include the object types DATABASES and SHARES, the failover group
must include those object types also.

Copy code

```
CREATE FAILOVER GROUP provider_dr_fg
  OBJECT_TYPES = DATABASES,SHARES,REPLICATION GROUPS
  -- ... other clauses ...
```

### Complete subset constraints (all-or-nothing rule)

- When adding OBJECT\_TYPES to a failover group, if any object is referenced by a replication group,
  all objects referenced by that same replication group must be included in the same failover group.
- When removing OBJECT\_TYPES from a failover group, if any object is referenced by a replication
  group, all objects referenced by that same replication group must be removed together.
- You can’t remove REPLICATION GROUPS from a failover group’s OBJECT\_TYPES if any databases or
  shares exist in the failover group that are referenced by the replication groups.

### Constraints for DROP REPLICATION GROUP

- If a replication group is included in a failover group, you can’t run DROP REPLICATION GROUP for
  that group from the failover group secondary account.

### Constraints for DROP FAILOVER GROUP

- Dropping a secondary failover group (that is, on the secondary account) also drops its contained replication groups.
- Dropping a primary failover group (that is, on the primary account) doesn’t drop its contained replication groups.
