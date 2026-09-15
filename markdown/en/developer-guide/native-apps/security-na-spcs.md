# Secure a Snowflake Native App with Snowpark Container Services

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes the security considerations for a Snowflake Native App with Snowpark Container Services. In addition to the general
security requirements for all apps, apps with containers have specific security implications
and considerations. The security review process for apps with containers includes a thorough
examination of the container images they contain.

Snowflake uses container image scanning tools to detect known vulnerabilities and
security best practice violations.

## Network isolation and egress control

Apps with containers use strict network isolation and egress control measures to help prevent unauthorized
data exfiltration and to protect consumer data. Each app with containers runs in its own isolated network
environment, with controlled access to external systems and services.

Snowflake uses network monitoring and filtering mechanisms to detect and block suspicious egress traffic
patterns. App providers are required to explicitly declare all external endpoints in the application
manifest, which undergoes a security review.

Consumer data is protected using the following:

- Secure data access patterns.
- Encryption in transit and at rest.
- Fine-grained access controls.

The Snowflake Native App Framework ensures that app with containers can only access the specific data and resources to which
an app has been granted access. This minimizes the risk of data exfiltration.

## Additional approval requirements for apps with containers

Snowflake implements an additional approval process for an app with containers. The approval is
mandatory before an app with containers can be published to the Snowflake Marketplace. Before a provider
can create a public or private listing for an app with containers, they must be approved by the
Snowflake Product Security team.

Providers who successfully pass this approval process are authorized to publish a public listing
for an app with containers. This allows the app to be discoverable and accessible to Snowflake customers.

If a provider does not pass the approval process, they may not publish a listing for an
app with containers.

### Initiate the provider approval process

When a provider sets the DISTRIBUTION=EXTERNAL property for an application package of an app with
containers, Snowflake returns the following error if the provider has not been approved to publish an app with
containers:

```
Error Code: 093197 Account is not allowed to create application package versions or patches with
Snowpark Container Services for EXTERNAL distribution
```

If you receive this error, you must submit a
[security questionnaire](https://docs.google.com/forms/d/1XLjbcSrp689kXEvVELa6KbEUOPfsJIirSTG5pGQDMZE/edit?ts=65fb4866)
to begin the approval process.

The security questionnaire assesses the following:

- The provider’s security practices.
- The provider’s compliance readiness.

Submitting the security questionnaire begins the provider approval process.

### Evaluation of the security questionnaire

After a provider submits the security questionnaire, Snowflake’s Security and Compliance
team evaluates each response and the documentation included by the provider. Responses are
evaluated to ensure alignment with industry best practices and standards.

In some cases, providers may be asked to provide additional information or undergo a more in-depth
review to clarify any potential concerns or risks.

After reviewing the questionnaire, Snowflake makes a decision to allow the provider to publish an
app with containers. If a provider is not approved, they must wait until Snowflake Native App with Snowpark Container Services is generally
available.

The provider receives an email from Snowflake indicating if they are approved or wait listed
until general availability.

### Scanning an app with containers

After a provider is approved, the app with containers undergoes the automated security scan. This
scan includes a normal app security scan and a scan of the container images included in the app.

The guidelines for how long the security scan takes to complete are:

| App size | Approximate time to complete scan |
| --- | --- |
| Five images or fewer / smaller than 40 GB | Less than 8 hours |
| Ten images or fewer / smaller than 70 GB | Less than 24 hours |
| Ten images or more / larger than 70 GB | 2 business days or more |

Expand

Show lessSee more

Caution

The time frames provided are for information only. They do not constitute formal
service-level agreements (SLAs).
