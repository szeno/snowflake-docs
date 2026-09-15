# Snowflake SCIM support

Snowflake supports SCIM 2.0, lets you integrate Snowflake with Okta and Microsoft Azure AD as identity providers. You can use
custom identity providers, which are identity providers that are neither Okta nor Microsoft Azure. You can provision users and groups
(roles) from the identity provider into Snowflake, which functions as the service provider.

Note

SCIM roles in Snowflake must own any users or roles that are imported from the identity provider. If the Snowflake SCIM role does not own
the imported users or roles, updates in the identity provider will not be synced to Snowflake. Snowflake SCIM roles correlate with their
identity provider (IdP):

- Okta SCIM Role: `OKTA_PROVISIONER`
- Microsoft Entra ID SCIM Role: `AAD_PROVISIONER`
- Custom SCIM Role: `GENERIC_SCIM_PROVISIONER`

For more information on how to use the Snowflake SCIM Role, see the SCIM configuration sections for [Okta](/user-guide/scim-okta#label-scim-okta-config),
[Microsoft Entra ID](/user-guide/scim-azure#label-scim-azure-config), and the [Custom SCIM integration](/user-guide/scim-custom#label-scim-custom-config).

## Use cases

The Snowflake SCIM API can address the following use cases.

- [Managing users](/user-guide/scim-user-api-reference): Administrators can provision and manage their users from their organization’s
  identity provider to Snowflake. User management is a one-to-one mapping from the identity provider to Snowflake.
- [Managing groups](/user-guide/scim-group-api-reference): Administrators can provision and manage their groups (that is, roles) from
  their organization’s identity provider to Snowflake. Role management is a one-to-one mapping from the identity provider to Snowflake.
- [Auditing SCIM API requests](/user-guide/scim-api-references#label-scim-auditing-rest-api-requests): Administrators can query the `rest_event_history` table to determine whether the
  identity provider is sending updates (that is, SCIM API requests) to Snowflake.

## Implementing SCIM

1. Choose your preferred identity provider (IdP) to send SCIM requests. Snowflake supports [Okta, Microsoft Entra ID, and custom integrations](/user-guide/scim-security-integrations).
2. [Create a SCIM security integration](/user-guide/scim-security-integrations) to establish an interface between Snowflake and your IdP.
3. [Configure Snowflake](/user-guide/scim-authentication) so that you can authenticate SCIM requests.
4. Use your IdP to send SCIM requests. For information about the API and auditing requests, see [SCIM API requests](/user-guide/scim-api-references).

## User invitation emails

Snowflake sends invitation emails to users created using SCIM by default.
Invitation emails are sent within 24-48 hours of users being created.
To opt out of this feature, contact [Snowflake Support](https://community.snowflake.com/s/article/How-To-Submit-a-Support-Case-in-Snowflake-Lodge).
