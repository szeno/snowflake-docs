# Aug 29, 2025: Snowflake Native Apps: Restricted caller’s rights (*General availability*)

Snowflake Native App support for restricted caller’s rights is now generally available. Restricted caller’s rights allow an app’s stored procedures and Snowpark Container Services (SPCS) services to execute with caller’s rights. However, these executables can only use a select subset of
available privileges. These privileges must be requested by the app and
granted by the admin of the consumer account when configuring the app.

For information on using restricted caller’s rights in an app, see
[Grant restricted caller’s rights to an executable in an app](/developer-guide/native-apps/ui-consumer-restricted-callers-rights).
