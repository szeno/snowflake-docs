# Appeal a failed security review

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to file an appeal for an app that failed the security review process.

## Guidelines for appealing a failed security review

The following guidelines apply to the appeals process for a failed security review:

- Before submitting an appeal for a failed security review, review the security policies
  outlined in the following topics:

  - [Security requirements and guidelines for a Snowflake Native App](/developer-guide/native-apps/security-overview)
  - [Run the automated security scan](/developer-guide/native-apps/security-run-scan)
  - [Security requirements and best practices for a Snowflake Native App](/developer-guide/native-apps/security-app-requirements)
  - [Secure a Snowflake Native App with Snowpark Container Services](/developer-guide/native-apps/security-na-spcs)
- Snowflake does not provide information about the details of the security scan of an app.
- Snowflake allows one appeal per patch of an app. You must provide all information about
  your appeal in a single support case. Snowflake rejects subsequent appeals for the same
  patch of an app.
- If you do not include all required information in the support case for your appeal, the
  appeal may be rejected without review.

## Submit an appeal for a failed security review

To submit an appeal, you must [file a support case](/user-guide/contacting-support) that
includes the following information for each field:

- Summary: Use the following format in the summary of the issue:

  ```
  Appeal <App Name>, <Version>, <Patch>
  ```
- Description: Provide the following information in the description of the issue:

  - Application information: App Name, Version, Patch
  - Rejection reason(s): paste in the rejection reason & code located in **Projects** » **App packages**
  - Information required to appeal the rejection(s): Identify your rejection reason and include all information under “information required to appeal the rejection.”
- Category: Select General Administration
- Subcategory: Select Other
- Severity: 4

  All appeals have a turnaround time of 3-5 business days (Monday to Friday).
  Cases submitted with a higher severity may be downgraded to Severity 4.

Warning

If you do not provide the information outlined above, your appeal may be rejected without
review.

## Rejection reasons and information required for appeals

There are multiple reasons why an app may fail the security review. Before filing an appeal,
ensure that you have reviewed the following topics:

> - [Security requirements and guidelines for a Snowflake Native App](/developer-guide/native-apps/security-overview)
> - [Run the automated security scan](/developer-guide/native-apps/security-run-scan)
> - [Security requirements and best practices for a Snowflake Native App](/developer-guide/native-apps/security-app-requirements)
> - [Secure a Snowflake Native App with Snowpark Container Services](/developer-guide/native-apps/security-na-spcs)

Possible reasons for rejection include:

- [All app code must be defined in the application package](#label-native-apps-security-rejection-app-package).
- [All app code must be un-obfuscated](#label-native-apps-security-rejection-unobfuscated).
- [Dependencies and libraries must not contain critical or high CVEs](#label-native-apps-security-rejection-dependencies).
- [An app cannot store or require customer secrets to be in plain text](#label-native-apps-security-rejection-secrets)
- [Apps must not contain functionality harmful to Snowflake, customers, or 3rd parties](#label-native-apps-security-rejection-harmful).
- [Apps must communicate required privileges to the consumer](#label-native-apps-security-rejection-communicate-privs).
- [Apps must only request the minimum set of privileges possible](#label-native-apps-security-rejection-minimum-privs).

### App code must be defined in the application package

Snowflake security policies require that all the application code, including all library dependencies
and setup code, must be included in the app version defined in the application package.

**Reason for the rejection**

Your app is using code that is not available for review in the application package. This may be from
code that exists in a source that is outside the application package.

**How to fix this issue**

Update the app to include all the code required by the app in the application package.

Additional context is provided in the rejection reason.

**Information required to appeal the rejection**

If your app imports data from outside the application package, this can cause the app to be rejected.
This can be from tables not in the consumer account or through other external integrations.

Please provide a list of all the data imported by the app and the details about the use of the data.

### All app code must be un-obfuscated

Snowflake security policy requires all application code to be un-obfuscated, meaning that the code must be
human readable. This requirement includes minified JavaScript code.

**Reason for the rejection**

Your application includes obfuscated code that could not be reviewed by Snowflake. This could be
due to minified javascript or other forms of obfuscation like encryption or encoding. Please update
the app to remove all obfuscated code.

Additional context is provided in the rejection reason.

**Information required to appeal the rejection**

Appeals are only allowed for minified JavaScript. Please provide the location of the corresponding
source map file to the minified JavaScript.

### Dependencies and libraries must not contain critical or high CVEs.

Snowflake security policy requires all dependencies or libraries with critical or high Common
Vulnerabilities and Exposures (CVE) to be updated to a secure version, if available. See
[Common Vulnerabilities and Exposures (CVE) considerations](/developer-guide/native-apps/security-cve) for more information on identifying CVEs in a Snowflake Native App.

**Reason for the rejection**

An app may be rejected if you are using components that have known CVEs that can be harmful to
consumers if exploited. The specific CVEs in your app are provided in the rejection reason.

Different tools can detect different results based on their configuration, internal policies and depth
of scanning. Snowflake’s tools are configured to enforce the Snowflake Marketplace policies. Snowflake
may identify CVEs that you do not find in your own CVE scanning.

**Information required to appeal the rejection**

To appeal this rejection, you must provide the following information:

- Justification for why the CVE cannot be exploited in your app.
- A reachability analysis report, if available.
- A plan for an update to the fixed version.
- If there are no plans for update, provide a detailed explanation for why a vulnerable version
  cannot be updated to a fixed version.

### An app must not store or require plain text customer secrets

Snowflake security policy requires that apps do not store or require any customer secrets
to be in plain text.

**Reason for the rejection**

This result indicates that some customer secrets are stored in plain text.

Additional context is provided in the rejection reason.

**Information required to appeal the rejection**

If your app stores customer secrets, you must provide details of the secrets stored and their
uses. Also, provide details about how the secrets are stored.

Caution

Do not include the secrets in your support ticket.

### Apps must not contain functionality harmful to Snowflake, customers, or 3rd parties

Snowflake’s security policy requires that applications do not contain any functionality that
could result in harm to Snowflake, its customers, or third parties.

**Reason for the rejection**

Your app contains functionality that Snowflake deems harmful.

**Information required to appeal the rejection**

Rejections due to this reason cannot be appealed.

### Apps must communicate required privileges to the consumer

Snowflake security policy requires that apps must provide all privileges required by the
app on all objects and all API integrations.

**Reason for the rejection**

This rejection may occur when the app requests that a consumer grants privileges on an
object without communicating the required privileges to the consumer in advance.

**How to resolve this issue**

To resolve this issue, you must provide information about the permissions required by the
application and objects created by the application before asking the consumer to grant
privileges.

**Information required to appeal the rejection**

To appeal this rejection, provide the following information in your support ticket:

- A list of all the permissions required by the application.
- A list of all the objects created by the application.
- The location in the application where the privileges are disclosed to the consumer
  before asking the consumer to grant the privileges.

### Apps must only request the minimum set of privileges possible

Snowflake security policy requires that applications should only ask for the minimum set of
privileges needed for the application to function.

**Reason for the rejection**

The app is requesting broad permissions in the consumer account. For example, the app is
requesting ownership on a database when usage permissions might be sufficient.

**How to resolve this issue**

To resolve this issue, modify your app to request only the minimum required privileges
for the application to function.

**Information required to appeal the rejection**

To appeal this rejection, provide the following information in your support ticket:

- A list of all the permissions required by the application.
- A list of all the objects created by the application.
- A detailed explanation for the use of any account-level privileges, ownership grants
  or admin role requests/grants.
