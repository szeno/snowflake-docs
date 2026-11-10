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

The Snowflake Native App Framework ensures that an app with containers can only access the specific data and resources to which
an app has been granted access. This minimizes the risk of data exfiltration.

## Additional approval requirements for apps with containers

Snowflake implements an additional approval process for an app with containers. The approval is
mandatory before an app with containers can be published to the Snowflake Marketplace. Before an organization
can publish a public or private listing for an app with containers outside the organization, it
must pass the NA+SPCS security questionnaire.

Organizations that pass this approval process are authorized to publish public or private listings
for an app with containers outside their organization.

If an organization doesn’t pass the approval process, it can’t publish a listing for an
app with containers outside the organization. Approval covers the whole organization: after approval,
other apps in the organization don’t need a new questionnaire submission. Each app must still
undergo the automated security scan.

### Initiate the provider approval process

When a provider sets `DISTRIBUTION` = `EXTERNAL` for an application package of an app with
containers, Snowflake returns the following error if the organization hasn’t been approved to publish
an app with containers:

```
Error Code: 093197 Account is not allowed to create application package versions or patches with
Snowpark Container Services for EXTERNAL distribution
```

If you receive this error, you must submit the security questionnaire to begin the approval process.
You can [complete the questionnaire in Snowsight](#label-native-apps-spcs-questionnaire-snowsight)
or [with SQL](#label-native-apps-spcs-questionnaire-sql).

The security questionnaire assesses the following:

- The provider’s security practices.
- The provider’s compliance readiness.

Submitting the security questionnaire begins the provider approval process.

## Access

To submit or view the questionnaire, use a role that has the application role `SNOWFLAKE.NASPCS_PUBLISH_ADMIN`.

Snowflake grants this role to `ACCOUNTADMIN`. An account administrator can grant it to other roles in the account:

Copy code

```
GRANT APPLICATION ROLE SNOWFLAKE.NASPCS_PUBLISH_ADMIN TO ROLE my_role;
```

## Complete the questionnaire in Snowsight

1. In Snowsight, open **Provider Studio** and go to the **Settings** tab.
2. Open the NA+SPCS security questionnaire.
3. Answer the questions for the application you intend to distribute, then submit.

Snowsight shows the result. If rejected, review the comments, update your answers, and submit again.
After approval, Snowsight no longer shows a form to submit.

## Complete the questionnaire with SQL

### Submit a questionnaire

The procedure has the following syntax:

Copy code

```
CALL SNOWFLAKE.NATIVE_APPS_SPCS.APP_SUBMIT_NA_SPCS_SECURITY_QUESTIONNAIRE(
  <response> [ , <customer_comments> ]
);
```

Replace `<response>` with a `VARIANT` containing your questionnaire JSON, such as the result of
`PARSE_JSON`. For a complete submission example, see [Example](#label-native-apps-spcs-questionnaire-example).

| Argument | Type | Description |
| --- | --- | --- |
| `response` | `VARIANT` | The questionnaire, as a JSON object. Required. |
| `customer_comments` | `VARCHAR` | Optional comments for the submission. Defaults to `NULL`. |

Expand

Show lessSee more

The procedure returns a human-readable message indicating approval or rejection. Approval messages can
include notes about answers that did not block approval. Rejection messages list the areas to improve.
The message text is localized. For automation, call
`SNOWFLAKE.NATIVE_APPS_SPCS.APP_VIEW_NA_SPCS_SECURITY_QUESTIONNAIRE` and use the returned `reviewStatus`
field described in the following section.

Submitting again after approval fails with:

```
Organization is already approved to publish NA+SPCS applications.
```

A rejected submission can be replaced by calling the procedure again. The new response becomes the account’s
current submission.

`customer_comments` can be at most 1,000 characters. The JSON response can be at most 90,000 UTF-8 bytes.

### View the current result

Copy code

```
CALL SNOWFLAKE.NATIVE_APPS_SPCS.APP_VIEW_NA_SPCS_SECURITY_QUESTIONNAIRE();
```

The procedure returns a JSON string with the organization approval status or the most recent rejected
submission on the current account:

| `reviewStatus` | Meaning |
| --- | --- |
| `null` | This account has not submitted a questionnaire, and the organization is not approved. |
| `1` | Approved. |
| `2` | Rejected. |

Expand

Show lessSee more

When the organization is approved, including from another account, the result contains only
`reviewStatus`. After a rejection, it includes the following relevant fields:

| Field | Description |
| --- | --- |
| `reviewStatus` | `2` |
| `formResponse` | The submitted questionnaire serialized as a JSON string, rather than a nested JSON object. |
| `customerComments` | Comments supplied with the submission, or `null`. |
| `reviewerComments` | The evaluation comments. |
| `reviewedOn` | When the submission was evaluated, in UTC, such as `2026-08-01T10:15:30Z`. |
| `submittedOn` | When this submission was recorded, in UTC. |
| `updatedOn` | When the submission record was last updated, in UTC. |

Expand

Show lessSee more

For example, a rejected response can contain the following fields:

Copy code

```
{
  "reviewStatus": 2,
  "formResponse": "{\"sdlcPractices\": []}"
}
```

This excerpt omits the other response fields. Parse the returned JSON string, then parse
`formResponse` separately to access the questionnaire fields.

## Questionnaire format

The `response` argument is one JSON object. Include every required text and Boolean field described
in this section. Missing required fields, blank required text, and values of the wrong type are rejected
before the questionnaire is evaluated.

Checkbox answers are arrays of the exact option labels in the following sections.
A missing array is treated as no selections. Duplicate labels, null entries, and labels that are not in
the list are rejected.

### Required text fields

Each of the following fields must be a nonblank JSON string. Describe your application’s configuration
and provide relevant documentation links. If a component or practice doesn’t apply, state that in your
answer rather than omitting the field or leaving it blank:

| Field | Description |
| --- | --- |
| `organizationName` | Your organization’s name. |
| `email` | The provider’s contact email address. |
| `applicationName` | The application’s name. |
| `applicationPurpose` | What the application does. |
| `applicationUseCases` | Use cases for the application. |
| `containers` | All containers in the application. |
| `externalIntegrations` | All integrations with provider services or third-party services. |
| `udfs` | All user-defined functions in the application. |
| `authenticationControls` | The application’s authentication and authorization controls. |
| `architectureDiagram` | A link to an architecture diagram showing information flow between application components. |
| `consumerData` | All consumer data accessed by the application. |
| `incidentContact` | Contact information for your organization in case of a security incident. |
| `customCodePath` | Paths to all code developed by you in the container images. |
| `criticalCves` | Whether the images contain critical or high-severity CVEs. If they do, explain why the application isn’t affected. |
| `objectsAndPermissions` | All objects created and permissions requested by the application in a consumer account. |

Expand

Show lessSee more

### Secure development practices

`sdlcPractices` accepts any of:

- `Threat modeling`
- `Authenticated access to source code`
- `Peer reviews`
- `Static analysis to discover security issues`
- `Dependency scans for supply chain risks`
- `CVE scans`
- `Dynamic security testing`
- `Penetration testing by a third party`

### Vulnerability management

`vulnerabilityManagementPractices` accepts any of:

- `Endpoint vulnerability scanning`
- `Network vulnerability scanning`
- `Patch management`
- `Vulnerability risk assessment`
- `Risk based vulnerability remediation SLA`
- `Vulnerabilities remediated with SLA`

### Compliance certifications

`complianceCertifications` accepts any of:

- `SOC 2`
- `PCI DSS`
- `HIPAA`
- `ISO 27034/27001 compliance`
- `NIST SP 800.218 compliance`

### Application security

Each of the following fields is required and must be an explicit JSON Boolean value, `true` or
`false`. Omitting a field, using `null`, or supplying a string such as `"false"` causes validation to
fail:

| Field | Set to `true` when |
| --- | --- |
| `readyToPublish` | The application is ready to publish. |
| `readSecurityRequirements` | You have read the [security requirements](/developer-guide/native-apps/security-app-requirements). |
| `meetsSecurityRequirements` | The application meets the [security requirements](/developer-guide/native-apps/security-app-requirements). |
| `readSecurityBestPractices` | You have read the [security best practices](/developer-guide/native-apps/security-app-requirements#label-native-apps-security-best-practices). |
| `storesConsumerDataOutside` | The application stores consumer data outside the consumer account. |
| `accessesProviderData` | The application accesses data stored in the provider account. |
| `imageHistoryAvailable` | Image layers and command history are available in the images. |
| `unauthenticatedFunctionality` | A user can access application functionality without first authenticating through Snowflake. |
| `imagesScannedForCves` | Container images are scanned for CVEs. |
| `imagesScannedForMalware` | Container images are scanned for malware. |
| `containerRunsNonRoot` | The container runs as a non-root user. |
| `createsPublicEndpoints` | The application creates public endpoints. |
| `usesWildcardEgress` | The application allows egress to `0.0.0.0`. |
| `usesMinimalBaseImages` | The application uses minimal base images. |
| `hasVendorSecurityProgram` | The provider has a vendor security program. |
| `hasIncidentResponsePlanWithSlas` | The provider has an incident response plan with SLAs. |
| `loadsDynamicMlModelsNotInPackage` | The application loads machine-learning models that are not included in the application package. |
| `loadsDynamicCodeNotInPackage` | The application loads code that is not included in the application package. |

Expand

Show lessSee more

### Optional details

SQL submissions can include the following optional string fields. If you supply a field, its value
must be a JSON string. An empty string is allowed:

| Field | Description |
| --- | --- |
| `snowflakeContacts` | Email addresses of Snowflake employees you work with. |
| `publicEndpoints` | Public endpoints exposed by the application. |
| `egressUrls` | Egress URLs used by the application. |
| `otherSecurityControls` | Additional application security controls. |
| `consumerDataStoredOutside` | Consumer data stored outside the consumer account. |
| `providerData` | Provider data accessed by the application that isn’t included in the application package. |
| `otherSdlcActivities` | Secure development activities not listed in `sdlcPractices`. |
| `otherVulnerabilityActivities` | Vulnerability management activities not listed in `vulnerabilityManagementPractices`. |
| `vendorSecurityProgramDetails` | Details about the provider’s vendor security program. |
| `otherCertifications` | Certifications not listed in `complianceCertifications`. |

Expand

Show lessSee more

The optional fields `otherSdlcSelected`, `otherVulnerabilitySelected`, and `otherCertificationSelected`
indicate that you selected an additional activity or certification. If supplied, each must be an
explicit JSON Boolean value. Describe the activity or certification in `otherSdlcActivities`,
`otherVulnerabilityActivities`, or `otherCertifications`, respectively.

### Example

Copy code

```
CALL SNOWFLAKE.NATIVE_APPS_SPCS.APP_SUBMIT_NA_SPCS_SECURITY_QUESTIONNAIRE(
  PARSE_JSON($$
    {
      "organizationName": "Example organization",
      "email": "security@example.com",
      "applicationName": "Example analytics app",
      "applicationPurpose": "Summarize consumer data within the consumer account",
      "applicationUseCases": "Generate aggregate reports from consumer-provided tables",
      "containers": "One reporting service container",
      "externalIntegrations": "None",
      "udfs": "None",
      "authenticationControls": "Snowflake authentication and application roles",
      "architectureDiagram": "https://example.com/app/architecture",
      "consumerData": "Tables explicitly shared with the application",
      "incidentContact": "security@example.com",
      "customCodePath": "/app/reporting",
      "criticalCves": "No critical or high-severity CVEs identified",
      "objectsAndPermissions": "A service and a results table in the application schema",
      "readyToPublish": true,
      "readSecurityRequirements": true,
      "meetsSecurityRequirements": true,
      "readSecurityBestPractices": true,
      "sdlcPractices": [
        "Peer reviews",
        "Static analysis to discover security issues"
      ],
      "vulnerabilityManagementPractices": [
        "Patch management"
      ],
      "complianceCertifications": [
        "SOC 2"
      ],
      "imagesScannedForCves": true,
      "imagesScannedForMalware": true,
      "containerRunsNonRoot": true,
      "createsPublicEndpoints": false,
      "usesWildcardEgress": false,
      "usesMinimalBaseImages": true,
      "hasVendorSecurityProgram": true,
      "hasIncidentResponsePlanWithSlas": true,
      "loadsDynamicMlModelsNotInPackage": false,
      "loadsDynamicCodeNotInPackage": false,
      "storesConsumerDataOutside": false,
      "accessesProviderData": false,
      "imageHistoryAvailable": true,
      "unauthenticatedFunctionality": false,
      "egressUrls": "None",
      "vendorSecurityProgramDetails": "Security reviews of third-party suppliers"
    }
  $$),
  'Security review for our SPCS application'
);
```

Replace the sample text, contact information, documentation URL, and Boolean values with your own
answers. The example includes every required field and shows the JSON shape. It is not a statement
of which answers pass the review.

## Evaluation of the security questionnaire

Snowflake evaluates the questionnaire automatically when you submit it and returns the result
immediately. Approval applies to the whole organization, rather than a single application package:
accounts in the approved organization can set application packages that use SPCS to external distribution.

After successful approval, propagation to other accounts in the organization takes only a
short time. If an account still can’t set an application package to external distribution after the
questionnaire is approved, wait briefly and retry. If the problem persists, contact Snowflake Support.

If your questionnaire is rejected and you believe the result is incorrect or you can’t meet a specific
requirement, contact Snowflake Support.

If your organization is in Virtual Private Snowflake (VPS), you must submit the questionnaire
from an account within that VPS for your global organization to be approved. Submitting from an
account outside the VPS approves that account locally, but doesn’t approve your global organization.

## Scanning an app with containers

After an organization is approved, the app with containers undergoes the automated security scan. This
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
