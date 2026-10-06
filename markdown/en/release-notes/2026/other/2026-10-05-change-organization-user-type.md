# Oct 5, 2026: Change the type of an organization user

With this release, you can change the type of an existing organization user. Use the [ALTER ORGANIZATION USER](/sql-reference/sql/alter-organization-user)
command to set the `TYPE` property to `PERSON` or `SERVICE`, or unset the property to make the organization user a `PERSON` user, which
is the default type. Previously, you could only set the type when you created the organization user.

When you change the type of an organization user, Snowflake also changes the type of the corresponding user object in every regular
account that imported the organization user, including existing users that were linked to it. Because the type of a user determines which
authentication methods it can use, make sure that these users authenticate with a method that the new type supports before you change the
type.

For more information, see the following topics:

- [Change the type of an organization user](/user-guide/organization-users#label-org-users-types-change)
- [Types of users](/user-guide/admin-user-management#label-user-management-types)
- [ALTER ORGANIZATION USER](/sql-reference/sql/alter-organization-user)
