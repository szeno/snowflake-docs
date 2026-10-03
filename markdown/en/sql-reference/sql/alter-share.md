# ALTER SHARE

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire about enabling
it, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies the properties for an existing [share](/user-guide/data-sharing-intro):

- Adds or removes accounts from the list of accounts.
- Sets a new list of accounts with which the corresponding database for the share is shared.
- Modifies other properties. For parameter details, see [Parameters](/sql-reference/parameters).

See also:
:   [CREATE SHARE](/sql-reference/sql/create-share) , [DROP SHARE](/sql-reference/sql/drop-share) , [DESCRIBE SHARE](/sql-reference/sql/desc-share) , [SHOW SHARES](/sql-reference/sql/show-shares)

## Syntax

Copy code

```
ALTER SHARE [ IF EXISTS ] <name> { ADD | REMOVE } ACCOUNTS = <consumer_account> [ , <consumer_account> , ... ]
                                        [ SHARE_RESTRICTIONS = { TRUE | FALSE } ]

ALTER SHARE [ IF EXISTS ] <name> SET { [ ACCOUNTS = <consumer_account> [ , <consumer_account> ... ] ]
                                       [ COMMENT = '<string_literal>' ] }

ALTER SHARE [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER SHARE <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER SHARE [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the share to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`ADD | REMOVE ACCOUNTS = consumer_account [ , consumer_account , ... ]`
:   Specifies the name of the account(s) to add or remove from the list of accounts for the share:

    - Adding an account to a share that was already in the list has no effect.
    - Removing an account that has already imported the shared database immediately revokes that account’s access to the database. If the account
      is later added back to the share, the account must re-create the database before they can use it again.
    - Removing an account from a share that was not already in the list of shared accounts has no effect.

    This parameter adds to (or removes from) the existing list of accounts for the share. If you want to replace the entire list of accounts, use
    `SET` instead.

    `SHARE_RESTRICTIONS = { TRUE | FALSE }`

    > `FALSE`: A Standard or Enterprise consumer account can be added to a share belonging to a Business Critical provider account.
    > A non-HIPAA consumer account can be added to a share belonging to a HIPAA-compliant provider account.
    >
    > `TRUE`: A Standard or Enterprise consumer account cannot be added to a share belonging to a Business Critical provider account.
    > A non-HIPAA consumer account cannot be added to a share belonging to a HIPAA-compliant provider account.
    >
    > Default:
    > :   `TRUE`
    >
    > Important
    >
    > You must set this parameter each time you add a new non-Business Critical consumer account to the share belonging to a Business Critical provider account,
    > or each time you add a new non-HIPAA consumer account to the share belonging to a HIPAA-compliant provider account.
    > For more information see, [Direct share restrictions](/user-guide/direct-share-restrictions).

`SET...`

> `ACCOUNTS = consumer_account [ , consumer_account ... ]`
> :   Specifies the account(s) to replace all previous accounts with which the share was shared. To add/remove individual accounts from the
>     list, use `ADD | REMOVE` instead.
>
> `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
> :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.
>
>     The tag value is always a string, and the maximum number of characters for the tag value is 256.
>
>     For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).
>
> `COMMENT = 'string'`
> :   Adds a comment or overwrites an existing comment for the share.

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the share, which resets them back to their defaults:

    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

## Usage notes

- To alter a share, a role must have the OWNERSHIP privilege on the share. The role that creates a share owns it.
- To add or remove accounts (share targets), a role must have both of the following privileges:

  - OWNERSHIP on the share.
  - MANAGE SHARE TARGET on the account.

  CREATE SHARE doesn’t include the ability to add or remove accounts. For more information, see
  [MANAGE SHARE TARGET privilege](/user-guide/security-access-privileges-shares#label-manage-share-target-privilege).
- Keywords `ACCOUNT` and `ACCOUNTS` are both supported and can be used interchangeably.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Add accounts `org1.consumer1` and `org1.consumer2` to the existing share named `sales_s`:

> Copy code
>
> ```
> ALTER SHARE sales_s ADD ACCOUNTS = org1.consumer1, org1.consumer2;
>
> +----------------------------------+
> | status                           |
> |----------------------------------|
> | Statement executed successfully. |
> +----------------------------------+
> ```

Remove account `org1.consumer1` from `sales_s`:

> Copy code
>
> ```
> ALTER SHARE sales_s REMOVE ACCOUNT = org1.consumer1;
>
> +----------------------------------+
> | status                           |
> |----------------------------------|
> | Statement executed successfully. |
> +----------------------------------+
> ```

Grant the `MANAGE SHARE TARGET` privilege to the `share_admin` role, grant that role to user `jsmith`, and use the role to add accounts to
`sales_s`. The `share_admin` role must also own `sales_s`:

Copy code

```
GRANT MANAGE SHARE TARGET ON ACCOUNT TO ROLE share_admin;

GRANT ROLE share_admin TO USER jsmith;

USE ROLE share_admin;

ALTER SHARE sales_s ADD ACCOUNTS = org1.consumer1, org1.consumer2;
```

Set a new comment for `sales_s`:

> Copy code
>
> ```
> ALTER SHARE sales_s SET COMMENT='This share contains sales data for 2017';
>
> +----------------------------------+
> | status                           |
> |----------------------------------|
> | Statement executed successfully. |
> +----------------------------------+
> ```
