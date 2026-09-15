# Define the referral link for a Marketplace listing

This topic explains how to define the referral link for a listing offered on the Snowflake Marketplace.

Referral links let you send consumers a link directly to your listing on the Snowflake Marketplace. When a consumer accesses
the referral link, they are prompted to either sign in to their existing Snowflake account or sign up for a
Snowflake trial account. In both cases, the consumer is then redirected to your listing in the Snowflake Marketplace.

Note

Referral links are currently not available for private listings.

To define the referral link for a listing on the Snowflake Marketplace, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search for your listing.
4. Note the listing ID in the URL:

   For example, if your listing URL is:

   `https://app.snowflake.com/marketplace/listing/ABC123XYZ789`

   The listing ID is `ABC123XYZ789`
5. Define the referral link by appending the listing ID to the following URL:

   `https://signup.snowflake.com/?listing=`

   For example, the referral link for the earlier example would be:

   `https://signup.snowflake.com/?listing=ABC123XYZ789`

You can share this link with consumers to provide direct access to your listing on the Snowflake Marketplace.
