Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ENABLE\_PREVIEW\_ACCESS

Enables access to [open preview](/release-notes/preview-features) features.

See also:

> [SYSTEM$GET\_PREVIEW\_ACCESS\_STATUS](/sql-reference/functions/system_get_preview_access_status), [SYSTEM$DISABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_disable_preview_access)

## Syntax

Copy code

```
SYSTEM$ENABLE_PREVIEW_ACCESS()
```

## Arguments

None.

## Returns

Returns a VARCHAR status message that open preview features have been enabled:

```
+---------------------------------------------------------------+
| SELECT SYSTEM$ENABLE_PREVIEW_ACCESS();                        |
+---------------------------------------------------------------+
| Preview access has been successfully enabled for this account |
+---------------------------------------------------------------+
```

## Access control requirements

- Only account administrators (users with the ACCOUNTADMIN role) can execute this function.

## Usage notes

- This is an all-or-nothing setting that affects all users and all previews within an account.
- SYSTEM$ENABLE\_PREVIEW\_ACCESS only can enable [open preview features](/release-notes/preview-features).

  [Contact Snowflake Support](/user-guide/contacting-support) to enable or re-enable private preview features.
- Snowflake Marketplace products, which are managed separately through [IMPORTED PRIVILEGES](/user-guide/data-exchange-marketplace-privileges),
  are not covered as part of this capability.
- Client-side libraries (such as Snowpark API) are not covered as part of this capability.
- For customers who have not agreed to the Snowflake [Preview Terms of Service](https://www.snowflake.com/legal/preview-terms-of-service/) (“Preview Terms”),
  enabling preview features may not be possible.

  To agree to Preview Terms, contact your account representative or [Snowflake Support](/user-guide/contacting-support) for assistance.

## Examples

Enable preview features:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$ENABLE_PREVIEW_ACCESS();
```
