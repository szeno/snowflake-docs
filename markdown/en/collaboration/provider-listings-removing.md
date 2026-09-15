# Remove listings as a provider

When you delete a listing, you permanently remove the listing. A deleted listing cannot be recovered
or republished to the Snowflake Marketplace.

You must have MODIFY or OWNERSHIP privileges on a listing to delete a listing.

## About removing listings, remote data, and data access

After a provider deletes a listing, no one can access the listing page. However, the listing might appear in search results until the change propagates throughout the system.

If there are existing consumers, they are immediately notified by email that the listing is being retired. The notification includes the date when listing will become unavailable. That date is based on the type of listing and the date when the provider initiated the removal.

Snowflake Marketplace consumers get to keep access to the listing for a period of time, called a retirement window, between the date when the notification is sent and when the listing becomes inaccessible. This window gives consumers time to plan for the change, reducing their risk of data loss. During the retirement window, consumers still retain access to the listing. The data auto-fulfilled to remote regions for the deleted listing remains in place and available to existing consumers throughout the retirement window.

Note

When a listing is retired, the consumer billing contact is notified by email of the listing retirement.

**Paid listings**

- Paid listings are those that are paid for through Snowflake Marketplace.
- The retirement window for a paid listing always contains one full calendar month, regardless of the number of days in the month.
- Providers can unpublish advance payment listings from the Snowflake Marketplace immediately, but they must fulfill all existing consumer subscription terms for the unpublished listing.
- If you delete a listing on the first day of the month (March 1, for example),
  the retirement window continues through the last day of the month (March 31). The effective date for the removal of the listing is the first day of the next month (April).
- If you delete a listing after first day of the month (March 2, for example),
  the retirement window continues until the first and last day of a complete month pass. The effective date for the removal of the listing is the first day of the next month (May).

**Free and limited trial listings**

- Free listings include listings that are provided at no charge through the marketplace.
  Free listings also include listings that are paid for on a platform outside Snowflake.
- The retirement window for free and limited trial listings is exactly 30 days from the
  date of deletion. For example, let’s say you delete the listing on March 10. The effective date for the removal of the listing is April 9.

When the retirement window closes on the date of removal, the listing is no longer accessible to consumers. If the data was replicated to other regions using Cross-Cloud Auto-Fulfillment, it is removed from those regions on the effective date of removal.

Warning

Deleted listings cannot be recovered.

## Delete a published listing

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the published listing you want to delete.
4. In the top-right corner of the listing page, select the vertical ellipsis ([![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)), and then select **Unpublish** to
   begin the unpublish process.

   A confirmation message displays, reminding you that unpublishing a listing removes the listing from Snowflake Marketplace, but existing
   consumers will continue to have access to the listing.
5. Select **Unpublish** to complete the unpublish process.

   The status at the top of the page changes from **Live** to **Unpublished**. You can select that status to view the listing status summary.
6. After the listing is unpublished, select the vertical ellipsis ([![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)) again, and then select **Initiate removal** to
   begin the listing removal process.
7. Review the **Delete Listing** summary, and then select **Delete** to confirm that you want to delete the listing and complete the removal process.

   Warning

   This removal process cannot be reversed.

   When the listing is removed, the status at the top of the page changes from **Unpublished** to **Pending retirement**.

   Listings that are pending retirement are no longer accessible to new consumers, and existing consumers will lose access after a period of
   about 30 days.

   Select the **Pending retirement** status at the top of the listing page to see the exact date when existing consumers will lose access
   to the listing.
