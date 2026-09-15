# Get support for a Native App

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## The provider is your support contact for all app issues

The provider is the seller of record and is responsible for supporting the application. All issues
related to the app (functional bugs, unexpected behavior, performance problems, data questions,
integration failures) should be reported directly to the provider. The provider will engage
Snowflake where appropriate.

Snowflake Support does not have knowledge of the specifics of individual Native Apps and will not be
able to provide support for them directly.

To contact the provider, use the contact information in the Snowflake Marketplace listing for the app.
When filing a support request with the provider, include:

- The app name and current version (visible in the [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) app management view)
- A description of the issue and the steps to reproduce it
- Relevant error messages
- Query IDs for any failed queries (available in query history)

## Snowflake Support: the narrow exception

Snowflake Support is appropriate only for issues that are clearly at the platform level and not
related to the specific app:

- Installation failure due to a Snowflake infrastructure issue (not an app configuration issue)
- Billing discrepancies
- [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) not loading or other platform-level interface issues

If you are unsure whether an issue is platform-level or app-level, start with the provider. They
are better positioned to diagnose and will escalate to Snowflake if needed. Snowflake Support cannot
provide support for third-party applications.

## Security concerns and suspected misuse

If you believe the app is accessing objects or performing actions beyond what you authorized:

**First:** revoke the relevant grants and/or suspend the app’s resources (compute pools, warehouses)
immediately to stop any ongoing access while you investigate.

**Second:** collect evidence using the monitoring queries in
[Monitor and audit a Native App](/developer-guide/native-apps/consumer-guide-monitor): query `GRANTS_TO_ROLES` to see current
access, `APPLICATION_CALLBACK_HISTORY` to see recent callback executions, and the standard Snowflake
`QUERY_HISTORY` and `ACCESS_HISTORY` views to see what queries ran and what objects were accessed.

**Third:** contact the provider. In most cases, unexpected behavior has an explanation: a new
feature in an upgrade, a misconfiguration, or a bug. The provider should be able to explain or
remediate.

If the concern cannot be resolved with the provider, file a case with Snowflake Support in the same
way you would for any other Snowflake security concern. For instructions, see
[Contacting Snowflake Support](/user-guide/contacting-support).

## Vulnerability disclosures

If you discover a security vulnerability:

- **In the app’s logic, data handling, or behavior:** report to the provider. The provider is
  responsible for patching app-level vulnerabilities.
- **In the Snowflake platform itself:** report to Snowflake through the standard Snowflake
  vulnerability disclosure process. For instructions, see
  [Contacting Snowflake Support](/user-guide/contacting-support).
