# Jan 23, 2026: Organization users (*General availability*)

Multi-account organizations that need the same person to be a user in more than one account
can now create an organization user for the person. Each organization user acts as a global user entity that can be imported into regular
accounts by account administrators, simplifying the process of creating a user object for the same person in multiple accounts.

Organization users are grouped into logical units called organization user groups. When an account administrator imports an organization user
group into a regular account, all of its organization users are added to the account. The organization user group becomes an access control
role in the account, allowing you to have consistent roles across the organization.

If an existing user needs to be an organization user, you can import the organization group into each account, then link the
existing local user object to the new organization user.

Organization users and organization user groups require an organization account.

For more information, see [Organization users](/user-guide/organization-users).
