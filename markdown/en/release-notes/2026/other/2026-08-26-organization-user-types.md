# Aug 26, 2026: Organization user types (*General availability*)

With this release, you can specify whether an organization user represents a person or a service. Set the `TYPE` property to `SERVICE` for
a service or application that interacts with Snowflake without human interaction. If you don’t specify a type, the organization user is a
`PERSON` user, which matches the previous behavior.

The type of an organization user determines the following:

- The type of the user objects that Snowflake creates when an account administrator imports an organization user group. Importing a group
  that contains a `SERVICE` organization user creates a `SERVICE` user in the regular account.
- The existing users that the organization user is eligible to link to. The
  [SYSTEM$LINK\_ORGANIZATION\_USER](/sql-reference/functions/system_link_organization_user) function now requires the type of the local user to be compatible with the
  type of the organization user.

`PERSON` and `SERVICE` are the only types available to an organization user, and you can’t change the type after you create the
organization user.

For more information, see the following topics:

- [Organization user types](/user-guide/organization-users#label-org-users-types)
- [Types of users](/user-guide/admin-user-management#label-user-management-types)
- [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user)
- [SYSTEM$LINK\_ORGANIZATION\_USER](/sql-reference/functions/system_link_organization_user)
