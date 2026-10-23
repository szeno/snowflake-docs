# Oct 05, 2026: Trust Center, Data Security scanner package (*General availability*)

The **Data Security** scanner package is now generally available in the Trust Center. You can access additional
security insights by enabling this package, which helps you detect unauthorized or anomalous data movement in your
Snowflake account, including anomalous data exports to external and internal stages.

The package includes the following event-driven scanners:

- **Users with anomalous amount of data unloaded to external stage**: Identifies users who sent an anomalous amount of
  data to an external stage in the last 24 hours compared to their historical baseline.
- **Users with anomalous amount of data unloaded to internal stage**: Identifies users who sent an anomalous amount of
  data to an internal stage in the last 24 hours compared to their historical baseline, and flags cases where GET
  operations followed the unload activity.

For more information, see
[Data Security scanner package](/user-guide/trust-center/overview#label-data-security-scanner-package) and
[Enable the Data Security scanner package](/user-guide/trust-center/getting-started#label-trust-center-enable-data-security-scanner-package).
