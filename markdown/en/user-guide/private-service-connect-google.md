# Google Cloud Private Service Connect and Snowflake

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

This topic describes concepts and how to configure Google Cloud Private Service Connect to connect your Google Cloud Virtual
Private Cloud (VPC) network subnet to your Snowflake account hosted on Google Cloud without traversing the public Internet.

Note that Google Cloud Private Service Connect is not a service provided by Snowflake. It is a Google service that Snowflake
enables for use with your Snowflake account.

## Overview

Google Cloud [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) provides private connectivity to
Snowflake by ensuring that access to Snowflake is through a private IP address. Snowflake appears as a resource in your network (that is,
customer network), but the traffic flows one-way from your VPC to Snowflake VPC over the Google networking backbone. This setup
significantly simplifies the network configuration while providing secure and private communication.

The following diagram summarizes the Google Cloud Private Service Connect architecture with respect to the customer Google Cloud VPC and
the Snowflake service.

![Architecture overview](/static/images/google-private-service-connect-overview.png)

The Google Compute Engine (that is, a virtual machine) connects to a private, virtual IP address that routes to a forwarding rule (1). The
forwarding rule connects to the service attachment through a private connection (2). The connection is routed through a load balancer (3)
that redirects to Snowflake (4).

### Limitations

- Maximum 10 connections per project.
- Maximum 50 connections per account.
- Some Snowflake system functions for self-service management are not supported. For information, see
  [Current Limitations for Accounts on Google Cloud](/user-guide/intro-cloud-platforms#label-gcp-cloud-unavailable-features).

  For details, see:

  - [Account identifiers](/user-guide/admin-account-identifier)
  - [Connecting to your accounts](/user-guide/organizations-connect)

## Authorize Private Service Connect for your account

This section describes how to authorize Snowflake to accept network traffic over Private Service Connect.

1. Sign in to the Google Cloud account that has access to the project that you plan to authorize. You can use your
   [Google Cloud CLI](https://cloud.google.com/sdk/gcloud) environment to execute the following:

   Copy code

   ```
   gcloud auth login
   ```

   If you want to check the current account, execute the following:

   Copy code

   ```
   gcloud auth list
   ```
2. Use the Google Cloud CLI to create an access token by executing the following command:

   Copy code

   ```
   gcloud auth print-access-token
   ```

   This command generates an access token for your Google Cloud account. By default, the token expires after 1 hour. If you need to
   authorize, verify, or revoke authorization for Private Service Connect after the token expires, you’ll need to repeat this step to
   generate a new token.

   If you have a service account to the Google Cloud project, you can generate a [short-lived access token](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-oauth) instead, but be sure the lifetime of the token is long enough to finish
   these configuration steps.
3. As a Snowflake account administrator (that is, a user with the ACCOUNTADMIN system role), call the
   [SYSTEM$AUTHORIZE\_PRIVATELINK](/sql-reference/functions/system_authorize_privatelink) function to authorize (that is, enable) Private Service Connect for your
   Snowflake account. The syntax of this function for Private Service Connect is:

   Copy code

   ```
   SELECT SYSTEM$AUTHORIZE_PRIVATELINK ( '<gcp_project_id>' , '<access_token>' )
   ```

   Where:

   - `gcp_project_id` is the Google Cloud Project ID from which you plan to create endpoints and connect to Snowflake securely.
   - `access_token` is the access token that you generated in a previous step in this configuration procedure.

   For example:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$AUTHORIZE_PRIVATELINK (
    'my-gcp-project-id',
    'ya29.a0AcM612zT4pJaXdYfwgY8aiMoDE9W_xkqQ20coFTB1TJcImKDPo...'
   );
   ```
4. Call the [SYSTEM$GET\_PRIVATELINK](/sql-reference/functions/system_get_privatelink) function to verify that Private Service Connect was successfully
   authorized for your Snowflake account. Pass in the same arguments that you used to authorize. For example:

   Copy code

   ```
   SELECT SYSTEM$GET_PRIVATELINK(
    'my-gcp-project-id',
    'ya29.a0AcM612zT4pJaXdYfwgY8aiMoDE9W_xkqQ20coFTB1TJcImKDPo...'
   );
   ```

   Snowflake returns `Account is authorized for PrivateLink` if the account is authorized for Private Service Connect.

## Configure your Google Cloud VPC environment

This section covers the Snowflake-specific details for configuring your Google Cloud VPC environment.

Important

Snowflake is not responsible for the configuration of your Google Cloud environment. This procedure shows the basics of using the
Google Cloud CLI, but is not a definitive guide. For example:

- You could use the Google Cloud console to configure your Google Cloud environment instead of the Google Cloud CLI, which would change the
  steps. For example, when using the Google Cloud console, you are creating an endpoint, not a forwarding rule.
- It does not show you how to configure required firewall updates and DNS records.
- It does not show you how to make an endpoint available in other regions (Private Service Connect endpoints are regional resources).
  For more information about making an endpoint available in other regions, see the [Google documentation](https://cloud.google.com/vpc/docs/about-accessing-vpc-hosted-services-endpoints#global-access).

For additional help, contact your internal Google Cloud administrator.

1. As a Snowflake account administrator (that is, a user with the ACCOUNTADMIN system role), open a worksheet and call the
   [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function. You need to save the output for subsequent steps.

   For example:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT key, value FROM TABLE(flatten(input=>parse_json(system$get_privatelink_config())));
   ```
2. Use the Google Cloud CLI to update the
   [gcloud library](https://cloud.google.com/sdk/gcloud/reference/components/update) to the latest version:

   Copy code

   ```
   gcloud components update
   ```
3. [Authenticate](https://cloud.google.com/sdk/gcloud/reference/auth/login) to Google Cloud using the following command:

   Copy code

   ```
   gcloud auth login
   ```
4. In your Google Cloud VPC, set the project [ID](https://cloud.google.com/sdk/gcloud/reference/config/set) in which the forwarding
   rule should reside.

   Copy code

   ```
   gcloud config set project <project_id>
   ```

   To obtain a list of project IDs, execute the following command:

   Copy code

   ```
   gcloud projects list --sort-by=projectId
   ```
5. In your Google Cloud VPC, [create](https://cloud.google.com/sdk/gcloud/reference/compute/addresses/create) a virtual IP address:

   Copy code

   ```
   gcloud compute addresses create <customer_vip_name> \
   --subnet=<subnet_name> \
   --addresses=<customer_vip_address>
   --region=<region>
   ```

   Where:

   - `customer_vip_name` specifies the name of the virtual IP rule (for example, `psc-vip-1`).
   - `subnet_name` specifies the name of the subnet.
   - `customer_vip_address` specifies an IP address to which all private connectivity URLs resolve. Specify an IP address from your
     network or use CIDR notation to specify a range of IP addresses.
   - `region` specifies the cloud region where your Snowflake account is located.

   For example:

   Copy code

   ```
   gcloud compute addresses create psc-vip-1 \
   --subnet=psc-subnet \
   --addresses=192.168.3.3 \
   --region=us-central1
   ```

   Output:

   ```
   Created [https://www.googleapis.com/compute/v1/projects/docstest-123456/regions/us-central1/addresses/psc-vip-1].
   ```
6. Create a [forwarding rule](https://cloud.google.com/sdk/gcloud/reference/compute/forwarding-rules/create) to have your subnet route
   to the Private Service Connect endpoint, and then to the Snowflake service endpoint.

   Copy code

   ```
   gcloud compute forwarding-rules create <name> \
   --region=<region> \
   --network=<network_name> \
   --address=<customer_vip_name> \
   --target-service-attachment=<privatelink-gcp-service-attachment>
   ```

   Where:

   - `name` specifies the name of the forwarding rule.
   - `region` specifies the cloud region where your Snowflake account is located.
   - `network_name` specifies the name of the network for this forwarding rule.
   - `customer_vip_name` specifies the `<name>` value (that is, `psc-vip-1`) of the virtual IP address created in the previous
     step.
   - `privatelink-gcp-service-attachment` specifies the endpoint for the Snowflake service, which you obtained when you executed the
     [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function in an earlier step.

   For example:

   Copy code

   ```
   gcloud compute forwarding-rules create test-psc-rule \
   --region=us-central1 \
   --network=psc-vpc \
   --address=psc-vip-1 \
   --target-service-attachment=projects/us-central1-deployment1-c8cc/regions/us-central1/serviceAttachments/snowflake-us-central1-psc
   ```

   Output:

   ```
   Created [https://www.googleapis.com/compute/projects/mdlearning-293607/regions/us-central1/forwardingRules/test-psc-rule].
   ```
7. Use the following command to verify the forwarding-rule was created
   [successfully](https://cloud.google.com/sdk/gcloud/reference/compute/forwarding-rules/list):

   Copy code

   ```
   gcloud compute forwarding-rules list --regions=<region>
   ```

   Where:

   - `region` is the cloud region where your Snowflake account is located. For example, if your Snowflake account is located in
     the `europe-west2` region, replace `<region>` with `europe-west2`.

   For a complete list of Google Cloud regions and their formatting, see [Viewing a list of available regions](https://cloud.google.com/compute/docs/regions-zones/viewing-regions-zones#viewing_a_list_of_available_regions).
8. Update your DNS settings.

   All requests to Snowflake need to be routed through the Private Service Connect endpoint so that the URLs returned by the
   [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function resolve to the VIP address that you created (`<customer_vip_address>`).

   The values to obtain from the output of SYSTEM$GET\_PRIVATELINK\_CONFIG depend on which Snowflake features you access using private
   connectivity. For a description of the possible values, see [Return values](/sql-reference/functions/system_get_privatelink_config#label-get-privatelink-config-output).

   Note that the values for `regionless-snowsight-privatelink-url` and `snowsight-privatelink-url` allow access to
   Snowsight and the Snowflake Marketplace using private connectivity. However, there is additional configuration if you want to enable
   URL redirects. For information, see [Snowsight & Private Connectivity](/user-guide/ui-snowsight-gs#label-ui-snowsight-gs-private-connectivity).

   Note

   A full explanation of DNS configuration is beyond the scope of this procedure. For example, you can choose to integrate a private DNS
   zone into your environment using [Cloud DNS](https://cloud.google.com/dns/docs/overview). Please consult your internal Google Cloud
   and cloud infrastructure administrators to configure and resolve the URLs in DNS properly.

## Connect to Snowflake

Before connecting to Snowflake, you can optionally leverage SnowCD (Snowflake Connectivity Diagnostic tool) to evaluate the
network connection with Snowflake and Private Service Connect. For more information, see
[SnowCD](/user-guide/snowcd) and [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink).

To connect to Snowflake with your private connectivity account, see [Connecting with a URL](/user-guide/organizations-connect#label-connecting-via-url).

## Revoke authorization

If it’s necessary to disable Private Service Connect in your Snowflake account, call the
[SYSTEM$REVOKE\_PRIVATELINK](/sql-reference/functions/system_revoke_privatelink) function, using the same argument values that you used to authorize the account.
For example:

Copy code

```
SELECT SYSTEM$REVOKE_PRIVATELINK(
 'my-gcp-project-id',
 'ya29.a0AcM612zT4pJaXdYfwgY8aiMoDE9W_xkqQ20coFTB1TJcImKDPo...'
);
```

## Using SSO with Google Private Service Connect

Snowflake supports using SSO with Google Cloud Private Service Connect. For more information, see:

- [SSO with private connectivity](/user-guide/admin-security-fed-auth-overview#label-sso-private-connectivity)
- [Using Snowflake OAuth with PrivateLink and SaaS clients](/user-guide/oauth-snowflake-overview#label-oauth-private-connectivity)

## Using Client Redirect with Google Cloud Private Service Connect

Snowflake supports using Client Redirect with Google Cloud Private Service Connect.

For more information, see [Redirecting client connections](/user-guide/client-redirect).

## Using Replication & Tri-Secret Secure with Private Connectivity

Snowflake supports replicating your data from the source account to the target account, regardless of whether you enable
Tri-Secret Secure or this feature in the target account.

## Blocking public access — *Recommended*

After testing the Google Cloud Private Service Connect connectivity with Snowflake, you can optionally block public access to
Snowflake using network policies. For more information, see [Controlling network traffic with network policies](/user-guide/network-policies).

Configure the CIDR block range to block public access to Snowflake using your organization’s IP address range. This range can be
from within your virtual network.

Once the CIDR Block ranges are set, only IP addresses within the CIDR block range can access Snowflake.

To block public access using a network policy:

1. Create an IPv4 network rule or edit an existing IPv4 network rule to add the CIDR block range for your organization.
2. Create or modify a network policy to use the IPv4 network rule.
3. Activate the network policy for your account.
