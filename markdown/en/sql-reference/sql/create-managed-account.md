# CREATE MANAGED ACCOUNT

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire about
enabling it, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new managed account. Currently used by data providers to create reader accounts for their consumers. For more details, see
[Manage reader accounts](/user-guide/data-sharing-reader-create).

See also:
:   [DROP MANAGED ACCOUNT](/sql-reference/sql/drop-managed-account) , [SHOW MANAGED ACCOUNTS](/sql-reference/sql/show-managed-accounts)

## Syntax

Copy code

```
CREATE MANAGED ACCOUNT <name>
    ADMIN_NAME = <username> , ADMIN_PASSWORD = <user_password> ,
    TYPE = READER ,
    [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Identifier for the managed account; must be unique for your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`).

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Important

    The identifier for the managed account is not the same as the account name, which is required to access the account. The account name,
    also known as the *locator*, is assigned by Snowflake.

`ADMIN_NAME = username`
:   Identifier, as well as login name, for the initial user in the managed account. This user serves as the account administrator for the
    account (i.e. this user is automatically created when the account is created and is assigned the ACCOUNTADMIN role).

    Once the account is created, you will log into the account as this user to configure (i.e. “bootstrap”) the account.

`ADMIN_PASSWORD = user_password`
:   Password for the initial user in the managed account. The password is a string literal that must be enclosed in single or double quotes
    and must conform to the [Snowflake-provided password policy](/user-guide/password-authentication#label-snowflake-password-policy).

`TYPE = READER`
:   Specifies the type of managed account. Currently, the only type supported is `READER` (i.e. reader accounts used for data sharing).

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the managed account.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ACCOUNT | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- By default, the total number of reader accounts a provider can create is 20. If you reach the limit and require creating additional
  accounts, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

  If you dropped a reader account in order to create a new account without exceeding this limit, you cannot create the new reader account for
  7 days, which is the retention period for deleted reader accounts.
- If the command completes successfully, it returns a JSON object containing the account name/locator and the URL for accessing the account.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Copy code

```
CREATE MANAGED ACCOUNT reader_acct1
    ADMIN_NAME = user1 , ADMIN_PASSWORD = 'Sdfed43da!44' ,
    TYPE = READER;
```

```
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| status                                                                                                                                                                            |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| {"accountName":"READER_ACCT1","accountLocator":"IIB88126","url":"https://myorg-reader_acct1.snowflakecomputing.com","accountLocatorUrl":"https://iib88126.snowflakecomputing.com"}|
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
