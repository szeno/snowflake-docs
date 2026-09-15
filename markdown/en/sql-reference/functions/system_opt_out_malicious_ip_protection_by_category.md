Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$OPT\_OUT\_MALICIOUS\_IP\_PROTECTION\_BY\_CATEGORY

Disables [Malicious IP Protection](/user-guide/malicious-ip-protection) for one or more curated IP categories in the current account.
Use this function to allow traffic that would otherwise be blocked based on its category. For example, you can opt out of blocking IP
addresses that are categorized as low-risk and opt out of blocking the addresses for a specific user.

## Syntax

Copy code

```
SYSTEM$OPT_OUT_MALICIOUS_IP_PROTECTION_BY_CATEGORY( '<category>,<category>' [ , '<user_name>' ] )
```

## Arguments

**Required:**

`'category'`
:   A case-insensitive string that identifies the curated IP category you want to opt out.

    Allowed values:

    - `'ANONYMOUS_VPN'`
    - `'ANONYMOUS_PROXIES'`
    - `'MALICIOUS_BEHAVIOR'`
    - `'TOR_EXITS'`
    - `''`

    For definitions of these categories, see [Malicious IP Protection](/user-guide/malicious-ip-protection).

**Optional:**

`'user_name'`
:   A string that specifies the user name to opt out of Malicious IP Protection for the specified category.
    If no user is provided, the opt-out applies to all users in the account.

## Returns

Returns a VARCHAR status message that indicates that Malicious IP Protection was disabled for the specified category
and user, if provided, in the account.

## Access control requirements

Only account administrators, which are users with the ACCOUNTADMIN role, can execute this function.

## Usage notes

- Changes can take time to propagate across the Snowflake control plane.
- Opting out reduces protection for the selected traffic category. Use this function with discretion and review it regularly.
- Each call of this function overwrites results of the previous call.
- To re-enable blocking for all categories, pass in *‘’* as the `category` argument.
- To review blocked connection attempts, query [LOGIN\_HISTORY view](/sql-reference/account-usage/login_history). Find rows with
  `IS_SUCCESS = 'NO'`, `ERROR_CODE = 390422`, and `ERROR_MESSAGE = 'INCOMING_REQUEST_BLOCKED'`. For those rows, review the output in the
  LOGIN\_DETAILS column.

## Examples

Disable protection for all IPs in the `ANONYMOUS_VPN` and `MALICIOUS_BEHAVIOR` categories:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$OPT_OUT_MALICIOUS_IP_PROTECTION_BY_CATEGORY('ANONYMOUS_VPN,MALICIOUS_BEHAVIOR');
```

```
+-------------------------------------------------------------------------------------------------+
| Successfully set malicious IP protection opt-out categories to ANONYMOUS_VPN,MALICIOUS_BEHAVIOR |
+-------------------------------------------------------------------------------------------------+
```

Disable protection for a specific user in the `ANONYMOUS_VPN` category:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$OPT_OUT_MALICIOUS_IP_PROTECTION_BY_CATEGORY('ANONYMOUS_VPN', 'JSMITH');
```

```
+----------------------------------------------------------------------------------------------+
| Successfully set malicious IP protection opt-out categories to ANONYMOUS_VPN for user JSMITH |
+----------------------------------------------------------------------------------------------+
```

Re-enable protection for a specific user:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$OPT_OUT_MALICIOUS_IP_PROTECTION_BY_CATEGORY('', 'JSMITH');
```

```
+---------------------------------------------------------------------------------+
| Successfully cleared malicious IP protection opt-out categories for user JSMITH |
+---------------------------------------------------------------------------------+
```
