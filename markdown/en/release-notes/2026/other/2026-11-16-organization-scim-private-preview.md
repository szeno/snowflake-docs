# Nov 16, 2026: SCIM provisioning for organization users and organization user groups (*Private preview*)

With this release, we introduce the private preview of organization-scoped SCIM. With a SCIM security integration that has
`SCOPE = ORGANIZATION` in the organization account, Okta, Microsoft Entra ID, or a custom identity provider provisions organization users
and organization user groups once for the whole organization, instead of through a separate SCIM integration in each regular account.

The identity provider creates, updates, and deletes organization users and organization user groups, and manages group membership.
Changes to an organization user apply in every regular account that imported it. For example, deactivating a user in the identity
provider disables the user in each of those accounts. SCIM doesn’t set the visibility of an organization user group or import it into
regular accounts. You still do both with SQL.

For more information, see the following topics:

- [Organization users](/LIMITEDACCESS/organization-users)
- [Set up organization-scoped SCIM](/LIMITEDACCESS/scim/provision-organization-users)
- [Organization-scoped SCIM API differences](/LIMITEDACCESS/scim/organization-scim-api-differences)
