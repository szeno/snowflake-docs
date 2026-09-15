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
- Resharers can only reshare tables, dynamic tables, and views from the incoming data products allowed for resharing.
- Reshared listings don’t support disaster recovery.

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

1. Sign in to Snowsight and select **Data** » **Databases**.
2. In **Database Explorer**, locate the imported database.
3. Hover over the database name to open its details card.
4. On the **Details** tab, confirm that **Reshare** is set to **Allowed**.

## Cross-region resharing

Note

Be sure that you understand [auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment) before you enable
auto-fulfillment for your reshared listings. Snowflake also provides several views to monitor auto-fulfillment costs and usage. For more
information, see [Monitor resources and view costs](/collaboration/provider-listings-auto-fulfillment-monitor-view-costs).

To reshare data to consumers in other regions, listing auto-fulfillment must be enabled. The `auto-fulfillment` property
includes a `warehouse` field that you must specify when resharing across regions. This field can be omitted when resharing within the
same region.

Resharing data cross-region requires a local copy of the data for further replication downstream. Snowflake automatically creates dynamic
tables to manage this. The warehouse you specify is used to create and refresh these dynamic tables.

Copy code

```
auto_fulfillment:
  warehouse: my_wh
```

You can use the [SYSTEM$SHOW\_DYNAMIC\_TABLES\_CREATED\_FOR\_RESHARING](/sql-reference/functions/system_show_dynamic_tables_created_for_resharing) system function to view the dynamic tables created for
resharing.

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
