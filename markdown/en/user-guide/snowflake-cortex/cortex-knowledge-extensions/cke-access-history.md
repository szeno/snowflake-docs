# CKE document access history

To help providers know which documents are being accessed in their [Cortex Knowledge Extensions (CKE)](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview), Snowflake provides the following features:

- CKE access history data in the [LISTING\_ACCESS\_HISTORY view](/sql-reference/data-sharing-usage/listing-access-history) in the [SHARE\_OBJECTS\_ACCESSED array](/sql-reference/data-sharing-usage/listing-access-history#label-share-objects-accessed-array).
- A [SYSTEM$ENCODE\_CKE\_PRIMARY\_KEY](/sql-reference/functions/system_encode_cke_primary_key) system function.
- A [SYSTEM$CKE\_HASH\_FUNCTION](/sql-reference/functions/system_cke_hash_function) system function.

## Prerequisites

Because [primary keys](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) define a unique identifier for each document, you must specify a primary key
for the [Cortex Search Service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) to get the access history.

Note

Modifying the primary key columns of an existing Cortex Search Service invalidates the previous CKE access history.

To interpret the previous CKE access history, save a mapping from the old primary key columns to the new primary key columns.

## Understand document IDs

Document IDs are composed of Cortex Search Service [primary keys](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys). To protect customer data, Snowflake encodes and hashes the primary key columns when tracking the access history. You can map the primary keys to the provided hashed document ID using the following functions:

- [SYSTEM$ENCODE\_CKE\_PRIMARY\_KEY](/sql-reference/functions/system_encode_cke_primary_key) function: Transform and anonymize the primary key from the set of selected columns.
- [SYSTEM$CKE\_HASH\_FUNCTION](/sql-reference/functions/system_cke_hash_function) function: Hash the primary key.

## Example CKE access history in the LISTING\_ACCESS\_HISTORY view

This example performs the following actions:

- Retrieves only CKE access information from the [LISTING\_ACCESS\_HISTORY view](/sql-reference/data-sharing-usage/listing-access-history) view and excludes all other events
- Uses the [SYSTEM$ENCODE\_CKE\_PRIMARY\_KEY](/sql-reference/functions/system_encode_cke_primary_key) function to build an encoded representation of the CKE document’s primary key columns
- Retrieves the hash version and uses the [SYSTEM$CKE\_HASH\_FUNCTION](/sql-reference/functions/system_cke_hash_function) to compute a hashed document ID for every primary key
- Joins the computed hashed IDs and versions to the view to recover the original primary key columns

Step 1. Create a daily access summary table that retrieves only CKE access information.

Copy code

```
CREATE TABLE IF NOT EXISTS cke_document_daily_access AS
SELECT query_date,
       consumer_account_name,
       consumer_name,
       hashed_doc_id,
       hash_version,
       total_access_count
  FROM (
    SELECT query_date,
           consumer_account_name,
           consumer_name,
           flattened.value::string AS hashed_doc_id,
           lah.share_objects_accessed[0]:"hashVersion"::string AS hash_version,
      COUNT(*) AS total_access_count
      FROM snowflake.data_sharing_usage.listing_access_history AS lah,
        LATERAL FLATTEN(
          input => lah.share_objects_accessed[0]:"hashedDocumentIds"
        ) AS flattened
      WHERE lah.share_objects_accessed[0]:"objectDomain" = 'Cortex Search Service'
        AND lah.share_objects_accessed[0]:"hashVersion" IS NOT NULL
      GROUP BY query_date,
               consumer_account_name,
               consumer_name,
               hashed_doc_id,
               hash_version
);
```

Step 2. Create a table to store the encoded primary keys.

Copy code

```
CREATE TABLE IF NOT EXISTS encoded_primary_keys AS
  (
    SELECT pkCol1,
           pkCol2,
           SYSTEM$ENCODE_CKE_PRIMARY_KEY(pkCol1, pkCol2) AS encoded_primary_key
      FROM your_cortex_search_table
  )
```

Step 3. From the table you created in the previous step, prepare hash versions and compute hashed IDs for your primary keys. Then join the
`cke_document_daily_access` table with the hashed primary key view to recover the original primary key columns.

Copy code

```
WITH hash_versions AS
  (
    SELECT DISTINCT hash_version AS hash_version
      FROM cke_document_daily_access
  ),
  hashed_primary_key AS
  (
    SELECT pkCol1,
           pkCol2,
           hash_version,
           SYSTEM$CKE_HASH_FUNCTION(hash_version, encoded_primary_key) AS hashed_doc_id
      FROM encoded_primary_keys
      CROSS JOIN hash_versions
  )
SELECT pk.pkCol1,
       pk.pkCol2,
       a.query_date,
       a.consumer_account_name,
       a.consumer_name,
       a.total_access_count
  FROM cke_document_daily_access AS a
  JOIN hashed_primary_key AS pk
    ON a.hashed_doc_id = pk.hashed_doc_id
    AND a.hash_version = pk.hash_version;
```
