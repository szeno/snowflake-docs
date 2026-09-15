Categories:
:   [System functions](/sql-reference/functions-system) (System information)

# SYSTEM$ENCODE\_CKE\_PRIMARY\_KEY

Takes one or more [primary key](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) columns from a [Cortex Knowledge Extensions (CKE)](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview) document and converts them into an encoded representation.

The encoded primary key is used as an input for further hashing, which anonymizes document identifiers in access history tables. This process helps protect customer data by ensuring that Snowflake stores hashed values derived from the encoded primary key instead of plain-text document IDs.

See also:
:   [SYSTEM$CKE\_HASH\_FUNCTION](/sql-reference/functions/system_cke_hash_function)

## Syntax

Copy code

```
SYSTEM$ENCODE_CKE_PRIMARY_KEY(
  '<pk_column_name>'
  [ , '<additional_pk_column_name>' ]
  [ , '<additional_pk_column_name>' ]
  [ , '<additional_pk_column_name>' ]
  [ , '<additional_pk_column_name>' ]
)
```

## Arguments

**Required:**

`pk_column_name`
:   The primary key column name.

**Optional:**

`additional_pk_column_name`
:   Additional primary key column names.

    You can specify up to four additional primary key column names as separate arguments.

## Returns

Returns a length-encoded string from the combined primary keys. This serves as the unique document ID.

## Examples

The following example returns the encoded primary key for the primary key columns pkCol1 and pkCol2:

Copy code

```
SELECT ["pkCol1", "pkCol2"], SYSTEM$ENCODE_CKE_PRIMARY_KEY('primary_key_col_1' , 'primary_key_col_2') AS encoded_primary_key
  FROM your_cortex_search_service_table;
```
