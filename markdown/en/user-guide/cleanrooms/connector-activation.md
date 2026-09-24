# Snowflake Data Clean Rooms: Activation connectors

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Note

Snowflake Data Clean Rooms do not currently support data subject consent management. Customers are responsible for ensuring they have
obtained all necessary rights and consents to use the data linked in their clean rooms. Customers must also ensure compliance with all
applicable laws and regulations when using Data Clean Rooms, including in connection with third-party connectors.

You can use connectors to integrate your clean room environment with what your ecosystem partners provide. This topic describes how the
clean room admin can configure a connector so that clean room users can push the result of an analysis to an activation partner.

If you are a provider who wants to control which connectors show up as options when a clean room user runs an analysis, see
[Customize available connectors](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-admin-customize-connectors).

Important

Third-party connectors are not offered by Snowflake and may be subject to additional terms. These integrations are made available for
your convenience, but you are responsible for any content sent to or received from the integrations.

Customers are responsible for obtaining any necessary consents in connection with their use of Snowflake Data Clean Rooms. Please ensure
that you are complying with applicable laws and regulations when using Snowflake Data Clean Rooms, including in connection with
third-party connectors for activation purposes.

## Google Ads connector

Google Ads is an online advertising platform where advertisers bid to display brief advertisements, service offerings, product listings, or
videos to web users.

Configuration guideUser guide

You must have the MANAGE\_DCR\_CONNECTORS role to configure this connector.

To configure the connector so that your clean room environment is integrated with your Google Ads account:

1. In the left navigation of the clean rooms UI, select **Connectors**.
2. Select the **Activation** tab.
3. Expand **Google Ads**.
4. Enter your Google credentials.
5. In the **Account ID** field, enter the ID associated with your Google Ads account.
6. Specify your API preference. If you select **My Developer Token**, enter your developer token for the Google Ads API.
7. Select **Save**.

See the **user guide** tab to learn how to activate results using this connector.

Here is how to activate analysis results with Google Ads. These instructions assume that this connector has been properly installed
and configured.

To push the results of an analysis to Google Ads for activation:

1. Run an analysis that returns data that can be activated. For example, analyses using the **Audience Overlap & Segmentation**
   template can be activated.

   For more information about running an analysis, see [Run an analysis as a provider](/user-guide/cleanrooms/web-app-working#label-web-app-provider-run) or
   [Run an analysis as a consumer](/user-guide/cleanrooms/web-app-working#label-web-app-working-run-analysis-consumer).
2. In the **Results** section, select **Activate**.
3. In the **Activation Hub** dialog, select **Google Ads**.
4. In the **Account ID** field, enter the identifier for the account where you want to push the segment.
5. In the **Segment Name** field, enter a descriptive name for your results.
6. In the **Description** field, enter a description of the data you are pushing to Google Ads.
7. In the **Activation IDs** section, select the columns that contain hashed email and/or hashed phone identifiers.
8. Select **Push Data**.

## Meta Ads Manager connector

Meta Ads Manager is an ad platform that lets you build targeted campaigns and optimize ad spend.

Configuration guideUser guide

You must have the MANAGE\_DCR\_CONNECTORS role to configure this connector.

To configure the connector so that your clean room environment is integrated with your Meta Ads Manager account:

1. In the left navigation of the clean rooms UI, select **Connectors**.
2. Select the **Activation** tab.
3. Expand **Meta Ads Manager**.
4. Enter your Meta Business Manager credentials.
5. In the **Meta Ads Manager Account ID** field, enter the ID of your Meta Ads Manager account.
6. Select **Save**.

See the **user guide** tab to learn how to activate results using this connector.

These instructions assume that this connector has been properly installed and configured.

To push the results of an analysis to Meta Ads Manager for activation:

1. Run an analysis that returns data that can be activated. For example, analyses using the **Audience Overlap & Segmentation**
   template can be activated.

   For more information about running an analysis, see [Run an analysis as a provider](/user-guide/cleanrooms/web-app-working#label-web-app-provider-run) or
   [Run an analysis as a consumer](/user-guide/cleanrooms/web-app-working#label-web-app-working-run-analysis-consumer).
2. In the **Results** section, select **Activate**.
3. In the **Activation Hub** dialog, select **Meta Ads Manager**.
4. In the **Account ID** field, enter the identifier for the account where you want to push the segment.
5. In the **Segment Name** field, enter a descriptive name for your results.
6. In the **Description** field, enter a description of the data that you are pushing.
7. In the **Activation IDs** section, select the columns that contain identifiers, then select the type of those identifiers.
8. Select **Push Data**.
