# CREATE PRIVACY POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) or replaces an existing privacy policy.

See also:
:   [ALTER PRIVACY POLICY](/sql-reference/sql/alter-privacy-policy) , [DESCRIBE PRIVACY POLICY](/sql-reference/sql/desc-privacy-policy) , [DROP PRIVACY POLICY](/sql-reference/sql/drop-privacy-policy) , [SHOW PRIVACY POLICIES](/sql-reference/sql/show-privacy-policies)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] PRIVACY POLICY [ IF NOT EXISTS ] <name>
  AS () RETURNS PRIVACY_BUDGET -> <body>
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (that is, name) for the privacy policy; must be unique for the schema in which the privacy policy is
    created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`body`
> The SQL expression of the body calls two functions to control the return value of the policy:
> NO\_PRIVACY\_POLICY and PRIVACY\_BUDGET. When a query is executed against a table that has been assigned the
> policy, Snowflake evaluates the conditions of the body to call the appropriate function and return a value. This return value determines
> which privacy budget, if any, is associated with the query against the privacy-protected table.
>
> The expression can use context functions such as [CURRENT\_ROLE](/sql-reference/functions/current_role) or [INVOKER\_ROLE](/sql-reference/functions/invoker_role)
> to associate a user or group of users with a privacy budget.
>
> If you use a [CASE](/sql-reference/functions/case) block in the body’s expression, it must include an ELSE statement that
> calls either NO\_PRIVACY\_POLICY or PRIVACY\_BUDGET. Every user must either be associated with a privacy budget or have unrestricted access to
> the privacy-protected table. If a user should not have any access to a privacy-protected table or view, revoke SELECT privileges rather than
> trying to define this in the privacy policy.
>
> `NO_PRIVACY_POLICY`
>
> > Use the body’s expression to call the `NO_PRIVACY_POLICY` function when you want a query to have unrestricted access to the table or view to which the privacy policy is assigned.
>
> `PRIVACY_BUDGET`
>
> > Use the body’s expression to call the `PRIVACY_BUDGET` function when you want to return a privacy budget from the policy. The
> > expression can contain conditions that allow the policy to return different privacy budgets for different queries based on factors like
> > the user who is executing the query.
> >
> > In cross-account collaboration, privacy budgets are automatically namespaced by the account identifier of the consumer account, which
> > prevents two different consumer accounts from sharing the same privacy budget even if the name of the privacy budget is the same. Using
> > the [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) function to concatenate the name of the account with the name of the privacy budget
> > can help distinguish between privacy budgets. For example, you could call the function as follows:
> > `PRIVACY_BUDGET(BUDGET_NAME => 'external_budget.' || CURRENT_ACCOUNT())`.
> >
> > The signature of the `PRIVACY_BUDGET` function is:
> >
> > Copy code
> >
> > ```
> > PRIVACY_BUDGET(
> >   BUDGET_NAME=> '<string>'
> >   [, BUDGET_LIMIT=> <decimal> ]
> >   [, MAX_BUDGET_PER_AGGREGATE=> <decimal> ]
> >   [, BUDGET_WINDOW=> <string> ]
> > )
> > ```
> >
> > **Privacy budget arguments:**
> >
> > `BUDGET_NAME => expression`
> > :   Resolves to the name of a privacy budget. Snowflake creates the privacy budget automatically when its name is
> >     specified in the body of the privacy policy.
> >
> > `BUDGET_LIMIT => decimal`
> > :   A decimal number > 0 that specifies the budget limit for this privacy policy.
> >     This controls the total amount of privacy loss allowed. Adjusting this value
> >     changes how many total differentially private aggregates can be calculated
> >     against tables protected by this privacy budget during the refresh period. When a query is run that would
> >     cause the cumulative privacy loss to exceed this number, the query will fail.
> >     As a rough estimate, a budget
> >     limit of 233 with `MAX_BUDGET_PER_AGGREGATE=1` permits about 1000 aggregates
> >     per refresh period.
> >
> >     Default: 233.0
> >
> > `MAX_BUDGET_PER_AGGREGATE => decimal`
> > :   Specifies how much privacy budget is used for each aggregate function in a
> >     query. Adjusting this value changes the amount of noise added to each aggregate
> >     query, as well as the number of aggregates that can be calculated before the budget limit is reached. As an example, the query
> >     `select count(*), avg(a) ...` has two aggregates: `count(*)` and `avg(a)`. Specify a decimal value > 0.
> >
> >     Default: 0.5
> >
> > `BUDGET_WINDOW => string`
> > :   How often the privacy budget is refreshed, that is, has its cumulative privacy loss reset to 0. Valid values:
> >
> >     - `Daily`: Refreshed every day at 12:00 AM UTC
> >     - `Weekly`: Refreshed every Sunday at 12:00 AM UTC
> >     - `Monthly`: Refreshed on the first day of the calendar month at 12:00 AM UTC
> >     - `Yearly`: Refreshed on January 1 at 12:00 AM UTC
> >     - `Never`: Privacy budget is never refreshed.
> >
> >     Default: Weekly

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the privacy policy.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE PRIVACY POLICY | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create a privacy policy that always returns a budget named `analysts`:

> Copy code
>
> ```
> CREATE PRIVACY POLICY my_priv_policy
>   AS ( ) RETURNS PRIVACY_BUDGET ->
>   PRIVACY_BUDGET(BUDGET_NAME=> 'analysts');
> ```

Create a privacy policy that will give `admin` unrestricted access to the privacy-protected table while associating all other users with
the privacy budget `analysts`:

> Copy code
>
> ```
> CREATE PRIVACY POLICY my_priv_policy
>   AS () RETURNS PRIVACY_BUDGET ->
>     CASE
>       WHEN CURRENT_USER() = 'ADMIN'
>         THEN NO_PRIVACY_POLICY()
>       ELSE PRIVACY_BUDGET(BUDGET_NAME => 'analysts')
>     END;
> ```
