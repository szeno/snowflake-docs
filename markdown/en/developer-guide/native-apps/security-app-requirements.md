# Security requirements and best practices for a Snowflake Native App

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes the security requirements and best practices that providers must
follow when developing a Snowflake Native App. All apps that meet the conditions described in
[Automated security reviews](/developer-guide/native-apps/security-overview#label-native-apps-security-scan-initiate) must conform to the security requirements
outlined in the following sections:

- [Security requirements for application code](#label-native-apps-security-scan-app-code)
- [Security requirements for app functionality](#label-native-apps-security-scan-app-functionality)
- [Security requirements for app permissions](#label-native-apps-security-scan-app-permissions)

Note

Security requirements are subject to change as Snowflake continues to monitor new potential risks.

## Security requirements for application code

App code included within an application package must conform to the following security requirements:

1. Your app must not load or execute any code from outside the application package except
   Snowflake-provided libraries. All the app code, including all library dependencies and setup code,
   must be included in the app version defined in the application package.
2. All app code must be un-obfuscated, meaning that the code must be human readable. This requirement
   includes minified JavaScript code.

   Note

   If an app needs to use minified JavaScript code, it must include a corresponding source map file
   that can be used to recover the un-minified code.
3. All dependencies or libraries with critical or high common vulnerabilities and exposures (CVE) must be
   updated to a secure version, if available.

## Security requirements for app functionality

The following security requirements apply to the functionality of your app:

1. All apps must provide the following information to customers as part of a listing:

   1. All app functionality and features.
   2. All Internet endpoints and URLs that the app connects to.
   3. All external functions in the app.
   4. Any consumer data logged, collected, or stored by the app.
      1. Apps should prohibit all non-essential cookies.
      2. Apps should communicate all essential cookies to consumers
2. Apps should function as advertised in the app listing.
3. All app installation and setup instructions must be included in the app listing.
4. Apps must not store or require any plain text customer secrets.
5. Any communication between the app and the Internet should be over an HTTPS connection with a valid
   TLS certificate.
6. Apps must not have any functionality that could result in harm to Snowflake, its customers, or third
   parties. Harm includes but is not limited to:

   1. Data leakage and/or loss;
   2. Restricting consumer access to their data unless explicitly designed as part of the app
      functionality, for example, data masking for data access policies.
   3. Excessive resource consumption.
   4. Arbitrary code injection/execution.
7. All connections to an app, including web-based user interfaces and APIs, must first authenticate using a
   Snowflake-provided method of authentication. Any app-specific authentication must be presented to users
   after Snowflake authentication has succeeded.
8. Apps should not create any public endpoints that allow connections to the app without a successful
   authentication through Snowflake first.

## Security requirements for app permissions

The following security requirements apply to the privileges set by your app:

1. All apps must provide the following information in the manifest file:

   1. All privileges required by the app on all objects.
   2. All API integrations.
2. Apps should only ask for the minimum set of privileges needed for the app to function.

## Recommended security best practices

In addition to the security requirements imposed by the automated security scan, Snowflake recommends the
following best practices when developing a Snowflake Native App. Following these best practices helps reduce
the likelihood of an app being blocked during security review.

- Follow secure Software Development Life Cycle (SDLC) practices.

  - Review app code for vulnerabilities during the development lifecycle and fix them before creating
    an app version.
  - Review third-party libraries for vulnerabilities and update them to the latest secure version.
  - Review and update all third-party libraries in the app at least once a quarter.
- Follow Snowflake security best practices as described in the following:

  - [Security Practices for UDFs and Procedures](/developer-guide/udf-stored-procedure-security-practices)
  - [Securing an external function](/sql-reference/external-functions-security)

## Recommended security best practices for an app with containers

In addition to the security best practices for a core Snowflake Native App outlined in
[Recommended security best practices](#label-native-apps-security-best-practices), the following
security best practices apply to an app with containers:

- Limit the use of external dependencies and libraries to minimize the attack surface of an app and
  reduce the risk of supply chain vulnerabilities.
- Follow container image hardening requirements, such as the use of minimal base images, removal of
  unnecessary packages, and secure configuration of runtime environments.
- Use secure communication protocols and encryption for all inter-container and external communication.
- Generate comprehensive logging and auditing of container activities and data access patterns.
- Update and patch container images regularly to address known vulnerabilities and security issues.
- Implement only required privileges to minimizing the attack surface of containerized apps.
- Managing secrets and sensitive data securely, using appropriate encryption and access controls.
- Conduct thorough security testing and vulnerability assessments before submitting apps for review.
- Respond promptly to security incidents and collaborate with Snowflake during incident response.
- Provide clear and accurate documentation of app functionality, dependencies, and security controls.
- Educate and guide consumers on the secure use and configuration of their apps.

## Best practices for developing and publishing an application package

To streamline the development and publishing process for a Snowflake Native App, Snowflake recommends creating
two separate application packages:

- Development application package

  The development application package is intended for rapid iteration and testing purposes. It should
  have its DISTRIBUTION property set to `INTERNAL`. This ensures that the application package remains
  internal and is not distributed to external consumers or to Snowflake scanning and approval.

  By keeping this package separate from the production package, developers can quickly make changes and
  test new features without triggering the security review process for each iteration.
- Production application package

  The production application package is intended for publishing an application package and distributing it
  to Snowflake for scanning and approval and to external consumers. The production application package should have
  its DISTRIBUTION property set to `EXTERNAL`.

  Only versions that have passed the provider’s security review should be added to this package, ensuring
  that the app meets the required security standards before being made available to consumers.

By following the best practice of having separate development and production packages, developers can maintain an efficient
development lifecycle while ensuring that only secure and approved versions of the app are published and
distributed to external consumers.
