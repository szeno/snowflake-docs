# Manage listing requests as a provider

You might get requests for a listing depending on how you offer your data product:

- You offer a limited trial of a paid listing and consumers request the full data product after a trial.
- You offer a free listing and choose to manually fulfill your data product in remote regions.

## Review and respond to listing requests

To view requests for the data product attached to a listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the **Listings** section, locate the listing for which you want to view requests.
4. Select **Consumer Requests** to view requests from consumers.

   You can review details about the consumer requesting the data product, such as their Snowflake region, company, contact information,
   and a brief message from the consumer.

Depending on the type of listing you offer, take next steps:

| Listing | Next steps |
| --- | --- |
| Free listing with manual fulfillment | To fulfill a consumer request for a free listing in a remote region, manually replicate the listing. See [Manually replicate data to fulfill a listing request](#label-manually-replicate-listing). |
| Limited trial of a paid listing | To fulfill a consumer request for the full data product after evaluating your limited trial, contact the consumer and share a data product with them privately. See [Fulfill a limited trial request for a full data product](#label-limited-trial-fulfillment). |

Expand

Show lessSee more

Email notifications are sent to providers to notify them of requests. In Snowsight, you can view them on the **Requests**
tab in **External sharing** or [Provider Studio](https://app.snowflake.com/#/provider-studio).

## Fulfill a limited trial request for a full data product

When you publish a paid listing, consumers can get the trial and request the full data product.

After a consumer requests the full data product, fulfill their request by following these steps:

1. Optionally contact the consumer to gather more details about their data product request and if relevant, negotiate payment terms.
2. Prepare the data product for the consumer. See [Prepare to offer a limited trial listing](/collaboration/provider-listings-preparing#label-prepare-limited-trial-listing).
3. Fulfill the data product request by publishing a private listing to the consumer. See [Share data or apps with specific consumers using a private listing](/collaboration/provider-listings-creating-publishing#label-listings-create).

## Fulfill a listing request from a remote region

If you cannot use Cross-Cloud Auto-Fulfillment, such as if your data product contains objects other than the [objects supported for auto-fulfillment](/collaboration/provider-understand-auto-fulfillment-objects#label-listings-auto-fulfill-supported-objects),
and a consumer in a remote region wants to get your listing, you must manually replicate the data product to fulfill the consumer request
in that region.

### Manually replicate data to fulfill a listing request

If you offer free listings with manual data product fulfillment, you must manually replicate the data product to other regions when
consumers request your listing.

To manually replicate the data product to other regions, you must do the following:

1. Set up accounts in the regions where you make your listing available. The remote accounts must be part of the same organization as
   the account you published the listing from.
2. Replicate the data product to each account. You do not need to replicate the data to a region until a consumer in that region requests it.

See [Share data securely across regions and cloud platforms](/user-guide/secure-data-sharing-across-regions-platforms) for details on creating accounts in the relevant remote regions and
replicating the data shares used by your listings.

After completing those steps, you can approve listing requests.

### Approve a listing request

To approve and fulfill listing requests, you must use a role that has been granted or inherits the OWNERSHIP or MODIFY privilege on the listing.

To approve a request for a data product by a specific consumer:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the listing for which you want to view requests.
4. For the listing, select **Consumer Requests**.
5. Select the consumer request that you want to fulfill.
6. Sign in to the account in the remote region where the consumer is located.
7. Select the role in that account that has the OWNERSHIP privilege on the share and the shared database objects, or has the necessary
   privileges on the database objects to be able to add them to a share.
8. Choose **Select Data**.
9. If a secure share exists, navigate to the share, and select it. If a share does not exist, navigate to the desired database, and select the
   database objects you want to add to the share.

   Note

   If you do not see a share, it is either already attached to another listing, or has been previously shared with consumers.
10. Select **Associate Selected Data** to associate the share in the remote region to this listing.
11. Select **Done**.
12. Select **Fulfill Request**.

The consumer request for that region shows as approved and subsequent consumers in that region can instantly get your data product.

To approve all requests for a data product in a specific region:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the listing for which you want to view requests.
4. In the message noting that **Data unavailable in some regions**, select **associate shares**.
5. For the **Region**, select the region that you want to fulfill the data product to.
6. For **Configuration**:

   1. Sign in to an account or choose an account that you are already signed in to.
   2. Select the role that owns the data that you want to share.
   3. Select the data objects or secure share that you want to attach to the listing in the remote region. If you choose data objects,
      a secure share is created for you.
   4. Select **Associate Selected Data**.
7. Select **Done**.

The requests for any consumers in that region show as approved.

### Viewing shares in a remote region

If you manually replicated data for a listing in a remote region and want to view the shares attached to the listing, you must sign in to
the remote account you used to attach the share to the listing.
