# CREATE AGGREGATION POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new [aggregation policy](/user-guide/aggregation-policies) in the current/specified schema or replaces an existing
aggregation policy.

After creating an aggregation policy, assign the aggregation policy to a table using an [ALTER TABLE](/sql-reference/sql/alter-table) command or a view using an [ALTER VIEW](/sql-reference/sql/alter-view) command.

See also:
:   [Aggregation policy DDL reference](/user-guide/aggregation-policies#label-aggregation-policy-ddl)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] AGGREGATION POLICY [ IF NOT EXISTS ] <name>
  AS () RETURNS AGGREGATION_CONSTRAINT -> <body>
  [ COMMENT = '<string_literal>' ]
```

## Parameters

`name`
:   Identifier for the aggregation policy; must be unique for your schema.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`body`
> SQL expression that determines the restrictions of an aggregation policy.
>
> To define the constraints of the aggregation policy, use the SQL expression to call one or more of the following functions:
>
> NO\_AGGREGATION\_CONSTRAINT
>
> > When the policy body returns a value from this function, queries can return data from an aggregation-constrained table or view
> > without restriction. For example, the body of the policy could call this function when an administrator needs to obtain unaggregated
> > results from the aggregation-constrained table or view.
> >
> > Call NO\_AGGREGATION\_CONSTRAINT without an argument.
>
> AGGREGATION\_CONSTRAINT
>
> > When the policy body returns a value from this function, queries must aggregate data in order to return results. Use the
> > MIN\_GROUP\_SIZE argument to specify how many records must be included in each aggregation group.
> >
> > The syntax of the AGGREGATION\_CONSTRAINT function is:
> >
> > Copy code
> >
> > ```
> > AGGREGATION_CONSTRAINT ( MIN_GROUP_SIZE => <integer_expression> )
> > ```
> >
> > Where:
> >
> > `MIN_GROUP_SIZE => integer_expression`
> > :   Specifies how many rows or [entities](/user-guide/aggregation-policies-entity-privacy) must be included in the groups returned by
> >     a query against the aggregation-constrained table or view.
> >
> >     There is a difference between passing a `1` and a `0` as the argument to the function. Both require results to be aggregated.
> >
> >     - Passing a `1` also requires that each aggregation group contain at least one record from the aggregation-constrained table. So for
> >       outer joins, at least one record from the aggregation-constrained table must match a record from an unprotected table.
> >     - Passing a `0` allows the query to return groups that consist entirely of records from another table. So for outer joins between an
> >       aggregation-constrained table and an unprotected table, a group could consist of records from the unprotected table that do not match
> >       any records in the aggregation-constrained table.
>
> The body of a policy cannot reference user-defined functions, tables, or views.

`COMMENT = 'string_literal'`
:   Adds a comment or overwrites an existing comment for the aggregation policy.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE AGGREGATION POLICY | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on aggregation policy DDL and privileges, see [Privileges and commands](/user-guide/aggregation-policies#label-aggregation-policy-manage).

## Usage notes

- If you want to update an existing aggregation policy and need to see the current body of the policy, run the
  [DESCRIBE AGGREGATION POLICY](/sql-reference/sql/desc-aggregation-policy) command or [GET\_DDL](/sql-reference/functions/get_ddl) function.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create an aggregation policy that requires queries to return groups of five or more rows:

> Copy code
>
> ```
> CREATE AGGREGATION POLICY my_policy AS ()
>   RETURNS AGGREGATION_CONSTRAINT ->
>   AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5);
> ```

Create an aggregation policy that allows a user with role `admin` to return unaggregated results while requiring all other queries
to return groups of five or more rows:

> Copy code
>
> ```
> CREATE AGGREGATION POLICY my_policy AS ()
>   RETURNS AGGREGATION_CONSTRAINT ->
>     CASE
>       WHEN CURRENT_ROLE() = 'ADMIN'
>         THEN NO_AGGREGATION_CONSTRAINT()
>       ELSE AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5)
>     END;
> ```
