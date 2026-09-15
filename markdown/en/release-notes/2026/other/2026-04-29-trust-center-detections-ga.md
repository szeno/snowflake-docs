# Apr 29, 2026: Trust Center detections (*General availability*)

The following Trust Center capabilities are now generally available:

- *Detection findings*: A new finding type to surface anomalous and potentially suspicious events.
  For more information, see [Detections](/user-guide/trust-center/overview#label-trust-center-detections).
- *Event-driven scanners*: scanners that generate detection findings in response to relevant events, such as changes to sensitive parameters
  or sign-ins from unusual IP addresses, in addition to the existing schedule-based scanners. For more information, see
  [Event-driven scanners](/user-guide/trust-center/overview#label-trust-center-scanners-event-driven).
- New scanners in the [Threat Intelligence scanner package](/user-guide/trust-center/overview#label-threat-intelligence-scanner-package) that report detection findings:
  - Authentication policy changes (event-driven)
  - Dormant user sign-ins (event-driven)
  - Entities with long-running queries (schedule-based)
  - Login protection (event-driven)
  - Sensitive parameter protection (event-driven)
  - Users with administrator privileges (schedule-based)
  - Users with unusual applications used in sessions (schedule-based)

To view detection findings in the Trust Center, see [View Trust Center detection findings](/user-guide/trust-center/using-the-trust-center#label-trust-center-alerts-managing).
