Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$VERIFY\_CMK\_INFO

Verifies your customer-managed key (CMK) configuration and returns a message about the registered CMK.

See also:
:   [Understanding CMK self-registration with support activation of Tri-Secret Secure](/user-guide/security-encryption-tss#label-encryption-tss-self-register)

## Syntax

Copy code

```
SYSTEM$VERIFY_CMK_INFO( [ '<ssa_account_name>' ] )
```

## Arguments

**Required:**

None.

**Optional:**

`ssa_account_name`
:   A string that specifies the SSA account name for which you want to verify the CMK configuration.

## Returns

Returns a successful status message or, as shown in the following example outputs, information about the unsuccessful verification:

- **AWS**:

  ```
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                                                                                                                                                                                               SYSTEM$VERIFY_CMK_INFO()                                                                                                                                                                                               |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Verification failed due to an exception with message: Access is denied to the customer managed key (CMK) for this account. This could be because: 1) the CMK access permissions granted to Snowflake have been revoked OR 2) the CMK is disabled OR 3) the CMK is scheduled for deletion OR 4) the CMK specified is wrong. CMK ARN used: arn:aws:kms:us-west-2:736112632311:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59 |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  ```
- **Azure:**:

  ```
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                                                                                                                                                     SYSTEM$VERIFY_CMK_INFO()                                                                                                                                                     |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Verification failed due to an exception with message: Error received from the customer managed key (CMK) provider caused by user: 'Your request cannot be completed because of the failure of an external dependency. Please try again later.'. CMK KEY URI used: https://trisecretsite.vault.azure.net/keys/TriSecretAZKeyWrong |
  +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  ```
- **Google Cloud**:

  ```
  +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                                                                                                                                                                                                                   SYSTEM$VERIFY_CMK_INFO()                                                                                                                                                                                                                    |
  +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Verification failed due to an exception with message: Access is denied to the customer managed key (CMK) for this account. This could be because: 1) the CMK access permissions granted to Snowflake have been revoked OR 2) the CMK is disabled OR 3) the CMK is scheduled for deletion OR 4) the CMK specified is wrong. CMK resource ID used: projects/my-env/locations/us-west2/keyRings/TriSecretTest/cryptoKeys/TriSecretGCPKey                         |
  +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  ```

## Access control requirements

- Only users with the ACCOUNTADMIN role or a with role that is granted the MONITOR SECURITY privilege can call this
  function.
- Only users with the GLOBALORGADMIN role or ORGADMIN role can specify an SSA account name.

## Examples

Verify the status of the CMK for your Snowflake account:

> Copy code
>
> ```
> SELECT SYSTEM$VERIFY_CMK_INFO();
> ```

Verify the status of the CMK for a specific SSA account:

> Copy code
>
> ```
> SELECT SYSTEM$VERIFY_CMK_INFO('AUTO_FULFILLMENT_AREA$PUBLIC_AZURE_EASTUS2');
> ```
