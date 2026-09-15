# Business Continuity and Disaster Recovery for Declarative Sharing

Business Continuity and Disaster Recovery (BCDR) for Declarative Native Apps allows providers to include app packages of type `DATA` in [failover groups](/user-guide/account-replication-intro). When a regional outage occurs, your app package, reference databases, and listing automatically replicate to a secondary provider account, keeping consumers connected to your data with minimal disruption.

Without BCDR, providers must manually re-create listings after a failover, which causes extended downtime for consumers and requires them to remount to new listing URLs.

This feature builds on top of [BCDR for listings](/collaboration/listings-bcdr). You should read that page alongside this one.

## Key capabilities

- **Listing failover**: Failover groups now support Native App listings of type `DATA`, replicating the app package and reference databases to the secondary account on failover.
- **Full database replication**: Failover groups perform full database replication (unlike standard listing auto-fulfillment sub-database replication), supporting bidirectional failover.
- **Refresh continuity**: Consumer accounts using listing auto-fulfillment automatically find and refresh from the new primary account after failover.
- **Application state visibility**: The `APPLICATION_STATE` view in the failover account reconciles global data after failover, though there may be a period of staleness before reconciliation completes.

## Unsupported scenarios

The following scenarios are not supported:

- Full account migration (permanent moves).
- Cumulative cross-account views for Account or Organization usage.
- BCDR for app packages that don’t have a published listing.
- Automatic account-level role replication (you must include roles manually in the failover group).

## Constraints

Before configuring BCDR, review these constraints carefully.

Superset rule
:   A failover group must be a complete superset of any associated listing auto-fulfillment replication group. You must explicitly include the app package, every reference database, and the listing in the same failover group.

Dependency management
:   If an app uses a view in `DB_A` that references data in `DB_B`, both databases must be in the same failover group.

Version creation dependency
:   If a new version of your app introduces new reference databases, add those databases to the failover group before or during the version creation command.

Listing constraints
:   Only active, published listings are supported. Draft listings and listings without [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) enabled are not eligible.

Secondary account read-only mode
:   To prevent split-brain scenarios, write operations are blocked on secondary accounts. You can’t create versions, patches, or modify listings in a secondary account.

## Set up BCDR

### Access control requirements

To replicate and fail over group objects, see [Replication privileges](/user-guide/account-replication-considerations#label-replication-privileges) for the required roles.

### Step 1: Create a failover group

Create a failover group that includes your app package, reference databases, shares, and listing. The following example creates a failover group named `provider_dr_fg` and allows replication to a secondary account:

Copy code

```
CREATE FAILOVER GROUP provider_dr_fg
  OBJECT_TYPES = DATABASES, APPLICATION_PACKAGES, SHARES, LISTINGS
  ALLOWED_APPLICATION_PACKAGES = my_app_package
  ALLOWED_DATABASES = my_reference_db
  ALLOWED_SHARES = my_listing_share
  ALLOWED_ACCOUNTS = my_org.secondary_account;
```

### Step 2: Create the secondary failover group

From the secondary account, create a replica of the failover group and refresh it:

Copy code

```
CREATE FAILOVER GROUP provider_dr_fg
  AS REPLICA OF my_org.primary_account.provider_dr_fg;

ALTER FAILOVER GROUP provider_dr_fg REFRESH;
```

### Step 3: Validate the secondary failover group

Confirm that the listing and app package are available in the secondary account:

Copy code

```
SHOW LISTINGS IN FAILOVER GROUP provider_dr_fg;
SHOW APPLICATION PACKAGES IN FAILOVER GROUP provider_dr_fg;
```

### Modify failover group membership

To add or remove an app package from an existing failover group:

Copy code

```
ALTER FAILOVER GROUP provider_dr_fg
  ADD my_app_package TO ALLOWED_APPLICATION_PACKAGES;
```

Copy code

```
ALTER FAILOVER GROUP provider_dr_fg
  REMOVE my_app_package FROM ALLOWED_APPLICATION_PACKAGES;
```

### Perform a failover

To promote the secondary account to primary, run the following from the secondary account:

Copy code

```
ALTER FAILOVER GROUP provider_dr_fg PRIMARY;
```

To refresh the failover group from the secondary (before promoting), run:

Copy code

```
ALTER FAILOVER GROUP provider_dr_fg REFRESH;
```

## Operational behavior

Application state lag
:   The `APPLICATION_STATE` view may be stale immediately after a failover while global reconciliation normalizes. Plan accordingly and don’t rely on this view for real-time accuracy during the failover transition.

Failover account freshness
:   Keep the failover account current by refreshing the failover group regularly, so all required published versions are available in the secondary account. If the new primary account is behind consumers on versions, subsequent upgrades can result in a consumer version rollback.

Data integrity during failback
:   Before promoting the original primary account back to active status, ensure the failover group has performed a final refresh from the temporary primary to prevent data loss.

## Migrate from a manual DR workflow

Some providers have set up their own disaster recovery workflows by manually creating failover groups, adding reference databases, and coordinating direct shares. Use the following steps to migrate to the native BCDR capability.

Step 1: Audit current group membership
:   Identify every database, share, and listing in your existing failover and replication groups. Note which objects are in listing auto-fulfillment replication groups versus your manual failover group, and flag any databases that appear in both.

Step 2: Resolve replication and failover group conflicts
:   For any database that appears in both a replication group and a failover group, move it fully into the failover group. The failover group must become the superset, covering all members of the auto-fulfillment replication group. Contact your Snowflake partner contact before executing this step to avoid disrupting active consumers.

Step 3: Remove the manual failover group configuration
:   Once the native BCDR failover group covers all packages, reference databases, shares, and listings, remove the manually created failover group to avoid overlapping group membership.

Step 4: Recreate using native BCDR syntax
:   Create a new failover group using the syntax in [Step 1: Create a failover group](#label-dsna-bcdr-create-failover-group). Include `APPLICATION_PACKAGES` as an object type alongside your databases, shares, and listings.

Step 5: Validate LAF continuity
:   Confirm that listing auto-fulfillment replication is working from both the primary and failover accounts. Use `SHOW LISTINGS IN FAILOVER GROUP` to verify listing visibility, and review `APPLICATION_STATE` in the failover account to confirm consumer instance data is populating.

Step 6: Sunset direct share DR if applicable
:   If you were using direct shares as part of your manual DR workflow, coordinate with your consumers to transition them to the listing-based model. Direct shares and native BCDR failover groups can coexist during the transition.
