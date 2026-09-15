# Creating an account

[As the organization administrator](/user-guide/organization-administrators), you can create an account through the web interface or
using SQL:

> [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in):
> :   In the navigation menu, select **Admin** » **Accounts**, and then select **+ Account**.
>
> SQL:
> :   Execute a [CREATE ACCOUNT](/sql-reference/sql/create-account) command.
>
> Note
>
> For instructions on how to create a Snowflake Open Catalog account, see [Create a Snowflake Open Catalog account](https://other-docs.snowflake.com/en/opencatalog/create-open-catalog-account)

When creating an account, you can specify a [cloud platform](/user-guide/intro-cloud-platforms), a
[region](/user-guide/intro-regions), and a [Snowflake edition](/user-guide/intro-editions). You can optionally specify a region
group if you have, or want to have, accounts in multiple region groups. For more details see [Region groups](/user-guide/admin-account-identifier#label-region-groups).

If you are having trouble creating or accessing a new account, consider:

- By default, the maximum number of On Demand accounts in an organization is 25. If the organization has a capacity contract,
  the default maximum number of accounts is 100. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to have these limits raised.
- You can only create an account in a region that is enabled for your organization. For a list of available regions,
  see [View a list of regions available for an organization](/user-guide/intro-regions#label-show-organization-regions). To request access to additional regions, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
- It takes about 30 seconds for the DNS changes to propagate before you can access a newly created account. If the account is not
  accessible immediately, wait for approximately 30 seconds and try again.

Each account in your organization can have its own set of users, roles, databases, and warehouses.

You will be billed for usage in all of your accounts on a single bill. To monitor usage for your organization accounts, see [Organization Usage](/sql-reference/organization-usage) views.

## Initial user of an account

When you create a new account, you specify the first user of the account, who is assigned the ACCOUNTADMIN role. It is important to specify
whether this initial user is a human user or a service user because this determines whether the user must enroll in
MFA (multi-factor authentication).

### Enforce MFA enrollment on a human ACCOUNTADMIN

If a human directly uses the ACCOUNTADMIN role on your account, you can secure your account by forcing this account administrator to enroll
in MFA during account creation.

Execute the following SQL statement during account creation to specify that a human uses the ACCOUNTADMIN role, and is required to enroll in
MFA:

Copy code

```
CREATE ACCOUNT my_admin ADMIN_USER_TYPE = PERSON;
```

### Prevent MFA from being enforced on a non-human ACCOUNTADMIN

If a human does not use the ACCOUNTADMIN role on your account, you must prevent MFA enrollment from being enforced to allow the service that
is using the ACCOUNTADMIN role to run successfully. A service-type ACCOUNTADMIN cannot use passwords to authenticate, and must specify an
[ADMIN\_RSA\_PUBLIC\_KEY](/sql-reference/sql/create-account#label-create-account-admin-rsa-public-key) during account creation.

Execute the following SQL statement during account creation to specify that a service uses the ACCOUNTADMIN role, uses an RSA key to
authenticate, and is not required to enroll in MFA:

Copy code

```
CREATE ACCOUNT my_admin
  ADMIN_USER_TYPE = SERVICE
  ADMIN_RSA_PUBLIC_KEY = 'MIIBIj...';
```
