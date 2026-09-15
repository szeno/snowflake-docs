# Snowflake Java Runtime Support

Going forward, Snowflake intends to support new LTS Java runtimes within one year of their
[first official release](https://adoptium.net/support/).

## Deprecating and decommissioning runtimes (end of support)

To keep your functions up-to-date and secure, we occasionally need you to update your UDFs and stored procedures and re-deploy them to
use a supported runtime.

Snowflake applies updates to Java runtimes as the updates are made available by the upstream maintainers. When a Java runtime is no longer
actively maintained, Snowflake will deprecate and, eventually, remove the runtime. The Snowflake deprecation schedule will follow the
End-of-Availability schedule of [Adoptium Temurin](https://adoptium.net/support/) .

This process involves three aspects: the deprecation announcement, a deprecation period, and a target decommission date.
The deprecation date posted below indicates the start of the deprecation period and the expected decommission date.

| Java Runtime | Snowflake Deprecation Date | Decommission Date |
| --- | --- | --- |
| 11 | Oct 2027 | Jan 2028 |
| 17 | Oct 2027 | TBD |
| 21 | Dec 2029 | TBD |

Expand

Show lessSee more

During the deprecation period, Snowflake will no longer apply security patches or other updates to the runtime. You can continue to use
the runtime, but you should use this time to migrate any functions that still use the deprecated runtime to a more up-to-date
runtime. Note that functions that use a deprecated runtime are not eligible for technical support.

After the decommission date, you can no longer create, update, or invoke functions using the runtime. You must choose a more up-to-date
runtime to deploy your functions.
