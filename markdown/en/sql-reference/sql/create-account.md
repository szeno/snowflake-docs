# CREATE ACCOUNT

Creates a new account in your organization.

See also:
:   [DROP ACCOUNT](/sql-reference/sql/drop-account), [SHOW ACCOUNTS](/sql-reference/sql/show-accounts), [UNDROP ACCOUNT](/sql-reference/sql/undrop-account)

## Syntax

Copy code

```
CREATE ACCOUNT <name>
      ADMIN_NAME = '<string_literal>'
    { ADMIN_PASSWORD = '<string_literal>' | ADMIN_RSA_PUBLIC_KEY = '<string_literal>' }
    [ ADMIN_USER_TYPE = { PERSON | SERVICE | LEGACY_SERVICE | NULL } ]
    [ FIRST_NAME = '<string_literal>' ]
    [ LAST_NAME = '<string_literal>' ]
      EMAIL = '<string_literal>'
    [ MUST_CHANGE_PASSWORD = { TRUE | FALSE } ]
      EDITION = { STANDARD | ENTERPRISE | BUSINESS_CRITICAL }
    [ REGION_GROUP = <region_group_id> ]
    [ REGION = <snowflake_region_id> ]
    [ COMMENT = '<string_literal>' ]
    [ POLARIS = { TRUE | FALSE } ]
```

## Required parameters

`name`
:   Specifies the `account_name` substring in an [account identifier](/user-guide/admin-account-identifier).

    This name should conform with all the [requirements for account identifiers](/user-guide/admin-account-identifier#label-note-requirements-account-id).

`ADMIN_NAME = 'string_literal'`
:   Login name of the initial administrative user of the account. A new user is created in the new account with this name and password and
    granted the ACCOUNTADMIN role in the account.

    A login name can be any string consisting of letters, numbers, and underscores. Login names are always case-insensitive.

`ADMIN_PASSWORD = 'string_literal'`
:   Password for the initial administrative user of the account. The password for the user must be enclosed in single or double quotes.

    Optional if the `ADMIN_RSA_PUBLIC_KEY` parameter is specified.

    For more information about passwords in Snowflake, see [Snowflake-provided password policy](/user-guide/password-authentication#label-snowflake-password-policy).

`ADMIN_RSA_PUBLIC_KEY = 'string_literal'`
:   Assigns a public key to the initial administrative user of the account in order to implement
    [key pair authentication](/user-guide/key-pair-auth) for the user.

    Optional if the `ADMIN_PASSWORD` parameter is specified.

`EMAIL = 'string_literal'`
:   Email address of the initial administrative user of the account. This email address is used to send any notifications about the account.

`EDITION = { STANDARD | ENTERPRISE | BUSINESS_CRITICAL }`
:   [Snowflake Edition](/user-guide/intro-editions) of the account.

## Optional parameters

`ADMIN_USER_TYPE = { PERSON | SERVICE | LEGACY_SERVICE | NULL }`
:   Used for setting the [type](/user-guide/admin-user-management#label-user-management-types) of the first user that is assigned the ACCOUNTADMIN role during account
    creation.

    Note

    The LEGACY\_SERVICE type is being deprecated. Use the SERVICE type for services and applications. For a timeline of the deprecation of
    LEGACY\_SERVICE, see [Planning for the deprecation of single-factor password sign-ins](/user-guide/security-mfa-rollout).

    Default: `NULL` (Same as `PERSON`).

`FIRST_NAME = string` , `LAST_NAME = string`
:   First and last name of the initial administrative user of the account.

    Default: `NULL`

`MUST_CHANGE_PASSWORD = { TRUE | FALSE }`
:   Specifies whether the new user created to administer the account is forced to change their password upon first login into the account.

    Default: `FALSE`

`REGION_GROUP = region_group_id`
:   ID of the region group where the account is created. To retrieve the region group ID for existing accounts in your organization, execute
    the [SHOW REGIONS](/sql-reference/sql/show-regions) command. For information about when you might need to specify region group, see
    [Region groups](/user-guide/admin-account-identifier#label-region-groups).

    Default: Current region group.

`REGION = snowflake_region_id`
:   [Snowflake Region ID](/user-guide/admin-account-identifier#label-snowflake-region-ids) of the region where the account is created. If no value is provided, Snowflake
    creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is
    executed.)

    To obtain a list of the regions that are available for an organization, execute the [SHOW REGIONS](/sql-reference/sql/show-regions) command.

    Default: Current Snowflake Region.

`COMMENT = 'string_literal'`
:   Specifies a comment for the account.

    Default: No value

`POLARIS = { TRUE | FALSE }`
:   Specifies whether to create a Snowflake Open Catalog account.

    Default: FALSE

## Access control requirements

Only [organization administrators](/user-guide/organization-administrators) can execute this SQL command.

## Usage notes

- An account can be associated with your organization in one of the following ways:

  - Create a new account using the SQL command described in the current topic.
  - Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to link an existing account to your organization.
- By default, the maximum number of accounts in an organization cannot exceed 25. To have this limit raised, contact Snowflake Support.
- It takes about 30 seconds for the DNS changes to propagate before you can access a newly created account. If the account is not accessible
  immediately, wait for approximately 30 seconds and try again.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a new Snowflake account in the `aws_us_west_2` Snowflake Region on Amazon Web Services (AWS). The user who executes the CREATE ACCOUNT
statement can be logged into an account in the same or a different Snowflake Region:

> Copy code
>
> ```
> create account myaccount1
>   admin_name = admin
>   admin_password = 'TestPassword1'
>   first_name = Jane
>   last_name = Smith
>   email = 'myemail@myorg.org'
>   edition = enterprise
>   region = aws_us_west_2;
> ```

Create a new Snowflake account in the same region group and Snowflake Region in which the CREATE ACCOUNT statement is executed. The new account
administrator user must change their password upon first login:

> Copy code
>
> ```
> create account myaccount2
>   admin_name = admin
>   admin_password = 'TestPassword1'
>   email = 'myemail@myorg.org'
>   edition = enterprise;
> ```

Create a new Open Catalog account in the aws\_us\_west\_2 Snowflake Region on Amazon Web Services (AWS):

> Copy code
>
> ```
> create account myaccount1
>   admin_name = admin
>   admin_password = 'TestPassword1'
>   first_name = Jane
>   last_name = Smith
>   email = 'myemail@myorg.org'
>   edition = enterprise
>   region = aws_us_west_2
>   polaris = true;
> ```
