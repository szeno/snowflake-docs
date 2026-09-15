# ALTER PRIVACY POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies the properties of an existing [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies).

Caution

When changing `budget_limit`, `max_budget_per_aggregate`, or
`budget_window`, any property not specified in your ALTER command will revert
back to its default value. To obtain the current values of the parameters, execute the [DESCRIBE PRIVACY POLICY](/sql-reference/sql/desc-privacy-policy) command.

See also:
:   [CREATE PRIVACY POLICY](/sql-reference/sql/create-privacy-policy) , [DESCRIBE PRIVACY POLICY](/sql-reference/sql/desc-privacy-policy) , [DROP PRIVACY POLICY](/sql-reference/sql/drop-privacy-policy) , [SHOW PRIVACY POLICIES](/sql-reference/sql/show-privacy-policies)

## Syntax

Copy code

```
ALTER PRIVACY POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER PRIVACY POLICY [ IF EXISTS ] <name> SET BODY -> <expression>

ALTER PRIVACY POLICY <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER PRIVACY POLICY <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER PRIVACY POLICY [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER PRIVACY POLICY [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the privacy policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the privacy policy; must be unique for your schema. The new identifier cannot be used if the
    identifier is already in place for a different privacy policy.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`SET ...`
:   Specifies one (or more) properties to set for the privacy policy:

    `BODY -> expression`
    :   Specifies a new body for the policy.

        The SQL expression of the body calls two functions to control the return value of the policy:
        NO\_PRIVACY\_POLICY and PRIVACY\_BUDGET. When a query is executed against a table that has been assigned the
        policy, Snowflake evaluates the conditions of the body to call the appropriate function and return a value. This return value determines
        which privacy budget, if any, is associated with the query against the privacy-protected table.

        The expression can use context functions such as [CURRENT\_ROLE](/sql-reference/functions/current_role) or [INVOKER\_ROLE](/sql-reference/functions/invoker_role)
        to associate a user or group of users with a privacy budget.

        If you use a [CASE](/sql-reference/functions/case) block in the body’s expression, it must include an ELSE statement that
        calls either NO\_PRIVACY\_POLICY or PRIVACY\_BUDGET. Every user must either be associated with a privacy budget or have unrestricted access to
        the privacy-protected table. If a user should not have any access to a privacy-protected table or view, revoke SELECT privileges rather than
        trying to define this in the privacy policy.

        `NO_PRIVACY_POLICY`

        > Use the body’s expression to call the `NO_PRIVACY_POLICY` function when you want a query to have unrestricted access to the table or view to which the privacy policy is assigned.

        `PRIVACY_BUDGET`

        > Use the body’s expression to call the `PRIVACY_BUDGET` function when you want to return a privacy budget from the policy. The
        > expression can contain conditions that allow the policy to return different privacy budgets for different queries based on factors like
        > the user who is executing the query.
        >
        > In cross-account collaboration, privacy budgets are automatically namespaced by the account identifier of the consumer account, which
        > prevents two different consumer accounts from sharing the same privacy budget even if the name of the privacy budget is the same. Using
        > the [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) function to concatenate the name of the account with the name of the privacy budget
        > can help distinguish between privacy budgets. For example, you could call the function as follows:
        > `PRIVACY_BUDGET(BUDGET_NAME => 'external_budget.' || CURRENT_ACCOUNT())`.
        >
        > The signature of the `PRIVACY_BUDGET` function is:
        >
        > Copy code
        >
        > ```
        > PRIVACY_BUDGET(
        >   BUDGET_NAME=> '<string>'
        >   [, BUDGET_LIMIT=> <decimal> ]
        >   [, MAX_BUDGET_PER_AGGREGATE=> <decimal> ]
        >   [, BUDGET_WINDOW=> <string> ]
        > )
        > ```
        >
        > **Privacy budget arguments:**
        >
        > `BUDGET_NAME => expression`
        > :   Resolves to the name of a privacy budget. Snowflake creates the privacy budget automatically when its name is
        >     specified in the body of the privacy policy.
        >
        > `BUDGET_LIMIT => decimal`
        > :   A decimal number > 0 that specifies the budget limit for this privacy policy.
        >     This controls the total amount of privacy loss allowed. Adjusting this value
        >     changes how many total differentially private aggregates can be calculated
        >     against tables protected by this privacy budget during the refresh period. When a query is run that would
        >     cause the cumulative privacy loss to exceed this number, the query will fail.
        >     As a rough estimate, a budget
        >     limit of 233 with `MAX_BUDGET_PER_AGGREGATE=1` permits about 1000 aggregates
        >     per refresh period.
        >
        >     Default: 233.0
        >
        > `MAX_BUDGET_PER_AGGREGATE => decimal`
        > :   Specifies how much privacy budget is used for each aggregate function in a
        >     query. Adjusting this value changes the amount of noise added to each aggregate
        >     query, as well as the number of aggregates that can be calculated before the budget limit is reached. As an example, the query
        >     `select count(*), avg(a) ...` has two aggregates: `count(*)` and `avg(a)`. Specify a decimal value > 0.
        >
        >     Default: 0.5
        >
        > `BUDGET_WINDOW => string`
        > :   How often the privacy budget is refreshed, that is, has its cumulative privacy loss reset to 0. Valid values:
        >
        >     - `Daily`: Refreshed every day at 12:00 AM UTC
        >     - `Weekly`: Refreshed every Sunday at 12:00 AM UTC
        >     - `Monthly`: Refreshed on the first day of the calendar month at 12:00 AM UTC
        >     - `Yearly`: Refreshed on January 1 at 12:00 AM UTC
        >     - `Never`: Privacy budget is never refreshed.
        >
        >     Default: Weekly

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the privacy policy.

        Default: No value

`UNSET ...`
:   Specifies one or more properties and/or parameters to unset, by resetting them to their defaults, for the privacy policy:

    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

    When resetting a property/parameter, specify only the name; specifying a value for the property will return an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Privacy policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If you want to update an existing privacy policy and need to see the current definition of the policy, run the
  [DESCRIBE PRIVACY POLICY](/sql-reference/sql/desc-privacy-policy) command. You can also use the [GET\_DDL](/sql-reference/functions/get_ddl) function to obtain the full definition
  of the privacy policy, including its body.
- Moving a privacy policy to a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas)
  (using the ALTER PRIVACY POLICY … RENAME TO syntax) is prohibited unless the privacy policy owner
  (that is, the role that has the OWNERSHIP privilege on the privacy policy) also owns the target schema.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Modify the body of a privacy policy `my_priv_policy` so it always returns a budget named `analysts`:

> Copy code
>
> ```
> -- Modify the body of privacy policy "my_priv_policy" so it always returns a
> -- budget named "analysts"
> ALTER PRIVACY POLICY my_priv_policy SET BODY ->
>   PRIVACY_BUDGET(BUDGET_NAME => 'analysts');
>
> -- Set budget limit to 50 and max budget per aggregate to 0.1
> -- budget window is not mentioned so it is reset to its default value
> ALTER PRIVACY POLICY users_policy SET BODY ->
>   privacy_budget(budget_name=>'analysts', budget_limit=>50, max_budget_per_aggregate=>0.1);
> ```
