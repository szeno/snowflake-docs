# Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow - Snowflake Deployments access external domain resources. Snowflake controls access to external domains
using [network rules](/user-guide/network-rules) and
[external access integrations](/developer-guide/external-network-access/creating-using-external-network-access)
to either grant or deny access to specific domains.

This topic describes the process of [creating a network rule](/sql-reference/sql/create-network-rule)
and [creating an external access integration](/sql-reference/sql/create-external-access-integration) to grant access to a specific domain.
In addition, the known domains used by Openflow connectors are provided.

Two possible workflows exist for managing access to external domains:

- [Create a new network rule and external access integration](#label-openflow-create-new-network-rule-grant-domain-access): Create a new network rule that defines a list of allowed domain/port combinations
  and create a new external access integration using the newly created network rule.
- [Alter an existing network rule](#label-openflow-alter-existing-network-rule-grant-domain-access): Alter an existing network rule
  to add a list of allowed domain/port combinations.

## Create a network rule granting access to one or more domains

To create a new network rule that grants access to one or more domain/port combinations,
execute an SQL statement similar to:

Copy code

```
USE ROLE OPENFLOW_ADMIN;
USE DATABASE <openflow_db>;
USE SCHEMA <openflow_schema>;

CREATE NETWORK RULE MY_OPENFLOW_NETWORK_RULE
   TYPE = HOST_PORT
   MODE = EGRESS
   VALUE_LIST = ('<domain>', '<domain>');
```

For example, to allow Snowflake to access `googleads.googleapis.com`, execute the following.

Copy code

```
USE ROLE OPENFLOW_ADMIN;
USE DATABASE <openflow_db>;
USE SCHEMA <openflow_schema>;

CREATE NETWORK RULE GOOGLEADS_OPENFLOW_NETWORK_RULE
   TYPE = HOST_PORT
   MODE = EGRESS
   VALUE_LIST = ('googleads.googleapis.com');
```

For more information, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule).

After the network rule is created, a external access integration has to be created.

To create a new integration, execute an SQL statement similar to:

Copy code

```
USE ROLE OPENFLOW_ADMIN;

CREATE EXTERNAL ACCESS INTEGRATION MY_OPENFLOW_EAI
   ALLOWED_NETWORK_RULES = (MY_OPENFLOW_NETWORK_RULE)
   ENABLED = TRUE
   COMMENT = 'External Access Integration for Openflow connectivity';
```

## Alter an existing network rule granting access to one or more domains

To alter an existing network rule to grant access to one or more domain/port combinations,
execute an SQL statement similar to:

Copy code

```
USE ROLE OPENFLOW_ADMIN;
USE DATABASE <openflow_db>;
USE SCHEMA <openflow_schema>;

ALTER NETWORK RULE GOOGLEADS_OPENFLOW_NETWORK_RULE SET
   VALUE_LIST = ('<existing domain>', '<existing domain>', 'googleads.googleapis.com');
```

For more information, see [ALTER NETWORK RULE](/sql-reference/sql/alter-network-rule).

Note

Use [SHOW NETWORK RULES](/sql-reference/sql/show-network-rules) to list the existing network rules.   
Use [DESCRIBE NETWORK RULE](/sql-reference/sql/desc-network-rule) to describe the properties of a specific network rule.

If the altered network rule is already associated with an external access integration, it will be updated automatically.
If you do not have an external access integration for the altered network rule,
refer to the section above for instructions on creating a new integration.

## Alter an existing external access integration

To add a network rule to an existing external access integration, first check
which network rules the EAI already allows, then add the new rule alongside them:

Copy code

```
USE ROLE OPENFLOW_ADMIN;

ALTER EXTERNAL ACCESS INTEGRATION <eai_name> SET
  ALLOWED_NETWORK_RULES = (<existing_network_rules>, <new_network_rule>);
```

Use  to see which network
rules an EAI already references.

## Next steps

1. Associate an external access integration with your runtime:

   1. Navigate to the Openflow canvas.
   2. Select the **Runtimes** tab.
   3. For the runtime which requires the new external access integration,
      click the [![Vertical more icon](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) menu.
   4. Select **External access integrations**.
   5. Select all required external access integrations from the dropdown list.

        

      Note you may select multiple external access integrations.
   6. Click **Save**.

      Note

      Restarting the runtime is not required and the changes are applied immediately.
2. Deploy a connector in a runtime, for a list of connectors available in Openflow, see [Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors).

## Domains used by Openflow connectors

The following domains are used by Openflow connectors and require network rules to be granted access.

### Amazon Ads

The following domains are used by the Amazon Ads connector.

- `advertising-api.amazon.com`
- `advertising-api-eu.amazon.com`
- `advertising-api-fe.amazon.com`
- `api.amazon.com`
- `api.amazon.co.uk`
- `api.amazon.co.jp`
- Report location.
  For example, `offline-report-storage-eu-west-1-prod.s3.eu-west-1.amazonaws.com` is used to download reports.

The exact report URL location is not always known before creating a report.
Snowflake recommends allow listing all s3 regions:

> - `*.s3.eu-west-[1-3].amazonaws.com`
> - `*.s3.eu-central-[1-2].amazonaws.com`
> - `*.s3.eu-north-1.amazonaws.com`
> - `*.s3.eu-south-[1-2].amazonaws.com`
> - `*.s3.il-central-1.amazonaws.com`

- For advertising-api-fe.amazon.com (Far East / APAC):
  - `*.s3.ap-northeast-[1-3].amazonaws.com`
  - `*.s3.ap-south-[1-2].amazonaws.com`
  - `*.s3.ap-southeast-[1-7].amazonaws.com`
  - `*.s3.ap-east-[1-2].amazonaws.com`
  - `*.s3.me-south-1.amazonaws.com`
  - `*.s3.me-central-1.amazonaws.com`
  - `*.s3.af-south-1.amazonaws.com`

The last domain is obtained from the report URL, which is returned after the report is ready to
fetch. This is an Amazon S3 bucket where the report is stored. Customers will need to specify their
own AWS region, for example, `us-east-1` or `eu-west-1`, and a specific bucket. As it may be not
possible to know the exact region and bucket, Snowflake suggests using wildcards and listing all
possible regions for a given location.

### AWS Secret Manager

The following domains are used by the AWS Secret Manager connector.

- `secretsmanager.us-west-2.amazonaws.com`
- `sts.us-west-2.amazonaws.com`
- `aws.amazon.com`
- `amazonaws.com`

### BigQuery

The following domains are used by the BigQuery connector.

- `bigquery.googleapis.com`
- `bigquerystorage.googleapis.com`
- `oauth2.googleapis.com`

### Box

The following domains are used by the Box connector.

> - `api.box.com`
> - `box.com`

### Confluence

The following domains are used by the Confluence connector.

> - Customer-specific domain name, such as `https://company-name.atlassian.net/`.
> - For OAuth, <https://atlassian.company-name.com/>

### Microsoft Dataverse

The following domains are used by the Dataverse connector.

- Customer-specific domain name, such as `org12345467.crm.dynamics.com`
- For OAuth, `login.microsoftonline.com`

### Google Ads

The following domains are used by the Google Ads connector.

- `googleads.googleapis.com`

### Google Drive

The following domains are used by the Google Drive connector:

- `drive.google.com`
- `www.googleapis.com`
- `oauth2.googleapis.com`
- `www.googleapis.com`

### Google Sheets

The following domains are used by the Google Sheets connector.

- `sheets.googleapis.com`

### Hubspot

The following domains are used by the HubSpot connector.

- `api.hubapi.com`

### Jira Cloud

The following domains are used by the Jira Cloud connector.

- Customer-specific domain name, for example `company-name.atlassian.net`
- `api.atlassian.com`

### Kafka

The following domains are used by the Kafka connector.

- Customer Kafka bootstrap servers and all Kafka brokers

### Kinesis

The following domains are used by the Kinesis connector.

- AWS region dependent. For example:
  for us-west-2:

  - `kinesis.us-west-2.amazonaws.com`
  - `kinesis-fips.us-west-2.api.aws`
  - `kinesis-fips.us-west-2.amazonaws.com`
  - `kinesis.us-west-2.api.aws`
  - `*.control-kinesis.us-west-2.amazonaws.com`
  - `*.control-kinesis.us-west-2.api.aws`
  - `*.data-kinesis.us-west-2.amazonaws.com`
  - `*.data-kinesis.us-west-2.api.aws`
  - `dynamodb.us-west-2.amazonaws.com`

### LinkedIn Ads

The following domains are used by the LinkedIn Ads connector.

- `www.linkedin.com`
- `api.linkedin.com`

### Meta Ads

The following domains are used by the Meta Ads connector.

- `graph.facebook.com`

### MySQL

The following domains are used by the MySQL connector.

- Customer-specific domain and port combination.

### PostgreSQL

The following domains are used by the PostgreSQL connector.

- Customer-specific domain and port combination.

### Salesforce Bulk API

The following domains are used by the Salesforce Bulk API connector.

- Customer-specific domain and port combination.

### SharePoint

The following domains are used by the SharePoint connector.

- Customer-specific domain—for example, `company-domain.sharepoint.com` or an alias that redirects to `company-domain.sharepoint.com`
- `graph.microsoft.com:80`
- `graph.microsoft.com:443`
- `login.microsoftonline.com`
- `*.svc.ms`

### Shopify

The following domains are used by the Shopify connector.

- Customer-specific domain (for example, `<your_store>.myshopify.com`): Shopify Admin GraphQL API.
- `storage.googleapis.com`: Shopify bulk-operation result downloads. When a bulk query completes, Shopify returns a signed Google Cloud Storage URL for the JSONL result file. The connector must be able to reach this host to download the file.

### Slack

The following domains are used by the Slack connector.

- `slack.com`
- `api.slack.com`
- `hooks.slack.com`
- `files.slack.com`
- `wss-primary.slack.com`
- `wss-backup.slack.com`

### SQL Server

The following domains are used by the SQL Server connector.

- Customer-specific domain and port combination.

### Veeva Vault

The following domains are used by the Veeva Vault connector.

- Customer-specific vault hostname.

### Workday

The following domains are used by the Workday connector.

- Customer-specific domain and port combination. For example, `company-domain.tenant.myworkday.com`.

  To obtain the domain, you can use the report URL (base URL is always the same).
