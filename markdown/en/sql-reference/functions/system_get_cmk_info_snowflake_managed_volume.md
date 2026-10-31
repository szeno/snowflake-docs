Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME

Returns the registration and activation status of your customer-managed key (CMK) for use with Tri-Secret Secure for Snowflake storage for Iceberg tables.

See also:
:   [Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-snowflake-storage-tss)

## Syntax

Copy code

```
SYSTEM$GET_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME()
```

## Arguments

None.

## Returns

Returns a status message indicating the state of your CMK. An account has at most one registered CMK and one active CMK at a time, so
the message is one of the following:

- No CMK is registered or active:

  ```
  CMK info has not been pre-registered in this account yet.
  ```
- A CMK is registered but not yet activated:

  ```
  CMK with <identifier> is pre-registered for Snowflake-managed storage.
  ```
- A CMK is active:

  ```
  CMK with <identifier> is activated for Snowflake-managed storage.
  ```
- A CMK is active and a different CMK is registered for an upcoming key change:

  ```
  CMK with <identifier> is active and another <identifier> is pre-registered for Snowflake-managed storage.
  ```

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Examples

Obtain the status of the CMK for your Snowflake account:

Copy code

```
SELECT SYSTEM$GET_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
```
