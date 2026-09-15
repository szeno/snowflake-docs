# ALTER ORGANIZATION

Modifies properties of a Snowflake [organization](/user-guide/organizations), including the default
tenant type for new accounts and the allowlist of email domains for internal accounts.

See also:
:   [ALTER ACCOUNT](/sql-reference/sql/alter-account), [CREATE ACCOUNT](/sql-reference/sql/create-account),
    [SHOW ACCOUNTS](/sql-reference/sql/show-accounts)

## Syntax

Copy code

```
ALTER ORGANIZATION SET DEFAULT_TENANT_TYPE = { INTERNAL | EXTERNAL }

ALTER ORGANIZATION SET DOMAIN_NAMES = ( '<domain>' [ , '<domain>' , ... ] )

ALTER ORGANIZATION UNSET DOMAIN_NAMES
```

## Parameters

`SET ...`
:   Specifies an organization property to set.

    `DEFAULT_TENANT_TYPE = { INTERNAL | EXTERNAL }`
    :   Sets the default tenant type for new accounts in the organization. When
        [CREATE ACCOUNT](/sql-reference/sql/create-account) omits `TENANT_TYPE`, new accounts use this default.

        If you don’t set `DEFAULT_TENANT_TYPE`, new accounts default to `INTERNAL`.

        For tenant type concepts, privileges, and legal requirements when setting `EXTERNAL`, see
        [Third party (publisher–subscriber) accounts](/user-guide/third-party-publisher-subscriber-accounts).

    `DOMAIN_NAMES = ( 'domain' [ , 'domain' , ... ] )`
    :   Sets the allowlist of email domains for users of all internal accounts in the organization.
        Provide domain names as a list of string literals.

        Each `ALTER ORGANIZATION SET DOMAIN_NAMES` statement sets the full list and overrides any
        previously set organization-level `DOMAIN_NAMES`. It does not append to an earlier list.

        Account-level domain allowlists for external accounts are set with [ALTER ACCOUNT](/sql-reference/sql/alter-account).

`UNSET DOMAIN_NAMES`
:   Clears the organization-level allowlist of email domains for internal accounts.

## Access control requirements

You can run this command only from the [organization account](/user-guide/organization-accounts)
or an `ORGADMIN` role-enabled account. The following privileges and roles can run this command:

| Privilege or role | Object | Notes |
| --- | --- | --- |
| GLOBALORGADMIN | Organization account | Can set and unset these organization properties. |
| ORGADMIN | Account | Can set and unset these properties from an `ORGADMIN` role-enabled account. |
| MANAGE TENANTS | Account | A custom role granted this privilege in the organization account can set and unset these properties. See [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- Run this command from the organization account or another context where you have organization
  administrator privileges.
- To view the current organization-level default tenant type and domain allowlist, call
  `SYSTEM$SHOW_ORGANIZATION`.
- For account-level tenant type and domain allowlists on an individual account, see
  [ALTER ACCOUNT](/sql-reference/sql/alter-account).

## Examples

Set the default tenant type for new accounts to `EXTERNAL`:

Copy code

```
ALTER ORGANIZATION SET DEFAULT_TENANT_TYPE = EXTERNAL;
```

Set the allowlist of email domains for internal accounts:

Copy code

```
ALTER ORGANIZATION SET DOMAIN_NAMES = ('domain1.com','domain2.org');
```

Clear the organization-level domain allowlist:

Copy code

```
ALTER ORGANIZATION UNSET DOMAIN_NAMES;
```
