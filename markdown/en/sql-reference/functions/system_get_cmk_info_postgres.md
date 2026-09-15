Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_CMK\_INFO\_POSTGRES

Returns the status of your customer-managed key (CMK) for use with Snowflake Postgres Tri-Secret Secure. Information is returned only for currently
registered and activated keys.

## Syntax

Copy code

```
SYSTEM$GET_CMK_INFO_POSTGRES()
```

## Returns

Returns a status message indicating the state of your CMK. The output includes the values that you specified when calling
[SYSTEM$REGISTER\_CMK\_INFO\_POSTGRES](/sql-reference/functions/system_register_cmk_info_postgres).

The following messages are possible, using CMKs on Amazon Web Services as a representative example:

- Your CMK is registered, but not yet enabled, to use Snowflake Postgres Tri-Secret Secure:

  ```
  CMK with ARN: arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59
  is pre-registered for Tri-Secret Secure.
  ```
- Your CMK is activated and in use with Snowflake Postgres Tri-Secret Secure:

  ```
  CMK with ARN: arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59
  is activated for Tri-Secret Secure.
  ```
- You have an active CMK, but you just pre-registered a new key:

  ```
  CMK with ARN: arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59
  is activated with Tri-Secret Secure, but
  CMK with ARN: arn:aws:kms:us-west-2:481048248138:key/e08cb6c0-7c09-4f37-8e55-e395a12fe965
  is pre-registered for Tri-Secret Secure.
  ```
- You have an active key, but have not registered any CMK to use Snowflake Postgres Tri-Secret Secure:

  ```
  CMK info has not been pre-registered in this account yet, but
  CMK arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59
  is activated with Tri-Secret Secure.
  ```
- You have not registered any CMK to use Snowflake Postgres Tri-Secret Secure:

  ```
  CMK info has not been pre-registered in this account yet.
  ```

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) or a role that is granted the MONITOR SECURITY privilege on the account
can call this function.

## Examples

Obtain the status CMK for your Snowflake account:

Copy code

```
SELECT SYSTEM$GET_CMK_INFO_POSTGRES();
```
