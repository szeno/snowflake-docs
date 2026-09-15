# Tutorial

## Use case: A provider shares a listing on the internal marketplace. It’s then reshared with a consumer.

In this use case, a provider shares a reshareable listing on the internal marketplace. Consumer A retrieves the listing and then reshares it
with Consumer B.

Note

The steps for resharing listings on the Snowflake Marketplace and for resharing private listings are similar to the steps provided in this use case.

### Step 1. The provider creates a reshareable listing on the internal marketplace

Note

To enable resharing across regions, the provider must enable `change_tracking` on their tables. This can only be done
programmatically using [CREATE TABLE](/sql-reference/sql/create-table) or [ALTER TABLE](/sql-reference/sql/alter-table). For more information, see
[Change tracking not enabled on base tables](/user-guide/dynamic-tables/troubleshoot-creation#label-dynamic-tables-and-change-tracking).

1. Follow the steps for [creating an organization listing](/user-guide/collaboration/listings/organizational/org-listing-create#label-organizational-listing-create-in-snowsight-or-sql) on the internal
   marketplace in Snowsight.

   This use case creates a listing named *Daily revenue reshare*. The listing contains a table named *daily\_revenue\_table*.
2. Review the **Resharing** section in the lower-right corner.

   Listings can be reshared by default.
3. Add Consumer A to the targeting of the listing, and then publish the listing.

   The listing will be discoverable in the organization’s internal marketplace after it’s published.

### Step 2. Consumer A retrieves and reshares the listing

In this example, Consumer A retrieves the shared listing from the internal marketplace and then reshares it with a second-level consumer
(Consumer B).

#### Verify that you can see the listing

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as Consumer A.
2. In the navigation menu, select **Catalog** » **Internal Marketplace**.
3. Verify that the shared listing is available.

   In this use case, the shared listing is named *Daily revenue reshare*.
4. On the **Internal Marketplace** page, select the shared listing, and then copy the listing ULL.

   You’ll include this ULL when you create a view.

   In this use case, the copied ULL is ORGDATACLOUD$INTERNAL$DAILY\_REVENUE\_RESHARE.

#### Create a new view

Create a view in a new or existing database that references objects from the shared listing.

The view references the listing as shown in the following example. Include the listing ULL that you copied earlier. This ULL includes the
listing name, the schema, and the table name. This view becomes the *outgoing* view.

Copy code

```
CREATE SECURE VIEW drt_secure_view
  COMMENT = '<comment>'
  AS SELECT * FROM ORGDATACLOUD$INTERNAL$DAILY_REVENUE_RESHARE.public.daily_revenue_table;
```

The new view is listed in the database’s public views.

#### Reshare the listing with Consumer B

To reshare the listing with Consumer B, follow these steps:

1. In the navigation menu, select **Marketplace** » **Provider Studio**.
2. On the **Listings** page, select **Create listing** » **Specified consumer**.
3. Specify a name for the listing.

   For this example, the listing is named *Resharing Daily Revenue Table*.
4. Select **Add data product**.

   1. Select the secure view you created above.

      In this use case, the secure view is named *DRT\_SECURE\_VIEW*.
   2. To add the data product, select **Done**, and then select **Save**.
5. Continue updating the required listing fields.

   > For this use case, edit the resharing section so that this listing can’t be reshared. This is optional. You can configure a reshared
   > listing so that it can continue to be reshared.
   >
   > Note
   >
   > If you enable auto-fulfillment for a reshared listing that crosses databases, you must specify a warehouse. This can be done in the UI
   > in the listing’s auto-fulfillment settings, or it can be done programmatically by specifying the `warehouse` in the listing
   > manifest’s `auto-fulfillment` property.
6. Publish the listing.

   The listing is now available to the business partner.
7. To see the listings that you’re sharing, follow these steps:

   1. In the navigation menu, select **Data sharing** » **External sharing**.
   2. On the **External sharing** page, select the **Shared by your account** tab.

### Step 3. Consumer B retrieves the reshared listing

In this example, Consumer B retrieves the listing that was reshared in the previous step.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as Consumer B.
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. On the **External sharing** page, select the **Shared with you** tab.
4. Select **Get** to retrieve the listing, and then select **Get** once more to confirm.

   At this point, the reshared listing is ready to use. To test the listing, run the following command:

   Copy code

   ```
   SELECT * FROM resharing_daily_revenue_table.public.drt_secure_view;
   ```
