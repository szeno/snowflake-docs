# Set up PrivateLink UI access in Openflow - Snowflake Deployments

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic explains how to configure access to the Snowflake Openflow Runtime UI using private connectivity.

Important

This is an optional task. If you will not be accessing the Openflow Runtime UI using public connectivity,
you can skip this task.

There are two tasks to configure access to the Snowflake Openflow Runtime UI using private connectivity:

1. [Determine PrivateLink URLs](#label-openflow-spcs-configure-pr-ui-access-ui)
2. [Configure PrivateLink for Openflow Runtime UI access](#label-openflow-spcs-configure-pr-ui-create-deployment)

## Prerequisites

Before configuring private link for the Openflow Runtime UI, enable PrivateLink for your account as described in [AWS PrivateLink and Snowflake](/user-guide/admin-security-privatelink).

## Determine PrivateLink URLs

1. Using the ACCOUNTADMIN role, call the SYSTEM$GET\_PRIVATELINK\_CONFIG function in your Snowflake account and identify the value for `openflow-privatelink-url`. This is the URL for accessing Openflow UI over PrivateLink in the form:

   - `<org>-<account>.openflow.<shard-id>.privatelink.snowflakecomputing.com`
2. The URL for accessing the Runtime UI in a Snowflake deployment will be in the form:

   - `of--<org>-<account>.spcs.<shard-id>.privatelink.snowflake.app`
3. Create CNAME records in your DNS to resolve these URL values to your VPC endpoint.
4. Confirm that your DNS settings can resolve the value.
5. Confirm that you can connect to Openflow UI using this URL from your browser.
6. Confirm that you can connect to Runtime UI using this URL from your browser.

## Configure PrivateLink for Openflow Runtime UI access

Perform the following steps:

1. Retrieve Snowflake’s VPC endpoint service ID and Openflow PrivateLink URLs:

   1. As a user with the ACCOUNTADMIN role, execute

   Copy code

   ```
   SELECT SYSTEM$GET_PRIVATELINK_CONFIG();
   ```

   1. From the output, identify and save the values for the following keys:

      - `privatelink-vpce-id`
      - `openflow-privatelink-url`
      - `external-telemetry-privatelink-url`
   2. Construct the Runtime URL

      - `of--<org>-<account>.spcs.<shard-id>.privatelink.snowflake.app`
2. Create a VPC endpoint with parameters:

   Note

   If the Snowflake account where you plan to create your Openflow Deployment
   had previously configured PrivateLink for Snowsight,
   use the existing AWS VPC endpoint and add the additional OpenFlow DNS records to your Route 53.

   - Type: `PrivateLink Ready partner services`
   - Service: `privatelink-vpce-id` value obtained in the previous step.
   - VPC: The VPC where your Openflow deployment will be running.
   - Subnets: Select two availability zones and private subnets where your Openflow deployment will run.
3. Set up a Route 53 private hosted zone for Openflow UI with the following parameters:

   - Domain: `privatelink.snowflakecomputing.com`
   - Type: `Private hosted zone`
   - Select the region and VPC where your Openflow deployment will run.
4. Set up a Route 53 private hosted zone for Openflow UI with the following parameters:

   - Domain: `privatelink.snowflakecomputing.com`
   - Type: `Private hosted zone`
   - Select the region and VPC where your Openflow deployment will run.
5. Set up a Route 53 private hosted zone for Runtime UI with the following parameters:

   - Domain: `privatelink.snowflake.app`
   - Type: `Private hosted zone`
   - Select the region and VPC where your Openflow deployment will run.
6. Add two CNAME records for the URLs identified in the first step:

   - For `openflow-privatelink-url`

     - Record name: `openflow-privatelink-url` value obtained in the first step
     - Record type: `CNAME`
     - Value: DNS name of your VPC endpoint
   - For Runtime UI URL

     - Record name: `openflow-runtime-ui-privatelink-url` value obtained in the first step
     - Record type: `CNAME`
     - Value: DNS name of your VPC endpoint

Note

When creating a new Openflow - Snowflake Deployment, ensure the **PrivateLink** option is enabled.

### Next steps

[Create deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment)
