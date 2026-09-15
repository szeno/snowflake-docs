# Listing support in Business Continuity and Disaster Recovery

Providers can include listings and their dependencies — such as shares and databases — in [account replication and failover groups](/user-guide/account-replication-intro). With failover groups, if a service degradation or outage occurs, the listing relies on failover groups for data replication and disaster recovery.

Note

- This feature is only available for listings that have enabled [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment).
- Review the [Behavior, considerations, and constraints](#label-listings-bcdr-behavior-and-constraints) section before using this feature.

## Terms

- Primary listings: Listings in the primary failover group
- Secondary listings: Listings in the secondary failover group

## Understanding the need for Business Continuity and Disaster Recovery

In the event of an outage in the primary region, Business Continuity and Disaster Recovery (BCDR) becomes crucial for providers.

- Providers must continue to support their data products with minimal interruptions during an outage.
- Providers must meet service level agreements (SLAs) with respect to RTO (Recovery Time Objective) and RPO (Recovery Point Objective) to avoid financial penalties.
- Providers must maintain replicas of their data in secondary regions in the event of an outage.

### Manual configuration for failover and recovery

Providers who don’t add listings to their failover groups have higher recovery times and stale information for their consumers. Without
BCDR, providers must re-create listings in the secondary regions after failover. And then consumers must remount to new listing URLs. This
manual replication causes massive disruptions on ETL pipelines and applications, leading to extended downtime for consumers and added data
transfer costs for providers.

### Automated failover and recovery

BCDR for listings improves enterprise-readiness and decreases disruption from a failure.

- BCDR for listings eliminates the requirement for providers to re-create listings after a failover.
- The new primary region doesn’t re-replicate to the Secure Share Area (SSA) accounts, which saves data transfer costs because only incremental changes are replicated to the SSA accounts.

With BCDR support for listings, after a failover:

- Consumers still have access to provider data without downtime.
- Providers can fulfill new consumer regions from the new primary region.
- Providers can still meet consumer data freshness requirements because the listing refreshes from the new primary.

## BCDR workflow for listings

A typical BCDR workflow for listings is as follows:

1. An outage hits the region, affecting the primary region.

   - While the primary region is down, listings in consumer regions can’t refresh. As a result, consumers are operating with stale data.
2. The data recovery administrator initiates the organization’s runbook.
3. The administrator gets approval to fail over to the secondary region.

   - This secondary region becomes the new primary region.
   - The replica in the failover group becomes the new source of information for all objects.
4. The administrator refreshes the new primary with the latest updates from the data sources, such as external tables and ETL pipelines.

   - The administrator gets a snapshot of objects in the new primary to verify it has the most up-to-date data.
   - The administrator audits the new primary region to confirm whether it is ready for production.
   - After the failover is complete, auto-fulfillment begins working again at the next refresh interval from the new primary.

Note

The administrator can use the [SHOW LISTINGS IN FAILOVER GROUP](/sql-reference/sql/show-listings-in-failover-group) command to confirm that the listings are ready for production.

## BCDR selection criteria

BCDR is not supported when:

- The listing is in draft state.
- The listing is backed by a stage.
- The listing is a paid listing.
- The listing doesn’t have [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) enabled.
- The listing is a Snowflake Native App listing.

## Behavior, considerations, and constraints

Review the sections below to understand the behavior, considerations, and constraints of BCDR for listings.

### Behavior

- If a secondary failover group is dropped, the secondary listings in the failover group are automatically dropped.

### Considerations

- Failover of externally managed Iceberg tables isn’t supported at this time, even though they are supported for auto-fulfillment. Failover
  of managed Iceberg tables is supported. For more information, see [Configure replication for Snowflake-managed Apache Iceberg™ tables](/user-guide/tables-iceberg-replication).
- Some features might not be supported for failover under the database but could be supported for failover under the listing. The unsupported objects will be ignored during replication.

### Constraints

Ensure that you understand the following constraints before configuring BCDR for listings:

- [Complete subset constraints (all-or-nothing rule)](#label-listings-bcdr-complete-subset-constraints)
- [Failover group object type requirements](#label-listings-bcdr-fg-object-type-requirements)
- [Listing auto-fulfillment setup constraints](#label-listings-bcdr-laf-setup-constraints)
- [Internal Marketplace listings constraints](#label-listings-bcdr-im-constraints)
- [Profile replication constraints](#label-listings-bcdr-profile-replication-constraints)
- [Read-only secondary listing constraints](#label-listings-bcdr-read-only-secondary-listing-constraints)

#### Complete subset constraints (all-or-nothing rule)

- When adding an object to a failover group, if any object is referenced by a listing that has auto-fulfillment enabled, all objects referenced by that same listing must be included in the same failover group.
- When removing an object from a failover group, if any object is referenced by a listing that has auto-fulfillment enabled, all objects referenced by that same listing must be removed together.

#### Failover group object type requirements

When a failover group contains databases or shares that are referenced by listings that have auto-fulfillment enabled, the failover group must include `LISTINGS` in its `OBJECT_TYPES` parameter. For example:

Copy code

```
CREATE FAILOVER GROUP provider_dr_fg
  OBJECT_TYPES = DATABASES, LISTINGS
  ...
```

#### Listing auto-fulfillment setup constraints

- Before enabling auto-fulfillment on a listing or publishing a listing that has auto-fulfillment enabled, all listing dependencies — including shares and databases — must be configured in a failover group that includes the `LISTINGS` object type.
- Auto-fulfillment must be enabled on the secondary account manually (if it’s not already enabled). For more information, see [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account).
- When the [REFERENCE\_USAGE](/sql-reference/sql/grant-privilege-share) privilege is used by listings, there can be objects that aren’t
  directly related to the listing but that also counted as part of the subset in the complete subset constraint.

#### Internal Marketplace listings constraints

The following constraints apply to listings on the Internal Marketplace (organizational listings):

##### Request approval workflow

- If a consumer submits a request for an organizational listing that hasn’t been approved, and the system fails over to a secondary
  deployment, the replica provider won’t see the consumer’s request. This is because requests are tied to the deployment where the requests
  were originally made. The consumer needs to re-request the listing.
- Attempting to unpublish the listing after failing back to the primary region will fail in the following scenario:

  - A consumer requests a listing that’s in a primary region and in its failover regions, and
  - The consumer re-requests the listing, which was approved while in the secondary region.

  This failure occurs because the original pending request remains. To successfully unpublish, the provider must explicitly reject the
  original request and then re-attempt the unpublish operation.

##### Data Dictionary

- Featured objects aren’t part of the failover replication process. As a result, any featured objects selected on the primary instance will
  not be reflected on the secondary instance after a failover. The provider must manually reset these objects after a failover. If the
  provider doesn’t reset the featured objects, the consumer would see a stale Data Dictionary, even if they add new tables. This is because the background job skips this listing. The background job will pick up this listing after featured objects are set.
- If any modifications are made to featured objects while the system is operating as a replica, those changes won’t be synchronized back to the original primary instance after failback.

##### Data Preview

- Data preview information is not replicated to secondary regions. As a result, after a failover, consumers won’t see any Data Preview
  files. On the secondary region, the provider must regenerate Data Preview files.
- Similar to Data Dictionary, any changes made to Data Preview during a failover state won’t be synchronized back to the original primary after failback. The provider can reset the data preview information on the original primary after failback.

##### Organization profiles

- Both the primary provider and the secondary provider must use a [profile](/user-guide/collaboration/organization-profiles/org-profiles-create-manage) that can publish the listing.

#### Profile replication constraints

- If profiles aren’t replicated by a failover group, then listings on the secondary account continue to work with no profiles attached.
- If profiles aren’t replicated by a failover group, the original primary account’s profiles will remain unchanged after a failover and failback refresh.
- The secondary account’s profiles are read-only until failover happens. After failover, the new primary account can create, alter, or drop profiles.
- If the secondary account has an existing local profile, the initial failover group refresh will fail intentionally to avoid potential data loss. Follow the steps in the query result message to proceed.
- Profile approval requests aren’t replicated. If there is any pending approval request in the original primary account, then after failover, the new primary account can re-request approval.

#### Read-only secondary listing constraints

Secondary listings can’t be modified directly. All write operations, such as ALTER and DROP, must be performed on the primary listing.
