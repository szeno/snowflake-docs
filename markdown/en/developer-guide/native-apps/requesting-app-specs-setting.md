# Request permission for restricted operations

This topic describes how to configure a Snowflake Native App to use a `SETTING` app
specification to request consumer approval to perform operations that are
otherwise restricted.

## About SETTING app specifications

Some operations are restricted by default in a consumer account. A native app
can’t perform these operations unless the consumer explicitly grants the app
permission to do so.

A `SETTING` app specification lets the app declare that it needs permission to
perform a specific restricted operation and presents the consumer with a clear
approval prompt. When the consumer approves the specification, the app may
perform the requested operation until the consumer declines the specification
or the app removes the request.

## Supported settings

The following settings are available for `SETTING` app specifications:

| Setting name | Permission granted when approved |
| --- | --- |
| `ENABLE_UNLOAD_TO_INTERNAL_STAGES` | Allows the app to copy data to internal stages contained within the application, even when the `PREVENT_UNLOAD_TO_INTERNAL_STAGES` account parameter is enabled on the consumer account. When the consumer declines or drops the specification, the app loses this permission and the account-level restriction applies again. |

Expand

Show lessSee more

## SETTING app specification workflow

1. In the app’s setup script, create the app specification by calling
   [ALTER APPLICATION SET SPECIFICATION](/sql-reference/sql/alter-application-set-app-spec)
   with `TYPE = SETTING`.

   Note

   App specifications require that `manifest_version: 2` be set in
   the manifest file.
2. When the consumer installs or upgrades the app, the setup script creates
   the specification. The consumer can then review and approve or decline the
   request. For more information on how consumers view and approve app
   specifications, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).
3. When the consumer approves the specification, the app may perform the
   requested operation until the consumer declines the specification or the
   app removes the request.
4. If the consumer later declines the specification or the app removes the
   request, the app can no longer perform the previously permitted operation.

## App specification definition for a SETTING

The app specification definition for a `SETTING` specification contains the
following entries:

- `SETTING`: The name of the account-level setting to request, for example
  `ENABLE_UNLOAD_TO_INTERNAL_STAGES`.
- `VALUE`: The value for the setting. Defaults to `'true'` when omitted.
  For boolean settings, only `'true'` is accepted.

The `SETTING` attribute can’t be changed after the app specification is
created. To request a different setting, drop the existing specification and
create a new one.

## Add a SETTING specification to the setup script

To create a `SETTING` app specification, add an
[ALTER APPLICATION SET SPECIFICATION](/sql-reference/sql/alter-application-set-app-spec)
statement to the app’s setup script:

Copy code

```
ALTER APPLICATION SET SPECIFICATION unload_setting_spec
  TYPE = SETTING
  LABEL = 'Write to internal stages'
  DESCRIPTION = 'Allows the app to copy data to internal stages'
  SETTING = ENABLE_UNLOAD_TO_INTERNAL_STAGES;
```

## Determine whether a SETTING request is needed

Before creating a `SETTING` specification, the app can use GET\_PARAMETER
to check the current value of the relevant account-level parameter and determine
whether the request is necessary:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$APPLICATION', 'GET_PARAMETER', 'PREVENT_UNLOAD_TO_INTERNAL_STAGES')::BOOLEAN;
```

This function returns the current value of the parameter (for example,
`TRUE` or `FALSE`). If the parameter indicates that the operation is
already permitted, the app doesn’t need to create a `SETTING` specification.

## Usage notes

- The `SETTING` attribute is immutable. You can’t change the setting name
  on an existing app specification. Drop and recreate the specification to use
  a different setting name.
- For boolean settings, `VALUE` may be omitted (defaults to `'true'`), or
  if specified, must be `'true'`. Passing `'false'` or any other value
  returns an error. For non-boolean settings, `VALUE` is required.
- When a consumer declines a `SETTING` specification or the app removes the
  request, the app can no longer perform the previously permitted operation.

## The system\_description field

`SETTING` specifications include a `system_description` field in the output
of [SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications) and
[DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification). This
field contains Snowflake’s own description of the behavior associated with the
setting.

This is distinct from the `description` field, which contains the text the
provider supplied to explain to the consumer why the app requires this
permission. Both fields are visible to the consumer when reviewing the
specification:

- `description`: The provider’s explanation of why the app needs this
  permission.
- `system_description`: Snowflake’s description of what the setting does.
