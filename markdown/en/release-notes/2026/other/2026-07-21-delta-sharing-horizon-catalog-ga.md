# Jul 21, 2026: Consuming Delta Shares in Horizon Catalog (*General availability*)

Snowflake builds for interoperability. Horizon Catalog is the metadata hub for your entire data estate, giving
every team a single, unified window into every data asset regardless of where it lives or what format it uses.

Today we expand that commitment. Consuming Delta Shares as a Catalog Linked Database in Horizon Catalog is now
generally available.

This did not come out of nowhere. We founded the Apache Polaris project, the open source catalog engine at the
heart of Horizon Catalog, and continue to invest heavily alongside a growing open source community because the
industry needs a truly open catalog standard. Polaris already supports Delta tables through the Generic Table
Format, making Delta Share support the natural next step.

Delta Sharing built its foundation on the Legacy Delta Table Format. Iceberg Table Format has since become the
modern, industry-agreed open standard, and Horizon Catalog automatically converts every Delta table in a consumed
share to Iceberg, giving your users a consistent, open, queryable experience across your entire data estate. Those
converted tables inherit the full governance capabilities Horizon Catalog applies everywhere: the masking policies,
row access policies, and data controls you enforce on your own tables apply here equally, without exception.

Getting started takes two SQL statements. First, create a Catalog Integration pointing at your Delta Sharing
endpoint. Then create a Catalog Linked Database to bring the share into Horizon Catalog.

Copy code

```
-- Create Catalog Integration
CREATE OR REPLACE CATALOG INTEGRATION UNITY_BEARER_TOKEN_SHARE
  CATALOG_SOURCE = DELTA_SHARING
  TABLE_FORMAT = DELTA
  REST_CONFIG = (
    CATALOG_URI = '<delta_sharing_endpoint_from_credential>'
    CATALOG_NAME = 'shares/<share_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = BEARER
    BEARER_TOKEN = '<bearer_token_from_credential>'
  )
  ENABLED = TRUE;

-- Create Catalog Linked Database
CREATE OR REPLACE DATABASE delta_sharing_cld
  LINKED_CATALOG = (
    CATALOG = UNITY_BEARER_TOKEN_SHARE
    ALLOWED_WRITE_OPERATIONS = 'NONE'
    SYNC_INTERVAL_SECONDS = 30
  );
```

Full documentation is available at
[Configure a catalog integration for Delta Sharing](/user-guide/tables-iceberg-configure-catalog-integration-delta-sharing).

You can also set up, verify, and troubleshoot Delta Sharing catalog integrations with the
[`delta-sharing`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-delta-sharing) CoCo CLI skill.

Consuming Delta Shares in Horizon Catalog is generally available to all customers today. Get started in the
documentation above.
