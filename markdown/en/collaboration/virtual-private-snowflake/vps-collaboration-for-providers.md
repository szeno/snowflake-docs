# About providing VPS Private Listings

As a provider of VPS private listings on Snowflake, it’s essential to understand how
to efficiently manage and share your data with consumers. This section guides
you through steps to create a private listing, locate and respond to consumer
requests for access, and securely share your data with them. This process not only
ensures that your data remains protected and accessible only to trusted partners
but also streamlines the collaboration experience by leveraging Snowflake’s powerful
sharing capabilities. Whether you’re sharing data with a few trusted organizations
or managing multiple requests, you’ll find the tools and strategies you need to
successfully manage private listings and enhance your data-sharing workflows.

## Enable provisioning of private listings for your consumers

When you are ready to share private listings with a consumer, and you or your
new consumer uses Virtual Private Snowflake (VPS), contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support)
to enable the provider/consumer relationship through private listings
as described in this section.

1. Contact the consumer to collect the consumer’s Organization Name and Account Identifier.
   For details on how to locate this information, see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
2. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and ask for VPS Provider Sharing to be enabled between you
   and your new consumer. Include the following information:
   - Your VPS deployment name and account identifier.
   - The consumer’s account identifiers.

### Create or Manage a VPS Private Listing by using Provider Studio

When you are set up to provide listings, create a private listing for the consumer.
Provider Studio is the web interface that you use to create and otherwise work with
private listing. This section describes how to use it to create a private listing.

Note

Before you create the listing, your data product must already exist.

If you have a direct share that needs to be converted to a listing,
see [Create a new listing](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing).

The organization administrator should have already signed any terms and disclaimers that apply,
as described in [Enable VPS collaboration with other organizations](/collaboration/virtual-private-snowflake/vps-enable-collaboration#label-vps-collab-enable-listings).
If this isn’t done, you won’t be able to create a listing.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. To add a listing, select **Create Listing** » **Specified consumers**.
4. Enter a descriptive title for your listing. It doesn’t have to be a unique title.
5. Review and/or edit the SQL listing name.

   Note

   You can’t change the SQL listing name after the listing is published.
6. Select the **Product type** button, then select **+ Select** to select the objects to attach to the listing.
7. In the **Access type** drop-down, select **Free**.
8. (Optional) If you have multiple provider profiles, select which provider profile to publish this listing as.
   If you don’t select a provider profile, your organization and account name are used.
9. In the **Who can access** section, add the [organization and account names](/user-guide/admin-account-identifier#label-account-name-find) for the consumers that you
   want to share the listing with.
10. Enter a description for your listing.
11. (Optional) Provide data dictionary information for your listing. For more information, see [Set up a data dictionary for your listing](/collaboration/provider-listings-reference#label-listings-data-dictionaries-setup).
12. (Optional) Provide up to six business needs for your listing. For more information, see [Required for public listings. At least 1 business need is required.](/collaboration/provider-listings-reference#label-listing-provider-business-need).
13. (Optional) Provide a sample SQL query or a notebook that demonstrates how to use the data product. For more information, see
    [Attach a notebook to a Snowflake Marketplace listing](/collaboration/provider-listings-creating-publishing#label-listings-attach-notebook-to-listing).
14. Add legal terms for your listing.
15. (Optional) In the **Attributes** section, add custom attributes to your listing. For more information, see [Required for public listings. Define additional attributes that](/collaboration/provider-listings-reference#label-listings-data-product-attributes).
16. Select **Publish** to publish the listing to the selected consumers, or select **Save Draft** to save it as a draft.
    If you exit without saving, a draft is saved automatically.

When you publish the listing to the consumer, the consumer is notified that you have shared the listing with them.

To manage a listing you’ve already shared, you can use either [Private Sharing](https://app.snowflake.com/#/data/shared) or [Provider Studio](https://app.snowflake.com/#/provider-studio).

## Limitations

# Limitations on collaborating with Virtual Private Snowflake (VPS)

The following limitations apply to collaboration support for Virtual Private Snowflake (VPS):

- Listings that use manual fulfillment are not supported.
- Listings that use Snowflake connectors are not supported.

## Finding consumers for private listings

For listings that aren’t publicly visible, attracting a consumer for your data products,
especially those in a VPS environment, typically involves a more direct and targeted approach.

Here are some ways providers might bring a private listing to the attention of potential consumers:

- The provider can directly invite specific customers or partners to access the listing. This is common
  in scenarios where the provider has identified potential customers who would benefit from the data.
- The provider can leverage existing business relationships, networks, or partnerships to offer the
  private listing to trusted entities.
- Some providers use targeted marketing efforts, contacting potential customers to offer webinars or
  private meetings.
- Satisfied customers or partners often refer other businesses or contacts to the provider, who can
  then extend the offer to these new prospects.
- Many providers might offer the private listing as part of a customized proposal for clients, bundling
  it with other services or products tailored to the client’s specific needs.
- For providers who are able to do so, they can create a listing in the public marketplace just
  to advertise the availability of data. Anyone can browse data products available in Snowflake
  Marketplace, if they have access to this website: <https://app.snowflake.com/marketplace>.

In essence, the visibility of the private listing is managed through more controlled and direct
communication, ensuring that only the preferred audience is aware of it. If a VPS user learns of a
listing that’s of interest to them, they can formally request access to
that individual provider’s listing if they can see it. Otherwise, they can contact their account
representative to inquire about listings that meet their needs or request access to them.
