# Using External Tokenization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides instructions on how to use External Tokenization in Snowflake with partner integrations and how to create a custom
External Tokenization integration.

Snowflake supports External Tokenization on AWS, Microsoft Azure, and Google Cloud Platform.

Note that an external tokenization masking policy can be assigned to a tag to provide tag-based external tokenization. For details about
assigning a masking policy to a tag, see [Tag-based masking policies](/user-guide/tag-based-masking-policies).

Important

External tokenization requires [Writing external functions](/sql-reference/external-functions), which are included in the Snowflake [Overview of editions](/user-guide/intro-editions#label-snowflake-editions-standard), and you can use external functions with a tokenization provider.

However, if you choose to integrate your tokenization provider with Snowflake External Tokenization, you must upgrade to
[Enterprise Edition](/user-guide/intro-editions#label-snowflake-editions-enterprise) or higher.

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## External Tokenization partner integrations

The following partners facilitate external tokenization in Snowflake. To use these partner integrations, follow the instructions in the
partner documentation or contact the partner to begin the configuration process:

- [ALTR](https://altr.com/use-cases/tokenization/)
- [Baffle](https://baffle.io/snowflake/)
- [Capital One Databolt](https://www.capitalone.com/software/products/databolt/)
- [Comforte](https://insights.comforte.com/how-to-protect-data-on-snowflake)
- [Fortanix](https://support.fortanix.com/hc/en-us/articles/4407049792148-Using-Data-Security-Manager-with-Snowflake)
- [MicroFocus CyberRes Voltage](https://www.microfocus.com/en-us/cyberres/partners/snowflake)
- [Protegrity](https://www.protegrity.com/snowflake-partnership)
- [Privacera](https://privacera.com/partners/snowflake/)
- [SecuPI](https://www.secupi.com/solution/data-access-governance/)
- [Skyflow](https://info.skyflow.com/snowflake-partner-skyflow)
- [Spring Labs](https://springlabs.com/spring-labs-snowflake)
- [Thales](https://thalesdocs.com/ctp/ig/snowflake/index.html)

## Create a custom External Tokenization integration

Complete the following steps to create a custom integration for External Tokenization:

### Step 1: Create an external function

Create an external function in Snowflake and configure your cloud provider environment to communicate with the external function. For
details, see:

- [Creating external functions on AWS](/sql-reference/external-functions-creating-aws)
- [Creating external functions on Microsoft Azure](/sql-reference/external-functions-creating-azure)
- [Creating external functions on GCP](/sql-reference/external-functions-creating-gcp)

# Step 2: Grant Masking Policy Privileges to Custom Role

A [security or privacy officer](/user-guide/security-column-intro#label-security-column-mgmt-approach) should serve as the masking policy administrator (i.e. custom role: `MASKING_ADMIN`) and have the privileges to define, manage, and apply masking policies to columns.

Snowflake provides the following privileges to grant to a security or privacy officer for Column-level Security masking policies:

| Privilege | Object | Description |
| --- | --- | --- |
| CREATE MASKING POLICY | Schema | This privilege controls who can create masking policies. |
| APPLY MASKING POLICY | Account | This privilege controls who can [un]set masking policies on columns and is granted to the ACCOUNTADMIN role by default.   This privilege only allows applying a masking policy to a column and does  not provide any additional table privileges described in [Access control privileges](/user-guide/security-access-control-privileges). |
| APPLY | Masking policy | Optional. This policy-level privilege can be used by a policy owner to decentralize the [un]set operations of a given masking policy on columns to the object owners (i.e. the role that has the OWNERSHIP privilege on the object).   Snowflake supports [discretionary access control](/user-guide/security-access-control-overview) where object owners are also considered data stewards.   If the policy administrator trusts the object owners to be data stewards for protected columns, then the policy administrator can use this privilege to decentralize applying the policy [un]set operations. |

Expand

Show lessSee more

The following example creates the `MASKING_ADMIN` role and grants masking policy privileges to that role.

Create a masking policy administrator custom role:

> Copy code
>
> ```
> use role useradmin;
> CREATE ROLE masking_admin;
> ```

Grant privileges to `masking_admin` role:

> Copy code
>
> ```
> use role securityadmin;
> GRANT CREATE MASKING POLICY on SCHEMA <db_name.schema_name> to ROLE masking_admin;
> GRANT APPLY MASKING POLICY on ACCOUNT to ROLE masking_admin;
> ```

Allow `table_owner` role to set or unset the `ssn_mask` masking policy (optional):

> Copy code
>
> ```
> GRANT APPLY ON MASKING POLICY ssn_mask to ROLE table_owner;
> ```

Where:

- `{db_name.schema_name}`
  :   Specifies the identifier for the schema for which the privilege should be granted.

For more information, see:

- [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)
- [Security Access Control Configure](security-access-control-configure)
- [Security Access Control Privileges](security-access-control-privileges)

## Step 3: Grant the Custom Role to a User

Grant the `MASKING_ADMIN` custom role to a user serving as the security or privacy officer.

Copy code

```
use role useradmin;
grant role masking_admin to user jsmith;
```

## Step 4: Create a Masking Policy

In this representative example, users with the `ANALYST` custom role see the detokenized email values. Users without the `ANALYST` custom role see the tokenized values.

The external function to detokenize email values is `de_email()`.

Copy code

```
-- create masking policy

create or replace masking policy email_de_token as (val string) returns string ->
  case
    when current_role() in ('ANALYST') then de_email(val)
    else val
  end;
```

Tip

If you want to update an existing masking policy and need to see the current definition of the policy, call the [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy) command.

## Step 5: Apply the Masking Policy to a Table or View Column

These examples assume that a masking policy is not applied to the table column when the table is created and the view column when the view
is created. You can optionally apply a masking policy to a table column when you create the table with a
[CREATE TABLE](/sql-reference/sql/create-table) statement or a view column with a [CREATE VIEW](/sql-reference/sql/create-view) statement.

Execute the following statements to apply the policy to a table column or a view column.

Copy code

```
-- apply masking policy to a table column

alter table if exists user_info modify column email set masking policy email_de_token;

-- apply the masking policy to a view column

alter view user_info_v modify column email set masking policy email_de_token;
```

## Step 6: Query Data in Snowflake

Execute two different queries in Snowflake, one query with the `ANALYST` custom role and another query with a different role, to verify that users without the `ANALYST` custom role see tokenized values.

Copy code

```
-- using the ANALYST custom role

use role ANALYST;
select email from user_info; -- should see plain text value

-- using the PUBLIC system role

use role public;
select email from user_info; -- should see tokenized value
```

## External Tokenization best practices

- Synchronizing systems. On AWS, it is helpful to synchronize users and roles in your organization’s identity provider (IdP) with Snowflake
  and Protegrity. If users and roles are not synchronized, there can be unexpected behaviors, error messages, and complex troubleshooting
  regarding external functions, API integrations, masking policies, and tokenization policies. One option is to use
  [SCIM](/user-guide/scim-intro) to keep users and roles synchronized with your IdP and Snowflake.
- Root cause for error(s). Since External Tokenization requires coordinating multiple systems (e.g. IdP, Snowflake, Protegrity, AWS, Azure, GCP), always verify the privileges, current limitations, external functions, API integration, masking policies, and the columns that have masking policies for External Tokenization in Snowflake. To help determine the root cause, see:
  - [Understanding Column-level Security](/user-guide/security-column-intro)
  - [Troubleshooting External Tokenization](/user-guide/security-column-ext-token-intro#label-security-column-ext-token-troubleshooting)
  - [Creating external functions on AWS](/sql-reference/external-functions-creating-aws)
  - [Creating external functions on Microsoft Azure](/sql-reference/external-functions-creating-azure)
  - [Creating external functions on GCP](/sql-reference/external-functions-creating-gcp)

**Next Topic:**

- [Advanced Column-level Security topics](/user-guide/security-column-advanced)
