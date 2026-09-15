# DEREGISTER\_EXTENSION

Deregisters an extension from the Trust Center.

For more information, see [Using Trust Center extensions](/user-guide/trust-center/trust-center-extensions).

## Syntax

Copy code

```
SNOWFLAKE.TRUST_CENTER.DEREGISTER_EXTENSION(
  '<extension_id>')
```

## Arguments

`'extension_id'`
:   The identifier of the extension.

    To find the identifiers for registered extensions, query the
    [EXTENSIONS view](/sql-reference/trust_center/extensions).

## Returns

Returns a VARCHAR value:

- If deregistration is successful, the VARCHAR value contains the following message:

  ```
  Extension is successfully deregistered.
  ```
- If deregistration fails, the VARCHAR value contains an error message. Deregistration can fail for the following reasons:

  - The specified `extension_id` is invalid.

  The following example shows an error message that is returned for an invalid `extension_id`:

  ```
  Either the extension with given id does not exist or it is already deregistered
  ```

## Examples

The following example deregisters an extension with ID `extension_id`:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.DEREGISTER_EXTENSION(
  'extension_id');
```
