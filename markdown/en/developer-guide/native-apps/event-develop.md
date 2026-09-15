# Determine information about event sharing in the consumer account

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how a provider can set up an app to determine if a consumer has enabled
event sharing in their account.

## Verify event definitions by using system functions

To determine if event sharing is enabled in a consumer account, providers can call the following
system functions within the setup script:

- SYSTEM$IS\_APPLICATION\_AUTHORIZED\_FOR\_TELEMETRY\_EVENT\_SHARING()

  Returns TRUE if the AUTHORIZE\_TELEMETRY\_EVENT\_SHARING property is set, which indicates that
  event sharing is allowed in the consumer account. Otherwise, this system function returns FALSE.
- SYSTEM$IS\_APPLICATION\_ALL\_MANDATORY\_TELEMETRY\_EVENT\_DEFINITIONS\_ENABLED()

  Returns TRUE if all required event definitions have been enabled in the consumer account.
  Otherwise, this system function returns FALSE.

The following example shows a stored procedure that performs a calculation only if both
IS\_APPLICATION\_AUTHORIZED\_FOR\_TELEMETRY\_EVENT\_SHARING and
IS\_APPLICATION\_ALL\_MANDATORY\_TELEMETRY\_EVENT\_DEFINITIONS\_ENABLED are set to TRUE.

Copy code

```
CREATE OR ALTER VERSIONED SCHEMA app_schema;
CREATE OR REPLACE PROCEDURE app_schema.sum(num1 float, num2 float)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS $$
    BEGIN
      IF (SYSTEM$IS_APPLICATION_AUTHORIZED_FOR_TELEMETRY_EVENT_SHARING() and SYSTEM$IS_APPLICATION_ALL_MANDATORY_TELEMETRY_EVENT_DEFINITIONS_ENABLED()) THEN
        RETURN num1 + num2;
      ELSE
        -- notify consumers that they need to enable event sharing
        RETURN 'Sorry you can\'t access the API, please enable event sharing.';
      END IF;
    END;
$$;
```

## Verify event definitions by using the Permissions SDK

The Python Permission SDK provides the following functions to determine if even sharing is enabled
in a consumer account:

- `is_application_authorized_for_telemetry_event_sharing()`

  Returns `true` if the AUTHORIZE\_TELEMETRY\_EVENT\_SHARING property is `true`. Returns `false`, otherwise.

  See [is\_application\_authorized\_for\_telemetry\_event\_sharing()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-is-application-authorized-for-telemetry-event-sharing) for more information.
- `is_application_all_mandatory_telemetry_event_definitions_enabled()`

  Returns `true` if all mandatory event definitions have been enabled in the consumer account.

  See [is\_application\_all\_mandatory\_telemetry\_event\_definitions\_enabled()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-native-apps-is-application-all-mandatory-telemetry-event-definitions-enabled) for more information.

The following example shows how to use the `is_application_authorized_for_telemetry_event_sharing()`
and `is_application_all_mandatory_telemetry_event_definitions_enabled()` functions of the
Python Permission SDK to verify that event sharing is enabled in the consumer account and that mandatory
events have been enabled.

Copy code

```
import streamlit as st
import snowflake.permissions as permissions

def critical_feature_that_requires_event_sharing():
  st.write("critical_feature_that_requires_event_sharing")

def main():
  if permissions.is_application_authorized_for_telemetry_event_sharing() and permissions.is_application_all_mandatory_telemetry_event_definitions_enabled():
     critical_feature_that_requires_event_sharing()
  else:
     permissions.request_event_sharing()

if __name__ == "__main__":
  main()
```
