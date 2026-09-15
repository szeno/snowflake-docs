# Snowflake Python Runtime Support

Going forward, Snowflake intends to support new Python runtimes within 1 year of their
[first official release](https://devguide.python.org/versions/).

## Deprecating and decommissioning runtimes (end of support)

To keep your functions up-to-date and secure, we occasionally need you to update your UDFs and stored
procedures and re-deploy them to use a supported runtime.

Snowflake applies updates to Python runtimes as the updates are made available by the upstream maintainers.
When a Python runtime is no longer actively maintained, Snowflake will deprecate and, eventually, remove
the runtime. The Snowflake deprecation schedule will follow
[Python’s official end-of-life schedule](https://devguide.python.org/versions/).

This process involves three aspects: a publication of the deprecation date, a deprecation period,
and a target decommission date. The deprecation date posted below indicates the start of the deprecation
period and the expected decommission date.

| Python Runtime | Snowflake Deprecation Date | Decommission Date |
| --- | --- | --- |
| 3.8 | 14 Oct 2024 | 30 Apr 2025 |
| 3.9 | 05 Oct 2025 | 30 Apr 2026 |
| 3.10 | 04 Oct 2026 | TBD |
| 3.11 | 24 Oct 2027 | TBD |
| 3.12 | 02 Oct 2028 | TBD |
| 3.13 | 07 Oct 2029 | TBD |
| 3.14 | 07 Oct 2030 | TBD |

Expand

Show lessSee more

During the deprecation period, Snowflake will no longer apply security patches or other updates
to the runtime. You can continue to use the runtime, but you should use this time to migrate any functions that still use the deprecated runtime to a more up-to-date runtime.
Note that functions that use a deprecated runtime are not eligible for technical support.

After the decommission date, you can no longer create or update functions using the runtime.
You must choose a more up-to-date runtime to deploy your functions.
Note that existing functions using the runtime can still be invoked.
