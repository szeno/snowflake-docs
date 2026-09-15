Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_HASH\_FOR\_APPLICATION

Returns the hash value for a Snowflake Native App or query ID.

## Syntax

Copy code

```
SYSTEM$GET_HASH_FOR_APPLICATION( '<app_name>' [ , '<query_id>' ] )
```

## Arguments

**Required**

`'app_name'`
:   The name of the app whose hash value you want to return.

**Optional:**

`'query_id'`
:   The query ID whose hash value you want to return.

## Returns

Returns a signed 64-bit hash value. If a query ID is passed as
an argument to this function, this function returns the hash value of the query
ID. Otherwise, it returns the hash value for the app.

## Examples

The following example returns the hash value for the app ‘hello\_snowflake\_app’:

Copy code

```
SELECT SYSTEM$GET_HASH_FOR_APPLICATION('hello_snowflake_app');
```

```
+--------------------------------------------------------+
| SYSTEM$GET_HASH_FOR_APPLICATION('HELLO_SNOWFLAKE_APP') |
|--------------------------------------------------------|
| a1b2c3d4e5fg+1234567890+1234
+--------------------------------------------------------+
```

The following example returns the hash value for a query id associated with the app ‘hello\_snowflake\_app’:

Copy code

```
SELECT SYSTEM$GET_HASH_FOR_APPLICATION('hello_snowflake_app', 'abcd1234-12345-WXYZ-0000-0987654321');
```

```
+------------------------------------------------------------------------------------------------+
| SYSTEM$GET_HASH_FOR_APPLICATION('HELLO_SNOWFLAKE_APP', '<app_id>') |
|------------------------------------------------------------------------------------------------|
| a1b2c3d4e5fg+1234567890+1234                                                                   |
+------------------------------------------------------------------------------------------------+
```
