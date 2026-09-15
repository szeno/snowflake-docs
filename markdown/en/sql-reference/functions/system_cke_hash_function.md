Categories:
:   [System functions](/sql-reference/functions-system) (System information)

# SYSTEM$CKE\_HASH\_FUNCTION

Analyzes [Cortex Knowledge Extensions (CKE)](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview) usage by mapping `hashedDocumentIds` back to your original document primary keys in the Cortex Search Service. This is required because Snowflake shares only hashed IDs for privacy.

This function returns the hashed document identifier, which maps to the HASHED\_DOC\_ID in the [LISTING\_ACCESS\_HISTORY view](/sql-reference/data-sharing-usage/listing-access-history).

See also:
:   [SYSTEM$ENCODE\_CKE\_PRIMARY\_KEY](/sql-reference/functions/system_encode_cke_primary_key)

## Syntax

Copy code

```
SYSTEM$CKE_HASH_FUNCTION( '<hash_version>', '<encoded_primary_key>' )
```

## Arguments

`hash_version`
:   The version of the hash function used, provided in the [LISTING\_ACCESS\_HISTORY view](/sql-reference/data-sharing-usage/listing-access-history) view.

`encoded_primary_key`
:   The encoded primary keys returned when you call the [SYSTEM$ENCODE\_CKE\_PRIMARY\_KEY](/sql-reference/functions/system_encode_cke_primary_key) function.

## Returns

Returns the hashed encoded primary keys specified by the hash version.

## Examples

The following example retrieves the hash version and uses the SYSTEM$CKE\_HASH\_FUNCTION to compute a hashed document ID for every primary
key. In the following example, `cke_document_daily_access` is a view created from the [LISTING\_ACCESS\_HISTORY view](/sql-reference/data-sharing-usage/listing-access-history):

Copy code

```
WITH
  encoded_primary_keys AS
  (
    SELECT pkCol1,
          pkCol2,
          SYSTEM$ENCODE_CKE_PRIMARY_KEY(pkCol1, pkCol2) AS encoded_primary_key
      FROM your_cortex_search_table
  )
,
  hash_versions AS
  (
    SELECT DISTINCT(hash_version) AS hash_version
      FROM cke_document_daily_access
  )
SELECT pkCol1,
      pkCol2,
      hash_version,
      SYSTEM$CKE_HASH_FUNCTION(hash_version, encoded_primary_key) AS hashed_doc_id
  FROM encoded_primary_keys
  CROSS JOIN hash_versions;
```
