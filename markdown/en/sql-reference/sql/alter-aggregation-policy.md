# ALTER AGGREGATION POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Replaces the existing rules or comment of an [aggregation policy](/user-guide/aggregation-policies). Also allows you to rename an
aggregation policy.

See also:
:   [Aggregation policy DDL reference](/user-guide/aggregation-policies#label-aggregation-policy-ddl)

## Syntax

Copy code

```
ALTER AGGREGATION POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER AGGREGATION POLICY [ IF EXISTS ] <name> SET BODY -> <expression>

ALTER AGGREGATION POLICY <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER AGGREGATION POLICY <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER AGGREGATION POLICY [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER AGGREGATION POLICY [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the aggregation policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the aggregation policy; must be unique for your schema. The new identifier cannot be used if the
    identifier is already in place for a different aggregation policy.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`SET ...`
:   Specifies one (or more) properties to set for the aggregation policy:

    `BODY -> expression`
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

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the aggregation policy.

        Default: No value

`UNSET ...`
:   Specifies one or more properties and/or parameters to unset, by resetting them to their defaults, for the aggregation policy:

    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

    When resetting a property/parameter, specify only the name; specifying a value for the property will return an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Aggregation policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on aggregation policy DDL and privileges, see [Privileges and commands](/user-guide/aggregation-policies#label-aggregation-policy-manage).

## Usage notes

- If you want to update an existing aggregation policy and need to see the current body of the policy, run the
  [DESCRIBE AGGREGATION POLICY](/sql-reference/sql/desc-aggregation-policy) command. You can also use the [GET\_DDL](/sql-reference/functions/get_ddl) function to
  obtain the full definition of the aggregation policy, including its body.
- Moving an aggregation policy to a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas)
  (using the ALTER AGGREGATION POLICY … RENAME TO syntax) is prohibited unless the aggregation policy owner
  (i.e. the role that has the OWNERSHIP privilege on the aggregation policy) also owns the target schema.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Change the SQL expression of the aggregation policy to require a minimum group size of 2 rows in all circumstances:

> Copy code
>
> ```
> ALTER AGGREGATION POLICY my_policy SET BODY -> AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE=>2);
> ```

Rename an aggregation policy:

> Copy code
>
> ```
> ALTER AGGREGATION POLICY my_policy RENAME TO agg_policy_table1;
> ```
