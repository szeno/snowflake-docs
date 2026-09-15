# Manage organizational listings

You can alter a listing to add, change, or remove the settings of the organizational listing,
such as the title, ULL, target accounts or roles, auto-fulfillment, and more.

## View available organizational listings

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Internal Marketplace**.
3. Browse the available data products or use the search bar to find a specific listing.

Use [SHOW AVAILABLE LISTINGS](/sql-reference/sql/show-available-listings) to find listings in your organization which are available to
you.

Copy code

```
SHOW AVAILABLE LISTINGS
  IS_ORGANIZATION = TRUE;
```

Use `SHOW LISTINGS` to find listings on which you are granted USAGE, MODIFY, or OWNERSHIP.

Copy code

```
SHOW LISTINGS;
```

## Edit an organizational listing

Note

To avoid overwriting the existing settings of an organizational listing, you must include the existing manifest (`manifest_yaml`) when you make changes.
Use [DESCRIBE LISTING](/sql-reference/sql/desc-listing) to view the current settings.

You can’t change the [Uniform Listing Locator(ULL)](/user-guide/collaboration/listings/organizational/org-listing-configure#label-olisting-im-ull) or remove the data product after the listing has been published.

SnowsightSQL

1. Open the listing:

   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
   2. In the navigation menu, select **Data sharing** » **Internal sharing**.
   3. On the **Listings** tab, select the listing you want to edit.
      - To refine your search, select **Status** and choose a status, such as **Draft** or **Live**.
      - You can sort the result set by any column.
2. Edit the listing:

   1. To edit the listing title, select the title. The **Edit listing title** dialog appears.
   2. To edit other metadata on the listing page, select the **Edit** button near the item you want to change.
   3. To edit the data product information, select the **Data Product** icon. You can change the description of the
      data product or change the table or view selections.

In the following example, the organization target and the locations of an organizational listing named *my-org-listing1* are changed.
The ALTER statement includes the existing listing manifest, captured with the [DESCRIBE LISTING](/sql-reference/sql/desc-listing) command.

Note

You must have the OWNERSHIP privilege or have been granted the MODIFY privilege on the listing to alter it. You can grant modify privileges to other roles using the following command:

Copy code

```
grant modify on data exchange listing <listing_name> to role <role_name>
```

Copy code

```
USE ROLE <organizational_listing_role>;

ALTER LISTING my-org-listing1
AS
$$
title: "My title"
description: "One region, all accounts"
organization_profile: INTERNAL
organization_targets:
  access:
  - account: "<account_name>"
    roles:
    - "<role>"
locations:
  access_regions:
  - name: "PUBLIC.<snowflake_region>"
$$;
```

This example manifest targets all accounts in one Snowflake region.

Copy code

```
title: "My title"
description: "One region, all accounts"
organization_profile: INTERNAL
organization_targets:
  access:
  - account: "<account_name>"
    roles:
    - "<role>"
locations:
  access_regions:
  - name: "PUBLIC.<snowflake_region>"
```

This example manifest targets two accounts, with two roles each, in one Snowflake region.

Copy code

```
title: "My title"
description: "One region, two accounts, four roles"
organization_profile: INTERNAL
organization_targets:
  access:
  - account: "<account_name>"
    roles:
    - "<role>"
    - "<role>"
  - account: "<account_name>"
    roles:
    - "<role>"
    - "<role>"
locations:
  access_regions:
  - name: "PUBLIC.<snowflake_region>"
```

This example manifest targets all accounts in three Snowflake regions.

Copy code

```
title : 'My title'
description: "Three region, all accounts"
organization_profile: INTERNAL
organization_targets:
  access:
  - all_accounts : true
locations:
  access_regions:
  - names:
  "PUBLIC.<snowflake_region>"
  "PUBLIC.<snowflake_region>"
  "PUBLIC.<snowflake_region>"
auto_fulfillment:
  refresh_type: "SUB_DATABASE"
  refresh_schedule: "10 MINUTE"
```

This example manifest targets all accounts in all regions.

Copy code

```
title : "My title"
description: "Three region, all accounts"
organization_profile: INTERNAL
organization_targets:
  access:
  - all_accounts : true
locations:
  access_regions:
  - names: "ALL"
auto_fulfillment:
  refresh_type: "SUB_DATABASE"
  refresh_schedule: "10 MINUTE"
```

For a complete list of all fields and values for an Organization listing see [Organization listing manifest reference](/user-guide/collaboration/listings/organizational/org-listing-manifest-reference).

## Remove a listing from Internal Marketplace

To remove a listing from the Internal Marketplace, you must change its status.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. On the **Listings** tab, select the listing you want to remove from the Internal Marketplace.
4. Select the listing tile to open the listing page.
5. To unpublish the listing, select [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) » **Unpublish**.

Copy code

```
ALTER LISTING <organizational_listing_name> UNPUBLISH;
```

## Delete a listing

You must unpublish a listing before it can be deleted.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. On the **Listings** tab, select the unpublished listing you want to delete.
4. Select the listing tile to open the listing page.
5. To delete a listing, select the ⋮ icon. From the list that appears, select **Delete**.

To delete a listing, run the following command:

Copy code

```
DROP LISTING <organizational_listing_name>;
```
