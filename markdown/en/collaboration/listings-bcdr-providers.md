# Use BCDR for listings as a provider

## Key provider responsibilities

To maintain this seamless experience for your consumers, providers must ensure:

- **Failover group configuration**: All listings, shares, and linked databases must be part of a single failover group.
- **Metadata integrity**: You must regularly refresh the failover group to ensure the secondary account is a faithful replica of the primary.
- **Operational continuity**: In the event of a disaster, when you promote the secondary account to a primary, Snowflake automatically
  manages the redirection of the [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) pipelines. Providers must refresh the failover group in the original primary (when available) to serve consumers in that region.

Note

The “one mount point per region” constraint remains strictly enforced. This prevents data fragmentation and ensures that your consumers always have a clear, singular path to your data listings.

## Configure failover groups for listings and their dependencies

This section describes how to configure failover groups for your listings so that your listings and their dependencies are better protected during an outage.

### Access control requirements

To review the roles that are required to perform replication and failover on group objects in the system, see [Replication privileges](/user-guide/account-replication-considerations#label-replication-privileges).

### Step 1: Create a failover group on a listing

To create a new failover group that includes your listings, use [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group). To add listings to an existing failover group, use [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group).

Note

You must include dependencies along with listings when adding listings to a failover group. If your listing includes dependencies that
aren’t part of the failover group, such as dangling references, then Snowflake returns an error during the create or alter process.

Adding shares to listings is optional. Snowflake automatically selects all of the eligible listings and their shares for replication and failover.

The following example uses [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group) to create a new failover group for databases and listings. In this example, the failover group is named `provider_dr_fg`. The object types in the failover group include a database named `provider_dr_db` and an allowed account named `myorg.myaccount2`.

Copy code

```
CREATE FAILOVER GROUP provider_dr_fg
  OBJECT_TYPES = DATABASES, LISTINGS
  ALLOWED_DATABASES = provider_dr_db
  ALLOWED_ACCOUNTS = myorg.myaccount2;
```

### Step 2: Create a secondary failover group

To create a replica of the initial failover group on the allowed account, run the following commands:

Copy code

```
CREATE FAILOVER GROUP provider_dr_fg
  AS REPLICA OF myorg.myaccount1.provider_dr_fg;
ALTER FAILOVER GROUP provider_dr_fg REFRESH;
```

### Step 3: Validate the secondary failover group

1. To validate that the listing resolves, run the [SHOW LISTINGS IN FAILOVER GROUP](/sql-reference/sql/show-listings-in-failover-group) command followed by the
   [SHOW LISTINGS](/sql-reference/sql/show-listings) command.

   Copy code

   ```
   SHOW LISTINGS IN FAILOVER GROUP provider_dr_fg;
   SHOW LISTINGS LIKE 'provider_dr_listing_2';
   ```
2. To confirm that all shares are correctly associated with the listings in the secondary account, run the SHOW SHARES query.

   The response will include a non-NULL value in the `listing_global_name` field.

   Copy code

   ```
   SHOW SHARES LIKE 'provider_dr_listing_share';
   ```

   Note

   A NULL value in the `listing_global_name` field indicates an issue with attaching the share to the listing in the secondary account. Review your failover group configuration, or reach out to the Snowflake team for assistance.

## Limitations for providers after a failover

- **Listing Analytics**: Information in [Data Sharing Usage](/sql-reference/data-sharing-usage) is only available for listings in the account where the
  listings were originally created. This information may not be available in the failover account.
