# Sep 08, 2026: Trust Center, secure by default approach for scanner package enablement

Secure by default is available only for accounts on
[Business Critical Edition](/user-guide/intro-editions) or
[Virtual Private Snowflake (VPS)](/user-guide/intro-editions) with a capacity contract.

For those accounts, Snowflake now automatically enables the Trust Center
[AI Security scanner package](/user-guide/trust-center/getting-started#label-trust-center-enable-ai-security-scanner-package)
when AI feature usage is detected. New and existing accounts on those editions get this coverage without
manually enabling the package.

Snowflake automatically enables the AI Security scanner package only if it has never been
explicitly disabled.

The automatically enabled AI Security scanner package incurs
[serverless compute cost](/user-guide/trust-center/using-the-trust-center#label-trust-center-monitoring-cost)
the same way as a manually enabled package. You can disable the package at any time, and Snowflake
won’t re-enable it. You can also turn off secure by default for your account in Snowsight
or by using stored procedures.

For more information, see
[Secure by default](/user-guide/trust-center/using-the-trust-center#label-trust-center-secure-by-default) and
[Scanner Packages](/user-guide/trust-center/overview#label-trust-center-scanner-packages).
