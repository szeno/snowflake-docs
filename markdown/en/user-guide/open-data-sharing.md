# Share data with non-Snowflake consumers

[![Greater access to non-Snowflake customers — directly share with non-Snowflake consumers using the IRC endpoint](/static/images/collaboration/open-format-sharing-non-snowflake.png)](/static/images/collaboration/open-format-sharing-non-snowflake.png)

Snowflake Sharing allows you to securely share live, read-only data assets with consumers who do not use Snowflake, eliminating the
need for complex ETL pipelines, data duplication, or manual file exports.

Note

Open Data Sharing supports only Snowflake-managed Iceberg tables, which are Iceberg tables that use Snowflake as the catalog. External
consumers can’t read standard Snowflake tables or externally managed Iceberg tables. For more information, see
[Catalog options](/user-guide/tables-iceberg#label-tables-iceberg-catalog-options).

Each external consumer is bound to a single region, which determines where Snowflake stores and serves the shared data for that
consumer. The region doesn’t restrict where the consumer’s client connects from. For more information, see
[Share with external consumers in other regions](#label-open-data-sharing-regions).

## Why use Snowflake Sharing?

- **Universal access:** Consumers query live data using standard, open-source Iceberg REST Catalog APIs from any analytical tool or
  platform where this protocol is supported.
- **Zero data movement:** Data remains securely in your Snowflake storage layer, ensuring a single source of truth while removing data
  egress costs and storage duplication.
- **Granular control:** Secure data distribution using restricted external consumer identities that authenticate with workload identity
  federation or programmatic access tokens (PATs) that you manage directly.
- **Cross-region access:** When you add `auto_fulfillment` to a listing, Snowflake replicates the shared data to each external
  consumer’s region.

## Secure data sharing with external consumers

The following steps walk through how to share with non-Snowflake customers: create an external consumer and access token, prepare shared
Iceberg table data, create a share and listing, and retrieve the catalog URL for the external consumer.

## Determine your account region

Run the following command to return your account region:

Copy code

```
SELECT CURRENT_REGION();
```

The result is the Snowflake region ID for your account (for example, `AWS_US_WEST_2` or `PUBLIC.AWS_US_WEST_2`).

You can also identify your region from your account URL. If your URL includes a cloud region ID, such as `us-east-2` in
`organization-account.us-east-2.aws.snowflakecomputing.com`, your account is
hosted in that cloud region. For more information, see [Account identifiers](/user-guide/admin-account-identifier).

## Step 1: Use a role with the required privileges

To complete this workflow, use a role that has one of the following:

- The `ACCOUNTADMIN` role, or
- The `CREATE EXTERNAL CONSUMER` privilege granted at the account level, along with the privileges required to create shares, listings, and the database objects you plan to share.

To grant `CREATE EXTERNAL CONSUMER` to a custom role:

Copy code

```
GRANT CREATE EXTERNAL CONSUMER ON ACCOUNT TO ROLE my_role;
```

The following example uses `ACCOUNTADMIN`:

Copy code

```
USE ROLE ACCOUNTADMIN;
```

## Step 2: Create an external consumer

Create an external consumer for the party that will access your shared data outside Snowflake.

Copy code

```
CREATE EXTERNAL CONSUMER test_ext_consumer;

SHOW EXTERNAL CONSUMERS LIKE '%test_ext_consumer%';
```

External consumers are restricted users bound to a specific region at creation time. You can’t grant roles or other standard user
options to external consumers.

To serve the consumer from a region other than your provider account’s region, set the `REGION` property when you create the external
consumer. You can’t change the region after you create the consumer. Snowflake auto-fulfills the listing to that region, which incurs
replication and storage costs. For more information, see [Share with external consumers in other regions](#label-open-data-sharing-regions).

## Step 3: Configure authentication

Configure how the external consumer authenticates to the open-sharing catalog. External consumers can authenticate by using
workload identity federation (WIF) or a programmatic access token (PAT).

WIFPAT

With WIF, the external consumer authenticates by using a token from its identity provider, so you don’t need to create or distribute a
secret. Add a workload identity that matches the consumer’s identity. External consumers support the `AWS`, `AZURE`, `GCP`, and
`OIDC` types. The following examples show AWS and Google Cloud:

For AWS:

Copy code

```
ALTER EXTERNAL CONSUMER test_ext_consumer ADD WORKLOAD IDENTITY test_aws_wif
  TYPE = AWS
  ARN = 'arn:aws:iam::123456789012:role/example-consumer-role';
```

For Google Cloud:

Copy code

```
ALTER EXTERNAL CONSUMER test_ext_consumer ADD WORKLOAD IDENTITY test_gcp_wif
  TYPE = GCP
  SUBJECT = '123456789012345678901';
```

Provide the external consumer with the identity provider type and identity that you registered.

For all identity provider types, the full syntax, and the required privileges, see [Workload identity federation for external consumers](/user-guide/open-data-sharing-workload-identity).

Add a PAT for the external consumer:

Copy code

```
ALTER EXTERNAL CONSUMER test_ext_consumer ADD PAT test_ext_consumer_pat;
```

Important

You must save the PAT secret when Snowflake returns it. You can’t retrieve the secret later.

Provide the PAT secret to the external consumer through a secure channel.

For more information, see [ALTER EXTERNAL CONSUMER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token).

Caution

Network policies are enforced for external consumers in your provider account’s region. Network policies aren’t enforced when an
external consumer accesses a listing in a different region from your provider account. If you rely on network policies to restrict
access, don’t make the listing available to external consumers in other regions.

## Step 4: Create shared data

Create a database, schema, and Iceberg table for the data you want to share. The table must be a Snowflake-managed Iceberg table
(`CATALOG = 'SNOWFLAKE'`). You can store it in Snowflake-managed storage or in your own external volume. The following example uses
Snowflake-managed storage for the simplest demo setup:

Copy code

```
CREATE DATABASE test_db;
CREATE SCHEMA test_db.test_schema;

CREATE ICEBERG TABLE test_db.test_schema.test_table (id INT, val STRING)
  EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'
  CATALOG = 'SNOWFLAKE';

INSERT INTO test_db.test_schema.test_table VALUES (1, 'A'), (2, 'B'), (3, 'C');

SELECT * FROM test_db.test_schema.test_table;
```

### Share data from an external volume (optional)

If you do not use Snowflake-managed storage, you can create an Iceberg table that references an external volume instead. You can skip this
section if you used the Snowflake-managed table above.

First, create an external volume:

Copy code

```
CREATE OR REPLACE EXTERNAL VOLUME exvol
  STORAGE_LOCATIONS = (
    (
      NAME = 'exvol'
      STORAGE_PROVIDER = 'S3'
      STORAGE_BASE_URL = 's3://bucket/basepath'
      STORAGE_AWS_ROLE_ARN = ''
    )
  );
```

Then create an Iceberg table that uses the external volume:

Copy code

```
CREATE ICEBERG TABLE test_db.test_schema.test_table_ex_vol (id INT, val STRING)
  EXTERNAL_VOLUME = exvol
  CATALOG = 'SNOWFLAKE';
```

## Step 5: Create a share and grant privileges

Create a share and grant the required privileges on the database, schema, and table.

Copy code

```
CREATE SHARE test_share;

GRANT USAGE ON DATABASE test_db TO SHARE test_share;
GRANT USAGE ON SCHEMA test_db.test_schema TO SHARE test_share;
GRANT SELECT ON TABLE test_db.test_schema.test_table TO SHARE test_share;
```

## Step 6: Create an external listing

Create an external listing that attaches the share to the external consumer.

Copy code

```
CREATE EXTERNAL LISTING test_listing SHARE test_share AS
$$
title: "test open sharing"
description: "test open sharing"
open_sharing:
  catalog_identifier: "test-open-sharing"
listing_terms:
  type: "OFFLINE"
external_targets:
  access:
    - external_consumers: [TEST_EXT_CONSUMER]
$$;
```

For more information about listing manifest fields, see [Listing manifest reference](/progaccess/listing-manifest-reference).

### Add external consumers to an existing listing

If you already share a listing with Snowflake accounts, you can make the same listing available to open clients. You don’t need to
create a separate share or listing. Use [ALTER LISTING](/sql-reference/sql/alter-listing) to add the `open_sharing` field and add your external
consumers to `external_targets.access`, next to your existing Snowflake targets:

Copy code

```
ALTER LISTING my_listing AS
$$
title: "My listing"
description: "Shared with Snowflake accounts and open clients"
listing_terms:
  type: "OFFLINE"
open_sharing:
  catalog_identifier: "my-listing-catalog"
external_targets:
  access:
    - organization: MYORG
      accounts: [PARTNER_ACCOUNT]
    - external_consumers: [TEST_EXT_CONSUMER]
$$;
```

Keep the following in mind:

- Snowflake consumers continue to see every object in the share. External consumers see only the Snowflake-managed Iceberg tables in
  the share. Other objects, such as standard tables, aren’t visible to external consumers.
- The listing must include the `open_sharing` field to target external consumers. If you add `external_consumers` without
  `open_sharing`, the command fails with
  `external_targets.external_consumers can only be set when the open_sharing section is present in the listing manifest`.
- To add external consumers, the listing must use `external_targets`. You can’t combine `external_targets` with the `targets` field
  in the same manifest. If your listing uses `targets.accounts`, move those accounts to `external_targets.access` as shown in the
  example.
- If any external consumer is in a different region from your provider account, also add `auto_fulfillment`. For more information,
  see [Share with external consumers in other regions](#label-open-data-sharing-regions).

### Share with external consumers in other regions

Each external consumer is bound to one region, which you set when you create the consumer. The region determines where Snowflake
stores and serves the shared data for that consumer. It doesn’t restrict where the consumer’s client connects from: the client can
connect from anywhere.

To share with an external consumer in another region:

1. Create the external consumer with the `REGION` property, in the form `PUBLIC.snowflake_region`:

   Copy code

   ```
   CREATE EXTERNAL CONSUMER eu_consumer REGION = 'PUBLIC.AWS_EU_CENTRAL_1';
   ```

   To check a consumer’s region, run `DESC EXTERNAL CONSUMER eu_consumer` and review the `region` column. If you don’t specify
   `REGION`, the column is empty and the consumer uses your provider account’s region.
2. Add `auto_fulfillment` to the listing manifest so that Snowflake replicates the shared data to the consumer’s region. Without
   it, `CREATE EXTERNAL LISTING` fails with `Autofulfillment must be specified for listing to be available outside current region.`

   Copy code

   ```
   CREATE EXTERNAL LISTING test_listing_multi_region SHARE test_share AS
   $$
   title: "test open sharing"
   description: "test open sharing"
   open_sharing:
     catalog_identifier: "test-open-sharing-multi-region"
   listing_terms:
     type: "OFFLINE"
   external_targets:
     access:
       - external_consumers: [TEST_EXT_CONSUMER, EU_CONSUMER]
   auto_fulfillment:
     refresh_schedule: "10 MINUTE"
     refresh_type: "SUB_DATABASE"
   $$;
   ```

   One listing can include external consumers in different regions. In this example, `TEST_EXT_CONSUMER` uses the provider’s region
   and `EU_CONSUMER` uses `PUBLIC.AWS_EU_CENTRAL_1`. For more information about `refresh_schedule` and `refresh_type`, see
   [auto\_fulfillment](/progaccess/listing-manifest-reference#label-listing-api-manifest-auto-fulfillment).

Note

- Each external consumer supports only one region. To serve the same party in more than one region, create a separate external consumer
  for each region and add each consumer to the listing.
- You can’t change an external consumer’s region after you create it.
- Snowflake auto-fulfills the listing to each external consumer’s region through Cross-Cloud Auto-Fulfillment, which incurs replication
  and storage costs. For more information, see [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).
- When the listing targets external consumers in more than one region, specify the external consumer when you call
  `SYSTEM$GET_LISTING_URL_FOR_EXTERNAL_CONSUMER`. Each region has its own connection URLs. For more information, see
  [Step 8](#label-open-data-sharing-step-8).

#### Supported regions

- **Your provider account’s region:** External consumers in your provider account’s region are supported in commercial (`PUBLIC`)
  regions on AWS, Azure, and Google Cloud.
- **Other regions:** You can set `REGION` to a commercial (`PUBLIC`) region on AWS or Azure. Google Cloud regions aren’t supported
  for `REGION` yet.

US government (`GOV`) regions aren’t supported yet. If you specify an unsupported region, `CREATE EXTERNAL CONSUMER` fails.

Specify `REGION` in the form `PUBLIC.snowflake_region`, where *snowflake\_region* is a Snowflake
region ID such as `AWS_EU_CENTRAL_1` or `AZURE_WESTEUROPE`. To find region IDs, see [Supported cloud regions](/user-guide/intro-regions) or run
[SHOW REGIONS](/sql-reference/sql/show-regions).

## Step 7: Verify the listing

Confirm that the listing was created and review its properties.

Copy code

```
SHOW LISTINGS LIKE 'TEST_LISTING';

DESC LISTING test_listing;
```

## Step 8: Get the connection details for the external consumer

Call [SYSTEM$GET\_LISTING\_URL\_FOR\_EXTERNAL\_CONSUMER](/sql-reference/functions/system_get_listing_url_for_external_consumer) with the
listing name and the external consumer name to retrieve the connection values for that consumer: `catalog`, `catalog_uri`, `scope`,
and `oauth_token_uri`.

Copy code

```
CALL SYSTEM$GET_LISTING_URL_FOR_EXTERNAL_CONSUMER('TEST_LISTING', 'TEST_EXT_CONSUMER');
```

The values depend on the external consumer’s region. For an external consumer in another region, the URLs use a region-specific
open-sharing host instead of your account URL. Run the function once for each external consumer.

Give the external consumer the returned values, along with the PAT secret or workload identity details from
[Step 3](#label-open-data-sharing-step-3). The external consumer uses them to connect with an Iceberg REST Catalog client, as
described in [Connect to an open-sharing catalog](/user-guide/open-data-sharing-connect).

## Limitations

- External consumers can read only Snowflake-managed Iceberg tables (`CATALOG = 'SNOWFLAKE'`). Standard Snowflake tables and
  externally managed Iceberg tables in the share aren’t visible to external consumers.
- External consumers don’t support failover or disaster recovery (DR) yet. For more information about failover in Snowflake, see
  [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).
- Cross-region external consumers support only AWS and Azure commercial (`PUBLIC`) regions. Google Cloud regions are supported only
  for external consumers in your provider account’s region. US government (`GOV`) regions aren’t supported yet. For more information,
  see [Share with external consumers in other regions](#label-open-data-sharing-regions).
- Each external consumer supports only one region, and you can’t change the region after you create the consumer.
- Network policies aren’t enforced for external consumers in a different region from your provider account.
- An external consumer’s region doesn’t restrict where the consumer’s client connects from.
- You can’t drop an external consumer while any listing, published or unpublished, targets it. Remove the consumer from each listing’s
  `external_targets`, or drop the listing, and then drop the consumer. For more information, see
  [DROP EXTERNAL CONSUMER](/sql-reference/sql/drop-external-consumer).

## Listing manifest properties

The example listing uses the following manifest fields:

**title** and **description**

Identify the listing for providers and external consumers.

**listing\_terms**

Specifies how consumers accept terms for the listing. The example uses `OFFLINE`.

**external\_targets.access.external\_consumers**

Lists the external consumer identities that can access the listing.

**open\_sharing.catalog\_identifier**

A unique identifier for the catalog exposed to external consumers via the Iceberg REST Catalog API. This value is used by the consumer when configuring their Iceberg REST Catalog client to connect to the shared data.
