# REGISTER\_EXTENSION

Registers an extension with the Trust Center.

For more information, see [Using Trust Center extensions](/user-guide/trust-center/trust-center-extensions).

## Syntax

Copy code

```
SNOWFLAKE.TRUST_CENTER.REGISTER_EXTENSION(
  '<source_type>',
  '<source>',
  '<extension_name>')
```

## Arguments

`'source_type'`
:   The source type of the extension. Possible values are `LISTING` and
    `APPLICATION PACKAGE`.

`'source'`
:   The listing ID or the name of the application package.

    You can run the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) SQL command to see all of the
    Snowflake Native Apps that are installed in your account, including the extensions. The listing ID
    or application package for an extension is shown in the `source` column in the output.

`'extension_name'`
:   Name of the extension.

    In the output for the SHOW APPLICATIONS SQL command, the extension names are shown in the
    `name` column.

## Returns

Returns a VARCHAR value:

- If registration is successful, the VARCHAR value contains the following message:

  ```
  Extension <name> is successfully registered.
  ```
- If registration fails, the VARCHAR value contains an error message. Registration can fail for the following reasons:

  - The specified `source_type` is invalid.
  - The specified `source` is invalid.
  - The specified `extension_name` is invalid.
  - The combination of the `source_type`, `source`, and `extension_name` is invalid.
  - The `trust_center_integration_role` role in the namespace of the extension isn’t granted to the SNOWFLAKE application.

## Examples

The following example registers an extension that is named `tc_extension` that was installed from the private listing
*GZ13Z1VEWNG*:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.REGISTER_EXTENSION(
  'LISTING',
  'GZ13Z1VEWNG',
  'tc_extension');
```
