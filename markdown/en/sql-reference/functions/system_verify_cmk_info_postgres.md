Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$VERIFY\_CMK\_INFO\_POSTGRES

Verifies your customer-managed key (CMK) configuration for Snowflake Postgres Tri-Secret Secure and returns a message about the registered CMK.

## Syntax

Copy code

```
SYSTEM$VERIFY_CMK_INFO_POSTGRES()
```

## Returns

Returns a successful status message or information about the unsuccessful verification:

- **AWS**:

  ```
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                                                                                                                                                                                               SYSTEM$VERIFY_CMK_INFO_POSTGRES()                                                                                                                                                                                               |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Verification failed due to an exception with message: Access is denied to the customer managed key (CMK) for this account. This could be because: 1) the CMK access permissions granted to Snowflake have been revoked OR 2) the CMK is disabled OR 3) the CMK is scheduled for deletion OR 4) the CMK specified is wrong. CMK ARN used: arn:aws:kms:us-west-2:736112632311:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59 |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  ```
- **Azure:**:

  ```
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                                                                                                                                                     SYSTEM$VERIFY_CMK_INFO_POSTGRES()                                                                                                                                                     |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Verification failed due to an exception with message: Error received from the customer managed key (CMK) provider caused by user: 'Your request cannot be completed because of the failure of an external dependency. Please try again later.'. CMK KEY URI used: https://trisecretsite.vault.azure.net/keys/TriSecretAZKeyWrong |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  ```

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) or a role that is granted the MONITOR SECURITY privilege on the account
can call this function.

## Examples

Obtain the status of the CMK for your Snowflake account:

> Copy code
>
> ```
> SELECT SYSTEM$VERIFY_CMK_INFO_POSTGRES();
> ```
