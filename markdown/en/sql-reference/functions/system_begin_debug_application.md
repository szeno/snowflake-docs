Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$BEGIN\_DEBUG\_APPLICATION

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Enables [session debug mode](/developer-guide/native-apps/installing-testing-application#label-native-apps-session-debug-mode) for a Snowflake Native App.

## Syntax

Copy code

```
SYSTEM$BEGIN_DEBUG_APPLICATION( '<app_name>' [ , <execution_mode>] )
```

## Arguments

`'app_name'`
:   The name of the app on which session debug mode is being enabled.

`{execution_mode = }`
:   The behavior of commands run during session debug mode. Possible values are:

    - `'AS_APPLICATION'` (DEFAULT)

      All statements are executed as using the same privileges as the app. This mimics the
      behavior of the app in the consumer account.
    - `'AS_SETUP_SCRIPT'`

      All statements are executed using the same privileges as the setup script of the app. This
      allows providers to test the setup script using session debug mode.

## Usage notes

- Providers can use this function to enable session debug mode on an app created using development mode.
  This allows providers to test the behavior of the app and setup script.

## Examples

The following example shows how to set the execution mode to `AS_APPLICATION`:

Copy code

```
SELECT SYSTEM$BEGIN_DEBUG_APPLICATION( 'hello_snowflake_app', execution_mode ='AS_APPLICATION')
```

The following example show how to set the execution mode to *AS\_SETUP\_SCRIPT*:

Copy code

```
SELECT SYSTEM$BEGIN_DEBUG_APPLICATION( 'hello_snowflake_app', execution_mode = 'AS_SETUP_SCRIPT')
```
