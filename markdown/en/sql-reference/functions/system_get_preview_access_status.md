Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_PREVIEW\_ACCESS\_STATUS

Determine if access to all preview features is enabled or disabled.

See also:

> [SYSTEM$DISABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_disable_preview_access), [SYSTEM$ENABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_enable_preview_access)

## Syntax

Copy code

```
SYSTEM$GET_PREVIEW_ACCESS_STATUS()
```

## Arguments

None.

## Returns

Returns a VARCHAR status message representing whether preview features are enabled or disabled as shown below:

- Enabled:

  ```
  +--------------------------------------------+
  | SYSTEM$GET_PREVIEW_ACCESS_STATUS()         |
  +--------------------------------------------+
  | Preview access is ENABLED for this account |
  +--------------------------------------------+
  ```
- Disabled:

  ```
  +---------------------------------------------+
  | SYSTEM$GET_PREVIEW_ACCESS_STATUS()          |
  |---------------------------------------------|
  | Preview access is DISABLED for this account |
  +---------------------------------------------+
  ```

## Access control requirements

The SYSTEM$GET\_PREVIEW\_ACCESS\_STATUS function can be executed by any user in the account and does not require special privileges.

## Examples

Display the current state of preview features.

Copy code

```
SELECT SYSTEM$GET_PREVIEW_ACCESS_STATUS();
```
