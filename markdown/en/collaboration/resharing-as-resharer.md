# Reshare incoming data as a resharer

As a resharer, you can take data from a provider’s listing and share it with other accounts, either in its original state or transformed
with your own data. This topic describes how to reshare incoming data.

## Prerequisites

- The provider’s listing must have `resharing.enabled` set to `true`.
- You must create secure views in your own database. You can’t modify the imported database directly.
- The same role must create the share and grant it to the listing.

## Limitations

- Resharing of apps is not supported.
- You can’t attach data objects from imported databases or Uniform Listing Locators (ULLs) directly to another share. To reshare data
  objects from an incoming listing, you must create a secure view in your database.
- Resharers can reshare tables, dynamic tables, and views from incoming data products allowed for resharing by creating a secure view.
  UDFs and UDTFs can be reshared only from a `CALLER`-mode listing. For the full comparison, see
  [Objects supported for sharing and resharing](/collaboration/resharing-as-provider#objects-supported-for-sharing-and-resharing).
- Reshared listings don’t support disaster recovery.
- If the provider’s listing uses `reshare_policy_enforcement: CALLER`, the listing must be from the same Snowflake organization. You can
  create secure views that reference provider data either via the listing’s ULL or via a mounted imported database:

  Copy code

  ```
  -- Option 1: reference via ULL
  CREATE SECURE VIEW my_db.public.my_view
    AS SELECT * FROM ORGDATACLOUD$INTERNAL$MY_LISTING.schema.table;

  -- Option 2: reference via mounted imported database
  CREATE SECURE VIEW my_db.public.my_view
    AS SELECT * FROM imported_db.schema.table;
  ```
- If the provider’s listing uses `reshare_policy_enforcement: CALLER`, your reshared listing must also use
  `reshare_policy_enforcement: CALLER`. You cannot switch to `RESHARER` mode when resharing data from a CALLER-mode provider.

Note

To reshare UDFs or UDTFs from a provider’s data product, the provider’s listing must have `reshare_policy_enforcement` set to `CALLER`.
Resharing UDFs and UDTFs is not supported when the provider uses `RESHARER` mode.

## Resharing workflow

1. Create an imported database from the provider’s listing.
2. Verify that the imported database allows resharing. For details, see [Verify that an imported database allows resharing](#verify-that-an-imported-database-allows-resharing).
3. Create a secure view in your own database that references data from the imported database.
4. Create a share and grant SELECT on the secure view to the share.
5. Create a new listing using the share.

Copy code

```
CREATE DATABASE imported_db FROM LISTING provider_listing;
CREATE DATABASE reshared_db;
CREATE SECURE VIEW reshared_db.public.reshared_view
  AS SELECT * FROM imported_db.public.provider_table;

CREATE SHARE my_reshare;
GRANT USAGE ON DATABASE reshared_db TO SHARE my_reshare;
GRANT USAGE ON SCHEMA reshared_db.public TO SHARE my_reshare;
GRANT SELECT ON VIEW reshared_db.public.reshared_view TO SHARE my_reshare;
```

Note

A REFERENCE\_USAGE grant isn’t required on imported databases created from reshared listings.

## Verify that an imported database allows resharing

Before you reshare, confirm that the imported database is enabled for resharing. You can check this using SQL or Snowsight.

### Using SQL

Run [SHOW DATABASES](/sql-reference/sql/show-databases) and inspect the `resharing_settings` column for the imported database:

Copy code

```
SHOW DATABASES LIKE '<imported_db_name>';
```

When resharing is enabled, `resharing_settings` contains a JSON object similar to the following:

Copy code

```
{
  "enabled": true,
  "only_within_organization": false
}
```

Resharing is allowed when `enabled` is `true`. If `enabled` is `false`, work with the provider to enable resharing on the listing. For
local (non-imported) databases, `resharing_settings` is NULL.

### Using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**.
3. In the Horizon Catalog Explorer, locate the imported database.
4. Hover over the database name to open its details card.
5. On the **Details** tab, confirm that **Reshare** is set to **Allowed**.

## Cross-region resharing

Note

Be sure that you understand [auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment) before you enable
auto-fulfillment for your reshared listings. Snowflake also provides several views to monitor auto-fulfillment costs and usage. For more
information, see [Monitor resources and view costs](/collaboration/provider-listings-auto-fulfillment-monitor-view-costs).

To reshare data to consumers in other regions, listing auto-fulfillment must be enabled. The `auto-fulfillment` property
includes a `warehouse` field that you must specify when resharing across regions. This field can be omitted when resharing within the
same region.

Resharing data cross-region requires a local copy of the data for further replication downstream. Snowflake creates hidden dynamic tables
to manage this copy only for resharing in `RESHARER` mode. The warehouse you specify is used to create and refresh the dynamic tables.

Copy code

```
auto_fulfillment:
  warehouse: my_wh
```

You can use the [SYSTEM$SHOW\_DYNAMIC\_TABLES\_CREATED\_FOR\_RESHARING](/sql-reference/functions/system_show_dynamic_tables_created_for_resharing) system function to view the dynamic tables created for
resharing. To see whether auto-fulfillment has replicated the listing to a target region, and to view refresh errors, see
[Check whether auto-fulfillment reached a region](#label-resharing-refresh-history).

In `RESHARER` mode, Snowflake creates the hidden dynamic tables automatically for each reshared view granted to the share, including views
that you add to the share later. You don’t need to create them yourself.

### Privileges required for cross-region resharing

In `RESHARER` mode, Snowflake creates the hidden dynamic tables by running tasks using the role that owns the secure view in your share.
The view owner role must have both of the following privileges on the account:

- EXECUTE TASK
- EXECUTE MANAGED TASK

Both privileges are required. If the role is missing either one, Snowflake can’t create the hidden dynamic tables, and the listing isn’t
fulfilled to remote regions. For more information about these privileges, see [Task security](/user-guide/tasks-intro#label-task-security-reqs).

The following example grants both privileges to the role that owns the secure view. Run these statements with the ACCOUNTADMIN role:

Copy code

```
GRANT EXECUTE TASK ON ACCOUNT TO ROLE my_view_owner_role;
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE my_view_owner_role;
```

Alternatively, transfer ownership of the secure view to a role that already has both privileges.

If Snowflake couldn’t create the hidden dynamic tables initially because of missing privileges, it retries automatically after you grant
the privileges. You don’t need to recreate the secure view, the share, or the listing.

### How data is materialized in RESHARER mode

When the provider’s listing uses the default `RESHARER` enforcement mode, the hidden dynamic tables materialize the provider’s data as your
account sees it. Context functions such as [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) in the provider’s secure views or
governance policies resolve in your account’s context, not in the context of your consumers. As a result, consumers in remote regions see
the rows that your account can see.

If the provider needs each downstream consumer to see only the rows that the consumer is entitled to, the provider must use
`reshare_policy_enforcement: CALLER`. For more information, see
[Configuring policy enforcement mode](/collaboration/resharing-as-provider#label-resharing-policy-enforcement-mode).

### Cross-region resharing in CALLER mode

When the provider’s listing uses `reshare_policy_enforcement: CALLER`, Snowflake doesn’t create hidden dynamic tables in your account.
Instead, the provider’s data must be available in the remote region so that the provider’s policies can be evaluated in the context of
whoever queries the reshared data.

To make the provider’s data available in the remote region, Snowflake replicates the provider’s listing to that region by using
Cross-Cloud Auto-Fulfillment. This replication is in addition to the auto-fulfillment of your reshared listing.

## Enabling further resharing by your consumers

If you want your consumers to further reshare the listing you created, enable resharing on your own listing by setting
`resharing.enabled` to `true`. For details on configuring this as a provider, see
[Using resharing as a provider](/collaboration/resharing-as-provider).

## Troubleshooting

If consumers receive the error “The listing has resharing restrictions that prevent access to the underlying data,” work with the
provider to resolve the issue. This error can occur when:

- The provider disables resharing by setting `enabled` to `false`.
- The provider adds or changes [governance policies](/collaboration/resharing-as-provider#label-resharing-supported-governance-policies) or [context functions](/collaboration/resharing-as-provider#label-resharing-supported-context-functions) on the base tables that aren’t compatible with resharing.

To confirm whether resharing is currently enabled for the imported database, check the `resharing_settings` column in the output of
SHOW DATABASES, or in Snowsight verify that **Reshare** is **Allowed**. For detailed steps, see
[Verify that an imported database allows resharing](#verify-that-an-imported-database-allows-resharing).

### Consumers in a remote region can’t query a reshared view

If you reshare across regions and consumers in the remote region can’t query a reshared view, check whether Snowflake has created the
hidden dynamic tables for that view:

Copy code

```
SELECT SYSTEM$SHOW_DYNAMIC_TABLES_CREATED_FOR_RESHARING('my_db.my_schema.my_view');
```

- If no dynamic tables are returned, confirm that the role that owns the secure view has both the EXECUTE TASK and EXECUTE MANAGED TASK
  privileges. For details, see [Privileges required for cross-region resharing](#label-resharing-cross-region-privileges).
- If the dynamic tables exist, confirm that auto-fulfillment replicated the listing to the consumer’s region. For details, see
  [Check whether auto-fulfillment reached a region](#label-resharing-refresh-history). To start a refresh immediately, run
  [SYSTEM$TRIGGER\_LISTING\_REFRESH](/sql-reference/functions/system_trigger_listing_refresh):

  Copy code

  ```
  SELECT SYSTEM$TRIGGER_LISTING_REFRESH('LISTING', 'my_reshared_listing');
  ```

### Check whether auto-fulfillment reached a region

Call [LISTING\_REFRESH\_HISTORY](/sql-reference/functions/listing_refresh_history) on your reshared listing to see whether auto-fulfillment
replicated the data to a target region, and to see refresh errors. The function returns the past 14 days of refresh history for a listing
in your account. You need any privilege on the listing.

The following example returns the refresh history for one target region. Omit `SNOWFLAKE_REGION` to return every target region.

Copy code

```
SELECT *
  FROM TABLE(INFORMATION_SCHEMA.LISTING_REFRESH_HISTORY(
    LISTING_NAME => 'my_reshared_listing',
    SNOWFLAKE_REGION => 'AWS_US_EAST_1'));
```

Use these columns to tell whether replication finished:

- `PHASE_NAME` is `COMPLETED` and `ERROR` is null: the refresh finished for that region, and the data is replicated there.
- `ERROR` contains `errorCode` and `errorMessage`: the refresh failed. Those fields describe the failure.
- `PHASE_NAME` is still an in-progress phase, such as `PRIMARY_UPLOADING_DATA` or `SECONDARY_DOWNLOADING_DATA`: auto-fulfillment hasn’t
  finished for that region yet. `END_TIME` is also null while a phase is in progress.

For the full list of phases, see the [usage notes](/sql-reference/functions/listing_refresh_history#label-listing-refresh-history-function-usage-notes).

If the latest refresh failed or is still in progress, you can start a new refresh with
[SYSTEM$TRIGGER\_LISTING\_REFRESH](/sql-reference/functions/system_trigger_listing_refresh). Snowflake also sends a daily email that
summarizes failed listing refreshes to the email address specified on the listing. For more information, see
[How do I find out if an auto-fulfillment refresh fails?](/collaboration/provider-listings-auto-fulfillment#label-auto-fulfillment-faqs).
