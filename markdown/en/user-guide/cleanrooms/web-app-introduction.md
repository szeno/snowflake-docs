# Legacy Clean Rooms UI overview

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Note

The DCR UI in Snowsight is now available directly in Snowsight.
The DCR UI is built on top of the Collaboration API and provides native Snowsight integration
and Cortex Code AI assistance. For more information, see
[Data Clean Rooms UI in Snowsight](/user-guide/cleanrooms/collab-ui-overview).

Legacy provider and consumer clean rooms don’t appear in the DCR UI.
The DCR UI only supports Collaboration Data Clean Rooms. For more information about
getting started with the collaboration architecture, see
[Overview of Snowflake Data Clean Rooms](/user-guide/cleanrooms/overview).

The clean rooms UI provides a user interface to create, share, and use a
[Snowflake Data Clean Room](/user-guide/cleanrooms/overview), run queries, and more. The clean rooms UI allows non-technical
business users to collaborate in a secure environment in a browser-based GUI.

## Prerequisites

An administrator must configure the clean room environment and add you as a clean rooms UI user for your Snowflake account.

Customers without externally accessible endpoints (for instance, customers with only PrivateLink connections) cannot use the clean rooms UI.

## Sign in to the clean rooms UI

Note

The following login instructions and link work no matter [where your clean rooms UI is hosted](#label-web-app-hosting). If your
clean rooms UI is hosted in a different region, the login response might return an error, but it will include a link to the proper login
URL for your UI.

After an administrator has added you to the clean room, you can sign in to the UI using the following procedure:

2. Choose or provide the account locator for the account you want to sign in to.
3. Provide your Snowflake account credentials.
4. Do one of the following:
   - **If you’ve set up multi-factor authentication (MFA) before**, enter the one-time code from your authentication app.
   - **If this is your first time signing in**, scan the QR code with an [authentication app](#label-cleanroom-web-app-mfa) to
     enable MFA. Then do the following:
     1. When prompted, enter the one-time code from the app.
     2. Copy the recovery code to a separate location in case the authentication app is unavailable on your device when you sign in.

### Recommended authenticator apps for multi-factor authentication

All clean rooms UI users must log in using multi-factor authentication (MFA). Snowflake recommends using one of the following third-party
authenticator apps:

- Authy
- Google Authenticator
- Auth0 Guardian
- Microsoft Authenticator

Once MFA is enabled, you will be prompted to enter a one-time code from the authenticator app every time you sign in to the clean rooms UI.

## Clean rooms UI hosting locations and IP addresses

Important

Using the clean rooms UI to work with your data in a Snowflake Data Clean Room can result in that data being processed in a
different cloud platform and region than your Snowflake account.

The following table summarizes which cloud platform and region are used to process data for Snowflake accounts in a particular region of
Amazon Web Service (AWS), Microsoft Azure (Azure), and Google Cloud (GCP). It includes the following columns:

- **Snowflake account region**: The cloud region where your Snowflake account is registered.
- **UI gateway region**: The region that hosts the clean rooms UI for your account. Use this address to log into clean rooms UI.
- **Network addresses used by clean rooms UI**: These are the network addresses used by the clean rooms UI to communicate with your
  Snowflake account. If your Snowflake account uses a [network policy](/user-guide/network-policies) to control network traffic, your
  account administrator must explicitly allow traffic from all IP addresses in this column for your row. If your account has no externally
  available endpoints, you can’t use the clean rooms UI in your account.

| Snowflake account region | UI gateway region | Network addresses used by clean rooms UI |
| --- | --- | --- |
| - AWS South America (Sao Paulo) - AWS US East (N. Virginia) - AWS US East (Ohio) - AWS US West (Oregon) - Azure Central US (Iowa) - Azure East US 2 (Virginia) - Azure Mexico Central (Querétaro) - Azure South Central US (Texas) - Azure West US 2 (Washington) - GCP US Central1 (Iowa) - GCP US East4 (N. Virginia) | [AWS US East (N. Virginia)](https://cleanroom.c1.us-east-1.aws.app.snowflake.com/) | 52.7.249.136 34.195.16.248 52.7.210.215 |
| - AWS Canada (Central) - Azure Canada Central (Toronto) | [AWS Canada (Central)](https://cleanroom.c1.ca-central-1.aws.app.snowflake.com/) | 15.223.145.218 3.96.6.109 15.222.142.44 |
| - AWS Europe (London) - AWS EU (Ireland) - AWS EU (Frankfurt) - AWS EU (Paris) - AWS EU (Stockholm) - AWS EU (Zurich) - AWS Africa (Cape Town) - Azure North Europe (Ireland) - Azure Sweden Central (Gavie) - Azure Switzerland North (Zurich) - Azure UAE North (Dubai) - Azure UK South (London) - Azure West Europe (Netherlands) - GCP Middle East Central2 (Dammam) - GCP Europe West (Frankfurt) - GCP Europe West2 (London) - GCP Europe West4 (Netherlands) | [AWS EU (Frankfurt)](https://cleanroom.c1.eu-central-1.aws.app.snowflake.com/) | 54.93.86.99 3.126.238.8 3.127.143.168 |
| - AWS Asia Pacific (Mumbai) - Azure Central India (Pune) | [AWS Asia Pacific (Mumbai)](https://cleanroom.c1.ap-south-1.aws.app.snowflake.com/) | 35.154.94.29 13.235.168.249 15.206.48.175 |
| - AWS Asia Pacific (Singapore) - AWS Asia Pacific (Tokyo) - AWS Asia Pacific (Osaka) - AWS Asia Pacific (Seoul) - AWS Asia Pacific (Jakarta) - Azure Southeast Asia (Singapore) - Azure Japan East (Tokyo) - Azure Korea Central (Seoul) | [AWS Asia Pacific (Singapore)](https://cleanroom.c1.ap-southeast-1.aws.app.snowflake.com/) | 13.228.90.174 52.220.42.130 52.220.249.16 |
| - AWS Asia Pacific (Sydney) - Azure Australia East (New South Wales) | [AWS Asia Pacific (Sydney)](https://cleanroom.c1.ap-southeast-2.aws.app.snowflake.com/) | 52.65.205.236 52.62.198.227 3.104.160.96 |

Expand

Show lessSee more

## Learning Resources

After you sign in to the UI, see [Run an analysis in the UI](/user-guide/cleanrooms/v1/web-app-working) for information about
creating, sharing, and using a clean room. You can also use the **Help Center** in the clean room environment to guide you.

You can also complete a [tutorial](/user-guide/cleanrooms/v1/tutorials/cleanroom-web-app-tutorial) for help with getting started.
